from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Form, FormVersion, CustomUser, Tag, Category  # Import relevant models
from .forms import FormCreationForm, LoginForm  # Import relevant forms
from app.utils import is_manager  # Assuming `is_manager` is a utility function to check roles
import logging
from user_categories.models import UserCategoryMembership

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Tag, Category, UserCategory, UserCategoryMembership

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FormCreationForm
from .models import CustomUser, Tag, Category, UserCategoryMembership, Form

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FormCreationForm
from .models import CustomUser, Tag, Category

# @login_required
# def create_form(request):
#     # Initialize querysets for users and managers
#     managers = CustomUser.objects.filter(role='manager')  # Default: All managers to show
#     all_users = None  # Users based on logged-in user's sub-role
#     all_managers = CustomUser.objects.filter(role='manager')  # Default: Managers

#     # Get all tags and categories from the database
#     tags = Tag.objects.all()
#     categories = Category.objects.all()

#     # Handle filtering based on logged-in user's role and sub-role
#     if request.user.role == 'user':
#         if request.user.sub_role == 'user-access-to-all-users-with-role-user':
#             # User with this sub-role can see all users with role 'user'
#             all_users = CustomUser.objects.filter(role='user')
#     elif request.user.sub_role == 'manager-access-to-all-users-with-role-manager':
#         # Managers with this sub-role can see all users and managers, excluding themselves
#         all_users = CustomUser.objects.filter(role='user')
#         all_managers = CustomUser.objects.filter(role='manager').exclude(id=request.user.id)

#     # Handle filtering based on selected category (if any)
#     selected_category_id = request.GET.get('category', None)
#     if selected_category_id:
#         category = Category.objects.get(id=selected_category_id)
#         all_users = CustomUser.objects.filter(
#             usercategorymembership__category=category
#         )
#         all_managers = CustomUser.objects.filter(
#             role='manager',
#             usercategorymembership__category=category
#         ).exclude(id=request.user.id)

#     # Handle form submission
#     if request.method == 'POST':
#         form = FormCreationForm(request.POST, user=request.user)  # Pass logged-in user to form
#         if form.is_valid():
#             try:
#                 # Save form instance without committing to get the instance ID
#                 form_instance = form.save(commit=False)
#                 form_instance.save()  # Save to generate ID
                
#                 # Set ManyToMany and ForeignKey relationships after saving the form instance
#                 tags_selected = form.cleaned_data.get('tags')
#                 if tags_selected:
#                     form_instance.tags.set(tags_selected)  # Set tags to the form
                
#                 category_selected = form.cleaned_data.get('category')
#                 if category_selected:
#                     form_instance.category = category_selected  # Set category

#                 # Handle assigned managers (ManyToManyField)
#                 assigned_managers = form.cleaned_data.get('assigned_managers')
#                 if assigned_managers:
#                     form_instance.assigned_managers.set(assigned_managers)  # Assign managers
               
#                 # Handle added users (ManyToManyField)
#                 added_users = form.cleaned_data.get('added_users')
#                 if added_users:
#                     form_instance.added_users.set(added_users)  # Assign users to the form

#                 form_instance.save()  # Save again to commit ManyToMany and ForeignKey fields

#                 # Provide success message and redirect to form list
#                 messages.success(request, 'Form created successfully!')
#                 return redirect('form_list')  # Adjust URL as needed for form listing page
#             except Exception as e:
#                 # Handle any exceptions during save
#                 messages.error(request, f'Error saving the form: {e}')
#         else:
#             # If form is not valid, show field errors
#             field_errors = {field: error for field, error in form.errors.items()}
#             messages.error(request, f'There was an error creating the form: {field_errors}')
#     else:
#         # Initialize the form with the logged-in user instance
#         form = FormCreationForm(user=request.user)

#     # Render the form creation page with all necessary context
#     return render(request, 'form/create_form.html', {
#         'form': form,
#         'managers': managers,  # All managers (or filtered based on category)
#         'all_users': all_users,  # All users based on the logged-in user's sub-role or category
#         'all_managers': all_managers,  # All managers based on the selected category or sub-role
#         'tags': tags,
#         'categories': categories,  # Display categories for filtering
#         'user': request.user,  # Pass logged-in user to template for context
#     })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Tag, Category, CustomUser, Form
from .forms import FormCreationForm

