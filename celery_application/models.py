from django.db import models  # noqa:F401


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255, default="Some String")
    description = models.CharField(max_length=1000000, default="Some String")

    def __str__(self):
        return self.name


class Quotes(models.Model):
    texts = models.CharField(max_length=255, default="Some String")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.texts
