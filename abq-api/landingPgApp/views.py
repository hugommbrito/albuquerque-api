import json
import os
from django.conf import settings

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from .models import BlogArticle, Venture, VentureCategory
from .forms import EmailMessageForm


def Ventures_page(request):
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


def Venture_detail_page(request, slug):
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
        "unitsCount": venture.total_units,
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


def BlogPage_details(request):
    blogArticles = BlogArticle.objects.filter(is_active=True).order_by("-created_at")
    data = {"highlighted_articles": [], "regular_articles": []}

    for article in blogArticles:
        articleData = {
            "id": article.id,
            "title": article.title,
            "slug": article.slug,
            "tag": article.tag.name if article.tag else None,
            "short_description": article.short_description,
            "cover_image_url": article.cover_image.url if article.cover_image else None,
            # "content": article.content,
            "created_at": (
                article.created_at.isoformat() if article.created_at else None
            ),
        }
        if article.is_highlight:
            data["highlighted_articles"].append(articleData)
        else:
            data["regular_articles"].append(articleData)

    return JsonResponse(data)


def BlogArticle_details(request, slug):
    article = get_object_or_404(BlogArticle, slug=slug, is_active=True)
    suggested_articles = (
        BlogArticle.objects.filter(is_active=True)
        .exclude(id=article.id)
        .order_by("?")[:3]
    )

    response = {"article": {}, "suggested_articles": []}
    response["article"] = {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "tag": article.tag.name if article.tag else None,
        "short_description": article.short_description,
        "cover_image_url": article.cover_image.url if article.cover_image else None,
        "content": article.content,
        "created_at": article.created_at.isoformat() if article.created_at else None,
    }
    response["suggested_articles"] = [
        {
            "id": suggested.id,
            "title": suggested.title,
            "slug": suggested.slug,
            "short_description": suggested.short_description,
            "cover_image_url": (
                suggested.cover_image.url if suggested.cover_image else None
            ),
        }
        for suggested in suggested_articles
    ]

    return JsonResponse(response)


def Home_page_info(request):
    home_page_ventures = Venture.objects.filter(
        homepage_highlight=True, is_active=True
    ).order_by("-created_at")
    home_page_articles = BlogArticle.objects.filter(is_active=True).order_by(
        "-created_at"
    )[:3]
    data = {
        "home_page_ventures": [
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
            for venture in home_page_ventures
        ],
        "home_page_articles": [
            {
                "id": article.id,
                "title": article.title,
                "slug": article.slug,
                "short_description": article.short_description,
                "cover_image_url": (
                    article.cover_image.url if article.cover_image else None
                ),
            }
            for article in home_page_articles
        ],
    }
    return JsonResponse(data)


@csrf_exempt
def send_message_email(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        form = EmailMessageForm(data)
        if form.is_valid():
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"[CONTATO VIA SITE] Mensagem de {name}",
                message=f"Nome: {name}\nTelefone: {phone}\nMensagem: {message}",
                from_email=settings.EMAIL_HOST_USER or None,
                recipient_list=["eu@hugobrito.dev.br", "caue@albuquerqueengenharia.net"],
            )

            return JsonResponse({"success": "Message sent successfully"})
        else:
            return JsonResponse(
                {"error": "Invalid form data", "details": form.errors}, status=400
            )

    return JsonResponse(
        {"error": "Invalid request method, this endpoint only accepts POST requests"},
        status=405,
    )
