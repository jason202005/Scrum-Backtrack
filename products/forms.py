import re
from django import forms
from products.models import Product,PBI,Task,User
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import models as auth_models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):

    class Meta():
        model = Product
        fields = ('name','owner','scrum_master', 'sprint_status')

class RegisterationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta():
        model = get_user_model()
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        )

    def save(self, commit=True):
        user = super(RegisterationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_SCRUM_MASTER = True
        if commit:
            user.save()

        return user

class DevSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta():
        model = get_user_model()
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        )


    def save(self, commit=True):
        user = super(DevSignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_DEVELOPER = True
        if commit:
            user.save()

        return user

class POSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta():
        model = get_user_model()
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        )


    def save(self, commit=True):
        user = super(POSignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_PRODUCT_OWNER = True
        if commit:
            user.save()

        return user


class SMSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta():
        model = get_user_model()
        fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'password1',
        'password2',
        )


    def save(self, commit=True):
        user = super(SMSignUpForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_SCRUM_MASTER = True
        if commit:
            user.save()

        return user


class PBIForm(forms.ModelForm):

    class Meta():
        model = PBI
        fields = ('name','description','priority','story_point')


class TaskForm(forms.ModelForm):

    class Meta():
        model = Task
        fields = ('pbi','name','description','hour','status','owner')
