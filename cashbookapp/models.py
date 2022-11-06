import datetime
from email import contentmanager
from email.policy import default
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from account.models import CustomUser


# Create your models here.
class Cashbook(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name='작성자')
    title = models.CharField(max_length=200)
    content = models.TextField()
    detail = models.TextField()
    pub_date = models.DateTimeField('date published', default=datetime.datetime.now, editable=False)
    image = models.ImageField(upload_to = 'images/', blank =True, default='')
    likes = models.PositiveIntegerField(default=0, verbose_name='추천수')
    clicks = models.PositiveIntegerField(default=0, verbose_name='조회수') 
    tagging= models.ManyToManyField('Tag', blank = True, related_name='tagged')
    hashtags_count = models.PositiveIntegerField(verbose_name='해시태그수', null=True)
    post_like = models.ManyToManyField(CustomUser, related_name='like_users', blank=True)
    like_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

    def clean(self):
        title = self.title
        if title == "":
            raise ValidationError("글을 작성해주세요")
        return super(Cashbook,self).clean()

    def clean_content(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.content
        else:
            return self.cleaned_data['content']

class Tag(models.Model):
    tag_content = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_content


class Comment(models.Model):

    def __str__(self):
        return self.text
        
    comment_writer = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, blank=True, null = True, verbose_name='게시글 작성자')
    cashbook_id = models.ForeignKey(Cashbook, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.CharField(max_length=50)