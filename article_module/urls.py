from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles_list'),
    path('article-list-ajax', views.ArticleListAPIView.as_view()),
    path('categories-article-list/<str:category>', views.CategoriesArticleAPIView.as_view()),
    path('cat/<str:category>', views.ArticleListView.as_view(), name='articles_by_category_list'),
    path('<pk>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('add-article-comment', views.add_article_comment,name='add_article_comment')
]
