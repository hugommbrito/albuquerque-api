import datetime
import os

from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import admin
from django.contrib.postgres.fields import ArrayField

from storages.backends.s3boto3 import S3Boto3Storage

from django_ckeditor_5.fields import CKEditor5Field


def venture_image_upload_to(instance, filename):
  folder = 'venture_images'
  _, ext = os.path.splitext(filename)
  ext = (ext or '').lower() or '.img'

  venture = getattr(instance, 'venture', None)
  if venture is not None:
    venture_id = getattr(venture, 'id', 'noid')
    venture_slug = slugify(getattr(venture, 'name', 'venture'))
    prefix = f"{venture_id}-{venture_slug}"
  else:
    prefix = 'item'

  timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
  suffix = instance.pk or 'new'

  return f"{folder}/{prefix}/{timestamp}_{suffix}{ext}"

def site_image_upload_to(instance, filename):  
  folder = 'site_images'
  _, ext = os.path.splitext(filename)
  ext = (ext or '').lower() or '.img'

  page = getattr(instance, 'page', None)
  if page:
    prefix = slugify(page)
  else:
    prefix = 'general'

  timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
  suffix = instance.pk or 'new'

  return f"{folder}/{prefix}/{timestamp}_{suffix}{ext}"

def blog_article_image_upload_to(instance, filename):
  folder = 'blog_articles'
  _, ext = os.path.splitext(filename)
  ext = (ext or '').lower() or '.img'

  article = getattr(instance, 'article', None)
  if article is not None:
    article_id = getattr(article, 'id', 'noid')
    article_slug = slugify(getattr(article, 'title', 'article'))
    prefix = f"{article_id}-{article_slug}"
  else:
    prefix = 'item'

  timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
  suffix = instance.pk or 'new'

  return f"{folder}/{prefix}/{timestamp}_{suffix}{ext}"

class VentureStatus(models.Model):
  name = models.CharField(max_length=50, verbose_name="Nome")
  order = models.PositiveIntegerField(default=0, verbose_name="Ordem")
  is_visible = models.BooleanField(default=True, verbose_name="Visível?")

  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

  class Meta:
    verbose_name = "Status do Empreendimento"
    verbose_name_plural = "Status dos Empreendimentos"
    ordering = ['order', 'name']

  def __str__(self):
    return self.name
  
  
class VentureCategory(models.Model):
  name = models.CharField(max_length=50)

  # venture = models.ForeignKey('Venture', on_delete=models.CASCADE, related_name='categories', null=True, blank=True)
  # TODO: Remover imagens da categoria
  # images = models.ForeignKey('VentureImages', on_delete=models.CASCADE, null=True, blank=True)

  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

  class Meta:
    verbose_name = "Categoria do Empreendimento"
    verbose_name_plural = "Categorias dos Empreendimentos"

  def __str__(self):
    return self.name

class VentureHeroHighlight(models.Model):
  label = models.CharField(max_length=50, verbose_name="Rótulo")
  info = models.CharField(max_length=50, verbose_name="Informação")

  venture = models.ForeignKey('Venture', on_delete=models.CASCADE, related_name='hero_highlights')

  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

  class Meta:
    verbose_name = "Destaque do Banner do Empreendimento"
    verbose_name_plural = "Destaques do Banner dos Empreendimentos"

  def __str__(self):
    return self.label

class VentureAmenities(models.Model):
  icon = models.CharField(max_length=50, verbose_name="Icone")
  value = models.CharField(max_length=100, verbose_name="Valor")
  span = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(10)], verbose_name="Espaços")

  venture = models.ForeignKey('Venture', on_delete=models.CASCADE, related_name='amenities')

  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

  class Meta:
    verbose_name = "Comodidade do Empreendimento"
    verbose_name_plural = "Comodidades do Empreendimento"

  def __str__(self):
    return self.icon

