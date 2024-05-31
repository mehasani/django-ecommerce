from django.db.models import Count, Sum
from django.views.generic.base import TemplateView

from home_module.models import Slider
from product_module.models import Product, ProductCategory

# Create your views here.
from site_module.models import SiteSetting
from utils.convertors import group_list


class HomeView(TemplateView):
    template_name = "home_module/index_page.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(
            is_main_setting=True
        ).first()
        sliders: Slider = Slider.objects.filter(is_active=True)
        latest_products = Product.objects.filter(
            is_active=True, is_delete=False
        ).order_by("-id")[:4]
        most_visit_products = (
            Product.objects.filter(is_active=True, is_delete=False)
            .annotate(visit_count=Count("productvisit"))
            .order_by("-visit_count")[:12]
        )
        categories = list(
            ProductCategory.objects.annotate(
                products_count=Count("products_category")
            ).filter(is_active=True, is_delete=False, products_category__gt=0)[:6]
        )
        categories_products = []
        for category in categories:
            item = {
                "id": category.id,
                "title": category.title,
                "products": list(category.products_category.all()[:4]),
            }
            categories_products.append(item)
        most_bought_products = (
            Product.objects.filter(orderdetail__order__is_paid=True)
            .annotate(order_count=Sum("orderdetail__count"))
            .order_by("-order_count")[:12]
        )

        context["latest_products"] = group_list(latest_products)
        context["most_bought_products"] = group_list(most_bought_products)
        context["most_visit_products"] = group_list(most_visit_products)
        context["categories_products"] = categories_products
        context["site_setting"] = site_setting
        context["sliders"] = sliders

        return context


class AboutView(TemplateView):
    template_name = "home_module/about_page.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(
            is_main_setting=True
        ).first()
        context["site_setting"] = site_setting
        return context
