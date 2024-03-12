from django.urls import path
from django.urls.conf import include

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path("students/", views.students, name="students"),
    path("student_register/", views.student_register, name="student_register"),
    path("student_profile/<int:student_id>/", views.student_profile, name="profile"),
    path("editbio/", views.editbio, name="editbio"),
    path("uploadresume/", views.uploadresume, name="uploadresume"),
    path("changemajor/", views.changemajor, name="changemajor"),
    path("jobs/", views.jobs, name="jobs"),
    path("newjob/", views.newjob, name="newjob"),
    path("job/<int:job_id>/", views.job, name="job"),
    path("postings/", views.postings, name="postings"),
    path("apply/<int:job_id>/", views.apply, name="apply"),
    path("approve/<int:job_id>/", views.approve, name="approve"),
    path("mentorships/", views.mentorships, name="mentorships"),
    path("newrequest/", views.newrequest, name="newrequest"),
    path("workvalidation/", views.workvalidation, name="workvalidation"),
    path("allow/<int:request_id>/", views.allow, name="allow"),
    path("deny/<int:request_id>/", views.deny, name="deny"),
]
