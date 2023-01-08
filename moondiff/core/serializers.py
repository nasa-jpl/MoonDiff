from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from moondiff.core.models import Annotation, AnnotationReview, Visit, Comment

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

class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
