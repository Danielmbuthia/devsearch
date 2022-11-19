from django.db import models
import uuid

from users.models import Profile
# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile,blank=True,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    featured_image = models.ImageField(null=True,blank=True, default='default.jpg',upload_to='projects')
    demo_link = models.CharField(max_length=2000,blank=True,null=True)
    source_link =models.CharField(max_length=2000,null=True,blank=True)
    tags = models.ManyToManyField('Tag',blank=True)
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    VOTE_TYPE =(
        ('up','Up vote'),
        ('down','Down vote')
    )
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.SET_NULL)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        return self.value
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name
    