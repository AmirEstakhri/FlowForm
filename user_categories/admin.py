from django.contrib import admin
from .models import UserCategory, UserCategoryMembership

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users')  # Add a custom method to display users

    # Define a custom method to retrieve users associated with the category
    def get_users(self, obj):
        # Retrieve users related to the category through UserCategoryMembership
        return ", ".join([membership.user.username for membership in obj.usercategorymembership_set.all()])
    get_users.short_description = 'Users'  # Optional: set a custom column name in the admin list

class UserCategoryMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')  # Correct as 'user' is a ForeignKey to CustomUser

# Registering the models
admin.site.register(UserCategory, UserCategoryAdmin)
admin.site.register(UserCategoryMembership, UserCategoryMembershipAdmin)
