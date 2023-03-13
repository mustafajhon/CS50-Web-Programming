from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import datetime

class MyUserManager(BaseUserManager):
    def create_user(self,username, email, password,birthday):
        user=self.model(
            username = username,
            email= MyUserManager.normalize_email(email),
            birthday = birthday 
        )
        user.set_password(password)
        #user.save(using = self._db)
        return user



class User(AbstractUser):
    birthday = models.DateField(default=datetime.date.today, null = False, blank = False)
    objects = MyUserManager()
    REQUIRED_FIELDS=['email','password', 'birthday']

     
    
class AbstractNewText(models.Model):
    user=models.ForeignKey(User,null = True,blank=True,on_delete=models.CASCADE)
    username=models.CharField(max_length=999, default="")
    newPost = models.CharField(max_length=999999, default="")
    postDate=models.DateTimeField(default = datetime.datetime.now())
    likes=models.BigIntegerField(default = 0)
    
    class Meta:
        abstract: True

class NewPost(AbstractNewText):
    pass

class Comment(AbstractNewText):
    pass

class AbstractLike(models.Model):
    user=models.ManyToManyField(User)
    
    class Meta:
        abstract: True


class PostLike(AbstractLike):
    post= models.ForeignKey(NewPost, null = True, on_delete = models.CASCADE)

class CommentLike(AbstractLike):
    comment = models.ForeignKey(Comment, null = True, on_delete = models.CASCADE)
