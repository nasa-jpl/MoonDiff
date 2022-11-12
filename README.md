# MoonDiff web app
This is a web application for the collaborative science project MoonDiff. It displays pairs of old and new lunar orbital
imagery and provides an interface for the user to annotate differences they notice between the images. The idea is to
find new craters, rockfall areas, spacecraft, etc.

# Technologies used
 - Django / [geodjango](https://docs.djangoproject.com/en/4.1/ref/contrib/gis/) with spatialite
 - [Django REST framework](https://www.django-rest-framework.org/)
 - [Cloud-optimized geotiffs](https://www.cogeo.org/)
 - [Nginx](https://www.nginx.com/)
 - [Gunicorn](https://gunicorn.org/)
 - [VanillaJS](http://vanilla-js.com/) ;-)

# Setup
 1. Checkout this git repository
 1. Copy `example-env.dev` to `env.dev` and edit it with your server info
 1. Build with `docker-compose build`
 1. Serve with `docker-compose up -d`