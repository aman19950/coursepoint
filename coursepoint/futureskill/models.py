from pyexpat import model
from statistics import mode
from tkinter import CASCADE
from django.db import models
from sqlalchemy import null

# Create your models here.


class registration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    mobile = models.BigIntegerField()
    gender = models.CharField(max_length=40)

    def __str__(self):
        return self.first_name


class coursedtls(models.Model):
    name = models.CharField(max_length=50, null=True)
    slug = models.CharField(max_length=50, null=False, unique=True)
    desc = models.CharField(max_length=50, null=False)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False)
    date = models.DateTimeField(auto_now=True)
    resource = models.FileField(upload_to='files/resource')
    image = models.ImageField(upload_to='files/image')

    def __str__(self):
        return self.name


class courseinfo(models.Model):
    desc = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(
        coursedtls, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True


class Tag(courseinfo):
    pass


class prereq(courseinfo):
    pass


class learning(courseinfo):
    pass


class Videos(models.Model):
    title = models.CharField(max_length=100, null=True)
    course = models.ForeignKey(
        coursedtls, on_delete=models.CASCADE, null=True)
    video_id = models.CharField(max_length=100, null=True)
    s_no = models.IntegerField(null=True)
    is_preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class userCourse(models.Model):
    user = models.ForeignKey(registration, null=False,
                             on_delete=models.CASCADE)
    course = models.ForeignKey(
        coursedtls, null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} - {self.course.name}'


class Payment(models.Model):
    order_id = models.CharField(max_length=100, null=False)
    payment_id = models.CharField(max_length=100)
    user_info = models.ForeignKey(registration, on_delete=models.CASCADE)
    user_course = models.ForeignKey(
        userCourse, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(coursedtls, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.order_id


class RefCode(models.Model):
    code = models.CharField(max_length=10)
    course = models.ForeignKey(coursedtls, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.code
