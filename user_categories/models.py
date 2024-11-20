from django.db import models
from django.conf import settings

class UserCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class UserCategoryMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(UserCategory, on_delete=models.CASCADE)

    class Meta:
        # Enforce that a user can only belong to one category
        constraints = [
            models.UniqueConstraint(fields=['user'], name='unique_user_per_category')
        ]

    def save(self, *args, **kwargs):
        # Check if the user has the role of 'manager'
        if self.user.role == 'manager':
            # Check if there is already a manager in this category
            existing_manager = UserCategoryMembership.objects.filter(
                category=self.category, user__role='manager'
            ).exclude(user=self.user)  # Exclude the current user to allow updates
            if existing_manager.exists():
                raise ValueError(f"Category '{self.category.name}' can only have one manager.")

        # Call the parent save method to save the instance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} in {self.category.name}"

    
    
