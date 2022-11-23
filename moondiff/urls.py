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
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'annotations', AnnotationViewSet, basename='annotation')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('pair/(?P<pk>[a-z0-9]+)', PairDetailView.as_view(), name='pair-detail'),
    re_path('review/(?P<pk>[a-z0-9]+)', login_required(PairDetailView.as_view()), name='annotation-review-detail'),
    path('api/', include(router.urls)), # API urls
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path(r'^signup/$', SignupView.as_view(template_name="signup.html"),
                          name='signup'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
