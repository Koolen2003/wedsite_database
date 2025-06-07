
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import  StudentMarkForm, Teacher
from .form import  TeacherRegistrationForm, StudentMake, EditStudentForm

from django.http import HttpResponse
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Teacher
from .form import MyForm,TeacherLoginForm

from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.contrib import messages
# Import your Student model
from .form import MyForm  # Import your form

def submit_form(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')

        # Teacher Login
        if user_type == 'teacher':
            form = TeacherLoginForm(request, data=request.POST)
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
            
                login(request, user)
                messages.success(request, "Teacher logged in successfully!")
                return redirect('teachers_page')
                
        # Student Login
        elif user_type == 'student':
             
            form = StudentMake(request.POST)
            if form.is_valid():
              
                student_id = form.cleaned_data.get('student_id')
                cohort = form.cleaned_data.get('cohort')
                try:
                    student = StudentMarkForm.objects.get(student_id=student_id, cohort=cohort)
                    if student.user:
                        login(request, student.user)
                        messages.success(request, "Student logged in successfully!")
                        return redirect('view_csv')
                    else:
                        messages.error(request, "Student account not linked.")
                except StudentMarkForm.DoesNotExist:
                    messages.error(request, "Invalid student ID or cohort.")

                   
            return redirect('view_csv')
                  
     # Initial forms for GET request

    return render(request, 'login.html', {
        'teacher_form': TeacherLoginForm(),
        'student_form': StudentMake(),
        'form': MyForm()
    })


def view_csv(request):
    students = StudentMarkForm.objects.all()
    return render(request, 'view.html', {'students': students})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            if Teacher.objects.filter(username=username).exists():
                messages.error(request, "Teacher is already registered.")
                return redirect('/login/')
            
            user = User.objects.create_user(username=username, password=password)
            Teacher.objects.create(user=user, username=username, password=password)
            messages.success(request, "Teacher registered successfully!")
            return redirect('teachers_page')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'register_teacher.html', {'form': form})

@login_required
def teachers_page(request):
    student_count = StudentMarkForm.objects.count()
    cohort_count = StudentMarkForm.objects.values('cohort').distinct().count()
    students = StudentMarkForm.objects.all()
    cohorts = StudentMarkForm.objects.values_list('cohort', flat=True).distinct()
    return render(request, 'teachers.html', {'student_count': student_count, 'students': students, 'cohort_count': cohort_count, 'cohorts': list(cohorts)})

def home_page(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contract.html')

def log_in_out(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        studentid = request.POST.get('studentid')
        module = request.POST.get('module')
        
        if User.objects.filter(username=studentid).exists():
            messages.info(request, "Student is already registered.")
            return redirect('/register/')
        
        try:
            user = User.objects.create_user(username=studentid, first_name=first_name, last_name=last_name, password=None)
            user.save()
            StudentMake.objects.create(user=user, student_id=studentid, cohort=module, subjects='')
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('/register/')
        
        messages.info(request, "Account created successfully!")
        return redirect('/register/')
    
    return render(request, 'resgis.html')

@login_required
def mark(request):
    students = StudentMarkForm.objects.all()
    return render(request, 'marking.html', {'students': students})

@login_required
def studentmark(request):
    if request.method == 'POST':
        form = StudentMake(request.POST)
        if form.is_valid():
            # Extract data and create User/StudentMarkForm objects
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            student_id = form.cleaned_data['student_id']
            cohort = form.cleaned_data['cohort']
            Computer_Arquitecture = form.cleaned_data['Computer_Arquitecture']
            Networking = form.cleaned_data['Networking']
            R_Programming = form.cleaned_data['R_Programming']

            # Create User and StudentMarkForm
            user = User.objects.create_user(
                username=student_id,
                first_name=name,
                last_name=last_name,
                password=None
            )
            StudentMarkForm.objects.create(
                user=user,
                student_id=student_id,
                cohort=cohort,
                subjects=f"Computer_Arquitecture: {Computer_Arquitecture}, Networking: {Networking}, R_Programming: {R_Programming}"
            )
            messages.success(request, "Student registered successfully!")
            return redirect('marking')  # Use URL name 'mark'
    else:
        form = StudentMake()
    return render(request, 'studentmake.html', {'form': form})

@login_required
def edit_student(request, student_id):
    student = get_object_or_404(StudentMarkForm, student_id=student_id)
    if request.method == 'POST':
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('marking')  # Redirect to 'mark' instead of 'student_list'
    else:
        form = EditStudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})
