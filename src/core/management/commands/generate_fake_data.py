# app: core (or any app of your choice)
# File: core/management/commands/generate_fake_data.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta, date, datetime
from datetime import time
from student.models import Student
from teacher.models import Teacher
from staff.models import Staff
from classes.models import Class, Group, Attendance
from finance.models import Payment, Expanses, TeacherSalary, StaffSalary, Cost, Profit


fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for all apps'

    def add_arguments(self, parser):
        parser.add_argument('--students', type=int, default=100, help='Number of students')
        parser.add_argument('--teachers', type=int, default=10, help='Number of teachers')
        parser.add_argument('--staff', type=int, default=10, help='Number of staff members')
        parser.add_argument('--classes', type=int, default=5, help='Number of classes')
        parser.add_argument('--groups', type=int, default=20, help='Number of groups')
        parser.add_argument('--payments', type=int, default=200, help='Number of payments')
        parser.add_argument('--expanses', type=int, default=50, help='Number of expanses')
        parser.add_argument('--salaries', type=int, default=100, help='Number of salary records per type')

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        # Optionally clear existing data
        models = [Profit, Cost, StaffSalary, TeacherSalary, Payment, Expanses, Attendance, Group, Class, Student, Teacher, Staff]
        for m in models:
            m.objects.all().delete()

        # Generate Staff
        staff_list = []
        for _ in range(options['staff']):
            s = Staff.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(), middle_name=fake.first_name(),
                born_date=fake.date_between(start_date='-60y', end_date='-20y'),
                salary=round(random.uniform(500, 2000), 2),
                phone_number=fake.msisdn()[:11],
                join_date=fake.date_between(start_date='-5y', end_date='today'),
                status=random.randint(1, 6)
            )
            staff_list.append(s)

        # Generate Teachers
        teacher_list = []
        for _ in range(options['teachers']):
            t = Teacher.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(),
                age=random.randint(22, 70),
                phone_number=fake.msisdn()[:11], email=fake.email(), address=fake.address(),
                fixed_salary=fake.boolean(chance_of_getting_true=70),
                salary=random.randint(500, 3000), percentage=random.randint(0, 20),
                status=random.randint(1, 5)
            )
            teacher_list.append(t)

        # Generate Students
        student_list = []
        for _ in range(options['students']):
            st = Student.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name(),
                born_date=fake.date_between(start_date='-18y', end_date='-6y'),
                email=fake.email(), phone_number=fake.msisdn()[:11], dad_number=fake.msisdn()[:11], mum_number=fake.msisdn()[:11],
                join_date=fake.date_between(start_date='-2y', end_date='today'), status=random.randint(1, 4)
            )
            student_list.append(st)

        # Generate Classes
        class_list = []
        for _ in range(options['classes']):
            c = Class.objects.create(
                title=fake.bs().title(),
                cost_per_month=random.randint(50, 500),
                duration_per_lesson=time(minute=random.choice([30, 45, 59])),  # FIXED
                length=f"{random.randint(1, 12)} months",
                description=fake.text(max_nb_chars=200),
                status=random.randint(1, 2)
            )
            class_list.append(c)

        # Generate Groups
        group_list = []
        for _ in range(options['groups']):
            start = fake.date_time_between(start_date='-1y', end_date='now')
            end = start + timedelta(days=random.randint(30, 180))
            g = Group.objects.create(
                name=f"Group {fake.lexify(text='???')}",
                teacher=random.choice(teacher_list), classes=random.choice(class_list),
                start_at=start, end_at=end, lesson_per_week=random.randint(1,5), status=random.randint(1,4)
            )
            # add random students
            selected_students = random.sample(student_list, k=random.randint(5, 20))
            g.student.set(selected_students)
            group_list.append(g)

        # Generate Attendance
        for g in group_list:
            for st in g.student.all():
                # For each scheduled date, pick random status
                from django.utils.timezone import is_naive, make_aware

                current = g.start_at
                end_at = g.end_at

                # Ensure both are timezone-aware
                if is_naive(current):
                    current = make_aware(current)

                if is_naive(end_at):
                    end_at = make_aware(end_at)

                while current <= end_at:
                    if random.random() < 0.8:
                        Attendance.objects.create(group=g, student=st, date=current, status=random.randint(1,3))
                    current += timedelta(days=7 // g.lesson_per_week)

        # Generate Expanses
        exp_list = []
        for _ in range(options['expanses']):
            e = Expanses.objects.create(
                name=fake.word().capitalize(), description=fake.sentence(), date=fake.date_between('-1y', 'today'),
                amount=round(random.uniform(100, 1000), 2), status=fake.boolean()
            )
            exp_list.append(e)

        # Generate Payments
        payment_list = []
        for _ in range(options['payments']):
            month = fake.date_between('-1y', 'today')
            st = random.choice(student_list)
            g = random.choice(group_list)
            amt = round(g.classes.cost_per_month, 2)
            p = Payment.objects.create(student=st, paid_at=month, amount=amt,
                                       paid_for_month=month.month, to_group=g, to_teacher=g.teacher)
            payment_list.append(p)

        # Generate Salaries
        for _ in range(options['salaries']):
            t = random.choice(teacher_list)
            month = fake.date_between('-1y', 'today')
            TeacherSalary.objects.create(teacher=t, month=month,
                                        salary=round(random.uniform(500, 3000),2), paid=round(random.uniform(0, 3000),2),
                                        paid_date=month + timedelta(days=random.randint(1, 28)))

        for _ in range(options['salaries']):
            s = random.choice(staff_list)
            month = fake.date_between('-1y', 'today')
            StaffSalary.objects.create(staff=s, month=month,
                                       salary=round(random.uniform(400, 2000),2), paid=round(random.uniform(0, 2000),2),
                                       paid_date=month + timedelta(days=random.randint(1, 28)))

        # Generate Cost and Profit
        for p in payment_list:
            # pick matching cost record or create
            cost_month = p.paid_at
            for _ in range(random.randint(1,3)):
                cst = Cost.objects.create(
                    month=cost_month,
                    staff=random.choice(staff_list), teacher=random.choice(teacher_list),
                    total_teacher_cost=round(random.uniform(100, 1000),2),
                    total_staff_cost=round(random.uniform(100, 1000),2),
                    total_cost=round(random.uniform(500, 2000),2), expanses=random.choice(exp_list)
                )
                Profit.objects.create(payment=p, cost=cst,
                                      gross_profit=round(p.amount - cst.total_cost,2),
                                      profit=round((p.amount - cst.total_cost) * 0.8,2),
                                      month=cost_month)

        self.stdout.write(self.style.SUCCESS('Fake data generation complete.'))
