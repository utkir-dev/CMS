from django.db import models
from account.models import User

from .fields import OredrField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Subject(models.Model):
    title=models.CharField(("Subject Title"),max_length=100)
    slug=models.SlugField(("Subject Slug"),max_length=100, unique=True)

    class Meta:
        ordering=['title']
        verbose_name="Subject",
        verbose_name_plural="Subject"

    def __str__(self):
        return self.title   

class Course(models.Model):
    owner=models.ForeignKey(User,related_name='course_created',on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,related_name='courses',on_delete=models.CASCADE)
    title=models.CharField(("Course Title"),max_length=100)
    slug=models.SlugField(("Course Slug"),max_length=100, unique=True)
    overview=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['title']
        verbose_name="Course"
        verbose_name_plural="Course"

    def __str__(self):
        return self.title 
    
class Module(models.Model):
    course=models.ForeignKey(Course,related_name='modules',on_delete=models.CASCADE)
    title=models.CharField(('Module Title'),max_length=100)
    slug=models.SlugField(('Module Slug'),max_length=100,unique=True)
    description=models.TextField(('Module description'),null=True,blank=True)
    order=OredrField(blank=True,for_fields=['course'])
    def __str__(self):
        return f"{self.order} {self.title}"  
    class Meta:
        ordering=['order']  

class Content(models.Model):
    module=models.ForeignKey(Module,related_name='contents',on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={
        "model_in":('text','video','image','file',)
    })
    object_id=models.PositiveBigIntegerField(("Content ID"))
    item=GenericForeignKey("content_type","object_id")
    order=OredrField(blank=True,for_fields=['module'])
    class Meta:
        ordering=['order']  



class ItemBase(models.Model):
    owner=models.ForeignKey(User,related_name="%(class)s_related",on_delete=models.CASCADE)
    title=models.CharField(("ItemBase Title"),max_length=255)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True
    def __str__(self):
        return self.title   

class Text(ItemBase):
    content=models.TextField()

class Image(ItemBase):
    file=models.FileField(upload_to='images')  

class File(ItemBase):
    file=models.FileField(upload_to='files')

class Video(ItemBase):
    url=models.URLField()