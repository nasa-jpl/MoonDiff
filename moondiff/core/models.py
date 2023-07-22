from django.conf import settings
from django.contrib.gis.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
import random
import datetime

class MoonDiffUser(AbstractUser):
    groupcode = models.CharField(max_length=100, blank=True, null=True)

    @property
    def avg_visit_duration(self):
        """
        Compute the average time this user spends looking at an image pair.
        Caps the maximum time a user can spend in one session with one image at 10 minutes.
        :return:
        """
        visit_durations = [
            min(visit.duration, 600)
            for visit
            in self.visit_set.all()
        ]
        if len(visit_durations) > 0:
            return sum((visit_durations, datetime.timedelta()).total_seconds() / len(visit_durations))
        else:
            return 0


    @property
    def annotations_by_user_reviewed(self):
        return AnnotationReview.objects.filter(annotation__created_by=self)

    @property
    def annotations_by_user_unreviewed_count(self):
        return self.annotation_set.count() - self.annotations_by_user_reviewed.count()

    @property
    def score(self):
        # 1 point for every 20 seconds looking at pairs
        pts_for_looking = self.visit_set.count() * self.avg_visit_duration / 20
        # 10 points for every reported detection
        pts_for_reporting_changes = self.annotation_set.count() * 10
        # 250 points for every confirmed detection
        pts_for_discoveries = AnnotationReview.objects.filter(
            annotation__created_by=self,
            valid_discovery=True).count()
        return sum((pts_for_looking, pts_for_reporting_changes, pts_for_discoveries))

    @property
    def score_zeropadded(self):
        return f"{self.score:>05.0f}"

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
    spacecraft_camera = models.ForeignKey(SpacecraftCamera,
                                          on_delete=models.CASCADE)
    product_id = models.CharField(max_length=100)
    file_data = models.FileField(upload_to='images/')
    start_time = models.DateTimeField(blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    cropped = models.BooleanField(default=False)

    def __str__(self):
        return self.product_id


class PairSet(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.pair_set.count()} pairs)'


class PairManager(models.Manager):
    def unvisited_by_user(self, user):
        return self.get_queryset().difference(self.visited_by_user(user=user))

    def visited_by_user(self, user):
        return self.get_queryset().filter(visit__user=user).distinct()

    def compared_by_user(self, user):
        # Returns the pairs that this user clicked "Done" on
        return self.get_queryset().filter(visit__user=user,
                                          visit__finished=True).distinct()

    def not_compared_by_user(self, user):
        # Returns the pairs that this user clicked "Done" on
        return self.get_queryset().difference(self.compared_by_user(user=user))


class Pair(models.Model):
    old_image = models.ForeignKey(Image, on_delete=models.CASCADE,
                                  related_name='pairs_with_this_as_old')
    new_image = models.ForeignKey(Image, on_delete=models.CASCADE,
                                  related_name='pairs_with_this_as_new')
    pairset = models.ForeignKey(PairSet, on_delete=models.CASCADE, blank=True,
                                null=True)
    coreg_notes = models.TextField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=512)
    objects = PairManager()

    def __str__(self):
        if self.name:
            return self.name
        else:
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
        if self.pairset.name == 'examples':
            return reverse('example', kwargs={'pk': self.pk})
        else:
            return reverse('pair-detail', kwargs={'pk': self.pk})

    @property
    def example_annotations(self):
        if self.pairset.name == 'examples':
            # All example pair annotations should be made by user 1, the admin
            annots = [
                annot.shape.coords for annot in
                self.annotation_set.filter(created_by=MoonDiffUser.objects.get(pk=1))
            ]
            return annots
        else:
            return None


class Visit(models.Model):
    """
    One instance of this is created each time a user goes to PairDetailView.
    End time is set when they click "skip pair" or "pair done."
    """
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} viewed pair {self.pair.pk} at {self.start}"

    @property
    def duration(self):
        return self.end - self.start

    def get_absolute_url(self):
        return reverse('visit-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()

    def __str__(self):
        return f"{self.created_by} commented at {self.created_on}"


class Annotation(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   editable=False)
    shape = models.PolygonField()
    notes = models.TextField()
    pair = models.ForeignKey(Pair, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    classification = models.CharField(max_length=10,
                                      choices=(('CRATER', 'new crater'),
                                               ('SPLOTCH',
                                                'splotch (change in '
                                                'brightness over an area)'),
                                               ('HW', 'spacecraft hardware'),
                                               ))

    def __str__(self):
        return f"{self.created_by} reported a difference in {self.pair}"

    def get_absolute_url(self):
        return reverse('annotation-detail', kwargs={'pk': self.pk})


class AnnotationReview(models.Model):
    further_review_required = models.BooleanField()
    valid_discovery = models.BooleanField()
    comments = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    annotation = models.ForeignKey(Annotation, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer} reviewed {self.annotation}"