@login_required
def show_graph(request):
    students = StudentMake.objects.all()
    if not students:
        return HttpResponse("No student data available.")

    cohorts = {}
    for student in students:
        cohort = student.cohort
        subjects = dict(item.split(': ') for item in student.subjects.split(', '))
        if cohort not in cohorts:
            cohorts[cohort] = {'students': 0, 'Comp Arch': 0, 'Networking': 0, 'R Programming': 0}
        cohorts[cohort]['students'] += 1
        cohorts[cohort]['Comp Arch'] += float(subjects['Computer_Arquitecture'])
        cohorts[cohort]['Networking'] += float(subjects['Networking'])
        cohorts[cohort]['R Programming'] += float(subjects['R_Programming'])

    fig, ax = plt.subplots(figsize=(10, 5))
    labels = []
    ca_marks = []
    net_marks = []
    rp_marks = []

    for cohort, data in cohorts.items():
        labels.append(cohort)
        ca_marks.append(data['Comp Arch'] / data['students'])
        net_marks.append(data['Networking'] / data['students'])
        rp_marks.append(data['R Programming'] / data['students'])

    x = range(len(labels))
    ax.bar(x, ca_marks, width=0.2, label='Comp Arch', align='center')
    ax.bar([p + 0.2 for p in x], net_marks, width=0.2, label='Networking', align='center')
    ax.bar([p + 0.4 for p in x], rp_marks, width=0.2, label='R Programming', align='center')

    ax.set_xticks([p + 0.2 for p in x])
    ax.set_xticklabels(labels)
    ax.set_xlabel('Cohorts')
    ax.set_ylabel('Average Marks')
    ax.set_title('Average Marks per Subject by Cohort')
    ax.legend()

    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)
    plt.close(fig)
    response = HttpResponse(buffer.getvalue(), content_type='image/png')
    response['Content-Length'] = str(len(response.content))
    return response
def search_csv(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = StudentMarkForm.objects.get(student_id=student_id)
        except StudentMarkForm.DoesNotExist:
            messages.error(request, "Student not found.")
            return redirect('/mark/')
        return render(request, 'marking.html', {'student': student})
    return render(request, 'marking.html', {'student': None})

def searchs(request):
    query = request.GET.get('q', '').strip()  # Get and strip the search query
    results = []

    try:
        student = StudentMarkForm.objects.get(student_id=query)
        results.append(student)
    except StudentMarkForm.DoesNotExist:
        pass

    return render(request, 'view.html', {'results': results})

from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.db.models import Avg, Count


def upload_csv(request):
    students = StudentMarkForm.objects.all()
    
    # Prepare chart data
    avg_marks = {
        'labels': ['Computer Architecture', 'Networking', 'R Programming'],
        'data': [
            students.aggregate(Avg('Computer_Arquitecture'))['Computer_Arquitecture__avg'],
            students.aggregate(Avg('Networking'))['Networking__avg'],
            students.aggregate(Avg('R_Programming'))['R_Programming__avg'],
        ]
    }
    
    cohorts = StudentMarkForm.objects.values('cohort').annotate(total=Count('student_id')).order_by('cohort')
    cohort_counts = {
        'labels': [item['cohort'] for item in cohorts],
        'data': [item['total'] for item in cohorts]
    }
    
    return render(request, 'upload_csv.html', {
        'avg_marks': avg_marks,
        'cohort_counts': cohort_counts
    })

# View for displaying the student data table
