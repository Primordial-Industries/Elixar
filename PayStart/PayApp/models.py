from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.admin import User
import uuid
from PIL import Image

# Create your models here.
class UserProfile(models.Model):
    '''
        Model for managing the users registering on the elixar website and the developer admins.
        Email and first, last names are stored in the Django User model.
    '''
    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )

    auth_user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, unique=True, related_name="profile") #related_name for getting
                                                                                                                      # the profile of a user instance
    college = models.CharField(max_length=200, blank=True)
    college_id = models.CharField(max_length=20, blank=True) # Like BITS ID.
    phone = models.CharField(max_length=12)
    gender = models.CharField(choices=GENDERS, null=True, max_length=1)
    year_of_study = models.PositiveIntegerField(default=1) # 0 for a student of Kalam Science Lab
    qr_code = models.UUIDField(max_length=36, unique=True, default=uuid.uuid4)
    is_dev = models.BooleanField(default=False)
    portal_code = models.IntegerField(blank=True, null=True) 
    # image = models.ImageField(default='default_dp.jpeg', upload_to='profile_pics', null=False)
    github_link = models.CharField(max_length=200, blank=True)
    linkedin_link = models.CharField(max_length=200, blank=True)
    email_token = models.CharField(max_length=32, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        indexes = [models.Index(fields=['id']), models.Index(fields=['qr_code'])]

    def __str__(self):
        return "{} - {}".format(self.id, self.auth_user.username)

class Course(models.Model):
    name = models.CharField(max_length=30, unique = True)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=10,default="INR")

    def __str__(self):
        return self.name
class Enroll(models.Model):

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
    user = models.OneToOneField(Enroll, on_delete=models.CASCADE, unique=True)
    paid = models.BooleanField(default=False)
    phone = models.IntegerField()
    def __str__(self):
        return self.user.email

class ExplorerSub(models.Model):
    user = models.OneToOneField(Enroll, on_delete=models.CASCADE, unique=True)
    paid = models.BooleanField(default=False)
    phone = models.IntegerField()
    def __str__(self):
        return self.user.email

class FreeTrialSub(models.Model):
    user = models.OneToOneField(Enroll, on_delete=models.CASCADE, unique=True)
    # moneypaid = models.BooleanField(default=False)
    phone = models.IntegerField()
    def __str__(self):
        return self.user.email

class TrialMeeting(models.Model):
    user = models.OneToOneField(Enroll, on_delete = models.CASCADE)
    meetdate = models.CharField(max_length=20)
    meettime = models.TimeField()
    mailID = models.EmailField()
    def __str__(self):
        return self.user.name