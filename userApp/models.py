from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model) :
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    url = models.URLField()
    creation_date = models.DateTimeField(default=timezone.now,null=False)
    def __str__(self) -> str:
        return self.name

class University(models.Model):
    name = models.CharField(max_length=255)
    mail = models.CharField(max_length=255,primary_key=True)
    def __str__(self) -> str:
        return self.name;

class Question(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now,null=False)
    university = models.ForeignKey(University,on_delete=models.CASCADE)
    title = models.CharField(max_length=255) 
    detailed_question = models.CharField(max_length=1000) 
    upvotes = models.ManyToManyField(User ,related_name='upvote',blank=True)
    downvotes = models.ManyToManyField(User,related_name='downvote',blank=True)
    def __str__(self) :
        return self.title

class Answer(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now,null=False)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    text = models.CharField(max_length=1000) 
    upvotes = models.ManyToManyField(User ,related_name='answer_upvote',blank=True)
    downvotes = models.ManyToManyField(User,related_name='answer_downvote',blank=True)
    def __str__(self) :
        return self.text