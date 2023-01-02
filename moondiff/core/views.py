from django.views.generic import DetailView, RedirectView
from moondiff.core.models import Pair, Annotation, AnnotationReview, Visit, get_random
from moondiff.core.serializers import AnnotationSerializer, AnnotationForPairSerializer, ReviewFormSerializer, SubmitReviewSerializer, VisitSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse

@method_decorator(login_required, name='dispatch')
class PairDetailView(DetailView):
    model = Pair

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        # Add in a serializer for the annotation form
        context['annotation_serializer'] = AnnotationForPairSerializer(context={'request': self.request})

        # Create a Visit record and pass the pk
        new_visit = Visit.objects.create(pair=self.object, user=self.request.user)
        new_visit.save()
        context['visit'] = new_visit

        # Add in this user's annotations to the context
        if self.request.user.is_authenticated:
            context['annotations'] = [
                annot.shape.coords for annot in
                self.object.annotation_set.filter(created_by=self.request.user)
            ]
        else:
            context['annotations'] = None
            
        return context

class VisitsViewSet(viewsets.ModelViewSet):
    serializer_class = VisitSerializer
    queryset = Visit.objects.all()

    # From https://tech.serhatteker.com/post/2020-09/enable-partial-update-drf/ to allow partial updates 
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

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
        annotation = Annotation.objects.get(pk=kwargs['pk'])

        context = {
            'review_serializer': ReviewFormSerializer,
            'annotations': [annotation.shape.coords],
            'pair': annotation.pair
        }

        return Response(context)

    def post(self, request, *args, **kwargs):
        review_serialized = SubmitReviewSerializer(data=request.data)
        if review_serialized.is_valid():
            review_serialized.save(
                reviewer=self.request.user
            )
            # TODO bug: after a post, the page shown uses the wrong serializer
        return Response({'message': review_serialized.errors, 'review_serializer': SubmitReviewSerializer})

class SelectPairView(RedirectView):
    """
    This is a view that selects a random detection to review, and returns a
    redirect to the page for reviewing that detection.
    """
    def get_redirect_url(self, *args, **kwargs):
        pair = get_random(Pair)
        return pair.get_absolute_url()

class SelectReviewView(RedirectView):
    """
    This is a view that selects a random detection to review, and returns a
    redirect to the page for reviewing that detection.
    """
    def get_redirect_url(self, *args, **kwargs):
        annotation = get_random(Annotation)
        return reverse('review-detection', kwargs={'pk':annotation.pk})