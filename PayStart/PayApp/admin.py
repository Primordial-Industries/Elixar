from django.contrib import admin
from .models import Course, ConquereSub, ExplorerSub, FreeTrialSub, Student
from django.contrib.auth.models import User
# Register your models here.


admin.site.register(Course)
admin.site.register(Student)
admin.site.register(ConquereSub)
admin.site.register(ExplorerSub)
admin.site.register(FreeTrialSub)

