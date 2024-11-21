from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    Form,
    CustomUser,
    Tag,
    Category,
    UserCategory,
    UserCategoryMembership,
    FormVersion,
    FormVerificationLog,
)
from .forms import (
    FormCreationForm,
    LoginForm,
    FormCreateUpdateForm,
    FormEditForm,
)

from app.utils import is_manager  # Utility function for role checks
from user_categories.models import UserCategoryMembership

import logging


@login_required
def my_forms(request):
    user = request.user
    forms = Form.objects.filter(sender=user).select_related('category').prefetch_related('tags')

    return render(request, 'form/my_forms.html', {'forms': forms})


# Check if user is a manager
def is_manager(user):
    return user.role == 'manager'

# Check if user is admin or manager
def is_admin_or_manager(user):
    return user.role in ['admin', 'manager']

@login_required
def homepage(request):
    # Show links based on user role
    context = {
        'is_admin': request.user.role == 'admin',
        'is_manager': request.user.role == 'manager',
        'is_user': request.user.role == 'user',
    }
    return render(request, 'home/homepage.html', context)


# Set up logging for errors
logger = logging.getLogger(__name__)


@login_required
def create_form(request):
    # Check if the logged-in user is an admin
    if request.user.role == "admin":
        # Admins can access all users and managers
        assigned_managers = CustomUser.objects.filter(role="manager").exclude(id=request.user.id).distinct()
        assigned_users = CustomUser.objects.filter(role="user").exclude(id=request.user.id).distinct()
    else:
        # Get the logged-in user's categories
        user_categories = request.user.usercategorymembership_set.values_list('category', flat=True)
        
        # Debugging: Check categories assigned to the logged-in user
        print(f"Logged-in User Categories: {user_categories}")
        
        # Initialize querysets for managers filtered by shared categories, excluding the logged-in user
        assigned_managers = CustomUser.objects.filter(
            role='manager',
            usercategorymembership__category__in=user_categories
        ).exclude(id=request.user.id).distinct()  # Exclude the logged-in user

        # Initialize querysets for users only if the user has the required sub-role, excluding the logged-in user
        if request.user.sub_role == "user-access-to-all-users-with-role-user":
            assigned_users = CustomUser.objects.filter(
                role='user',
                usercategorymembership__category__in=user_categories
            ).exclude(id=request.user.id).distinct()  # Exclude the logged-in user
        else:
            assigned_users = CustomUser.objects.none()  # Empty queryset if no sub-role

    # Debugging: Check the assigned users and managers after filtering
    print(f"Assigned Managers: {assigned_managers}")
    print(f"Assigned Users: {assigned_users}")

    # Get all tags and categories from the database
    tags = Tag.objects.all()
    categories = Category.objects.all()

    # Handle form submission
    if request.method == 'POST':
        form = FormCreationForm(request.POST, user=request.user)  # Pass logged-in user to form
        if form.is_valid():
            try:
                # Save form instance without committing to get the instance ID
                form_instance = form.save(commit=False)
                form_instance.save()  # Save to generate ID
                
                # Set ManyToMany and ForeignKey relationships after saving the form instance
                tags_selected = form.cleaned_data.get('tags')
                if tags_selected:
                    form_instance.tags.set(tags_selected)  # Set tags to the form
                
                category_selected = form.cleaned_data.get('category')
                if category_selected:
                    form_instance.category = category_selected  # Set category

                # Handle assigned managers (ManyToManyField)
                assigned_managers_selected = form.cleaned_data.get('assigned_managers')
                if assigned_managers_selected:
                    form_instance.assigned_managers.set(assigned_managers_selected)  # Assign managers
               
                # Handle added users (ManyToManyField) only if user has the sub-role
                if request.user.sub_role == "user-access-to-all-users-with-role-user":
                    added_users_selected = form.cleaned_data.get('added_users')
                    if added_users_selected:
                        form_instance.added_users.set(added_users_selected)  # Assign users to the form

                form_instance.save()  # Save again to commit ManyToMany and ForeignKey fields

                # Provide success message and redirect to form list
                messages.success(request, 'Form created successfully!')
                return redirect('form_list')  # Adjust URL as needed for form listing page
            except Exception as e:
                # Handle any exceptions during save
                messages.error(request, f'Error saving the form: {e}')
        else:
            # If form is not valid, show field errors
            field_errors = {field: error for field, error in form.errors.items()}
            messages.error(request, f'There was an error creating the form: {field_errors}')
    else:
        # Initialize the form with the logged-in user instance
        form = FormCreationForm(user=request.user)

    # Render the form creation page with all necessary context
    return render(request, 'form/create_form.html', {
        'form': form,
        'assigned_users': assigned_users,  # Filtered users or empty queryset
        'assigned_managers': assigned_managers,  # Filtered managers
        'tags': tags,
        'categories': categories,  # Display categories for filtering
        'user': request.user,  # Pass logged-in user to template for context
    })


