from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import School, Student, User, Business, Job, HoursRequest
from django.core.files.storage import FileSystemStorage
import random
from os.path import exists
from os import remove
from django.utils import timezone
from datetime import datetime as time

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    return render(request, 'cte/index.html')

@login_required(login_url='/login')
def dashboard(request):
    if Student.objects.filter(user=request.user).exists():
        return HttpResponseRedirect('/student_profile/' + str(request.user.id))
    
    if Business.objects.filter(coordinator=request.user).exists():
        hours = 0
        for each in HoursRequest.objects.filter(program__business=Business.objects.get(coordinator=request.user)):
            if each.reviewed == True and each.approved == True:
                hours += each.hours
        
        students = 0
        for each in Job.objects.filter(business=Business.objects.get(coordinator=request.user)):
            for student in each.students.all():
                students += 1
            
        return render(request, 'cte/business_view.html', {
        "user_type": "Owner",
        "total_hours": hours,
        "total_students": students,
        "programs": Job.objects.filter(business=Business.objects.get(coordinator=request.user)).count(),
        "business": Business.objects.get(coordinator=request.user),
    })
    
    return HttpResponseRedirect('/students')

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect('/dashboard')
        else:
            return render(request, 'cte/login.html', {'error_message': 'Invalid login credentials'})
    else:
        return render(request, 'cte/login.html')

