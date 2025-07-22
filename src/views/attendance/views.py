# attendance/views.py
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from classes.models import Group, Attendance
from student.models import Student
from django.db.models import Count


def attendance_view(request):
    # Get current date or selected date
    date_str = request.GET.get('date', timezone.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    # Get all active groups
    groups = Group.objects.filter(status=1).prefetch_related('student', 'classes', 'teacher')

    context = {
        'current_date': selected_date,
        'groups': groups,
        'date': date_str
    }
    return render(request, 'attendance.html', context)


def group_attendance_view(request, group_id, date):
    try:
        # Parse date and get group
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        group = Group.objects.prefetch_related('student').get(id=group_id)

        # Process form submission
        if request.method == 'POST':
            for student in group.student.all():
                status_key = f'status_{student.id}'
                if status_key in request.POST:
                    # Get or create attendance record
                    attendance, created = Attendance.objects.get_or_create(
                        group=group,
                        student=student,
                        date=selected_date,
                        defaults={'status': request.POST[status_key]}
                    )
                    if not created:
                        attendance.status = request.POST[status_key]
                        attendance.save()
            return redirect('group_attendance', group_id=group_id, date=date)

        # Get attendance records for this group/date
        attendances = []
        for student in group.student.all():
            try:
                attendance = Attendance.objects.get(
                    group=group,
                    student=student,
                    date=selected_date
                )
            except Attendance.DoesNotExist:
                attendance = Attendance(
                    group=group,
                    student=student,
                    date=selected_date,
                    status=2  # Default to Absent
                )
            attendances.append(attendance)

        # Calculate status counts
        status_counts = Attendance.objects.filter(
            group=group,
            date=selected_date
        ).values('status').annotate(count=Count('status'))

        status_dict = {1: 0, 2: 0, 3: 0}
        for item in status_counts:
            status_dict[item['status']] = item['count']

        context = {
            'current_group_id': group_id,
            'group': group,
            'attendances': attendances,
            'status_counts': status_dict,
            'date': date
        }
        return render(request, 'attendance.html', context)

    except Group.DoesNotExist:
        return redirect('attendance')