from django.contrib import admin

# Register your models here.
from . models import courses,file,student,department,teacher,studentcourse
admin.site.register(courses)
admin.site.register(file)
admin.site.register(student)
admin.site.register(department)
admin.site.register(teacher)
admin.site.register(studentcourse)