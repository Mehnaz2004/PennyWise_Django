from django.urls import path

from . import views
from .views import (CategoryCreateView, CategoryListView,
                    ExpenseSheetCreateView, ExpenseSheetListView,
                    SpendingCreateView, SpendingListView)

urlpatterns = [
    path('', views.home, name="home"),
    path('create_expense_sheet/', ExpenseSheetCreateView.as_view(), name='create_expense_sheet'),
    path('create_category/', CategoryCreateView.as_view(), name='create_category'),
    path('create_spending/', SpendingCreateView.as_view(), name='create_spending'),
    path('expense_sheets/', ExpenseSheetListView.as_view(), name='expense_sheet_list'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('spending_list/', SpendingListView.as_view(), name='spending_list'),
    path('update_expense_sheet/<int:pk>/update/', views.ExpenseSheetUpdateView.as_view(), name='update_expense_sheet'),
    path('delete_expense_sheet/<int:pk>/delete/', views.ExpenseSheetDeleteView.as_view(), name='delete_expense_sheet'),
    path('update_category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('delete_category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete_category'),
    path('update_spending/<int:pk>/update/', views.SpendingUpdateView.as_view(), name='update_spending'),
    path('delete_spending/<int:pk>/delete/', views.SpendingDeleteView.as_view(), name='delete_spending'),
]

