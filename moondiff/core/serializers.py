from rest_framework import serializers
from moondiff.core.models import Annotation

class AnnotationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Annotation
        # Should have fields = '__all__' but it complains that User isn't in API
        fields = ['shape', 'notes', 'classification']

class AnnotationForPairSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Annotation
        # Should have fields = '__all__' but it complains that User isn't in API
        fields = ['notes', 'classification']