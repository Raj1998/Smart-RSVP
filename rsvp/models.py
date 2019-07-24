from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=200)
    event_desc = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


# Create your models here.
class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=300)
    max_rsvp = models.IntegerField()
    done_rsvp = models.IntegerField()
    digest = models.CharField(max_length=35)
    url = models.CharField(max_length=250)
    qrcode = models.ImageField(upload_to="rsvp", default="")


# deleting coresponding image on the deletion of record.
# credits: https://www.aceinthedeck.com/delete-image-after-deletion-from-database/
@receiver(post_delete, sender=Booking)
def photo_post_delete_handler(sender, **kwargs):
    try:
        listingImage = kwargs['instance']
        storage, path = listingImage.qrcode.storage, listingImage.qrcode.path
        storage.delete(path)
    except:
        print("Problem while image deletion")