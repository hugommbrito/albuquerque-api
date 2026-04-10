from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
    path("venture/<slug:slug>/", views.Venture_detail_page, name="venture_detail_page"),
    path("venture/<slug:slug>",views.Venture_detail_page,name="venture_detail_page_no_slash"),
    path("venture/", views.Ventures_page, name="ventures_page"),
    path("venture", views.Ventures_page, name="ventures_page_no_slash"),
    path("blog/", views.BlogPage_details, name="blog_page_details"),
    path("blog", views.BlogPage_details, name="blog_page_details_no_slash"),
    path("blog/<slug:slug>/", views.BlogArticle_details, name="blog_article_detail_page"),
    path("blog/<slug:slug>", views.BlogArticle_details, name="blog_article_detail_page_no_slash"),
    path("home-page-info/", views.Home_page_info, name="home_page_info"),
    path("home-page-info", views.Home_page_info, name="home_page_info_no_slash"),
    path("about-us/", views.About_us_page, name="about_us_page"),
    path("about-us", views.About_us_page, name="about_us_page_no_slash"),
    path("your-dreams/", views.Your_dreams_page, name="your_dreams_page"),
    path("your-dreams", views.Your_dreams_page, name="your_dreams_page_no_slash"),
    path("send-email/", views.send_message_email, name="send_email"),
    path("send-email", views.send_message_email, name="send_email_no_slash"),
    path("service-solicitation/", views.service_solicitation_term, name="service_solicitation_term"),
    path("service-solicitation", views.service_solicitation_term, name="service_solicitation_term_no_slash"),
    path("send-service-solicitation/", views.send_service_solicitation_email, name="send_service_solicitation_email"),
    path("send-service-solicitation", views.send_service_solicitation_email, name="send_service_solicitation_email_no_slash"),
]
