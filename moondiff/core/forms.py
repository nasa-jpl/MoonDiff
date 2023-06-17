from allauth.account.forms import SignupForm
from allauth.account.adapter import DefaultAccountAdapter
from django.forms import ValidationError
from django import forms
from django.conf import settings

class RestrictGroupcodeAdapter(DefaultAccountAdapter):
    def clean_groupcode(self, groupcode):
        if groupcode not in settings.ALLOWED_GROUPCODES:
            raise ValidationError('You are restricted from registering.\
                                                  Please contact admin.')
        return groupcode

class MoonDiffSignupForm(SignupForm):
    groupcode = forms.CharField(max_length=100, label='Group Code')
    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MoonDiffSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user