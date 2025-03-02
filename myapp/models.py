from django.db import models

class TrainingData(models.Model):
    oddsA = models.FloatField()
    oddsB = models.FloatField()
    ranking = models.FloatField()

