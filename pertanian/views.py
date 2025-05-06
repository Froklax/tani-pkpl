from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import timedelta, date
from .models import Plant, Field, Planting
from .forms import PlantForm, FieldForm, PlantingForm

@login_required(login_url='/login')
def dashboard(request):
    field_count = Field.objects.filter(user=request.user).count()
    active_plantings = Planting.objects.filter(
        field__user=request.user, 
        status__in=['Preparation', 'Planting', 'Maintenance']
    ).count()
    ready_maintenance = Planting.objects.filter(
    field__user=request.user,
    status='Maintenance',
    estimated_harvest__lte=date.today()
    )
    ready_harvest = Planting.objects.filter(
        field__user=request.user,
        status='Harvest'
    )
    ready_for_harvest = ready_maintenance.count() + ready_harvest.count()

    context = {
        'field_count': field_count,
        'active_plantings': active_plantings,
        'ready_for_harvest': ready_for_harvest
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='/login')
def plant_list(request):
    plants = Plant.objects.all()
    return render(request, 'plant_list.html', {'plant_list': plants})

@login_required(login_url='/login')
def plant_detail(request, pk):
    plant = get_object_or_404(Plant, pk=pk)
    return render(request, 'plant_detail.html', {'plant': plant})

@login_required(login_url='/login')
@transaction.atomic
def plant_create(request):
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plant added successfully!')
            return redirect('pertanian:plant_list')
    else:
        form = PlantForm()
    return render(request, 'plant_form.html', {'form': form})

@login_required(login_url='/login')
def field_list(request):
    fields = Field.objects.filter(user=request.user)
    return render(request, 'field_list.html', {'field_list': fields})

@login_required(login_url='/login')
def field_detail(request, pk):
    field = get_object_or_404(Field, pk=pk, user=request.user)
    plantings = Planting.objects.filter(field=field)
    return render(request, 'field_detail.html', {'field': field, 'planting_list': plantings})

@login_required(login_url='/login')
@transaction.atomic
def field_create(request):
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.user = request.user
            field.save()
            messages.success(request, 'Field added successfully!')
            return redirect('pertanian:field_list')
    else:
        form = FieldForm()
    return render(request, 'field_form.html', {'form': form})

@login_required(login_url='/login')
def planting_list(request):
    plantings = Planting.objects.filter(field__user=request.user)
    return render(request, 'planting_list.html', {'planting_list': plantings})

@login_required(login_url='/login')
def planting_detail(request, pk):   
    planting = get_object_or_404(Planting, pk=pk, field__user=request.user)
    return render(request, 'planting_detail.html', {'planting': planting})

@login_required(login_url='/login')
@transaction.atomic
def planting_create(request):
    if request.method == 'POST':
        form = PlantingForm(request.POST)
        form.fields['field'].queryset = Field.objects.filter(user=request.user)
        if form.is_valid():
            try:
                planting = form.save(commit=False)

                if planting.field.user != request.user:
                    raise Exception("You do not have access to this field")

                planting.total_cost = planting.plant.seed_price * planting.seed_count
                planting.estimated_harvest = planting.planting_date + timedelta(days=planting.plant.harvest_time)
                planting.save()

                messages.success(request, 'Planting recorded successfully!')
                return redirect('pertanian:planting_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
                print(f"Exception: {str(e)}")
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, f'Form is invalid: {form.errors}')
    else:
        form = PlantingForm()
        form.fields['field'].queryset = Field.objects.filter(user=request.user)

    return render(request, 'planting_form.html', {'form': form})

@login_required(login_url='/login')
@transaction.atomic
def planting_update_status(request, pk):
    print(f"Received request to update planting status for pk={pk}")
    planting = get_object_or_404(Planting, pk=pk, field__user=request.user)
    print(f"Found planting: {planting.pk}, current status: {planting.status}")
    
    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        new_status = request.POST.get('status')
        print(f"New status from form: {new_status}")
        
        valid_choices = dict(Planting.STATUS_CHOICES)
        print(f"Valid status choices: {valid_choices}")
        
        if new_status in valid_choices:
            print(f"Status valid, updating from {planting.status} to {new_status}")
            try:
                planting.status = new_status
                planting.save()
                print("Status updated successfully")
                messages.success(request, f'Planting status updated to {new_status} successfully!')
            except Exception as e:
                print(f"Error saving status: {str(e)}")
                messages.error(request, f'Error: {str(e)}')
        else:
            print(f"Invalid status: '{new_status}' not in {valid_choices}")
            messages.error(request, 'Invalid status!')
    else:
        print(f"Request method is {request.method}, not POST")
    
    return redirect('pertanian:planting_detail', pk=pk)