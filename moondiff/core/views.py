from django.views.generic import DetailView
from moondiff.core.models import Pair, Annotation
from moondiff.core.serializers import AnnotationSerializer
from rest_framework import viewsets

class PairDetailView(DetailView):
    model = Pair

class AnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        
    def get_queryset(self):
        return Annotation.objects.filter(created_by=self.request.user)

