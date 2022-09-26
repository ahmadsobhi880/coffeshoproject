from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import datetime

WEEK_DAYS = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (7, 'Sunday'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='profile_pics/default.png', upload_to='profile_pics/')
    holiday = models.IntegerField(choices=WEEK_DAYS, default=7, null=True)
    confinement = models.DateTimeField(auto_now_add=False, null=True, default=None)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_image_url(self):
        try:
            return self.image.url
        except:
            return ''

    def get_appointments(self):
        try:
            return self.user.appointments.all().order_by('-date_created')
        except:
            return None

    def is_confined(self):
        if self.confinement:
            current_date = datetime.datetime.now()
            interval = datetime.timedelta(days=14).total_seconds()
            if not current_date.timestamp() - self.confinement.timestamp() > interval:
                return True
        return False

    def get_confined_end_date(self):
        if self.confinement:
            end_date = self.confinement + datetime.timedelta(days=14)
            return end_date
        return False


from .signals import *