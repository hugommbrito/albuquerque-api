from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import Venture, VentureCategory


def ventures_page(request):
    ventures = Venture.objects.filter(is_active=True)
    categories = VentureCategory.objects.filter(ventures__in=ventures).distinct()

    data = {
        "categories": [
            {
                "id": category.id,
                "name": category.name,
                "ventures": [
                    {
                        "id": venture.id,
                        "name": venture.name,
                        "slug": venture.slug,
                        "short_description": venture.short_description,
                        "location": venture.location,
                        "status": venture.status.name if venture.status else None,
                        "total_units": venture.total_units,
                        "hero_image_url": (
                            image.image.url
                            if (image := venture.images.filter(is_cover=True).first())
                            else None
                        ),
                    }
                    for venture in ventures.filter(category=category)
                ],
            }
            for category in categories
        ],
    }

    return JsonResponse(data)


def venture_detail_page(request, slug):
    venture = get_object_or_404(Venture, slug=slug)

    venturePageInfo = {
        "slug": venture.slug,
        "name": venture.name,
        "subtitle": venture.short_description,
        "heroImage": venture.images.filter(is_cover=True).first().image.url,
        "heroHighLights": [
            {"label": h.label, "info": h.info} for h in venture.hero_highlights.all()
        ],
        "breadcrumb": [
            {"label": "Empreendimentos", "url": "/nossas-obras/"},
            {"label": venture.name, "url": f"/nossas-obras/{venture.slug}/"},
        ],
        "location": venture.location,
        "status": venture.status.name if venture.status else None,
        "lastUnits": venture.is_last_units,
        "amenities": [
            {"label": amenity.icon, "value": amenity.value, "span": amenity.span}
            for amenity in venture.amenities.all()
        ],
        "floorPlans": [
            {
                "id": fp.id,
                "name": fp.name,
                "descriptionList": fp.descriptionList,
                "images": [
                    {
                        "is_highlight": img.is_high_light,
                        "url": img.image.url,
                        "unit": img.floorPlan.name if img.floorPlan else None,
                        "area": img.area.name if img.area else None,
                    }
                    for img in fp.images.all()
                ],
            }
            for fp in venture.floor_plans.all()
        ],
        "areas": [area.name for area in venture.areas.all()],
        "ytVideoId": venture.yt_video_id if venture.yt_video_id else None,
        "galeries": {
            "highlighted": [
                {
                    "is_highlight": img.is_high_light,
                    "url": img.image.url,
                    "unit": img.floorPlan.name if img.floorPlan else None,
                    "area": img.area.name if img.area else None,
                }
                for img in venture.images.filter(is_high_light=True)
            ],
            "units": [
                {
                    "id": fp.id,
                    "name": fp.name,
                    "images": [
                        {
                            "is_highlight": img.is_high_light,
                            "url": img.image.url,
                            "unit": img.floorPlan.name if img.floorPlan else None,
                            "area": img.area.name if img.area else None,
                        }
                        for img in fp.images.all()
                    ],
                }
                for fp in venture.floor_plans.all()
            ],
            "areas": [
                {
                    "id": area.id,
                    "name": area.name,
                    "images": [
                        {
                            "is_highlight": img.is_high_light,
                            "url": img.image.url,
                            "unit": img.floorPlan.name if img.floorPlan else None,
                            "area": img.area.name if img.area else None,
                        }
                        for img in area.images.all()
                    ],
                }
                for area in venture.areas.all()
            ],
        },
    }

    return JsonResponse(venturePageInfo)
