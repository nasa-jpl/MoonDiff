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

# Setup using docker-compose (good for production)
 1. Get a working docker-compose installation.
 1. Get SSL keypairs. For development on your local machine, you can follow [this](https://gitlab.com/contextualcode/selfsigned-ssl-certificates)
to get a trusted self-signed certficate for development.
 1. Checkout this git repository
 1. Copy `example-env.dev` to `env.dev` and edit it with your server info
 1. Copy your ssl key and cert to nginx/
 1. Update your server name in nginx/default.conf
 1. Serve with `docker-compose up --build`

# Clearing the database

MoonDiff will create a new sqlite database `db/db.sqlite3` if there isn't one there, and load in a bunch of fixture data
. If there is one, it'll use the existing one. To clear the database, you can just delete that file, and when you run 
docker-compose with the --build option, a new database will be created.

# Certificates if using localhost
Use the following to create certs and put them in `nginx/certs`:
```
openssl req -x509 -out ssl_certificate.crt -keyout ssl_certificate.key \
  -newkey rsa:2048 -nodes -sha256 \
  -subj '/CN=localhost' -extensions EXT -config <( \
   printf "[dn]\nCN=localhost\n[req]\ndistinguished_name = dn\n[EXT]\nsubjectAltName=DNS:localhost\nkeyUsage=digitalSignature\nextendedKeyUsage=serverAuth")
```