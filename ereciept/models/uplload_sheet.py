from django.db import models




class Sheet(models.Model):
    file = models.FileField(upload_to = 'uploader')
    