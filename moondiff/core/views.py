from django.views.generic import DetailView
from moondiff.core.models import Pair, Annotation, AnnotationReview, get_random
from moondiff.core.serializers import AnnotationSerializer, AnnotationForPairSerializer, ReviewFormSerializer, SubmitReviewSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
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

class AnnotationViewSetThisUser(viewsets.ModelViewSet):
    # Views for creating and listing annotations
    serializer_class = AnnotationSerializer

    # TODO maybe this should be using serializers.CurrentUserDefault() in the serializer instead
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, pair_id=self.request.data['pair_id'])

    def get_queryset(self):
        return Annotation.objects.filter(created_by=self.request.user)

# Can't use a ViewSet because they don't support django templates as far as
# I can tell.
class AddReviewView(APIView):
    # Views for creating and listing annotation reviews
    model = AnnotationReview
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'core/annotation_review.html'
    
    #TODO should really have custom user model designating reviewers
    permission_classes = [permissions.IsAdminUser]
    
    # Get an annotation to review 
    def get(self, request, *args, **kwargs):
        
        # Find an unreviewed annotation and return it
        annotation = get_random(Annotation)
        
        # Remove the related annotation field from ReviewSerializer. We don't
        # want it as a combobox in the form because we already selected it --
        # it's in hidden input in the template.
        
        
        context = {
            'review_serializer': ReviewFormSerializer,
            'annotation': annotation,
            'pair': annotation.pair
        }
        
        return Response(context)

    def post(self, request):
        review_serialized = SubmitReviewSerializer(data=request.data)
        if review_serialized.is_valid():
            review_serialized.save(
                reviewer=self.request.user
            )
            # TODO bug: after a post, the page shown uses the wrong serializer
        return Response({'message': review_serialized.errors, 'review_serializer': SubmitReviewSerializer})