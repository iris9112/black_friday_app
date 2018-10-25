from django.db import models

# Create your models here.


class Document(models.Model):
    name = models.CharField(max_length=255, blank=True, verbose_name="Nombre documento")
    document = models.FileField(upload_to='documents/', verbose_name="Documento")   
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return '{0.name} - {0.updated}'.format(self)
