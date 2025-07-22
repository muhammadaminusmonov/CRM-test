# staff/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from staff.models import Staff
from .forms import StaffForm


def staff_list(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    role_filter = request.GET.get('role', 'all')

    # Start with all staff
    staff = Staff.objects.all()

    # Apply filters
    if search_query:
        staff = staff.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if status_filter != 'all':
        staff = staff.filter(status=status_filter)

    if role_filter != 'all':
        staff = staff.filter(role=role_filter)

    # Calculate stats
    total_staff = Staff.objects.count()
    active_staff = Staff.objects.filter(status=1).count()
    # admin_staff = Staff.objects.filter(role='admin').count()
    # support_staff = Staff.objects.filter(role='support').count()

    context = {
        'staff': staff,
        'current_date': timezone.now().strftime("%A, %B %d, %Y"),
        'search_query': search_query,
        'status_filter': status_filter,
        'role_filter': role_filter,
        'total_staff': total_staff,
        'active_staff': active_staff,
        # 'admin_staff': admin_staff,
        # 'support_staff': support_staff,
    }

    return render(request, 'staff.html', context)


def save_staff(request, pk=None):
    if request.method == 'POST':
        if pk:
            staff = get_object_or_404(Staff, pk=pk)
            form = StaffForm(request.POST, instance=staff)
            action = 'updated'
        else:
            form = StaffForm(request.POST)
            action = 'created'

        if form.is_valid():
            staff = form.save()
            messages.success(request, f'Staff {staff.first_name} {staff.last_name} {action} successfully!')
            return redirect('staff_list')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'staff/staff_list.html', {
                'form': form,
                'staff_id': pk,
                'staff': Staff.objects.all()
            })

    return redirect('staff_list')


def toggle_staff_status(request, pk):
    staff = get_object_or_404(Staff, pk=pk)

    # Toggle between active (1) and inactive (2)
    if staff.status == 1:  # Active
        staff.status = 2  # Inactive
    else:
        staff.status = 1  # Active

    staff.save()
    messages.success(request, f'Staff status updated successfully!')
    return redirect('staff_list')