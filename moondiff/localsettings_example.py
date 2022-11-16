# Example settings for if you're not using docker / docker compose
# Create a long random secret key and move this file to localsettings.py 
SECRET_KEY = "YOUR_SECRET_KEY"
DEBUG=True
ALLOWED_HOSTS=('127.0.0.1',)
LOCAL_MIDDLEWARE = ['DjangoRangeMiddleware.middleware.RangesMiddleware']