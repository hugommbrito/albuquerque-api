import json
import pprint
from django.shortcuts import render, get_object_or_404, get_list_or_404

from django.http import HttpResponse, Http404

from .models import Venture
from .models import VentureImages

# from .models import Question

# def index(request):
#   latest_question_list = Question.objects.order_by('-pub_date')[:5]
#   output = ', '.join([q.question_text for q in latest_question_list])
#   return HttpResponse("Latest questions are: %s" % output)

# def detail(request, question_id):
#   question = get_object_or_404(Question, pk=question_id)
#   return HttpResponse("You're looking at question %s." % question_id)

# def results(request, question_id):
#   response = "You're looking at the results of question %s."
#   return HttpResponse(response % question_id)

# def vote(request, question_id):
#   return HttpResponse("You're voting on question %s." % question_id)

def venture_detail_page(request, slug):
  venture = get_object_or_404(Venture, slug=slug)

  venturePageInfo = {
    'slug': venture.slug,
    'name': venture.name,
    'subtitle': venture.short_description,
    'heroImage': venture.images.filter(is_cover=True).first().image.url,
    'heroHighLights': [
      {
        'label': h.label,
        'info': h.info
      } for h in venture.hero_highlights.all()
    ],
    'breadcrumb': [
      {
        'label': 'Empreendimentos',
        'url': '/nossas-obras/'
      },
      {
        'label': venture.name,
        'url': f'/nossas-obras/{venture.slug}/'
      }
    ],
    'location': venture.location,
    'status': venture.status.name if venture.status else None,
    'lastUnits': venture.is_last_units,
    'amenities': [
        {
          'label': amenity.icon,
          'value': amenity.value,
          'span': amenity.span
        } for amenity in venture.amenities.all()
    ],
    'floorPlans': [
      {
        'id': fp.id,
        'name': fp.name,
        'images': [
          {
            'is_highlight': img.is_high_light,
            'url': img.image.url,
            'unit': img.floorPlan.name if img.floorPlan else None,
            'area': img.area.name if img.area else None,
          } for img in fp.images.all()
        ]
      } for fp in venture.floor_plans.all()
    ],
    'areas': [
      area.name for area in venture.areas.all()
    ],
    'ytVideoId': venture.yt_video_id if venture.yt_video_id else None,


  }

  return HttpResponse(json.dumps(venturePageInfo), content_type="application/json")