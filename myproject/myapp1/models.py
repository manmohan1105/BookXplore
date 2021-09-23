from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    isbn=models.CharField(max_length=500)
class savedbook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    bookid=models.CharField(max_length=500)



# Create your models here.
