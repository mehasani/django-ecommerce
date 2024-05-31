from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.list import ListView

from utils.user_auth import LoggedinUser

from .models import Article, ArticleCategory, ArticleComment


class ArticleListView(ListView):
    model = Article
    paginate_by = 1
    template_name = "article_module/articles_page.html"

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        category_name = self.kwargs.get("category")
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_module/article_detail_page.html"

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        request = self.request
        loggedin_user = LoggedinUser(request)
        article: Article = kwargs.get("object")
        context["comments"] = (
            ArticleComment.objects.filter(
                article_id=article.id, show_comment=True, parent=None
            )
            .order_by("-create_date")
            .prefetch_related("articlecomment_set")
        )
        context["loggedin_user"] = loggedin_user
        context["comments_count"] = ArticleComment.objects.filter(
            article_id=article.id
        ).count()

        return context


def article_categories_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related(
        "articlecategory_set"
    ).filter(is_active=True, parent_id=None)
    context = {"main_categories": article_main_categories}
    return render(
        request, "article_module/components/article_categories_component.html", context
    )


def add_article_comment(request: HttpRequest):
    loggedin_user = LoggedinUser(request)
    if loggedin_user:
        if request.method == "POST":
            article_id = request.POST["article_id"]
            article_comment = request.POST["article_comment"]
            parent_id = request.POST["parent_id"]
            new_comment = ArticleComment(
                article_id=article_id,
                text=article_comment,
                user_id=loggedin_user.id,
                parent_id=parent_id,
            )
            new_comment.save()
            return HttpResponse("request.POST")
        else:
            return HttpResponse("method is not post")
    else:
        return HttpResponse("user is not login")
