# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ProcessedImageField
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Category(MPTTModel):
    # Kategori adı
    title = models.CharField(max_length=500,null=True,unique=True,
                                     verbose_name="Kategori Adı",help_text="Kategori adını belirleyin.")
    # Kategori keywords
    tags = models.CharField(max_length=500,null=True,
                                         verbose_name="Anahtar Kelimeler",help_text="virgül (,) ile ayırarak belirtin.")
    # Kategori açıklama
    description = models.CharField(max_length=500,null=True,
                                   verbose_name="Açıklama",help_text="Kategori hakkında kısa açıklama belirtin.")

    # Kategori fa-fa icon
    icon = models.CharField(max_length=100,null=True,help_text='fa-fa icon',verbose_name="Icon")

    #Alt kategori :
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,
                            verbose_name="Alt Kategori",help_text="Alt kategori belirleyebilirsiniz.")

    # Kategori slug url oluşturma.
    url = models.CharField(max_length=500,null=True, blank=True)

    #Öne çıkan görsel
    image =  ProcessedImageField(upload_to='uploads/category/img',options={'quality': 30})

    class Meta:
        verbose_name_plural = "Kategoriler"
        ordering = ('title',)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        #dönüş değeri
        return self.title


    def save(self, *args, **kwargs):
        self.url = slugify(self.title, allow_unicode=False)
        super(Category, self).save(*args, **kwargs)

class Post(models.Model):
    #Makale başlığı
    title = models.CharField(max_length=500, null=True, unique=True,
                             verbose_name="Başlık",help_text="İçerik başlığı")
    #İçerik tarihi
    time = models.DateTimeField(auto_now=False, null=True,
                                verbose_name="Zaman",help_text="İçerik zamanı")
    #İçerik
    content = RichTextUploadingField(verbose_name="İçerik",help_text="İçeriğiniz")
    #İçerik Anahtarı
    keywords = models.CharField(max_length=500, null=True,
                                verbose_name="Anahtar Kelime",help_text="İçerik anahtarlarınız.")
    #açıklama
    description = models.TextField(null=True,verbose_name="Açıklama",help_text="description")
    #öne çıkan görsel
    image = ProcessedImageField(upload_to='uploads/blog/img',
                                           processors=[ResizeToFill(300, 350)],
                                           format='JPEG',
                                           options={'quality': 50},verbose_name="Resim",help_text="Öne çıkan görseli oluşturur.")
    #kategoriler
    category_list = TreeForeignKey(Category, null=True, blank=True, db_index=True,verbose_name="Kategoriler")
    #url
    seo_url = models.CharField(max_length=500, null=True, blank=True, verbose_name='Seo_URL : (Otomatik doldurur)')
    #yayınlama durumu
    is_active = models.BooleanField(default=False,verbose_name="Yayınla",help_text="Aktif olursa içerik yayınlanır.")

    class Meta:
        verbose_name_plural = "İçerik Yaz"
        ordering = ('title',)

    def __str__(self):
        return 'Başlık : {}'.format(self.title)

    def save(self, *args, **kwargs):
        self.seo_url = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


