# finance/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from finance.models import Expanses
from .forms import ExpenseForm
from decimal import Decimal


def expense_management(request):
    # Get all expenses ordered by date
    expenses = Expanses.objects.all().order_by('-date')

    # Calculate statistics
    total_expenses = sum(e.amount for e in expenses)

    # Group expenses by month for average calculation
    monthly_expenses = {}
    for expense in expenses:
        month_key = expense.date.strftime('%Y-%m')
        monthly_expenses.setdefault(month_key, 0)
        monthly_expenses[month_key] += expense.amount

    # Calculate monthly average
    monthly_avg = total_expenses / len(monthly_expenses) if monthly_expenses else 0

    # Calculate pending payments (unpaid expenses)
    pending_payments = sum(e.amount for e in expenses if not e.status)

    # Calculate savings (15% of total expenses as an example)
    savings = total_expenses * Decimal('0.15')

    # Prepare chart data
    categories = {
        'Rent': 0,
        'Utilities': 0,
        'Taxes': 0,
        'Supplies': 0,
        'Equipment': 0,
        'Other': 0
    }

    # For demo purposes - in real app, you'd categorize properly
    for expense in expenses:
        if 'rent' in expense.name.lower():
            categories['Rent'] += expense.amount
        elif 'internet' in expense.name.lower() or 'electric' in expense.name.lower():
            categories['Utilities'] += expense.amount
        elif 'tax' in expense.name.lower():
            categories['Taxes'] += expense.amount
        elif 'material' in expense.name.lower() or 'supply' in expense.name.lower():
            categories['Supplies'] += expense.amount
        elif 'projector' in expense.name.lower() or 'equipment' in expense.name.lower():
            categories['Equipment'] += expense.amount
        else:
            categories['Other'] += expense.amount

    context = {
        'expenses': expenses,
        'total_expenses': total_expenses,
        'monthly_avg': monthly_avg,
        'pending_payments': pending_payments,
        'savings': savings,
        'current_date': timezone.now(),
        'chart_labels': list(categories.keys()),
        'chart_data': list(categories.values()),
        'chart_colors': [
            'rgba(27, 197, 189, 0.8)',  # Rent - teal
            'rgba(54, 153, 255, 0.8)',  # Utilities - blue
            'rgba(137, 80, 252, 0.8)',  # Taxes - purple
            'rgba(255, 168, 0, 0.8)',  # Supplies - orange
            'rgba(246, 78, 96, 0.8)',  # Equipment - red
            'rgba(181, 181, 195, 0.8)'  # Other - gray
        ]
    }
    return render(request, 'expenses.html', context)


def create_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Expense "{expense.name}" created successfully!',
                'expense': {
                    'id': expense.id,
                    'name': expense.name,
                    'description': expense.description,
                    'date': expense.date.strftime('%b %d, %Y'),
                    'amount': expense.amount,
                    'status': expense.status,
                    'status_display': 'Paid' if expense.status else 'Pending'
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return HttpResponseBadRequest('Invalid request')


def update_expense(request, pk):
    expense = get_object_or_404(Expanses, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Expense "{expense.name}" updated successfully!',
                'expense': {
                    'id': expense.id,
                    'name': expense.name,
                    'description': expense.description,
                    'date': expense.date.strftime('%b %d, %Y'),
                    'amount': expense.amount,
                    'status': expense.status,
                    'status_display': 'Paid' if expense.status else 'Pending'
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    return HttpResponseBadRequest('Invalid request')


def delete_expense(request, pk):
    expense = get_object_or_404(Expanses, pk=pk)
    if request.method == 'POST':
        expense_name = expense.name
        expense.delete()
        return JsonResponse({
            'success': True,
            'message': f'Expense "{expense_name}" deleted successfully!'
        })
    return HttpResponseBadRequest('Invalid request')


def toggle_status(request, pk):
    expense = get_object_or_404(Expanses, pk=pk)
    if request.method == 'POST':
        expense.status = not expense.status
        expense.save()
        return JsonResponse({
            'success': True,
            'new_status': expense.status,
            'status_display': 'Paid' if expense.status else 'Pending'
        })
    return HttpResponseBadRequest('Invalid request')