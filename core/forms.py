from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
# class EmailForm(UserCreationForm):
#     email = forms.EmailField(max_length=200, help_text='Required')
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')
        
        
class EmailForm(forms.ModelForm):
    email = forms.EmailField(label='Your name', max_length=100)
    class Meta:
        model = User
        fields = ('email',)
        
# class mySetPasswordForm(forms.ModelForm):
#   error_messages = {
#         'password_mismatch': ("The two password fields didn't match."),
#     }
#   new_password1 = forms.CharField(label=("New password"),
#                                   widget=forms.PasswordInput)
#   new_password2 = forms.CharField(label=("New password confirmation"),
#                                   widget=forms.PasswordInput)
#   def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super(SetPasswordForm, self).__init__(*args, **kwargs)

#   def clean_new_password2(self):
#       password1 = self.cleaned_data.get('new_password1')
#       password2 = self.cleaned_data.get('new_password2')
#       if password1 and password2:
#           if password1 != password2:
#               raise forms.ValidationError(
#                   self.error_messages['password_mismatch'],
#                   code='password_mismatch',
#               )
#       return password2

#   def save(self, commit=True):
#       self.user.set_password(self.cleaned_data['new_password1'])
#       if commit:
#           self.user.save()
#       return self.user
        
#   password = forms.CharField(widget=forms.PasswordInput)
  
#   class Meta:
#       model = User
#       fields = ('password',)

# class mySetPasswordForm(SetPasswordForm):
  