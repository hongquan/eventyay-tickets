import json
import string
from io import BytesIO

from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from pypdf import PdfReader

from pretix.base.models import LoggedModel


def bg_name(instance, filename: str) -> str:
    secret = get_random_string(length=16, allowed_chars=string.ascii_letters + string.digits)
    return 'pub/{org}/{ev}/badges/{id}-{secret}.pdf'.format(org=instance.event.organizer.slug, ev=instance.event.slug, id=instance.pk, secret=secret)


class BadgeLayout(LoggedModel):
    event = models.ForeignKey('pretixbase.Event', on_delete=models.CASCADE, related_name='badge_layouts')
    default = models.BooleanField(
        verbose_name=_('Default'),
        default=False,
    )
    name = models.CharField(max_length=190, verbose_name=_('Name'))
    layout = models.TextField(
        default='[{"type":"textarea","left":"13.09","bottom":"49.73","fontsize":"23.6","color":[0,0,0,1],'
        '"fontfamily":"Open Sans","bold":true,"italic":false,"width":"121.83","content":"attendee_name",'
        '"text":"Max Mustermann","align":"center"}]'
    )

    size = models.TextField(default='[{"width": 148, "height": 105, "orientation": "landscape"}]')

    background = models.FileField(null=True, blank=True, upload_to=bg_name, max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.background:
            buffer = BytesIO()
            for chunk in self.background.chunks():
                buffer.write(chunk)
            buffer.seek(0)
            reader = PdfReader(buffer)
            page = reader.pages[0]
            width = round(float(page.mediabox.width) * 0.352777778, 2)
            height = round(float(page.mediabox.height) * 0.352777778, 2)
            orientation = 'portrait' if height > width else 'landscape'
            self.size = json.dumps([{'width': width, 'height': height, 'orientation': orientation}])
        super().save(*args, **kwargs)


class BadgeItem(models.Model):
    # If no BadgeItem exists => use default
    # If BadgeItem exists with layout=None => don't print
    item = models.OneToOneField('pretixbase.Item', null=True, blank=True, related_name='badge_assignment', on_delete=models.CASCADE)
    layout = models.ForeignKey('BadgeLayout', on_delete=models.CASCADE, related_name='item_assignments', null=True, blank=True)

    class Meta:
        ordering = ('id',)
