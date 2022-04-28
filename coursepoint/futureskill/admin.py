from django.contrib import admin

# Register your models here.
from .models import *


class Tag_info(admin.TabularInline):
    model = Tag


class learning_info(admin.TabularInline):
    model = learning


class prereq_info(admin.TabularInline):
    model = prereq


class videos_info(admin.TabularInline):
    model = Videos


class course_info(admin.ModelAdmin):
    inlines = [Tag_info, learning_info, prereq_info, videos_info]


admin.site.register(registration)
admin.site.register(coursedtls, course_info)
admin.site.register(userCourse)
admin.site.register(Payment)
admin.site.register(RefCode)
