from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from . import views
from music.views import output, saveAnswer,check,go,signup,sample_view,show_notification

app_name='music'
# SamsadSajid
urlpatterns = [
    #/music/
    url(r'^$',views.LogInFormView.as_view(),name='login'),
#url(r'badhon',go,name='badhon'),
    url(r'^home',sample_view, name='home'),

    url(r'^SignIn',views.UserFormView.as_view(),name='signin'),
    #/music/album_id/
    #url(r'^home',views.IndexView.as_view(),name='home'),
    url(r'^register',views.UserFormView.as_view(),name='register'),
    #url(r'^login',views.login(),name='login'),
    url(r'^(?P<pk>[0-9]+)', output,name='detail1'),
    url(r'^question/(?P<pk>[0-9]+)/ans', saveAnswer, name='detail'),

    #/music/album_id/favourite/
    #url(r'^(?P<album_id>[0-9]+)/favourite',views.favourite,name='favourite'),
    url(r'^album/add',views.AlbumCreate.as_view(),name='album-add'),

    url(r'^album/add',views.AlbumCreate.as_view(),name='album-add'),

    url(r'^askquestion',views.QuestionFormView.as_view(),name='ask_question'),

    url(r'^answer/(?P<pk>[0-9]+)',views.AnswerFormView.as_view(),name='answer'),
    url(r'^success',check,name='succ'),
    url(r'^getstart',signup,name='signup'),
    url(r'^notification/(?P<key>[0-9]+)',show_notification,name='notification'),
    url(r'^answer/vote/',views.vote,name='vote'),
    url(r'^search/', views.search, name='search'),
    url(r'^menu/(?P<string>[A-Za-z]+)',views.menu,name='menu'),

    #url(r'^search/(?P<>[A-Za-)', signup, name='signup'),

]

