from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import ProfileForm
from .models import Profile

# View to display user profile
@login_required
def view_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        raise Http404("Profile does not exist for this user.")
    return render(request, 'userprofile/view_profile.html', {'profile': profile})

# View to update the profile picture
@login_required
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES:  # Check if there are any files
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # Use the correct field name: profile_picture
            profile_picture_name = request.user.profile.profile_picture.name if request.user.profile.profile_picture else None
            return render(request, 'userprofile/update_picture.html', {'form': form, 'profile_picture_name': profile_picture_name})
        else:
            print(form.errors)  # Print form errors to debug
    else:
        form = ProfileForm(instance=request.user.profile)
        # Use the correct field name: profile_picture
        profile_picture_name = request.user.profile.profile_picture.name if request.user.profile.profile_picture else None
    
    return render(request, 'userprofile/update_picture.html', {'form': form, 'profile_picture_name': profile_picture_name})

# View to update the user's profile
@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('userprofile:update_profile')  # Redirect to avoid form resubmission
    else:
        form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'userprofile/update_profile.html', {'form': form})
