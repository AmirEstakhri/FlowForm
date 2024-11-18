from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import User
from django.conf import settings
from user_categories.models import UserCategory, UserCategoryMembership




# Custom manager for CustomUser model
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Set role for superuser
        return self.create_user(username, password, **extra_fields)

# CustomUser model with the added 'role' field
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=150)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Added 'role' field to define user roles
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    SUB_ROLE_CHOICES = [
        ('none', 'None'),
        ('user-access-to-all-users-with-role-user', 'User Access to All Users with Role User'),
        ('manager-access-to-all-users-with-role-manager', 'user Access to All Users with Role Manager'),
    ]
    sub_role = models.CharField(max_length=255, choices=SUB_ROLE_CHOICES, default='none')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_subrole(self, subrole):
        return self.sub_role == subrole
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


# Category model
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# Form model
from django.db import models
from django.conf import settings
from .models import Tag, Category, CustomUser

class Form(models.Model):
    title = models.CharField(max_length=255)
    sender_signature = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    receiver_signature = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    # Many-to-many relationship with Tag and Category models
    tags = models.ManyToManyField(Tag, related_name="forms", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="forms", null=True)
    users = models.ManyToManyField('app.CustomUser', blank=True)  # view-only users section

    sender_name = models.CharField(max_length=255)
    prioritize = models.BooleanField(default=False)
    priority = models.CharField(max_length=100, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium')

    # Foreign key to CustomUser for assigned manager
    assigned_managers = models.ManyToManyField(CustomUser, related_name="assigned_forms", blank=True, limit_choices_to={'role': 'manager'})
    
    # Replace `added_users` with `assigned_users`
    assigned_users = models.ManyToManyField(
        CustomUser, 
        related_name="viewable_forms", 
        blank=True, 
        limit_choices_to={'role': 'user'}
    )

    allowed_managers = models.ManyToManyField(CustomUser, related_name='allowed_forms', blank=True)  # Add this line

    sender = models.CharField(max_length=100)

    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name='verified_forms', blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Form'
        verbose_name_plural = 'Forms'


# FormVersion model to handle version control for forms
class FormVersion(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Version {self.version_number} of {self.form.title}"

    class Meta:
        verbose_name = 'Form Version'
        verbose_name_plural = 'Form Versions'


