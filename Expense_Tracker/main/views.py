# views.py
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, ExpenseSheet, Spending
from .forms import CategoryForm, ExpenseSheetForm, SpendingForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib import messages
from django.http import HttpResponse


def base(request):
    username = request.user.username
    # Pass the username to the context
    return render(request, 'main/base.html', {'username': username})

def home(request):
    return render(request, "main/home.html", {"name": "test"})

class ExpenseSheetCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseSheet
    form_class = ExpenseSheetForm
    template_name = 'main/create_expense_sheet.html'
    success_url = reverse_lazy('expense_sheet_list')
    def form_valid(self, form):
        # Set the user field to the currently logged-in user before saving
        form.instance.user = self.request.user
        response = super().form_valid(form)
        form.instance.remaining_budget = form.instance.budget
        form.instance.save()
        return response
    
class ExpenseSheetListView(LoginRequiredMixin, ListView):
    model = ExpenseSheet
    template_name = 'main/expense_sheet_list.html'
    context_object_name = 'expense_sheets'

    def get_queryset(self):
        # Filter expense sheets to show only those associated with the current user
        return ExpenseSheet.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_budget = self.get_queryset().aggregate(Sum('budget'))
        context['total_budget'] = total_budget['budget__sum'] if total_budget['budget__sum'] else 0
        return context

class ExpenseSheetUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseSheet
    form_class = ExpenseSheetForm
    template_name = 'main/update_expense_sheet.html'
    success_url = reverse_lazy('expense_sheet_list')

    def get_queryset(self):
        # Filter expense sheets to show only those associated with the current user
        return ExpenseSheet.objects.filter(user=self.request.user)

class ExpenseSheetDeleteView(DeleteView):
    model = ExpenseSheet
    success_url = reverse_lazy('expense_sheet_list')
    template_name = 'main/delete_expense_sheet.html'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/create_category.html'
    success_url = reverse_lazy('category_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user

        # Get the expense sheet for which the category is being created
        expense_sheet_id = self.request.POST.get('expense_sheet')
        expense_sheet = ExpenseSheet.objects.get(pk=expense_sheet_id)
        
        form.instance.remaining_budget = form.instance.budget
        # Get the sum of budgets of all categories in the expense sheet
        total_budget = expense_sheet.categories.aggregate(total_budget=Sum('budget'))['total_budget']
        total_budget = total_budget if total_budget else 0  # Handle None case

        # Get the budget of the expense sheet
        expense_sheet_budget = expense_sheet.budget

        # Check if adding the new category exceeds the expense sheet budget
        if total_budget + form.instance.budget > expense_sheet_budget:
            # Redirect to an error page or show a message
            return HttpResponse("Adding this category exceeds the expense sheet budget.")

        # If budget constraint is satisfied, proceed with saving the form
        return super().form_valid(form)

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'main/category_list.html'
    context_object_name = 'category_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the expense sheet details for the logged-in user
        expense_sheets = ExpenseSheet.objects.filter(user=self.request.user)
        # Create a dictionary to store expense sheet details and their related categories
        expense_sheet_category_dict = {}
        for expense_sheet in expense_sheets:
            # Get categories related to the expense sheet
            categories = Category.objects.filter(expense_sheet=expense_sheet)
            expense_sheet_category_dict[expense_sheet] = categories
        # Pass the dictionary to the template context
        context['expense_sheet_category_dict'] = expense_sheet_category_dict
        return context

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'main/update_category.html'
    success_url = reverse_lazy('category_list')
    def get_form_kwargs(self):
        kwargs = super(CategoryUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    template_name = 'main/delete_category.html'

class SpendingCreateView(LoginRequiredMixin,CreateView):
    model = Spending
    form_class = SpendingForm
    template_name = 'main/create_spending.html'
    success_url = reverse_lazy('spending_list')
    
    def get_form_kwargs(self):
        kwargs = super(SpendingCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs
    
    def form_valid(self, form):
        if form.instance.category:
            # Calculate the remaining budget of the associated category
            category_remaining_budget = form.instance.category.remaining_budget - form.instance.amount

            # Check if the category remaining budget is negative
            if category_remaining_budget < 0:
                messages.error(self.request, "Spending amount exceeds category remaining budget.")
                return self.form_invalid(form)

            # Calculate the remaining budget of the associated expense sheet
            expense_sheet_remaining_budget = form.instance.category.expense_sheet.remaining_budget - form.instance.amount

            # Check if the expense sheet remaining budget is negative
            if expense_sheet_remaining_budget < 0:
                messages.error(self.request, "Spending amount exceeds expense sheet remaining budget.")
                return self.form_invalid(form)

            # Update the remaining budget of the associated category and expense sheet
            form.instance.category.remaining_budget = category_remaining_budget
            form.instance.category.expense_sheet.remaining_budget = expense_sheet_remaining_budget

            # Save the changes to the category and expense sheet
            form.instance.category.save()
            form.instance.category.expense_sheet.save()

        # Call the parent class method to handle the default behavior of form validation
        form.instance.user=self.request.user
        response = super().form_valid(form)

        return response

class SpendingListView(LoginRequiredMixin, ListView):
    model = ExpenseSheet
    template_name = 'main/spending_list.html'
    context_object_name = 'expense_sheets'

    def get_queryset(self):
        # Filter expense sheets to show only those associated with the current user
        return ExpenseSheet.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all expense sheets associated with the current user
        expense_sheets = self.get_queryset()

        for expense_sheet in expense_sheets:
            # Fetch categories for the current expense sheet
            categories = Category.objects.filter(expense_sheet=expense_sheet)

            # Add spendings to the context for each category
            expense_sheet.spendings_data = []

            for category in categories:
                spendings = Spending.objects.filter(category=category)
                expense_sheet.spendings_data.append({'category': category, 'spendings': list(spendings)})

        context['expense_sheets'] = expense_sheets
        return context

class SpendingUpdateView(UpdateView):
    model = Spending
    form_class = SpendingForm
    template_name = 'main/update_spending.html'
    success_url = reverse_lazy('spending_list')

class SpendingDeleteView(DeleteView):
    model = Spending
    success_url = reverse_lazy('spending_list')
    template_name = 'main/delete_spending.html'