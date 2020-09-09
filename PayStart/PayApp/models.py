from django.db import models
# from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=30, unique = True)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=10,default="INR")

    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=40, default='')
    email = models.EmailField(unique=True, primary_key=True)
    phone = models.IntegerField()
    school = models.CharField(max_length=50)
    # gender = models.CharField(max_length=15, default='')
    courseapp = models.ForeignKey(Course, on_delete=models.CASCADE)
    active_key = models.IntegerField(default=2)
    verif = models.BooleanField(default=False)
    def __str__(self):
        return self.email

# class CourseSub(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
#     # moneypaid = models.BooleanField(default=False)
#     phone = models.IntegerField(max_length=12)
#     Course = models.ForeignKey(Course, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user

class ConquereSub(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, unique=True)
    paid = models.BooleanField(default=False)
    phone = models.IntegerField()
    def __str__(self):
        return self.user.email

class ExplorerSub(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, unique=True)
    paid = models.BooleanField(default=False)
    phone = models.IntegerField()
    def __str__(self):
        return self.user.email

class FreeTrialSub(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE, unique=True)
    # moneypaid = models.BooleanField(default=False)
    phone = models.IntegerField()
    def __str__(self):
        return self.user.email

class TrialMeeting(models.Model):
    user = models.OneToOneField(Student, on_delete = models.CASCADE)
    meetdate = models.CharField(max_length=20)
    meettime = models.TimeField()
    mailID = models.EmailField()
    def __str__(self):
        return self.user.name