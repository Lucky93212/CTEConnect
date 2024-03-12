from django.db import models
from django.contrib.auth.models import User

class School(models.Model):
    name = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    join_code = models.CharField(max_length=10)
    coordinator = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grad_year = models.CharField(max_length=15)
    hours = models.IntegerField(default=0)
    major = models.CharField(max_length=80)
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    resume = models.FileField(upload_to='cte/static/cte/resumes/', default='cte/static/cte/resumes/ucdoiowebqicndsup.pdf')
    information = models.TextField(default="Here is where your bio goes, keep it short, you can edit it by clicking the button in the top right corner...", max_length=600)

    def __str__(self):
        return (self.user.first_name + " " + self.user.last_name)
    
class Business(models.Model):
    name = models.CharField(max_length=100)
    coordinator = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Job(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField(max_length=600)
    hours = models.IntegerField(default=0)
    students = models.ManyToManyField(Student, blank=True)
    applicants = models.ManyToManyField(Student, related_name='applicants', blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    application_deadline = models.DateField()
    quick_apply = models.BooleanField(default=False)
    application_link = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

class HoursRequest(models.Model):
    program = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hours = models.IntegerField()
    reason = models.TextField(max_length=600, blank=True)
    approved = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    date = models.DateField()

    def __str__(self):
        return (self.student.user.first_name + " " + self.student.user.last_name)