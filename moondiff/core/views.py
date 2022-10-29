from django.views.generic import DetailView
from moondiff.core.models import Pair

class PairDetailView(DetailView):
    model = Pair

# Create your views here.
