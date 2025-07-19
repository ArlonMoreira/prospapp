from django.db import models

# Create your models here.
class VersionManager(models.Model):

    version = models.CharField(max_length=45)

    def __str__(self):
        return self.version    

    class Meta:
        verbose_name = 'Versão'
        verbose_name_plural = 'Versões'
