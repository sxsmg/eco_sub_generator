from django.db import models
from ecowiser.storage_backend import B2Storage
from django.conf import settings
from mongoengine import Document, ReferenceField, StringField, FloatField, connect

b2_storage = B2Storage(
    settings.B2_BUCKET_NAME,
    settings.B2_APPLICATION_KEY_ID,
    settings.B2_APPLICATION_KEY
)

class Video(models.Model):
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', storage=b2_storage)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Subtitle(Document):
    video = ReferenceField('Video')
    subtitle_text = StringField()
    start_time = FloatField()
    end_time = FloatField()