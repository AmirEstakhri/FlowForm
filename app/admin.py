from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Form, FormVersion, CustomUser, Tag, Category

# Register Form and FormVersion
admin.site.register(Form)
admin.site.register(FormVersion)

# Define the CustomUserAdmin class
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'sub_role', 'is_active', 'is_staff']
    list_filter = ['is_active', 'is_staff', 'role', 'sub_role']  # Add 'sub_role' to list filter
    search_fields = ['username', 'email']
    ordering = ['username']
    
    # Specify the fields to display in the form (include the 'role' and 'sub_role' fields here)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # Basic fields
        ('Personal info', {'fields': ('email', 'first_name', 'last_name')}),  # Personal info fields
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  # Permissions
        ('Roles', {'fields': ('role', 'sub_role')}),  # Add the 'role' and 'sub_role' fields here
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'role', 'sub_role')  # Add 'role' and 'sub_role' to the add form
        }),
    )
# from django.contrib import admin
# from .models import UserCategory

# @admin.register(UserCategory)
# class UserCategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     filter_horizontal = ('users',)


# Register the CustomUser model with CustomUserAdmin

admin.site.register(CustomUser, CustomUserAdmin)




# Register other models
admin.site.register(Tag)
admin.site.register(Category)
