from django.views.generic import DetailView, TemplateView
from moondiff.core.models import Pair, Annotation
from moondiff.core.serializers import AnnotationSerializer, AnnotationForPairSerializer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class PairDetailView(DetailView):
    model = Pair

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Add in a serializer for the annotation form
        context['annotation_serializer'] = AnnotationForPairSerializer(context={'request': self.request})

        # Add in this user's annotations to the context
        if self.request.user.is_authenticated:
            context['annotation_set_this_user'] = self.object.annotation_set.filter(created_by=self.request.user)
        else:
            context['annotation_set_this_user'] = None
            
        return context

class AnnotationViewSet(viewsets.ModelViewSet):
    # Views for creating and listing annotations
    serializer_class = AnnotationSerializer

    # TODO maybe this should be using serializers.CurrentUserDefault() in the serializer instead
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, pair_id=self.request.data['pair_id'])

    def get_queryset(self):
        return Annotation.objects.filter(created_by=self.request.user)