def user_login(request):
    if request.method == "POST":
        # Use AuthenticationForm to handle login
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to the home page or any other page after successful login
        else:
            # If authentication fails or form is invalid
            messages.error(request, "Invalid username or password.")
    else:
        # Initialize an empty form if it's a GET request
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})  # Pass the form to the template





def user_list(request):
    # Fetch users with the 'manager' role
    managers = CustomUser.objects.filter(role='manager')
    return render(request, 'your_template.html', {'managers': managers})




@login_required
def form_list(request):
    user = request.user

    # For users with the 'user' role
    if user.role == 'user':
        # Include forms where the user is either the sender or an assigned user
        forms = Form.objects.filter(
            Q(sender=user) | 
            Q(assigned_users=user)  # Using assigned_users field
        ).distinct()

    # For managers
    elif user.role == 'manager':
        # Managers can see forms where they are either assigned or allowed
        forms = Form.objects.filter(
            Q(assigned_managers=user) |  # Forms where the user is assigned as a manager
            Q(allowed_managers=user)    # Forms where the user is allowed as a manager
        ).distinct()

    # For admins or other roles
    else:
        # Admins see all forms
        forms = Form.objects.all()

    # Prefetch related fields to optimize queries (tags, category, and verification_logs)
    forms = forms.prefetch_related('tags', 'category', 'verification_logs')  # Include verification_logs

    # Check if the user has verified each form
    for form in forms:
        form.has_verified = form.verification_logs.filter(verified_by=user).exists()

    return render(request, 'form/form_list.html', {'forms': forms})






@login_required
def assigned_forms_view(request):
    # Get the current user
    current_user = request.user

    # Query forms where the current user is in the assigned_users field
    assigned_forms = Form.objects.filter(assigned_users=current_user).distinct()
    

    # Pass the filtered forms to the template
    context = {
        'assigned_forms': assigned_forms,
    }
    return render(request, 'form/assigned-pages/assigned_forms.html', context)


@login_required
def forms_assigned_to_manager(request):
    # Get the logged-in user
    current_user = request.user

    # Query forms where the current user is an assigned manager
    forms = Form.objects.filter(assigned_managers__username=current_user.username).distinct()

    # Render the filtered forms
    return render(request, 'forms/assigned-pages/assigned_to_manager.html', {'forms': forms})


def is_admin_or_manager(user):
    return user.role in ['admin', 'manager']



@login_required
def verify_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)

    # Check if the user is an assigned or allowed manager
    if request.user not in form.assigned_managers.all() and request.user not in form.allowed_managers.all():
        messages.error(request, 'You do not have permission to verify this form.')
        return redirect('form_list')

    # If the form has not been verified, mark it as verified by the first manager
    if not form.verified:
        form.verified = True
        form.verified_by = request.user  # Mark this manager as the one who verified the form
        form.verification_logs.create(verified_by=request.user, action="Form verified and completed")
        form.save()
        messages.success(request, 'Form successfully verified and marked as completed.')
    else:
        # If the form is already verified, log the new verification attempt
        form.verification_logs.create(verified_by=request.user, action="Manager verified the form")

        messages.success(request, 'Your verification has been logged.')

    return redirect('form_list')



