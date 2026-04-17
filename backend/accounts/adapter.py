from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return
        request.session['socialaccount_sociallogin'] = sociallogin.serialize()
        return redirect('accounts:complete_signup')