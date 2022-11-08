from django.views.generic import DetailView
from moondiff.core.models import Pair, Annotation
from moondiff.core.serializers import AnnotationSerializer, AnnotationForPairSerializer
from rest_framework import viewsets

class PairDetailView(DetailView):
    model = Pair

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Add in a serializer for the annotation form
        context['annotation_serializer'] = AnnotationForPairSerializer()
        
        # Add in this user's annotations to the context
        context['annotation_set_this_user'] = self.object.annotation_set.filter(created_by=self.request.user)
        return context

class AnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Annotation.objects.filter(created_by=self.request.user)

