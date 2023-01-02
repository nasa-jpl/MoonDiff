from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import random


def get_random(queryset):
    # Return a random pair
    pks = queryset.values_list('pk', flat=True)
    if pks:
        random_pk = random.choice(pks)
        return queryset.model.objects.get(pk=random_pk)
    else:
        return None


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
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class PairManager(models.Manager):
    def unvisited_by_user(self, user):
        return self.get_queryset().difference(self.visited_by_user(user=user))
    
    def visited_by_user(self, user):
        return self.get_queryset().filter(visit__user=user).distinct()

    def compared_by_user(self, user):
        # Returns the pairs that this user clicked "Done" on
        return self.get_queryset().filter(visit__user=user, visit__finished=True).distinct()

    def not_compared_by_user(self, user):
        # Returns the pairs that this user clicked "Done" on
        return self.get_queryset().difference(self.compared_by_user(user=user))

class Pair(models.Model):
    old_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='pairs_with_this_as_old')
    new_image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='pairs_with_this_as_new')
    pairset = models.ForeignKey(PairSet, on_delete=models.CASCADE, blank=True, null=True)
    coreg_notes = models.TextField(blank=True, null=True)
    
    objects = PairManager()
    
    def __str__(self):
        return f"{self.old_image} compared to {self.new_image}"

    def get_other(self):
        # Return a random pair other than this one
        pair_pks = [v['pk'] for v in Pair.objects.values('pk')]
        pair_pks.remove(self.pk)
        if pair_pks:
            random_pk = random.choice(pair_pks)
            return Pair.objects.get(pk=random_pk).get_absolute_url()
        else:
            return None

    def get_absolute_url(self):
        return reverse('pair-detail', kwargs={'pk': self.pk})

    class Meta:
        unique_together = ['old_image', 'new_image']


class Visit(models.Model):
    """
    One instance of this is created each time a user goes to PairDetailView.
    End time is set when they click "skip pair" or "pair done."
    """
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    finished = models.BooleanField(default=False)


class Comment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()


class Annotation(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    shape = models.PolygonField()
    notes = models.TextField()
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    classification = models.CharField(max_length=10,
        choices=(('CRATER','new crater'),
        ('SPLOTCH','splotch (change in brightness over an area)'),
        ('HW','spacecraft hardware'),
    ))


class AnnotationReview(models.Model):
    further_review_required = models.BooleanField()
    valid_discovery = models.BooleanField()
    comments = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