def is_admin_or_manager(user):
    return user.role in ['admin', 'manager']

from django.shortcuts import render, get_object_or_404
from .models import Form

@login_required
def form_detail(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return render(request, 'form/form_detail.html', {'form': form})


def is_manager(user):
    return user.role == 'manager' or user.role == 'user'

# Reuse or create a separate form class for both creating and updating

@login_required
def edit_form(request, form_id):
    # Fetch the form object by ID
    form_instance = get_object_or_404(Form, id=form_id, sender=request.user)

    if form_instance.verified:
        messages.error(request, "You cannot edit a verified form.")
        return redirect('my_forms')

    # Handle form submission
    if request.method == 'POST':
        form = FormCreateUpdateForm(request.POST, instance=form_instance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Form updated successfully!')
            return redirect('my_forms')
        else:
            messages.error(request, 'There were errors updating the form. Please try again.')
    else:
        # Prepopulate the form with the instance
        form = FormCreateUpdateForm(instance=form_instance)

    return render(request, 'form/edit_form.html', {'form': form, 'form_instance': form_instance})




def custom_logout(request):
    """
    Logs out the user and redirects to the login page or home page.
    """
    logout(request)  # Django's built-in logout function
    return redirect('login')  # Redirect to the login page or any page of your choice


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Authenticate the user and log them in
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('homepage')  # Redirect to the home page or any page after successful login
        else:
            # Display error message if form is not valid
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    # Render the login page with the form
    return render(request, 'login/login.html', {'form': form})



@login_required
def send_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    user = request.user

    if request.method == 'POST':
        # Prevent the form from being sent to the current user
        if form.sender == request.user:
            messages.error(request, "You cannot send a form to yourself.")
            return redirect('form_list')

        # Handle assigning allowed managers
        allowed_manager_ids = request.POST.getlist('allowed_managers')

        if allowed_manager_ids:
            try:
                # Add selected managers to allowed_managers (do not remove existing)
                for manager_id in allowed_manager_ids:
                    if manager_id:  # Ensure there's no empty ID
                        allowed_manager = CustomUser.objects.get(id=manager_id, role='manager')
                        form.allowed_managers.add(allowed_manager)

                messages.success(request, "Form successfully sent to the selected manager(s).")
            except CustomUser.DoesNotExist:
                messages.error(request, "One or more selected managers do not exist.")

        return redirect('form_list')

    # Prepare allowed managers list, excluding those already assigned
    excluded_ids = list(
        form.assigned_users.values_list('id', flat=True)
    ) + list(
        form.assigned_managers.values_list('id', flat=True)
    ) + list(
        form.allowed_managers.values_list('id', flat=True)
    )
    allowed_managers = CustomUser.objects.filter(role='manager').exclude(id__in=excluded_ids)

    return render(request, 'form/send_form.html', {
        'form': form,
        'allowed_managers': allowed_managers,
    })


@login_required
def revert_version(request, form_id, version_number):
    form = get_object_or_404(Form, id=form_id)
    version = get_object_or_404(FormVersion, form=form, version_number=version_number)
    form.data = version.data
    form.save()
    messages.success(request, 'Form has been reverted to the selected version.')
    return redirect('form_list')

@login_required
@user_passes_test(is_admin_or_manager)
def send_form_to_manager(request, form_id, manager_id):
    form = get_object_or_404(Form, id=form_id)
    manager = get_object_or_404(CustomUser, id=manager_id, role='manager')

    if request.user.role == 'manager' and manager == request.user:
        messages.error(request, 'Managers cannot send forms to themselves.')
        return redirect('form_list')

    form.recipient = manager
    form.save()
    messages.success(request, 'Form has been sent to the manager.')
    return redirect('form_list')

