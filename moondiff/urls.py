"""MoonDiff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from moondiff.core.views import PairDetailView, AnnotationViewSet, SignupView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from allauth.account.views import ConfirmEmailView, EmailView
from django.views.generic.base import RedirectView

router = routers.DefaultRouter()
router.register(r'annotations', AnnotationViewSet, basename='annotation')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('pair/(?P<pk>[a-z0-9]+)', PairDetailView.as_view(), name='pair-detail'),
    re_path('review/(?P<pk>[a-z0-9]+)', login_required(PairDetailView.as_view()), name='annotation-review-detail'),
    path('api/', include(router.urls)), # API urls
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'registration/account-confirm-email/(?P<key>[-:\w]+)/', ConfirmEmailView.as_view(),
          name='account_confirm_email'),
    re_path(r'registration/account-email/', EmailView.as_view(),
          name='account_email'),
    path('account/logout/', RedirectView.as_view(pattern_name='rest_framework:logout'), name='account_logout'),
    path('account/login/', RedirectView.as_view(pattern_name='rest_framework:login'), name='account_login'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^signup/$', SignupView.as_view(template_name="signup.html"),
                          name='signup'),
    path('', TemplateView.as_view(template_name='frontpage.html'), name='frontpage')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
