from django.db import models
from django.conf import settings

class UserCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # Dynamically reference the user model
        through='UserCategoryMembership',
        related_name="categories"
    )

    def __str__(self):
        return self.name


class UserCategoryMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(UserCategory, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} in {self.category.name}"
