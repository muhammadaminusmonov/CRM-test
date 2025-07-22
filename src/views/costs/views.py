import json
from datetime import datetime, timedelta
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Sum
from finance.models import TeacherSalary, StaffSalary, Expanses
from teacher.models import Teacher
from staff.models import Staff

import json
from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return str(obj)  # Or use float(obj) if integers are acceptable
    raise TypeError

def costs_management(request):
    # Calculate statistics (same as before)
    today = datetime.now()
    last_month = today - timedelta(days=30)

    # Teacher costs
    teacher_costs = TeacherSalary.objects.aggregate(total=Sum('paid'))['total'] or 0
    teacher_costs_last_month = TeacherSalary.objects.filter(
        month__gte=last_month
    ).aggregate(total=Sum('paid'))['total'] or 0

    # Staff costs
    staff_costs = StaffSalary.objects.aggregate(total=Sum('paid'))['total'] or 0
    staff_costs_last_month = StaffSalary.objects.filter(
        month__gte=last_month
    ).aggregate(total=Sum('paid'))['total'] or 0

    # Expenses
    expenses = Expanses.objects.aggregate(total=Sum('amount'))['total'] or 0
    expenses_last_month = Expanses.objects.filter(
        date__gte=last_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Total costs
    total_costs = teacher_costs + staff_costs + expenses
    total_costs_last_month = teacher_costs_last_month + staff_costs_last_month + expenses_last_month

    # Calculate trends
    teacher_trend = calculate_trend(teacher_costs, teacher_costs_last_month)
    staff_trend = calculate_trend(staff_costs, staff_costs_last_month)
    expenses_trend = calculate_trend(expenses, expenses_last_month)
    total_trend = calculate_trend(total_costs, total_costs_last_month)

    # Prepare data for chart
    months = []
    teacher_data = []
    staff_data = []
    expenses_data = []
    total_data = []

    for i in range(6, 0, -1):
        month = today - timedelta(days=30 * i)
        month_str = month.strftime("%b")
        months.append(month_str)

        # Teacher costs for month
        teacher_month = TeacherSalary.objects.filter(
            month__month=month.month,
            month__year=month.year
        ).aggregate(total=Sum('paid'))['total'] or 0
        teacher_data.append(teacher_month)

        # Staff costs for month
        staff_month = StaffSalary.objects.filter(
            month__month=month.month,
            month__year=month.year
        ).aggregate(total=Sum('paid'))['total'] or 0
        staff_data.append(staff_month)

        # Expenses for month
        expenses_month = Expanses.objects.filter(
            date__month=month.month,
            date__year=month.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        expenses_data.append(expenses_month)

        # Total for month
        total_data.append(teacher_month + staff_month + expenses_month)

    # Get all teachers and staff for form dropdowns
    teachers = Teacher.objects.filter(status=1)
    staff_members = Staff.objects.filter(status=1)

    # Prepare data for tables
    teacher_costs_data = TeacherSalary.objects.select_related('teacher').all()
    staff_costs_data = StaffSalary.objects.select_related('staff').all()
    expenses_data_list = Expanses.objects.all()

    context = {
        'teacher_costs': teacher_costs,
        'staff_costs': staff_costs,
        'expenses': expenses,
        'total_costs': total_costs,
        'teacher_trend': teacher_trend,
        'staff_trend': staff_trend,
        'expenses_trend': expenses_trend,
        'total_trend': total_trend,
        'chart_data': json.dumps({
            'months': months,
            'teacher_data': teacher_data,
            'staff_data': staff_data,
            'expenses_data': expenses_data,
            'total_data': total_data
        }, default=decimal_default),  # Add `default` parameter
        'teachers': teachers,
        'staff_members': staff_members,
        'teacher_costs_data': teacher_costs_data,
        'staff_costs_data': staff_costs_data,
        'expenses_data_list': expenses_data_list,
    }
    return render(request, 'costs.html', context)

def calculate_trend(current, previous):
    if previous == 0:
        return 0
    return round(((current - previous) / previous) * 100)


@require_http_methods(["POST"])
def save_teacher_salary(request):
    # Implementation would handle form submission
    pass


@require_http_methods(["POST"])
def save_staff_salary(request):
    # Implementation would handle form submission
    pass


@require_http_methods(["POST"])
def save_expense(request):
    # Implementation would handle form submission
    pass


@require_http_methods(["DELETE"])
def delete_teacher_salary(request, id):
    # Implementation would handle deletion
    pass


@require_http_methods(["DELETE"])
def delete_staff_salary(request, id):
    # Implementation would handle deletion
    pass


@require_http_methods(["DELETE"])
def delete_expense(request, id):
    # Implementation would handle deletion
    pass