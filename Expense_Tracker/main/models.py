from django.db import models
from register.models import CustomUser

# Create your models here.
class ExpenseSheet(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # If the object is being created (not updated), set remaining_budget to the initial budget value
        if not self.pk:
            self.remaining_budget = self.budget
        super().save(*args, **kwargs)
#Changes in models file
class Category(models.Model):
    name = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2)
    expense_sheet = models.ForeignKey(ExpenseSheet, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class Spending(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spendings')

    def __str__(self):
        return self.description