@login_required
def create_form(request):
    # Get the logged-in user's categories
    user_categories = request.user.usercategorymembership_set.values_list('category', flat=True)

    # Initialize querysets for managers filtered by shared categories
    assigned_managers = CustomUser.objects.filter(
        role='manager',
        usercategorymembership__category__in=user_categories
    ).distinct()  # Ensure unique results

    # Initialize querysets for users only if the user has the required sub-role
    if request.user.sub_role == "user-access-to-all-users-with-role-user":
        assigned_users = CustomUser.objects.filter(
            role='user',
            usercategorymembership__category__in=user_categories
        ).distinct()  # Ensure unique results
    else:
        assigned_users = CustomUser.objects.none()  # Empty queryset if no sub-role

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



# views.py
from django.shortcuts import render
from .models import CustomUser  

def user_list(request):
    # Fetch users with the 'manager' role
    managers = CustomUser.objects.filter(role='manager')
    return render(request, 'your_template.html', {'managers': managers})




from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Form

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Form

from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def form_list(request):
    user = request.user

    # For users with the 'user-access-to-all-users-with-role-user' sub-role
    if user.role == 'user':
        if user.sub_role == 'user-access-to-all-users-with-role-user':
            # Include forms where the user is either the sender or an assigned user
            forms = Form.objects.filter(
                Q(sender=user) | 
                Q(assigned_users=user)  # Using assigned_users field
            ).distinct()
        else:
            # For regular users, only show forms where they are the sender
            forms = Form.objects.filter(sender=user).distinct()

    # For managers
    elif user.role == 'manager':
        # No sub-role check is needed for managers; they can access forms where they are assigned as a manager
        if user.sub_role == 'manager-access-to-all-users-with-role-manager':
            # Managers with sub-role can access forms where they are an assigned manager, allowed manager, or if the sender is a user
            forms = Form.objects.filter(
                Q(assigned_managers=user) |  # Forms where the user is assigned as a manager
                Q(allowed_managers=user) |  # Forms where the user is allowed as a manager
                Q(sender__role='user')  # Or forms sent by a user
            ).distinct()
        else:
            # Managers without sub-role can still view forms where they are assigned as a manager or allowed as a manager
            forms = Form.objects.filter(
                Q(assigned_managers=user) |
                Q(allowed_managers=user)  # Using allowed_managers field
            ).distinct()

    # Admin or other roles
    else:
        # Admins see all forms
        forms = Form.objects.all()

    # Prefetch related fields to optimize queries (tags and category)
    forms = forms.prefetch_related('tags', 'category')  # Correct 'category' not 'categories'

    return render(request, 'form/form_list.html', {'forms': forms})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Form

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


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Form

@login_required
def forms_assigned_to_manager(request):
    # Get the logged-in user
    current_user = request.user

    # Query forms where the current user is an assigned manager
    forms = Form.objects.filter(assigned_managers__username=current_user.username).distinct()

    # Render the filtered forms
    return render(request, 'forms/assigned-pages/assigned_to_manager.html', {'forms': forms})


@login_required
@user_passes_test(is_manager)
def verify_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    if form.status == 'Pending':
        form.status = 'Verified'
        form.verified_by = request.user  # Track who verified the form
        form.verified_at = timezone.now()  # Track verification time
        form.save()
        messages.success(request, 'Form has been verified.')
    else:
        messages.warning(request, 'This form has already been verified.')
    return redirect('form_list')





def is_manager(user):
    return user.role == 'manager' or user.role == 'user'

@login_required
@user_passes_test(is_manager)
def edit_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    
    # Check if the user is allowed to edit this form
    user_is_form_owner = form.sender == request.user.username
    form_is_verified = form.verified

    # If the form is verified, only the 'Priority' field is editable
    restricted = form_is_verified or not user_is_form_owner
    if form_is_verified:
        messages.warning(request, 'This form is verified and can only have its priority updated.')
    elif not user_is_form_owner:
        messages.warning(request, 'You are not authorized to edit this form.')

    # Handle the form submission
    if request.method == 'POST':
        if restricted:
            form_form = FormCreationForm(request.POST, instance=form, user=request.user, restricted=restricted)
        else:
            form_form = FormCreationForm(request.POST, instance=form, user=request.user)

        if form_form.is_valid():
            form_form.save()
            messages.success(request, 'Form updated successfully.')
            return redirect('form_list')
    else:
        form_form = FormCreationForm(instance=form, user=request.user, restricted=restricted)

    return render(request, 'form/edit_form.html', {'form': form_form})





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

    if request.method == 'POST':
        if form.verified:
            messages.error(request, 'This form has already been verified and cannot be sent again.')
            return redirect('form_list')
        if request.user.role == 'manager' and form.sender_name == request.user.username:
            messages.error(request, 'You cannot send a form to yourself.')
            return redirect('form_list')

        form.verified = True
        form.save()
        messages.success(request, 'Form sent successfully and marked as verified!')
        return redirect('form_list')

    return render(request, 'form/send_form.html', {'form': form})

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
