import random
from django.shortcuts import render, redirect
from datetime import datetime
from tarot.models import Card,Reading, UserProfile
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from tarot.forms import CardForm, ReadingForm
import pandas
from django.urls import reverse
from django.db import connection
import plotly.express as px
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ExtendedUserCreationForm, UserProfileForm


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('tarot:home'))
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('tarot:home')
            else:
                print('User not found')
        else:
            # If there were errors, we render the form with these
            # errors
            return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('tarot:home')

def index(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = 'not logged in'

    context = {'username' : username}
    return HttpResponseRedirect('tarot:home')

@login_required
def profile(request):
    return render(request, 'profile.html')

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit = False)
            profile.user = user

            profile.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)

            return redirect('tarot:home')
    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()

    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'register.html', context)


def generate_reading(request):
    if request.method == "POST":
        num_cards = int(request.POST.get('num_cards'))
        question = request.POST.get('question')
        if request.user.is_authenticated and UserProfile.objects.filter(user = request.user.id):
            profile = request.user.userprofile
        else:
            profile = None
        reading = Reading.objects.create(num_of_cards = num_cards,question = question, owner = profile)
        reading.save()

        cards = random.sample(range(58, 135), num_cards)

        for i in cards:
            card_obj = Card.objects.get(pk = i)
            reading.cards.add(card_obj)
        return HttpResponseRedirect('results/%s' % reading.id)
    else:
        return render(request,'generate_reading.html')


	

def create_reading(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        data = form.__dict__['data']

        
        
        if form.is_valid():
            if request.user.is_authenticated:
                profile = request.user.userprofile
            else:
                profile = None
            reading = Reading.objects.create(num_of_cards = len(data.getlist('cards')),question = form.cleaned_data['question'], owner = profile)
            reading.save()
            for card in data.getlist('cards'):
                card_obj = Card.objects.get(pk = card)
                reading.cards.add(card_obj)
        return HttpResponseRedirect('results/%s' % reading.id)
       
        
    form = CardForm()
    return render(request,'create_reading.html',{'form':form})


def results(request,pk):
    reading = Reading.objects.get(pk=pk)
    query = str(reading.cards.all().query)
    df = pandas.read_sql_query(query, connection)
    
    fig_elements = px.pie(df,  names='card_element',color_discrete_sequence=px.colors.sequential.RdBu)
    graph_elements = fig_elements.to_html(full_html=False, default_height=350, default_width=350)

    fig_arcana_rank = px.pie(df,  names='card_arcana_rank',color_discrete_sequence=px.colors.sequential.RdBu)
    graph_arcana_rank = fig_arcana_rank.to_html(full_html=False, default_height=350, default_width=350)

    fig_categories = px.parallel_categories(df,dimensions=['card_element', 'card_astro_sign', 'card_astro_planet'])
    graph_categories = fig_categories.to_html(full_html=False, default_height=350, default_width=850)

    
    context = {
        "question": reading.question,
        "reading_id": reading.id,
        "reading_num_cards": reading.num_of_cards,
        "cards": reading.cards.all(),
        "plot_elements_div": graph_elements,
        "plot_arcana_rank_div":graph_arcana_rank,
        "plot_categories_div": graph_categories
        
    }
    return render(request, "results.html",context)
    

def review_reading(request):
    form = ReadingForm()
    if request.user.is_authenticated and UserProfile.objects.filter(user = request.user.id):
        form.fields['reading'].queryset = Reading.objects.filter(owner = request.user.userprofile.id)
    form.fields['reading'].queryset = Reading.objects.filter(owner=None)
    if request.method == 'POST':
            reading = request.POST['reading']
            return HttpResponseRedirect('results/%s' % reading)
        
    return render(request,'review_reading.html',{'form':form})

        
def home(request):
    return render(request,'homepage.html')
