from django.contrib import admin
from .models import ExpenseSheet, Category, Spending
# Register your models here.

admin.site.register(ExpenseSheet)
admin.site.register(Category)
admin.site.register(Spending)