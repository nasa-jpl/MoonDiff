from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from moondiff.core.models import Annotation, AnnotationReview

class AnnotationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Annotation
        # Should have fields = '__all__' but it complains that User isn't in API
        fields = ['shape', 'notes', 'classification']

class AnnotationForPairSerializer(serializers.HyperlinkedModelSerializer):
    # created_by = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )
    class Meta:
        model = Annotation
        # Should have fields = '__all__' but it complains that User isn't in API
        fields = ['notes', 'classification', 'created_by']

class ReviewFormSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationReview
        # need to exclude annotation field because that's already set
        exclude = ['annotation']

class SubmitReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnnotationReview
        fields = '__all__'