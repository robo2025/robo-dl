from django.db import models
from django.utils import timezone


# Create your dl_models here.

class WeldingImage(models.Model):
    url = models.URLField(verbose_name='图片url', help_text='图片url', default='')
    predict_label = models.TextField(null=True, blank=True, verbose_name='预测结果')
    has_welding = models.IntegerField(null=True, blank=True, verbose_name='是否有焊缝')
    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '焊接图片'
        verbose_name_plural = verbose_name
        db_table = 'welding_image'

    def __str__(self):
        return self.url
