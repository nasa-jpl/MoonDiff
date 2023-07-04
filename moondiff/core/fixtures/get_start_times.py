import requests
from datetime import datetime
import django
import os
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', 'moondiff.settings'
)
django.setup()
from moondiff.core.models import Image
ODE_API_URL = 'https://oderest.rsl.wustl.edu/live2/'

def get_start_time(pdsid):
    if pdsid.startswith('M'):
        pdsid = 'data.nac.' + pdsid
    else:
        pdsid = '_'.join(pdsid.split('_')[0:5])
    resp = requests.get(ODE_API_URL, params={
        'query':'product',
        'results':'m',
        'output':'json',
        'PDSID':pdsid
    })
    print(f'Using pdsid: {pdsid}')
    starttime = resp.json()['ODEResults']['Products']['Product']['UTC_start_time']
    return datetime.fromisoformat(starttime[:23])

def set_start_times_from_ode():
    for image in Image.objects.all():
        start_time = get_start_time(image.product_id)

        if start_time:
            image.start_time = start_time
            image.save()
            print(f'{image} start time set to {image.start_time}')
        else:
            print(f'{image} failed')
            pass

set_start_times_from_ode()