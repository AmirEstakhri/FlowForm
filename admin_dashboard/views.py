from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelform_factory
from django.shortcuts import render
from django.apps import apps
from django.http import Http404
from django.apps import apps
from django.shortcuts import render
from django.http import Http404
# Restrict access to superusers
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def model_add(request, model_name):
    app_model_map = {
        'Category': 'app',
        'Tag': 'app',
    }

    app_name = app_model_map.get(model_name)

    if not app_name:
        return render(request, 'error_template.html', {'message': 'Model not found'})

    try:
        model = apps.get_model(app_name, model_name)
        ModelForm = modelform_factory(model, exclude=())

        if request.method == 'POST':
            form = ModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin_dashboard:model_list', model_name=model_name)
        else:
            form = ModelForm()

        return render(request, 'admin_dashboard/model_form.html', {
            'form': form,
            'model_name': model_name
        })

    except LookupError:
        return render(request, 'error_template.html', {'message': 'Model not found'})

@superuser_required
def dashboard(request):
    models = apps.get_models()
    model_data = [
        {
            'name': model.__name__,
            'app_label': model._meta.app_label,
            'count': model.objects.count(),
        }
        for model in models
    ]
    return render(request, 'admin_dashboard/dashboard.html', {'models': model_data})

@superuser_required


@superuser_required
def model_list(request, model_name):
    # Define a mapping of model names to their corresponding apps
    app_model_map = {
        'CustomUser': 'app',
        'Tag': 'app',
        'Category': 'app',
        'Form': 'app',
        'FormVersion': 'app',
        'UserCategory': 'user_categories',
        'UserCategoryMembership': 'user_categories',
        'Profile': 'userprofile',
    }

    # Get the app name from the model name
    app_name = app_model_map.get(model_name)

    if not app_name:
        return render(request, 'error_template.html', {'message': 'Model not found in specified apps.'})

    try:
        # Get the model dynamically using apps.get_model()
        model = apps.get_model(app_name, model_name)

        # Retrieve all objects and model fields
        objects = model.objects.all()
        verbose_name_plural = model._meta.verbose_name_plural  # Get the plural form of the model's name
        fields = model._meta.fields  # Get the fields of the model

        # Render the list of objects and fields
        return render(
            request,
            'admin_dashboard/model_list.html',
            {
                'model_name': model_name,
                'verbose_name_plural': verbose_name_plural,
                'objects': objects,
                'fields': fields,
            }
        )
    except LookupError:
        # In case the model doesn't exist in the specified app
        return render(request, 'error_template.html', {'message': f'Model "{model_name}" not found in app "{app_name}".'})
    except Exception as e:
        # Catch any other unexpected errors
        return render(request, 'error_template.html', {'message': f'An error occurred: {str(e)}'})




@superuser_required
def model_add(request, model_name):
    app_model_map = {
        'Category': 'app',
        'Tag': 'app',
        'Form': 'app',  # Ensure Form model is mapped
    }

    app_name = app_model_map.get(model_name)

    if not app_name:
        return render(request, 'error_template.html', {'message': 'Model not found'})

    try:
        model = apps.get_model(app_name, model_name)
        ModelForm = modelform_factory(model, exclude=())

        if request.method == 'POST':
            form = ModelForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('admin_dashboard:model_list', model_name=model_name)
        else:
            form = ModelForm()

        return render(request, 'admin_dashboard/model_form.html', {
            'form': form,
            'model_name': model_name  # This is passed to the template
        })

    except LookupError:
        return render(request, 'error_template.html', {'message': 'Model not found'})


@superuser_required
def model_edit(request, model_name, pk):
    model = apps.get_model(app_label='app', model_name=model_name)
    obj = get_object_or_404(model, pk=pk)
    form_class = modelform_factory(model, fields='__all__')
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:model_list', model_name=model_name)
    else:
        form = form_class(instance=obj)
    return render(request, 'admin_dashboard/model_form.html', {'form': form, 'model': model})

@superuser_required
def model_delete(request, model_name, pk):
    model = apps.get_model(app_label='app', model_name=model_name)
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('admin_dashboard:model_list', model_name=model_name)
    return render(request, 'admin_dashboard/model_delete.html', {'object': obj, 'model': model})
