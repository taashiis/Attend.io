from django.db import models

# Create your models here.
class Login(models.Model):
    empid = models.CharField(max_length=10)
    empname = models.CharField(max_length=122)
    empemail = models.EmailField(max_length=122)
    emppass = models.CharField(max_length=20)
    userimg = models.ImageField(null=True, blank=True, upload_to = "", default="image.jpg")

    def __str__(self):
        return self.empname

class Session(models.Model):
    empid = models.CharField(max_length=10)
    start = models.TimeField(auto_now=False)
    end = models.TimeField(auto_now=False)