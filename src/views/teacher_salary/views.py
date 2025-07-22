from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Q
from teacher.models import Teacher
from finance.models import TeacherSalary
from .forms import TeacherSalaryForm, SalaryFilterForm
import datetime


def teacher_salary_view(request):
    # Initialize forms
    form = TeacherSalaryForm()
    filter_form = SalaryFilterForm(request.GET or None)

    # Handle CRUD operations
    if request.method == 'POST':
        # Create/Update record
        record_id = request.POST.get('record_id')
        if record_id:
            record = get_object_or_404(TeacherSalary, id=record_id)
            form = TeacherSalaryForm(request.POST, instance=record)
        else:
            form = TeacherSalaryForm(request.POST)

        if form.is_valid():
            salary = form.save()
            action = "updated" if record_id else "added"
            messages.success(request, f"Salary record {action} successfully!")
            return redirect('teacher_salary')

    # Handle record deletion
    delete_id = request.GET.get('delete')
    if delete_id:
        record = get_object_or_404(TeacherSalary, id=delete_id)
        record.delete()
        messages.success(request, "Salary record deleted successfully!")
        return redirect('teacher_salary')

    # Handle mark as paid
    mark_paid_id = request.GET.get('mark_paid')
    if mark_paid_id:
        record = get_object_or_404(TeacherSalary, id=mark_paid_id)
        record.paid = record.salary
        record.paid_date = datetime.date.today()
        record.save()
        messages.success(request, "Salary marked as paid successfully!")
        return redirect('teacher_salary')

    # Apply filters
    records = TeacherSalary.objects.all().order_by('-month')

    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        month = filter_form.cleaned_data.get('month')
        year = filter_form.cleaned_data.get('year')
        status = filter_form.cleaned_data.get('status')

        if search:
            records = records.filter(
                Q(teacher__first_name__icontains=search) |
                Q(teacher__last_name__icontains=search)
            )

        if month and month != 'all':
            records = records.filter(month__month=month)

        if year:
            records = records.filter(month__year=year)

        if status and status != 'all':
            if status == 'paid':
                records = records.filter(paid=F('salary'))
            elif status == 'unpaid':
                records = records.filter(paid=0)
            elif status == 'partial':
                records = records.filter(paid__gt=0, paid__lt=F('salary'))

    # Calculate statistics
    total_salaries = records.aggregate(total=Sum('salary'))['total'] or 0
    total_paid = records.aggregate(total=Sum('paid'))['total'] or 0
    pending_payments = total_salaries - total_paid
    teacher_count = Teacher.objects.count()

    context = {
        'form': form,
        'filter_form': filter_form,
        'records': records,
        'total_salaries': total_salaries,
        'total_paid': total_paid,
        'pending_payments': pending_payments,
        'teacher_count': teacher_count,
        'current_year': datetime.datetime.now().year
    }

    return render(request, 'teacher_salary.html', context)


from django.http import JsonResponse
from finance.models import TeacherSalary

def get_salary_record(request, record_id):
    try:
        record = TeacherSalary.objects.get(id=record_id)
        data = {
            'id': record.id,
            'teacher': record.teacher_id,
            'month': record.month.strftime('%Y-%m'),
            'salary': float(record.salary),
            'paid': float(record.paid),
            'paid_date': record.paid_date.strftime('%Y-%m-%d') if record.paid_date else None
        }
        return JsonResponse(data)
    except TeacherSalary.DoesNotExist:
        return JsonResponse({'error': 'Record not found'}, status=404)