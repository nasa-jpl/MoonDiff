from django.contrib.gis.db import models

class SpacecraftCamera(models.Model):
    name = models.CharField(max_length=100)


class Image(models.Model):
    spacecraft_camera = models.ForeignKey(SpacecraftCamera, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100)
    file_data = models.FileField()


class PairSet(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    pass


class Pair(models.Model):
    old_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='old_image')
    new_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='new_image')
    pairset = models.ForeignKey(PairSet, on_delete=models.CASCADE, blank=True)

    class Meta:
        unique_together = ['old_image', 'new_image']


class Annotation(models.Model):
    shape = models.PolygonField()
    notes = models.TextField()
    # classification = models.Choices([])
