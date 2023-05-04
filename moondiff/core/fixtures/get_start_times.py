import requests
from datetime import datetime
from moondiff.core.models import Image
ODE_API_URL = 'https://oderest.rsl.wustl.edu/live2/'

def get_start_time(pdsid):
    resp = requests.get(ODE_API_URL, params={
        'query':'product',
        'results':'l',
        'output':'json',
        'PDSID':pdsid
    })
    try:
        label = resp.json()['ODEResults']['Products']['Product']['label']['Line']
        for label_line in label:
            if label_line.startswith('START_TIME'):
                print(f'line is {pdsid}: {label_line}')
                return datetime.fromisoformat(label_line[-23:])
    except:
        return False

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