from django.contrib.gis.db import models

class SpacecraftCamera(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Image(models.Model):
    spacecraft_camera = models.ForeignKey(SpacecraftCamera, on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100)
    file_data = models.FileField()

    def __str__(self):
        return self.product_id

class PairSet(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class Pair(models.Model):
    old_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='old_image')
    new_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='new_image')
    pairset = models.ForeignKey(PairSet, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"{self.old_image}xx{self.new_image}"

    class Meta:
        unique_together = ['old_image', 'new_image']


class Annotation(models.Model):
    shape = models.PolygonField()
    notes = models.TextField()
    # classification = models.Choices([])
