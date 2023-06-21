from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django import forms
from django.conf import settings

class RestrictGroupcodeAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super(RestrictGroupcodeAdapter, self).save_user(request, user, form, commit=False)
        signup_code = request.POST.get('signup_code')
        if signup_code not in settings.SECRET_SIGNUP_CODES:
            raise ValidationError(f'Incorrect signup code, {signup_code}, for beta test.')
        user.signup_code = signup_code
        user.save()

class MoonDiffSignupForm(SignupForm):
    signup_code = forms.CharField(max_length=100, label='Signup Code')


    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MoonDiffSignupForm, self).save(request)
        user.signup_code = self.cleaned_data.get('signup_code')
        user.save()
        # Add your own processing here.

        # You must return the original result.
        return user