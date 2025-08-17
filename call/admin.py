from django.contrib import admin
from call.models import ClassOfStudent, Student, Call, UsersInClass
# Register your models here.
admin.site.register(ClassOfStudent)
admin.site.register(Student)
admin.site.register(Call)
admin.site.register(UsersInClass)