from django.db import models

class NewTask(models.Model):
    newTask = models.CharField(label="New task", max_length= 500)
    priority= models.IntegerField(label="Priority", min_value=1,max_value=10)
