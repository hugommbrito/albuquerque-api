from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import (
	BlogArticle,
	BlogTag,
	Venture,
	VentureAreas,
	VentureAmenities,
	VentureCategory,
	VentureFloorPlans,
	VentureHeroHighlight,
	VentureImages,
	VentureStatus,
)

class StringListWidget(forms.MultiWidget):
	def __init__(self, count=10, attrs=None):
		widgets = [forms.TextInput(attrs=attrs) for _ in range(count)]
		super().__init__(widgets, attrs)
		self.count = count

	def decompress(self, value):
		value = list(value or [])
		value.extend([''] * max(0, self.count - len(value)))
		return value[:self.count]


class StringListField(forms.MultiValueField):
	def __init__(self, count=10, *args, **kwargs):
		fields = [forms.CharField(required=False) for _ in range(count)]
		super().__init__(fields=fields, require_all_fields=False, *args, **kwargs)
		self.widget = StringListWidget(count=count)

	def compress(self, data_list):
		return [item for item in (data_list or []) if item]


class VentureImagesInline(admin.TabularInline):
	model = VentureImages
	extra = 0
	ordering = ('order',)
	fields = (
		'image',
		'preview',
		'caption',
		'is_cover',
		'is_high_light',
		'order',
		'floorPlan',
		'area',
	)
	readonly_fields = ('preview',)

	def get_formset(self, request, obj=None, **kwargs):
		formset = super().get_formset(request, obj, **kwargs)
		floor_field = formset.form.base_fields.get('floorPlan')
		area_field = formset.form.base_fields.get('area')
		if floor_field is not None:
			floor_field.queryset = (obj.floor_plans.all() if obj else VentureFloorPlans.objects.none())
		if area_field is not None:
			area_field.queryset = (obj.areas.all() if obj else VentureAreas.objects.none())
		return formset

	def preview(self, obj):
		if getattr(obj, 'image', None):
			return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image.url)
		return "(Sem imagem)"
	preview.short_description = "Pré-visualização"


class VentureAmenitiesInline(admin.TabularInline):
	model = VentureAmenities
	extra = 0
	fields = ('icon', 'value', 'span')


class VentureHeroHighlightInline(admin.TabularInline):
	model = VentureHeroHighlight
	extra = 0
	fields = ('label', 'info')


class VentureAreaInline(admin.TabularInline):
	model = VentureAreas
	extra = 0
	# fields = ('name', 'images')
	fields = ('name',)
	# raw_id_fields = ('images',)


class VentureFloorPlanInlineForm(forms.ModelForm):
	descriptionList = StringListField(count=15, required=False, help_text='Preencha até 15 itens; campos vazios serão ignorados.')

	class Meta:
		model = VentureFloorPlans
		fields = '__all__'


class VentureFloorPlanInline(admin.StackedInline):
	model = VentureFloorPlans
	form = VentureFloorPlanInlineForm
	extra = 0
	# fields = ('name', 'descriptionList', 'imgages')
	fields = ('name', 'descriptionList')
	# raw_id_fields = ('imgages')


@admin.register(Venture)
class VentureAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'status', 'category', 'is_last_units', 'created_at')
	list_filter = ('status', 'category', 'is_last_units')
	search_fields = ('name', 'slug', 'short_description', 'location')
	prepopulated_fields = {'slug': ('name',)}
	inlines = [
		VentureHeroHighlightInline,
		VentureAmenitiesInline,
		VentureFloorPlanInline,
		VentureAreaInline,
		VentureImagesInline,
	]
	readonly_fields = ('created_at', 'updated_at')
	fieldsets = (
		(None, {
			'fields': (
				'name',
				'slug',
				'short_description',
				'location',
				'total_units',
				'is_last_units',
				'yt_video_id',
				'status',
				'category',
			)
		}),
		('Controle', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
	)


@admin.register(VentureStatus)
class VentureStatusAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	search_fields = ('name',)
	readonly_fields = ('created_at', 'updated_at')

@admin.register(VentureCategory)
class VentureCategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'created_at', 'updated_at')
  readonly_fields = ('created_at', 'updated_at')

@admin.register(VentureImages)
class VentureImagesAdmin(admin.ModelAdmin):
	list_display = ('id', 'venture', 'caption', 'is_cover', 'is_high_light', 'order', 'preview')
	list_filter = ('is_cover', 'is_high_light', 'venture', 'area', 'floorPlan')
	search_fields = ('caption', 'venture__name')
	readonly_fields = ('preview',)
	list_editable = ('is_cover', 'is_high_light', 'order')
	

	def preview(self, obj):
		if getattr(obj, 'image', None):
			return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.image.url)
		return "(Sem imagem)"
	preview.short_description = "Pré-visualização"

@admin.register(BlogArticle)
class BlogArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'title', 'tag', 'is_highlight', 'is_active', 'created_at')
	list_filter = ('is_active', 'is_highlight', 'tag')
	search_fields = ('title', 'slug', 'content')
	prepopulated_fields = {'slug': ('title',)}
	readonly_fields = ('preview', 'created_at', 'updated_at')
	fieldsets = (
			(None, {
					'fields': (
							'title',
							'slug',
							'short_description',
							'tag',
							'cover_image',
							'preview',
							'is_highlight',
							'is_active',
							'content',
					)
			}),
			('Controle', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
	)

	def preview(self, obj):
		if getattr(obj, 'cover_image', None):
			return format_html('<img src="{}" style="max-height: 200px; max-width: 200px;" />', obj.cover_image.url)
		return "(Sem imagem)"
	preview.short_description = "Pré-visualização"


@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'created_at', 'updated_at')
	search_fields = ('name',)
	readonly_fields = ('created_at', 'updated_at')