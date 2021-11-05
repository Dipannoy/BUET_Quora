# -*- coding: utf-8 -*-


from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from Activity.models import Activity
class Album(models.Model):
     artist = models.CharField(max_length=270)
     album_title=models.CharField(max_length=500)
     genre=models.CharField(max_length=100)
     album_logo = models.CharField(max_length=1000)

     def get_absolute_url(self):
          return reverse('music:detail',kwargs={'pk':self.pk})

     def __str__(self):
          return self.album_title + '-' + self.artist
class Song(models.Model):
     album = models.ForeignKey(Album,on_delete=models.CASCADE)
     file_type=models.CharField(max_length=50)
     song_title=models.CharField(max_length=100)
     is_favourite = models.BooleanField(default=False)
     def __str__(self):
          return self.song_title

class Question(models.Model):
     text = models.CharField(max_length=400)
     tag = models.CharField(max_length=50)
     person=models.CharField(max_length=40)

     date = models.DateTimeField(default=datetime.now, blank=True)





#class Answer(models.Model):
     #question = models.ForeignKey(Question,on_delete=models.CASCADE())
     #text = models.CharField(max_length=300)


class Answer(models.Model):
    #user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    description = models.TextField(max_length=2000)
    person=models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now, blank=True)
    votes = models.IntegerField(default=0)

    def calculate_votes(self):
         up_votes = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                            answer=self.pk).count()
         down_votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                              answer=self.pk).count()
         self.votes = up_votes - down_votes
         self.save()
         return self.votes

    def get_up_voters(self):
         votes = Activity.objects.filter(activity_type=Activity.UP_VOTE,
                                         answer=self.pk)
         voters = []
         for vote in votes:
              voters.append(vote.user)
         return voters

    def get_down_voters(self):
         votes = Activity.objects.filter(activity_type=Activity.DOWN_VOTE,
                                         answer=self.pk)
         voters = []
         for vote in votes:
              voters.append(vote.user)
         return voters

    #create_date = models.DateTimeField(auto_now_add=True)
    #update_date = models.DateTimeField(null=True, blank=True)
    #votes = models.IntegerField(default=0)
    #is_accepted = models.BooleanField(default=False)

class Notification(models.Model):
     message=models.CharField(max_length=200)
     #message=models.TextField()
     viewed=models.BooleanField(default=False,editable=True)
     user=models.ForeignKey(User)
     question=models.ForeignKey(Question)
