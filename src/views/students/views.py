# students/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from student.models import Student
from .forms import StudentForm


def students_list(request):
    # Get search parameters
    students = Student.objects.all()

    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')

    if status_filter != 'all':
        try:
            status_filter_int = int(status_filter)
            students = students.filter(status=status_filter_int)
        except ValueError:
            status_filter = 'all'

    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    context = {
        'students': students,
        'current_date': timezone.now().strftime("%A, %B %d, %Y"),
        'search_query': search_query,
        'status_filter': status_filter,
        'Student': Student,
    }

    return render(request, 'students.html', context)


def save_student(request, pk=None):
    if request.method == 'POST':
        if pk:
            student = get_object_or_404(Student, pk=pk)
            form = StudentForm(request.POST, instance=student)
            action = 'updated'
        else:
            form = StudentForm(request.POST)
            action = 'created'

        if form.is_valid():
            student = form.save()
            messages.success(request, f'Student {student.first_name} {student.last_name} {action} successfully!')
            return redirect('students_list')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'students/students_list.html', {
                'form': form,
                'student_id': pk,
                'students': Student.objects.all()
            })

    return redirect('students_list')


def toggle_student_status(request, pk):
    student = get_object_or_404(Student, pk=pk)

    # Toggle between active (1) and inactive (2)
    if student.status == 1:  # Active
        student.status = 2  # Inactive
    else:
        student.status = 1  # Active

    student.save()
    messages.success(request, f'Student status updated successfully!')
    return redirect('students_list')
