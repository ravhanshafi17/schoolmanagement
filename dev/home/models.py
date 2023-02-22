from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_school = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    def __str__(self):
        return self.username



class School(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Admin(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class QuestionBank(models.Model):
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    classes = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    LEVEL_TYPES = (
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('hard', 'hard'),
    )
    question =models.ForeignKey(QuestionBank,on_delete=models.CASCADE)
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    admin=models.ForeignKey(Admin,on_delete=models.CASCADE)
    question_type = models.CharField(max_length=100)
    level = models.CharField(choices= LEVEL_TYPES , max_length=255)
    text=models.TextField()
    marks = models.IntegerField()
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return self.question_type


class QuestionGenerator(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=100)
    marks_type = models.IntegerField()
    is_required = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.question} - {self.question_type}'