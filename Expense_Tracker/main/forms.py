# forms.py
from django import forms
from .models import ExpenseSheet, Category, Spending

class ExpenseSheetForm(forms.ModelForm):
    class Meta:
        model = ExpenseSheet
        fields = ['title', 'budget']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'budget', 'expense_sheet']

    def __init__(self, user, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        # Filter available ExpenseSheets to only those belonging to the logged-in user
        self.fields['expense_sheet'].queryset = ExpenseSheet.objects.filter(user=user)
        self.user = user
        super(CategoryForm,self).__innit__(*args, **kwargs)

class SpendingForm(forms.ModelForm):
    class Meta:
        model = Spending
        fields = ['amount', 'description', 'category']

    def __init__(self, user, *args, **kwargs):
        super(SpendingForm, self).__init__(*args, **kwargs)
        # Filter available Categories (and their associated ExpenseSheets) to only those belonging to the logged-in user
        self.fields['category'].queryset = Category.objects.filter(expense_sheet__user=user)


