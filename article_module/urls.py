from django.urls import path

from . import views

urlpatterns = [
    path("", views.ArticleListView.as_view(), name="articles_list"),
    path(
        "cat/<str:category>",
        views.ArticleListView.as_view(),
        name="articles_by_category_list",
    ),
    path("<pk>/", views.ArticleDetailView.as_view(), name="article-detail"),
    path("add-article-comment", views.add_article_comment, name="add_article_comment"),
]
