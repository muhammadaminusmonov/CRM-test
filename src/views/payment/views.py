# finance/views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from finance.models import Payment
from .forms import PaymentForm
from student.models import Student
from classes.models import Group
import json
from decimal import Decimal

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    raise TypeError


def payment_management(request):
    payments = Payment.objects.all().order_by('-paid_at')

    # Calculate statistics
    total_payments = sum(p.amount for p in payments)

    # Group payments by month for average calculation
    monthly_payments = {}
    for payment in payments:
        month_key = payment.paid_at.strftime('%Y-%m')
        monthly_payments.setdefault(month_key, 0)
        monthly_payments[month_key] += payment.amount

    # Calculate monthly average
    monthly_avg = total_payments / len(monthly_payments) if monthly_payments else 0

    # Calculate pending payments (simplified)
    pending_payments = total_payments * Decimal('0.15')
  # 15% estimate

    # Calculate savings (15% of total payments)
    savings = total_payments * Decimal('0.15')

    # Prepare chart data
    categories = ['Group Fees', 'Teacher Payments', 'Other']
    amounts = [
        sum(p.amount for p in payments if p.to_group),
        sum(p.amount for p in payments if p.to_teacher),
        sum(p.amount for p in payments if not p.to_group and not p.to_teacher)
    ]

    context = {
        'payments': payments,
        'total_payments': total_payments,
        'monthly_avg': monthly_avg,
        'pending_payments': pending_payments,
        'savings': savings,
        'current_date': timezone.now(),
        'chart_labels': json.dumps(categories),
        'chart_data': json.dumps(amounts, default=decimal_default),
        'chart_colors': json.dumps([
            'rgba(54, 153, 255, 0.8)',  # Group Fees - blue
            'rgba(27, 197, 189, 0.8)',  # Teacher Payments - teal
            'rgba(137, 80, 252, 0.8)'  # Other - purple
        ])
    }
    return render(request, 'payment.html', context)


def create_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Payment for {payment.student} created successfully!',
                'payment': payment_json(payment)
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def update_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Payment for {payment.student} updated successfully!',
                'payment': payment_json(payment)
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def delete_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        student_name = str(payment.student)
        payment.delete()
        return JsonResponse({
            'success': True,
            'message': f'Payment for {student_name} deleted successfully!'
        })
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def toggle_payment_status(request, pk):
    # For payments, status is not directly toggleable in the model
    # This would be implemented based on your business logic
    return JsonResponse({
        'success': False,
        'message': 'Payment status cannot be toggled directly'
    })


def payment_json(payment):
    return {
        'id': payment.id,
        'student_id': payment.student.id,
        'student_name': f"{payment.student.first_name} {payment.student.last_name}",
        'paid_at': payment.paid_at.strftime('%b %d, %Y'),
        'amount': payment.amount,
        'paid_for_month': payment.paid_for_month.strftime('%B %Y'),
        'group_id': payment.to_group.id if payment.to_group else None,
        'group_name': payment.to_group.name if payment.to_group else '',
        'teacher_id': payment.to_teacher.id if payment.to_teacher else None,
        'teacher_name': f"{payment.to_teacher.first_name} {payment.to_teacher.last_name}" if payment.to_teacher else ''
    }