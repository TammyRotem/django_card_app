from django import forms
from django.forms import modelformset_factory
from tarot.models import Card, Reading,UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

    

class CardForm(forms.Form):
    cards = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple(attrs = {'class':'forming'}),queryset=Card.objects.all())
    question = forms.CharField(widget = forms.Textarea)

class ReadingForm(forms.Form):
    reading = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'forming'}), queryset=Reading.objects.all())



class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(max_length = 150)

    class Meta:
        model = User
        fields = ('username','email','first_name','password1','password2')

    def save(self, commit = True):
        user = super().save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']

        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()
        


    



    
