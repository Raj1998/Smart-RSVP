from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.
class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    guest_name = models.CharField(max_length=300)
    function_name = models.CharField(max_length=400)
    max_rsvp = models.IntegerField()
    done_rsvp = models.IntegerField()
    digest = models.CharField(max_length=35)
    url = models.CharField(max_length=250)
    qrcode = models.ImageField(upload_to="rsvp", default="")


# deleting coresponding image on the deletion of record.
# credits: https://www.aceinthedeck.com/delete-image-after-deletion-from-database/
@receiver(post_delete, sender=Booking)
def photo_post_delete_handler(sender, **kwargs):
    listingImage = kwargs['instance']
    storage, path = listingImage.qrcode.storage, listingImage.qrcode.path
    storage.delete(path)