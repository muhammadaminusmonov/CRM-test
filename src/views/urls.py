from django.urls import path, include

urlpatterns = [
    path('', include('views.statistic.urls')),
    path('teacher/', include('views.teacher.urls')),
    path('student/', include('views.students.urls')),
    path('staff/', include('views.staff.urls')),
    path('attendance/', include('views.attendance.urls')),
    path('class/', include('views.classes.urls')),
    path('group/', include('views.groups.urls')),
    path('cost/', include('views.costs.urls')),
    path('expense/', include('views.expenses.urls')),
    path('payment/', include('views.payment.urls')),
    path('profit/', include('views.profit.urls')),
    path('teacher_salary/', include('views.teacher_salary.urls')),
    path('staff_salary/', include('views.staff_salary.urls')),
]