from django.contrib import admin

from .models import Teacher
from .models import StudentMarkForm
from .models import UserProfile
# Register your models here.
admin.site.register(StudentMarkForm)
admin.site.register(UserProfile)
admin.site.register(Teacher)

admin.site.logout