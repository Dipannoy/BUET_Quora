#from django.contrib.auth.models import User
from django import forms
from .models import Question,Answer
class QuestForm(forms.ModelForm):
    #hours = forms.ChoiceField(choices=[(6, 6), (24, 24), (48, 48)], widget=forms.Select(attrs={'size': '3'}))
    ques_text =forms.CharField(widget=forms.Textarea)
    ques_tag=forms.CharField(label='Tag',max_length=50)

    class Meta:
        model=Question
        fields = ['ques_text', 'ques_tag']


class AnswerForm(forms.ModelForm):
    #question = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      #queryset=Question.objects.all())
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        max_length=2000)

    class Meta:
        model = Answer
        fields = [ 'description']

class UserForm(forms.ModelForm):
    username=forms.CharField(max_length=50)
    password=forms.CharField(max_length=60)
