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
from moondiff.core.views import PairDetailView, AnnotationViewSetThisUser, \
    VisitsViewSet, AddReviewView, SelectReviewView, SelectPairView, \
    ProfileView, \
    AllDoneView, CommentsViewSet
from django.views.generic import TemplateView, RedirectView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'annotations', AnnotationViewSetThisUser,
                basename='annotation')
router.register(r'visits', VisitsViewSet, basename='visit')
router.register(r'comments', CommentsViewSet, basename='comment')

inner_urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/<pk>', ProfileView.as_view(), name='profile'),
    path('admin/login/', RedirectView.as_view(pattern_name='account_login',
                                              permanent=True)),
    path('admin/', admin.site.urls),
    re_path('compare_pair/select', SelectPairView.as_view(), 
            name='select-pair-to-compare'),
    re_path('compare_pair/(?P<pk>[a-z0-9]+)', PairDetailView.as_view(),
            name='pair-detail'),
    re_path('review_detection/select', SelectReviewView.as_view(),
            name='select-detection-to-review'),
    re_path('review_detection/(?P<pk>[a-z0-9]+)', AddReviewView.as_view(),
            name='review-detection'),
    path('all_done/', AllDoneView.as_view(), name='all_done'),
    path('api/', include(router.urls)), # API urls
    path('', TemplateView.as_view(template_name='frontpage.html'), name='frontpage')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path(settings.BASE_URL + '/', include(inner_urlpatterns))
]
