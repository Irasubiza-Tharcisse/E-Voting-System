from django.db import models
from django.utils import timezone
from .utils import encrypt_vote, decrypt_vote
import hashlib


class Election(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    def is_active(self):
        now = timezone.now()
        return self.start_time <= now <= self.end_time


class Position(models.Model):
    title = models.CharField(max_length=100)
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='positions'
    )
    
    def __str__(self):
        return f"{self.title} - {self.election.title}"


class Candidate(models.Model):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='candidates/')
    manifesto = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.position.title})"


class Vote(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter_hash = models.CharField(max_length=64)
    candidate_encrypted = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('election', 'voter_hash')

    def set_candidate(self, candidate_id):
        self.candidate_encrypted = encrypt_vote(str(candidate_id))

    def get_candidate_id(self):
        return int(decrypt_vote(self.candidate_encrypted))
