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

# Setup without docker. (This is in some ways easier for development)
1. Checkout this git repository
1. Install dependencies. Essentially, you need geodjango set up with sqlite, djangorestframework, and DjangoRangeMiddleware for local development. Install as best for your system. On Ubuntu, you can use conda and pip as in the Dockerfile. On Windows, you can install gdal etc. using OSGEO4W -- there are lines in settings.py that will check if you're using windows and look for OSGEO4W.
1. Copy `localsettings_example.py` to `localsettings.py` and edit it according to comments inside
1. Change directories into MoonDiff/moondiff and run: 
   1. python ../manage.py makemigrations
   1. python ../manage.py migrate
   1. python ../manage.py createsuperuser
   1. python ../manage.py runserver


# Setup using docker-compose (good for production)
 1. Checkout this git repository
 1. Copy `example-env.dev` to `env.dev` and edit it with your server info
 1. Copy your ssl key and cert to nginx/
 1. Update your server name in nginx/default.conf 
 1. Build with `docker-compose build`
 1. Serve with `docker-compose up -d`

# Certificates if using localhost
Use the following to create certs and put them in `nginx/certs`:
```
openssl req -x509 -out ssl_certificate.crt -keyout ssl_certificate.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```