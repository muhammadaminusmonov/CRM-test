# teachers/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from teacher.models import Teacher
from .forms import TeacherForm


def teacher(request):
    # Get search parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    subject_filter = request.GET.get('subject', 'all')

    # Start with all teachers
    teachers = Teacher.objects.all()

    # Apply filters
    if search_query:
        teachers = teachers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    if status_filter != 'all':
        teachers = teachers.filter(status=status_filter)

    # Subject filter would require adding a subject field to the model
    # For now, we'll skip it since it's not in the original model

    context = {
        'teachers': teachers,
        'search_query': search_query,
        'status_filter': status_filter,
        'subject_filter': subject_filter,
    }

    return render(request, 'teacher.html', context)


def save_teacher(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        if teacher_id:
            teacher = get_object_or_404(Teacher, id=teacher_id)
            form = TeacherForm(request.POST, instance=teacher)
            action = 'updated'
        else:
            form = TeacherForm(request.POST)
            action = 'created'

        if form.is_valid():
            teacher = form.save()
            messages.success(request, f'Teacher {teacher.first_name} {teacher.last_name} {action} successfully!')
            return redirect('teacher')
        else:
            # Handle form errors
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'teacher.html', {
                'teachers': Teacher.objects.all(),
                'form': form,
                'teacher_id': teacher_id
            })

    return redirect('teacher')


def toggle_teacher_status(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Toggle between active (1) and inactive (5)
    if teacher.status == 1:  # Active
        teacher.status = 5  # Not working
    else:
        teacher.status = 1  # Active

    teacher.save()
    messages.success(request, f'Teacher status updated successfully!')
    return redirect('teacher')