from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class SpacecraftCamera(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    spacecraft_camera = models.ForeignKey(SpacecraftCamera, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100)
    file_data = models.FileField(upload_to='images/')

    def __str__(self):
        return self.product_id

class PairSet(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Pair(models.Model):
    old_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='pairs_with_this_as_old')
    new_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='pairs_with_this_as_new')
    pairset = models.ForeignKey(PairSet, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.old_image} compared to {self.new_image}"

    def get_absolute_url(self):
        return reverse('pair-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['old_image', 'new_image']


class Annotation(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    shape = models.PolygonField()
    notes = models.TextField()
    created_at = models.DateField(auto_now=True)
    # classification = models.Choices([])

class AnnotationReview(models.Model):
    further_review_required = models.BooleanField()
    valid_discovery = models.BooleanField()
    comments = models.TextField(blank=True)
    reviewer = User()
    created_at = models.DateField(auto_now=True)
