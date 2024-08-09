from typing import Iterable
from django.db import models

# Create your models here.
class ImageContent(models.Model):
    class Meta:
        verbose_name = 'imágen'
        verbose_name_plural = 'imágenes'
    image = models.ImageField(verbose_name='imágen')
    thumb = models.ImageField(verbose_name='miniatura', default=None, null=True, blank=True)

    def save(self, force_insert: bool = False, force_update: bool = False, using: str | None = None, update_fields: Iterable[str] | None = None) -> None:
        from PIL import Image as PImg
        from django.core.files import File
        from io import BytesIO
        creating = update_fields is None
        updating = update_fields is not None and "image" in update_fields
        if creating or updating:
            origin: PImg.Image  = PImg.open(self.image.file).convert("RGBA")
            thumbnail           = PImg.new("RGB", origin.size, (255, 255, 255))
            thumbnail.paste(origin, mask=origin)
            thumbnail.thumbnail(size=[128, 128])
            bIO2 = BytesIO(); thumbnail.save(bIO2, 'JPEG', optimize=True)
            self.thumb.save(f'thumb_{str(self.image.file.name).replace(".", "")}.jpg', File(bIO2, f'thb.jpg'), save=False)
            if updating:
                {"thumbnail"}.union(update_fields)
        super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

class QueryGroup(models.Model):
    class Meta:
        verbose_name = 'lote de solicitudes'
        verbose_name_plural = 'lotes de solicitudes'
    types = { 40: '4cm x 4cm', 50: '5cm x 5cm', 70: '7cm x 7cm', }
    maxes = { 40: 30, 50: 20, 70: 12 }
    type = models.IntegerField(verbose_name='tipo de impresion', choices=types)
    printed = models.BooleanField(verbose_name='lote impreso', default=False)
    imagelist = models.ManyToManyField(to=ImageContent, blank=True,
                                       through='QueryImageRelation',
                                       through_fields=('querygroup','imagecontent'),)
    def get_max(self) -> int:
        return self.maxes[self.type]
    def get_type_str(self) -> str:
        return f'{self.types[self.type]}'
    def get_state_str(self) -> str:
        if self.printed:
            return 'impreso'
        el = self.imagelist.count()
        if el == 0:
            return 'vacio'
        if el < self.get_max():
            return 'en proceso'
        return 'listo'

class QueryImageRelation(models.Model):
    querygroup = models.ForeignKey(to=QueryGroup, on_delete=models.CASCADE)
    imagecontent = models.ForeignKey(to=ImageContent, on_delete=models.CASCADE)