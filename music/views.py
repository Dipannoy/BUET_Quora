from django.contrib import messages
from django.views import generic
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import View

from .models import Album, Question,Answer,Notification
from .forms import UserForm,LogForm
from .questionform import QuestForm,AnswerForm
from Activity.models import Activity
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import DateTimeField
from django.db.models.functions import Trunc
from django.shortcuts import render_to_response


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_question'



    def get_queryset(self):
        return Question.objects.all()












class DetailView(generic.DeleteView):
    model = Question
    template_name = 'music/qst1.html'


class AlbumCreate(CreateView):
    model=Album
    fields = ['artist','album_title','genre','album_logo ']






class UserFormView(View):
    form_class=UserForm
    template_name='music/registration_form.html'
    #display blank form
    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})


    #process form data
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            print("hiiiiiiii")
            user = form.save(commit=False)

            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('music:home')

        return render(request, self.template_name, {'form': form})

class LogInFormView(View):
    form_class=LogForm
    template_name = 'music/start2.html'


    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):


        form = self.form_class(request.POST)
        print (form)

        if form.is_valid():
            print("Dipan")
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #user.set_password(password)

            #user.save()
            print(username,password)
            user = authenticate(request,username=username, password=password)
            if user is not None:
                print("log in")
                if user.is_active:
                    login(request, user)
                    return redirect('music:home')
            else:
                 # print("log in")
                return redirect('music:login')

        return render(request, self.template_name, {'form': form})


class QuestionFormView(View):
    form_class=QuestForm
    template_name = 'music/question_form.html'

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form,'id':request.user.id})


    #process form data
    def post(self,request):
        form=self.form_class(request.POST)
        current_user=request.user
        # print(form)
        if form.is_valid():
            question = form.save(commit=False)
            ques_text = form.cleaned_data['ques_text']
            ques_tag = form.cleaned_data['ques_tag']
            # print(ques_text)
            # print(ques_tag)
            qsn = Question(text=ques_text, tag=ques_tag,person=current_user.username)
            qsn.save()
        all_questions=Question.objects.all()
        page = request.GET.get('page', 1)
        current_user = request.user

        paginator = Paginator(all_questions, 4)
        try:
            allqsts = paginator.page(page)
        except PageNotAnInteger:
            allqsts = paginator.page(1)
        except EmptyPage:
            allqsts = paginator.page(paginator.num_pages)

        # return render(request, 'music/index2.html',
        #               {'all_question': all_questions, 'username': current_user.username, 'id': current_user.id})

        return redirect('home/')









class AnswerFormView(View):
    form_class=AnswerForm
    template_name = 'music/answer_form.html'

    def get(self,request, pk):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form,'question':pk,'id':request.user.id})


    #process form data
    def post(self,request):
        form=self.form_class(request.POST)
        # print(form)
        if form.is_valid():
            answer = form.save(commit=False)
            question = form.cleaned_data['question']
            description = form.cleaned_data['description']

            ans = Answer(question=question,description=description)
            ans.save()
        return render(request, self.template_name, {'form': form})



def output(request, pk):
    notifications=Notification.objects.all()
    qtion=Question.objects.get(id=pk)
    print (pk)
    for notification in notifications:
        # print (notification.question.id)
        if(notification.question.id==qtion.id):
            # print ("okkkkkk")
            notification.viewed=True
            notification.save()
            #print (notification.viewed)

    question=Question.objects.filter(id=pk)
    print()
    answer=Answer.objects.filter(question=question)
    form=AnswerForm()

    return render(request, 'music/qst1.html',{'answers':answer,'id':request.user.id,'question':qtion})

def saveAnswer(request, pk):
    question = Question.objects.get(id=pk)
    qst_prsn=question.person
    user=User.objects.get(username=qst_prsn)
    current_user=request.user
    ans_prsn=current_user.username
    string=ans_prsn + "has answered your question"
    notification_entry=Notification(message=string,user=user,question=question)
    notification_entry.save()
    #print(question.person)

    form=AnswerForm(request.POST)
    print(form)
    if form.is_valid():
        print("form is valid")
        answer = form.save(commit=False)
        #question = form.cleaned_data['question']
        description = form.cleaned_data['description']

        ans = Answer(description=description,person=current_user.username, question= question)
        ans.save()
    question1 = Question.objects.get(id=pk)

    answer1 = Answer.objects.filter(question=question1)


    return render(request, 'music/qst1.html',{'answers':answer1,'id':request.user.id,'question':question1})

