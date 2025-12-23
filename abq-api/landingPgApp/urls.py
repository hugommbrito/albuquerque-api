from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path("venture/<slug:slug>/", views.venture_detail_page, name="venture_detail_page"),
    path("venture/<slug:slug>",views.venture_detail_page,name="venture_detail_page_no_slash"),
    path("venture/", views.ventures_page, name="ventures_page"),
    path("venture", views.ventures_page, name="ventures_page_no_slash"),
    path("blog/", views.BlogPage_details, name="blog_page_details"),
    path("blog", views.BlogPage_details, name="blog_page_details_no_slash"),
    path("blog/<slug:slug>/", views.BlogArticle_details, name="blog_article_detail_page"),
    path("blog/<slug:slug>", views.BlogArticle_details, name="blog_article_detail_page_no_slash"),
]
