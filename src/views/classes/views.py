from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Avg
from django.http import JsonResponse
from classes.models import Class, Group
import datetime


def classes_view(request):
    # Get all classes
    classes = Class.objects.all().order_by('title')

    # Calculate statistics
    total_classes = classes.count()
    active_classes = classes.filter(status=1).count()
    active_percentage = round((active_classes / total_classes) * 100) if total_classes else 0

    # Calculate average cost
    avg_cost = classes.aggregate(avg_cost=Avg('cost_per_month'))['avg_cost'] or 0

    # Find most popular class (based on number of groups)
    popular_class = Group.objects.values('classes__title').annotate(
        group_count=Count('id')
    ).order_by('-group_count').first()
    popular_class_name = popular_class['classes__title'] if popular_class else "N/A"

    context = {
        'classes': classes,
        'total_classes': total_classes,
        'active_classes': active_classes,
        'active_percentage': active_percentage,
        'avg_cost': avg_cost,
        'popular_class': popular_class_name,
        'current_date': datetime.datetime.now().strftime("%A, %B %d, %Y")
    }
    return render(request, 'class.html', context)


def add_class_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cost_per_month = request.POST.get('cost_per_month')
        duration_per_lesson = request.POST.get('duration_per_lesson')
        length = request.POST.get('length')
        description = request.POST.get('description')
        status = request.POST.get('status', 1)

        errors = {}

        # Validation
        if not title:
            errors['title'] = ['Title is required']
        if not cost_per_month or float(cost_per_month) <= 0:
            errors['cost'] = ['Cost must be a positive number']
        if not duration_per_lesson or int(duration_per_lesson) < 15:
            errors['duration'] = ['Duration must be at least 15 minutes']
        if not length:
            errors['length'] = ['Course length is required']
        if not description:
            errors['description'] = ['Description is required']

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # Create class
        new_class = Class.objects.create(
            title=title,
            cost_per_month=cost_per_month,
            duration_per_lesson=datetime.time(
                hour=int(duration_per_lesson) // 60,
                minute=int(duration_per_lesson) % 60
            ),
            length=length,
            description=description,
            status=status
        )

        return JsonResponse({
            'success': True,
            'message': f'Class "{new_class.title}" added successfully!'
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def edit_class_view(request, class_id):
    cls = get_object_or_404(Class, id=class_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        cost_per_month = request.POST.get('cost_per_month')
        duration_per_lesson = request.POST.get('duration_per_lesson')
        length = request.POST.get('length')
        description = request.POST.get('description')
        status = request.POST.get('status', 1)

        errors = {}

        # Validation
        if not title:
            errors['title'] = ['Title is required']
        if not cost_per_month or float(cost_per_month) <= 0:
            errors['cost'] = ['Cost must be a positive number']
        if not duration_per_lesson or int(duration_per_lesson) < 15:
            errors['duration'] = ['Duration must be at least 15 minutes']
        if not length:
            errors['length'] = ['Course length is required']
        if not description:
            errors['description'] = ['Description is required']

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        # Update class
        cls.title = title
        cls.cost_per_month = cost_per_month
        cls.duration_per_lesson = datetime.time(
            hour=int(duration_per_lesson) // 60,
            minute=int(duration_per_lesson) % 60
        )
        cls.length = length
        cls.description = description
        cls.status = status
        cls.save()

        return JsonResponse({
            'success': True,
            'message': f'Class "{cls.title}" updated successfully!'
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def toggle_class_status(request, class_id):
    cls = get_object_or_404(Class, id=class_id)
    new_status = 2 if cls.status == 1 else 1
    cls.status = new_status
    cls.save()

    return JsonResponse({
        'success': True,
        'message': f'Class "{cls.title}" has been {"activated" if new_status == 1 else "deactivated"}',
        'new_status': new_status
    })