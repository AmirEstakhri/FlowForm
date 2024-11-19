# forms.py

from django import forms
from .models import Form, Tag, Category, CustomUser

class FormCreationForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        label="Tags"
    )
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Category"
    )

    receiver_signature = forms.CharField(required=False, label="Receiver's Signature")
    sender = forms.CharField(max_length=100, disabled=True, label="Sender")  # Disabled sender field, auto-filled
    assigned_users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        required=False,  # If this is optional
        label="Assigned Users"
    )

    assigned_managers = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='manager'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        required=True,
        label="Assigned Managers"
    )  # Field to allow selecting multiple managers
    
    allowed_managers = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(role='manager'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label="Allowed Managers (view-only)"
    )  # Allow additional managers for viewing the form

    class Meta:
        model = Form
        fields = [
            'title', 'sender', 'sender_signature', 'receiver', 'receiver_signature',
            'content', 'priority', 'tags', 'categories', 'assigned_users', 'assigned_managers', 'allowed_managers'
        ]

    def clean_assigned_managers(self):
        assigned_managers = self.cleaned_data.get('assigned_managers')

        # Ensure that the sender is not among the assigned managers
        if self.instance.sender and self.instance.sender in [manager.username for manager in assigned_managers]:
            raise forms.ValidationError("The sender cannot be the same as the assigned manager.")

        return assigned_managers

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Dynamically set queryset for 'assigned_managers' and 'allowed_managers' based on sub-role
        if user:
            self.fields['sender'].initial = user.username
            self.instance.sender = user.username

            # Check user's sub-role to determine allowed managers and users
            if user.sub_role == 'user-access-to-all-users-with-role-user':
                self.fields['assigned_managers'].queryset = CustomUser.objects.filter(role='manager')
                self.fields['allowed_managers'].queryset = CustomUser.objects.filter(role='manager')
            elif user.sub_role == 'manager-access-to-all-users-with-role-manager':
                self.fields['assigned_managers'].queryset = CustomUser.objects.filter(role='manager').exclude(id=user.id)
                self.fields['allowed_managers'].queryset = CustomUser.objects.filter(role='manager').exclude(id=user.id)

    def clean(self):
        cleaned_data = super().clean()
        assigned_managers = cleaned_data.get('assigned_managers')
        receiver = cleaned_data.get('receiver')

        # Automatically set the receiver to the assigned manager's username if it's empty
        if assigned_managers and not receiver:
            cleaned_data['receiver'] = assigned_managers[0].username  # Fill receiver with the first manager's username if assigned managers are selected

        return cleaned_data

    def save(self, commit=True):
        # Save the form instance without committing to get the object
        form_instance = super().save(commit=False)

        # Ensure the sender is set
        if not form_instance.sender:
            form_instance.sender = self.initial.get('sender')

        # Save the instance to assign an ID
        form_instance.save()

        # Many-to-many fields can now be set
        if self.cleaned_data.get('assigned_managers'):
            form_instance.assigned_managers.set(self.cleaned_data['assigned_managers'])

        if self.cleaned_data.get('allowed_managers'):
            form_instance.allowed_managers.set(self.cleaned_data['allowed_managers'])

        if self.cleaned_data.get('assigned_users'):
            form_instance.assigned_users.set(self.cleaned_data['assigned_users'])

        # If categories exist, set them
        category = self.cleaned_data.get('categories')
        if category:
            form_instance.category = category

        # Save again if commit is True
        if commit:
            form_instance.save()

        return form_instance


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")



class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']
