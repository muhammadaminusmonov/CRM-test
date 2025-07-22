# views.py
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Count
from django.contrib.humanize.templatetags.humanize import intcomma
from student.models import Student
from teacher.models import Teacher
from staff.models import Staff
from classes.models import Group, Class
from finance.models import Payment, Expanses, TeacherSalary, StaffSalary


def statistic(request):
    # Calculate current date
    current_date = timezone.now().strftime("%A, %B %d, %Y")

    # Financial statistics
    total_payments = round(float(Payment.objects.aggregate(total=Sum('amount'))['total'] or 0), 2)
    teacher_salaries = round(float(TeacherSalary.objects.aggregate(total=Sum('paid'))['total'] or 0), 2)
    staff_salaries = round(float(StaffSalary.objects.aggregate(total=Sum('paid'))['total'] or 0), 2)

    # Entity counts
    active_students = Student.objects.filter(status=1).count()
    active_teachers = Teacher.objects.filter(status=1).count()
    active_staff = Staff.objects.filter(status=1).count()
    active_groups = Group.objects.filter(status=1).count()

    # Recent salary payments (last 5)
    recent_teacher_salaries = TeacherSalary.objects.select_related('teacher').order_by('-paid_date')[:5]
    recent_staff_salaries = StaffSalary.objects.select_related('staff').order_by('-paid_date')[:5]

    # Combine and sort recent payments
    recent_salaries = list(recent_teacher_salaries) + list(recent_staff_salaries)
    recent_salaries = sorted(recent_salaries, key=lambda x: x.paid_date, reverse=True)[:5]

    # Profit analysis data (last 6 months)
    months = []
    gross_profits = []
    net_profits = []

    # This would be replaced with actual data from your models
    for i in range(6):
        months.append(f"Month {i + 1}")
        gross_profits.append(10000 * (i + 1))
        net_profits.append(8000 * (i + 1))

    # Expense distribution (example data)
    expense_categories = ['Salaries', 'Rent', 'Utilities', 'Supplies', 'Marketing']
    expense_data = [60, 15, 10, 10, 5]

    context = {
        'current_date': current_date,
        'total_payments': intcomma(total_payments),
        'teacher_salaries': intcomma(teacher_salaries),
        'staff_salaries': intcomma(staff_salaries),
        'active_students': active_students,
        'active_teachers': active_teachers,
        'active_staff': active_staff,
        'active_groups': active_groups,
        'recent_salaries': recent_salaries,
        'profit_labels': months,
        'gross_profits': gross_profits,
        'net_profits': net_profits,
        'expense_categories': expense_categories,
        'expense_data': expense_data,
    }

    return render(request, 'statistic.html', context)