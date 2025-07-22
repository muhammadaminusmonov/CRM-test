from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from .forms import ProfitForm, MonthSelectForm
from finance.models import Profit, Payment, Cost, Expanses, TeacherSalary, StaffSalary
from datetime import date, timedelta, datetime
import calendar
from django.contrib import messages


class ProfitAnalysisView(View):
    template_name = 'profit.html'

    def get(self, request):
        # Get selected month from request
        today = date.today().replace(day=1)
        selected_month = today

        # Check if a month was selected in the form
        month_param = request.GET.get('month', '')
        if month_param:
            try:
                # Parse YYYY-MM format from the month input
                year, month = map(int, month_param.split('-'))
                selected_month = date(year, month, 1)
            except (ValueError, TypeError):
                selected_month = today

        # Create forms
        form = ProfitForm()
        month_form = MonthSelectForm(initial={'month': selected_month})

        # Calculate financial data
        context = self.calculate_financials(selected_month)
        context.update({
            'form': form,
            'month_form': month_form,
            'selected_month': selected_month,
            'month_name': selected_month.strftime('%B'),
            'month_abbr': selected_month.strftime('%b'),
            'year': selected_month.year,
        })

        return render(request, self.template_name, context)

    def post(self, request):
        # Handle profit creation
        form = ProfitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profit record created successfully!')
            return redirect('profit_analysis')

        # If form is invalid, re-render page with errors
        selected_month = date.today().replace(day=1)
        month_param = request.POST.get('month', '')
        if month_param:
            try:
                # Parse YYYY-MM format from the month input
                year, month = map(int, month_param.split('-'))
                selected_month = date(year, month, 1)
            except (ValueError, TypeError):
                selected_month = date.today().replace(day=1)

        context = self.calculate_financials(selected_month)
        context.update({
            'form': form,
            'month_form': MonthSelectForm(initial={'month': selected_month}),
        })
        return render(request, self.template_name, context)

    def calculate_financials(self, month):
        # Calculate revenue
        revenue = Payment.objects.filter(
            paid_at__year=month.year,
            paid_at__month=month.month
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate expenses
        teacher_salaries = TeacherSalary.objects.filter(
            month__year=month.year,
            month__month=month.month
        ).aggregate(total=Sum('salary'))['total'] or 0

        staff_salaries = StaffSalary.objects.filter(
            month__year=month.year,
            month__month=month.month
        ).aggregate(total=Sum('salary'))['total'] or 0

        expenses = Expanses.objects.filter(
            date__year=month.year,
            date__month=month.month
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_costs = teacher_salaries + staff_salaries + expenses
        net_profit = revenue - total_costs

        # Revenue by class
        revenue_by_class = Payment.objects.filter(
            paid_at__year=month.year,
            paid_at__month=month.month
        ).values(
            'to_group__classes__title'
        ).annotate(
            total=Sum('amount')
        ).order_by('-total')

        # Previous month data
        prev_month = month.replace(day=1) - timedelta(days=1)
        prev_month_date = date(prev_month.year, prev_month.month, 1)

        # Previous month revenue
        prev_revenue = Payment.objects.filter(
            paid_at__year=prev_month.year,
            paid_at__month=prev_month.month
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Previous month expenses
        prev_teacher_salaries = TeacherSalary.objects.filter(
            month__year=prev_month.year,
            month__month=prev_month.month
        ).aggregate(total=Sum('salary'))['total'] or 0

        prev_staff_salaries = StaffSalary.objects.filter(
            month__year=prev_month.year,
            month__month=prev_month.month
        ).aggregate(total=Sum('salary'))['total'] or 0

        prev_expenses = Expanses.objects.filter(
            date__year=prev_month.year,
            date__month=prev_month.month
        ).aggregate(total=Sum('amount'))['total'] or 0

        prev_total_costs = prev_teacher_salaries + prev_staff_salaries + prev_expenses
        prev_net_profit = prev_revenue - prev_total_costs

        # Calculate percentage changes
        revenue_change = self.calculate_percentage_change(revenue, prev_revenue)
        costs_change = self.calculate_percentage_change(total_costs, prev_total_costs)
        profit_change = self.calculate_percentage_change(net_profit, prev_net_profit)

        return {
            'revenue': revenue,
            'teacher_salaries': teacher_salaries,
            'staff_salaries': staff_salaries,
            'expenses': expenses,
            'total_costs': total_costs,
            'net_profit': net_profit,
            'revenue_change': revenue_change,
            'costs_change': costs_change,
            'profit_change': profit_change,
            'revenue_by_class': revenue_by_class,
            'prev_net_profit': prev_net_profit,
            'prev_total_costs': prev_total_costs,
            'prev_revenue': prev_revenue,
        }

    def calculate_percentage_change(self, current, previous):
        if previous == 0:
            return 0
        return round(((current - previous) / previous) * 100, 1)