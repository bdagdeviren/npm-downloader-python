from django.db import models


class NpmPackage(models.Model):
    name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.name
