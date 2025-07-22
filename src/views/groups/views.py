import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from classes.models import Group
from .forms import GroupForm, StudentForm
from student.models import Student
from classes.models import Class
from teacher.models import Teacher
from datetime import datetime


def group_management(request):
    # Get all groups with related data
    groups = Group.objects.select_related('teacher', 'classes').prefetch_related('student').all()

    # Prepare data for template
    groups_data = []
    for group in groups:
        groups_data.append({
            'id': group.id,
            'name': group.name,
            'teacher': f"{group.teacher.first_name} {group.teacher.last_name}" if group.teacher else "No Teacher",
            'class_name': group.classes.title if group.classes else "No Class",
            'start_at': group.start_at,
            'end_at': group.end_at,
            'lessons_per_week': group.lesson_per_week,
            'status': group.get_status_display().lower(),
            'students': [
                {
                    'id': s.id,
                    'name': f"{s.first_name} {s.last_name}",
                    'email': s.email,
                    'join_date': s.join_date,
                    'status': s.get_status_display().lower(),
                } for s in group.student.all()
            ]
        })

    # Prepare statistics
    total_groups = Group.objects.count()
    active_groups = Group.objects.filter(status=1).count()

    # Get all teachers and classes for form dropdowns
    teachers = Teacher.objects.filter(status=1)
    classes = Class.objects.filter(status=1)

    context = {
        'groups_json': json.dumps(groups_data, default=str),
        'teachers': teachers,
        'classes': classes,
        'total_groups': total_groups,
        'active_groups': active_groups,
    }
    return render(request, 'group.html', context)


@require_http_methods(["POST"])
def save_group(request):
    form = GroupForm(request.POST)
    if form.is_valid():
        group = form.save()
        return JsonResponse({'success': True, 'group_id': group.id})
    return JsonResponse({'success': False, 'errors': form.errors})


@require_http_methods(["DELETE"])
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return JsonResponse({'success': True})


@require_http_methods(["POST"])
def add_student_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    student_id = request.POST.get('student_id')
    student = get_object_or_404(Student, id=student_id)
    group.student.add(student)
    return JsonResponse({'success': True})


@require_http_methods(["DELETE"])
def remove_student_from_group(request, group_id, student_id):
    group = get_object_or_404(Group, id=group_id)
    student = get_object_or_404(Student, id=student_id)
    group.student.remove(student)
    return JsonResponse({'success': True})