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
    
    class Meta:
        ordering = ['-vote_ratio','-vote_total','title']
        
    @property
    def reviewers_ids(self):
        query_set = self.review_set.all().values_list('owner__id',flat=True)
        return query_set
        
    @property
    def get_vote_count(self):
        reviews = self.review_set.all()
        up_votes = reviews.filter(value='up').count()
        total_votes = reviews.count() 
        
        ratio = (up_votes / total_votes) *100
        
        self.vote_ratio = ratio
        self.vote_total = total_votes
        self.save()
    
class Review(models.Model):
    VOTE_TYPE =(
        ('up','Up vote'),
        ('down','Down vote')
    )
    owner = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    
    class Meta:
        unique_together = [[    # one review from one onwer for specific project
            'owner','project'
        ]]
    
    def __str__(self):
        return self.value
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.name
    