@login_required(login_url='/login')
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def students(request):
    if not School.objects.filter(coordinator=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    return render(request, 'cte/students.html', {
        "school": School.objects.get(coordinator=request.user),
        "students": Student.objects.filter(school=School.objects.get(coordinator=request.user)).order_by('grad_year', 'user__last_name', 'user__first_name'),
        "user_type": "Coordinator",
    })
    

def student_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    if request.method == 'POST':
        # Get POST data
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        
        try:
            school = School.objects.get(zip=request.POST['zip'], join_code=request.POST['code'])
        except:
            return render(request, 'cte/register.html', {'error_message': 'Invalid zip code or join code'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'cte/register.html', {'error_message': 'Username already exists'})
        
        # Create user
        user = User.objects.create_user(username, password=password, first_name=first_name, last_name=last_name, email=email)
        
        # Create student
        student = Student(user=user, grad_year=request.POST['grad_year'], major=request.POST['major'], school=school)
        student.save()
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        auth_login(request, user)
        return HttpResponseRedirect('/dashboard')
    else:
        return render(request, 'cte/register.html')

@login_required(login_url='/login')
def student_profile(request, student_id):
    if Student.objects.filter(user__id=request.user.id).exists():
        if not Student.objects.filter(user__id=request.user.id).exists():
            return HttpResponseRedirect('/dashboard')
        
        return render(request, 'cte/student_profile.html', {
            "student": Student.objects.get(user__id=request.user.id),
            "jobs": Job.objects.filter(students=Student.objects.get(user__id=request.user.id)),
            "user_type": "Student",
        })
    else:
        if Business.objects.filter(coordinator=request.user).exists():
            return render(request, 'cte/student_profile.html', {
                "student": Student.objects.get(user__id=student_id),
                "jobs": Job.objects.filter(students=Student.objects.get(user__id=student_id)),
                "user_type": "Owner",
            })
            
        
        if not Student.objects.filter(user__id=student_id, school=School.objects.get(coordinator=request.user)).exists():
            return HttpResponseRedirect('/dashboard')

        return render(request, 'cte/student_profile.html', {
            "student": Student.objects.get(user__id=student_id),
            "jobs": Job.objects.filter(students=Student.objects.get(user__id=student_id)),
            "user_type": "Coordinator",
        })
    
@login_required(login_url='/login')
def editbio(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        student.information = request.POST['info']
        student.save()
        return HttpResponseRedirect('/student_profile/' + str(request.user.id))
    
@login_required(login_url='/login')
def uploadresume(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        try:
            remove("cte/" + str(student.resume))
        except:
            pass
        file = request.FILES["resumeupload"]
        fs = FileSystemStorage()
        done = False
        randstring = ""
        
        while not done:
            randstring = ""
            choice = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            
            for i in range(20):
                randstring += random.choice(choice)
            
            if not exists("cte/static/cte/resumes/" + randstring + ".pdf"):
                done = True
        
        fs.save("cte/static/cte/resumes/" + randstring + ".pdf", file)
        student.resume = "/static/cte/resumes/" + randstring + ".pdf"
        
        student.save()
        return HttpResponseRedirect('/student_profile/' + str(request.user.id))

@login_required(login_url='/login')
def changemajor(request):
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        student.major = request.POST['major']
        student.save()
        return HttpResponseRedirect('/student_profile/' + str(request.user.id))

@login_required(login_url='/login')
def jobs(request):
    if not Business.objects.filter(coordinator=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    return render(request, 'cte/jobs.html', {
        "business": Business.objects.get(coordinator=request.user),
        "jobs": Job.objects.filter(business=Business.objects.get(coordinator=request.user)),
        "user_type": "Owner",
    })
    
@login_required(login_url='/login')
def newjob(request):
    if request.method == 'POST':
        business = Business.objects.get(coordinator=request.user)
        title = request.POST['name']
        type = request.POST['progtype']
        description = request.POST['description']
        hours = int(request.POST['hours'])
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        deadline = request.POST['deadline']
        if request.POST['type'] == "quick":
            quickapply = True
            job = Job(business=business, title=title, type=type, description=description, hours=hours, start_date=startdate, end_date=enddate, application_deadline=deadline, quick_apply=quickapply)
            job.save()
        else:
            quickapply = False
            link = request.POST['apply_link']
            job = Job(business=business, title=title, type=type, description=description, hours=hours, start_date=startdate, end_date=enddate, application_deadline=deadline, quick_apply=quickapply, application_link=link)
            job.save()
        return HttpResponseRedirect('/jobs')
    else:
        return render(request, 'cte/newjob.html')
    
@login_required(login_url='/login')
def job(request, job_id):
    if not Job.objects.filter(id=job_id).exists():
        return HttpResponseRedirect('/dashboard')
    
    job = Job.objects.get(id=job_id)
    
    # check if past deadline
    past = False
    if job.application_deadline < time.date(time.now()):
        past = True
    
    if not Business.objects.filter(coordinator=request.user).exists():
        if not School.objects.filter(coordinator=request.user).exists():
            if not past:
                return render(request, 'cte/job_profile.html', {
                    "job": Job.objects.get(id=job_id),
                    "user_type": "Student",
                    "student": Student.objects.get(user=request.user),
                    "past": past,
                })
        else:
            return render(request, 'cte/job_profile.html', {
                "job": Job.objects.get(id=job_id),
                "user_type": "Coordinator",
                "past": past,
            })
    else:
        if not Job.objects.filter(id=job_id, business=Business.objects.get(coordinator=request.user)).exists():
            return HttpResponseRedirect('/dashboard')
        return render(request, 'cte/job_profile.html', {
            "job": Job.objects.get(id=job_id),
            "applicants": Job.objects.get(id=job_id).applicants.all(),
            "user_type": "Owner",
            "past": past,
        })
        
@login_required(login_url='/login')
def postings(request):
    if not Business.objects.filter(coordinator=request.user).exists():
        if not School.objects.filter(coordinator=request.user).exists():
            return render(request, 'cte/postings.html', {
                "jobs": Job.objects.filter(application_deadline__gte=timezone.now()).order_by('application_deadline'),
                "user_type": "Student",
            })
        else:
            return render(request, 'cte/postings.html', {
                "jobs": Job.objects.filter(application_deadline__gte=timezone.now()).order_by('application_deadline'),
                "user_type": "Coordinator",
            })
    else:
        return HttpResponseRedirect('/dashboard')

@login_required(login_url='/login')
def apply(request, job_id):
    if not Job.objects.filter(id=job_id).exists():
        return HttpResponseRedirect('/dashboard')
    
    job = Job.objects.get(id=job_id)
    
    if not Student.objects.filter(user=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    
    student = Student.objects.get(user=request.user)
    
    if student in job.applicants.all():
        return HttpResponseRedirect('/dashboard')
    
    job.applicants.add(student)
    return render(request, 'cte/applied.html')

@login_required(login_url='/login')
def approve(request, job_id):
    if not Job.objects.filter(id=job_id).exists():
        return HttpResponseRedirect('/dashboard')
    
    job = Job.objects.get(id=job_id)
    
    if not Business.objects.filter(coordinator=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    
    business = Business.objects.get(coordinator=request.user)
    
    if not Job.objects.filter(id=job_id, business=business).exists():
        return HttpResponseRedirect('/dashboard')
    
    for student in job.applicants.all():
        if request.POST["applicant-" + str(student.id)] == "approve":
            job.students.add(student)
    
    return HttpResponseRedirect('/job/' + str(job_id))

@login_required(login_url='/login')
def mentorships(request):
    if not Student.objects.filter(user=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    
    student = Student.objects.get(user=request.user)
    
    return render(request, 'cte/mentorships.html', {
        "student": student,
        "jobs": Job.objects.filter(applicants=student),
        "requests": HoursRequest.objects.filter(student=student),
        "user_type": "Student",
    })
    
@login_required(login_url='/login')
def newrequest(request):
    print(Job.objects.get(pk=1))
    if request.method == 'POST':
        student = Student.objects.get(user=request.user)
        hours = int(request.POST['hours'])
        job = int(request.POST['program'])
        reason = request.POST['description']
        date = request.POST['date']
        request = HoursRequest(student=student, program=Job.objects.get(id=job), hours=hours, reason=reason, date=date)
        request.save()
        return HttpResponseRedirect('/mentorships')
    else:    
        if not Student.objects.filter(user=request.user).exists():
            return HttpResponseRedirect('/dashboard')
        
        return render(request, 'cte/request.html', {
            "jobs": Job.objects.filter(students=Student.objects.get(user=request.user)),
        })
    
@login_required(login_url='/login')
def workvalidation(request):
    if not Business.objects.filter(coordinator=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    
    business = Business.objects.get(coordinator=request.user)
    
    return render(request, 'cte/workvalidation.html', {
        "business": business,
        "requests": HoursRequest.objects.filter(program__business=business, reviewed=False),
        "user_type": "Owner",
    })
    
@login_required(login_url='/login')
def allow(request, request_id):
    if not Business.objects.filter(coordinator=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    
    business = Business.objects.get(coordinator=request.user)
    
    if not HoursRequest.objects.filter(id=request_id, program__business=business).exists():
        return HttpResponseRedirect('/dashboard')
    
    student = HoursRequest.objects.get(id=request_id).student
    student.hours += HoursRequest.objects.get(id=request_id).hours
    student.save()
    
    request = HoursRequest.objects.get(id=request_id)
    request.approved = True
    request.reviewed = True
    request.save()
    
    return HttpResponseRedirect('/workvalidation')

@login_required(login_url='/login')
def deny(request, request_id):
    if not Business.objects.filter(coordinator=request.user).exists():
        return HttpResponseRedirect('/dashboard')
    
    business = Business.objects.get(coordinator=request.user)
    
    if not HoursRequest.objects.filter(id=request_id, program__business=business).exists():
        return HttpResponseRedirect('/dashboard')
    
    request = HoursRequest.objects.get(id=request_id)
    request.reviewed = True
    request.save()
    
    return HttpResponseRedirect('/workvalidation')