def check(request):
    all_questions=Question.objects.all()
    page = request.GET.get('page', 1)
    current_user = request.user

    paginator = Paginator(all_questions,4)
    try:
        allqsts = paginator.page(page)
    except PageNotAnInteger:
       allqsts = paginator.page(1)
    except EmptyPage:
        allqsts = paginator.page(paginator.num_pages)

    # all_questions.objects.order_by(
    #     Trunc('date', 'date', output_field=DateTimeField()).desc(),
    #     '-score')

    if request.method == 'POST':
        #print ("dibya")
        # form=UserForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print (username,password)
        #name(username)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)


                return render(request, 'music/index2.html',
                              {'all_question': allqsts, 'username': current_user.username,'id':current_user.id})
        else:
            # print ("No user detected")
            messages.add_message(request, messages.ERROR, "Username or Paswword"
                                " is invalid")
            return render(request, 'music/Start2.html')

    return render(request, 'music/index2.html',
                          {'all_question': allqsts, 'username': current_user.username, 'id': current_user.id})
    # if form.is_valid():
    #     print("form is valid")
    #     username = form.cleaned_data['username']
    #     password = form.cleaned_data['password']
    #     print(username, password)
    # return render(request, 'music/index.html')

def go(request):
    return render(request,'music/badhon.html')

def signup(request):
    all_questions = Question.objects.all()
    page = request.GET.get('page', 1)
    current_user = request.user

    paginator = Paginator(all_questions, 4)
    try:
        allqsts = paginator.page(page)
    except PageNotAnInteger:
        allqsts = paginator.page(1)
    except EmptyPage:
        allqsts = paginator.page(paginator.num_pages)

    # if request.method == 'POST':
    #     print ("dibya")
    #     # form=UserForm(request.POST)
    #     #email = request.POST.get('email')
    #     username = request.POST.get('username')
    #
    #     password = request.POST.get('password')
    #     print (username,password)
    # return render(request, 'music/badhon.html')
    form = UserForm(request.POST)
    # if request.method == 'POST':
    if form.is_valid():
        # print("form is valid")
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password=form.cleaned_data['password']
        user.set_password(password)
        user.save()
        # print (username)
    #         #email = form.cleaned_data['email']
    #         password=form.cleaned_data['password']
    #         print (username,password)
    #         user.set_password(password)
    #         user.save()
    #
    #         user = authenticate(username=username, password=password)
    #         if user is not None:
    #             if user.is_active:
    #                 login(request, user)
    #
    #
    #                 return render(request, 'music/index.html')
    #
    #         else:
    #             return render(request, 'music/index.html')
    messages.add_message(request, messages.SUCCESS, "Successfully Sign Up!!If you want to visit"
                                                  " please log in")
    return render(request, 'music/Start2.html')

    #







def sample_view(request):
    all_questions = Question.objects.all()
    page = request.GET.get('page', 1)
    current_user = request.user

    paginator = Paginator(all_questions, 4)
    try:
        allqsts = paginator.page(page)
    except PageNotAnInteger:
        allqsts = paginator.page(1)
    except EmptyPage:
        allqsts = paginator.page(paginator.num_pages)
    current_user = request.user
    # all_questions = Question.objects.all()
    # print(current_user.username)

    return render(request, 'music/index2.html',{'all_question':allqsts,'username':current_user.username,'id':request.user.id})


def show_notification(request,key):
    notification_set=Notification.objects.all()
    user=User.objects.get(id=key)
    not_list=list()
    chk=key
    #print (key)

    for notify in notification_set:


        if  notify.user.id==user.id:
            # print ("dibya")


            if notify.viewed==False:
                not_list.append(notify)




    return  render(request, 'music/notification.html', {'notifications':not_list, 'id':request.user.id})

def delete_notification(request,notification_id):
    no=Notification.objects.get(id=notification_id)
    no.viewed=True
    no.save()
#     return  render_to_response('notification.html',{'notification':no})


def vote(request):
    current_user=request.user
    name=current_user.username
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    ans_prsn=answer.person
    ans_qstid=answer.question_id
    question=Question.objects.get(pk=ans_qstid)
    user1=User.objects.get(username=ans_prsn)


    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(
        Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE) |  # noqa: E501
        Q(user=user) | Q(answer=answer_id))
    # if activity:
    #     activity.delete()
    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        activity = Activity(activity_type=vote, user=user, answer=answer_id)
        activity.save()
    if activity.activity_type == 'U':
        msg=" has voted up"
    else:
        msg=" has voted down"
    messge=name + msg + "your answer."
    notification = Notification(message=messge,user=user1,question=question)
    notification.save()

    return HttpResponse(answer.calculate_votes())

def search(request):


        #albums = Album.objects.filter(user=request.user)
        Questions=Question.objects.all()
        query = request.GET.get("q")
        if query:
            questions = Questions.filter(
                Q(tag__icontains=query)

            ).distinct()

            return render(request, 'music/request.html', {
                'qsts': questions,

            })
        else:
            return render(request, 'music/index2.html')


def menu(request,string):
    q=Question.objects.all()
    qq=Question.objects.filter(tag__icontains=string)
    # print(string)
    # for qst in qq:
    #     #if qst.tag == qq.tag:
    #         print(qst.id)
    return render(request, 'music/menu.html',{'qsts':qq})

