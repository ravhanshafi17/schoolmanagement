from django.contrib import admin
from .models import *
admin.site.register(User)
admin.site.register(School)
admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(QuestionBank)
admin.site.register(Question)