class VentureFloorPlans(models.Model):
  name = models.CharField(max_length=50)
  descriptionList = ArrayField(base_field=models.CharField(max_length=100), size=15, blank=True, default=list)

  # imgages = models.ForeignKey('VentureImages', on_delete=models.CASCADE)
  venture = models.ForeignKey('Venture', on_delete=models.CASCADE, related_name='floor_plans')

  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

  class Meta:
    verbose_name = "Planta do Empreendimento"
    verbose_name_plural = "Plantas do Empreendimento"
  
  def __str__(self):
    return f'{self.venture} - {self.name}'

class VentureAreas(models.Model):
  name = models.CharField(max_length=50)

  venture = models.ForeignKey('Venture', on_delete=models.CASCADE, related_name='areas')
  # images = models.ForeignKey('VentureImages', on_delete=models.CASCADE)

  created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
  updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

  class Meta:
    verbose_name = "Área do Empreendimento"
    verbose_name_plural = "Áreas do Empreendimento"

  def __str__(self):
    return f'{self.venture} - {self.name}'

class Venture(models.Model):
  slug = models.SlugField(unique=True)
  name = models.CharField(max_length=100, verbose_name="Nome")
  short_description = models.CharField(max_length=100, verbose_name="Descrição Curta")
  location = models.CharField(max_length=50, verbose_name='Localização')
  total_units = models.PositiveIntegerField(blank=True, verbose_name='Total de Unidades')
  is_last_units = models.BooleanField(default=False, verbose_name='Últimas Unidades?')
  homepage_highlight = models.BooleanField(default=False, verbose_name="Destaque na Página Inicial?")
  is_visible = models.BooleanField(default=True, verbose_name="Visível?")
  yt_video_id = models.CharField(max_length=50, blank=True, verbose_name="ID do Vídeo do YouTube")
  order = models.PositiveIntegerField(default=0, verbose_name="Ordem")

  status = models.ForeignKey(VentureStatus, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventures')
  category = models.ForeignKey(VentureCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventures')

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Empreendimento"
    verbose_name_plural = "..Empreendimentos"
    ordering = ['order', 'name']


  def __str__(self):
    return self.name
  
class VentureImages(models.Model):
  venture = models.ForeignKey(Venture, on_delete=models.CASCADE, related_name='images', verbose_name="Empreendimento")
  image = models.ImageField(storage=S3Boto3Storage(), upload_to=venture_image_upload_to, verbose_name="Imagem")
  caption = models.CharField(max_length=200, blank=True, verbose_name="Legenda")
  is_cover = models.BooleanField(default=False, verbose_name="Imagem de Capa")
  is_high_light = models.BooleanField(default=False, verbose_name="Imagem destacada")
  order = models.PositiveIntegerField(default=1, verbose_name="Ordem")
  is_active = models.BooleanField(default=True, verbose_name="Imagem Ativa?")

  floorPlan = models.ForeignKey(VentureFloorPlans, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')
  area = models.ForeignKey(VentureAreas, on_delete=models.SET_NULL, null=True, blank=True, related_name='images')

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)



  def save(self, *args, **kwargs):
      # Ensure only one cover image per venture
      if self.is_cover:
          VentureImages.objects.filter(venture=self.venture, is_cover=True).exclude(pk=self.pk).update(is_cover=False)

      # Auto-assign next order within the same venture when not provided
      if not self.pk and (self.order is None or self.order == 0):
          max_order = (
              VentureImages.objects
              .filter(venture=self.venture)
              .aggregate(models.Max('order'))
              .get('order__max')
          ) or 0
          self.order = max_order + 1

      # If another image in the same venture already has this order, shift subsequent ones
      if VentureImages.objects.filter(venture=self.venture, order=self.order).exclude(pk=self.pk).exists():
          to_reorder = VentureImages.objects.filter(venture=self.venture, order__gte=self.order).exclude(pk=self.pk).order_by('-order')
          for item in to_reorder:
              item.order = (item.order or 0) + 1
              super(VentureImages, item).save(update_fields=['order'])

      super().save(*args, **kwargs)


  class Meta:
    verbose_name = "Imagem do Empreendimento"
    verbose_name_plural = "Imagens dos Empreendimentos"

  def __str__(self):
     return self.image.name
  
class SiteImages(models.Model):
  class SitePage(models.TextChoices):
    HOME = "home", "Home"
    VENTURES = "ventures", "Nossas Obras"
    ABOUT_US = "about_us", "Nossa História"
    YOUR_DREAMS = "your_dreams", "Seus Sonhos"
    BLOG = "blog", "Blog"

  image = models.ImageField(storage=S3Boto3Storage(), upload_to=site_image_upload_to, verbose_name="Imagem")
  description = models.CharField(max_length=200, blank=True, verbose_name="Descrição")
  page = models.CharField(
    max_length=30,
    choices=SitePage.choices,
    default=SitePage.HOME,
    db_index=True,
    verbose_name="Página do Site",
  )
  is_active = models.BooleanField(default=True, verbose_name="Imagem Ativa?")
  is_desktop = models.BooleanField(default=True, verbose_name="Imagem para Desktop?")
  is_mobile = models.BooleanField(default=False, verbose_name="Imagem para Mobile?")
  
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
      # Imagem sem ambiente definido deve ser inativa
      if not self.is_desktop and not self.is_mobile:
          self.is_active = False

      if self.is_active:
          # Garante apenas uma imagem ativa por ambiente (desktop/mobile) por página
          if self.is_desktop:
              SiteImages.objects.filter(page=self.page, is_active=True, is_desktop=True).exclude(pk=self.pk).update(is_desktop=False)
          if self.is_mobile:
              SiteImages.objects.filter(page=self.page, is_active=True, is_mobile=True).exclude(pk=self.pk).update(is_mobile=False)

      super().save(*args, **kwargs)

  class Meta:
    verbose_name = "Imagem do Site"
    verbose_name_plural = "..Imagens do Site"

  def __str__(self):
     return f"{self.get_page_display()} - {self.image.name}"
  

class BlogArticle(models.Model):
  title = models.CharField(max_length=200, verbose_name="Título")
  short_description = models.CharField(max_length=300, verbose_name="Descrição Curta")
  content = CKEditor5Field('Content', config_name='extends')
  slug = models.SlugField(unique=True, verbose_name="Slug")
  tag = models.ForeignKey('BlogTag', on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', verbose_name="Tag")
  cover_image = models.ImageField(storage=S3Boto3Storage(), upload_to=blog_article_image_upload_to, verbose_name="Imagem da Capa", null=True, blank=True)
  is_highlight = models.BooleanField(default=False, verbose_name="Artigo em Destaque?")
  is_active = models.BooleanField(default=True, verbose_name="Artigo Ativo?")

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Artigo do Blog"
    verbose_name_plural = "..Artigos do Blog"

  def __str__(self):
    return self.title
  
class BlogTag(models.Model):
  name = models.CharField(max_length=50, verbose_name="Nome")

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Tag do Blog"
    verbose_name_plural = "Tags do Blog"

  def __str__(self):
    return self.name
  
class InstructionalVideo(models.Model):
  title = models.CharField(max_length=200, verbose_name="Título")
  video_url = models.URLField(max_length=500, verbose_name="URL do Vídeo")
  cover_image = models.ImageField(storage=S3Boto3Storage(), upload_to=blog_article_image_upload_to, verbose_name="Imagem da Capa", null=True, blank=True)
  is_active = models.BooleanField(default=True, verbose_name="Vídeo Ativo?")

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = "Vídeo Instrucional"
    verbose_name_plural = "..Vídeos Instrucionais"

  def __str__(self):
    return self.title


class Ebook(models.Model):
  title = models.CharField(max_length=200, verbose_name="Título")
  file = models.FileField(storage=S3Boto3Storage(), upload_to="ebooks/", verbose_name="Arquivo PDF")
  is_active = models.BooleanField(default=True, verbose_name="Ativo?")

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def save(self, *args, **kwargs):
      # Garante apenas um ebook ativo por vez
      if self.is_active:
          Ebook.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
      super().save(*args, **kwargs)

  class Meta:
    verbose_name = "Ebook"
    verbose_name_plural = "Ebooks"

  def __str__(self):
    return self.title
