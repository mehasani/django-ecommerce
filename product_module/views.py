from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from site_module.models import AdsBanner
from utils.user_auth import LoggedinUser
from utils.http_service import get_client_ip
from utils.convertors import group_list
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductFavorite


# Create your views here.


class ProductListView(ListView):
    template_name = 'product_module/product_list_page.html'
    model = Product
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        request: HttpRequest = self.request
        products = Product.objects.all()
        product: Product = products.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = request.GET.get('start_price') or 0
        context['end_price'] = request.GET.get('end_price') or db_max_price
        context['banners'] = AdsBanner.objects.filter(is_active=True,
                                                       position__iexact=AdsBanner.AdsBannerPositions.product_list)

        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        request: HttpRequest = self.request
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')

        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)

        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        return query


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        user_ip = get_client_ip(request)
        user_id = None
        loggedin_user = LoggedinUser(request)
        if loggedin_user:
            user_id = loggedin_user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()
        favorite_product_id = request.session.get("product_favorite")
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['related_products'] = group_list(
            list(Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12]), 3)
        context['product_galleries'] = group_list(galleries, 3)
        context["is_favorite"] = favorite_product_id == str(loaded_product.id)
        context['banners'] = AdsBanner.objects.filter(is_active=True,
                                                       position__iexact=AdsBanner.AdsBannerPositions.product_detail)
        return context


def add_product_to_favorite(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    user = LoggedinUser(request)

    if user:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            product_favorite, created = ProductFavorite.objects.get_or_create(product_id=product_id, user_id=user.id)
            if created:
                return JsonResponse({
                    'status': 'success',
                    'text': 'این کالا با موفقیت به لیست کالا های مورد علاقه شما افزوده شد',
                })
            else:
                return JsonResponse({
                    'status': 'exists',
                    'text': 'این کالا در لیست کالا های مورد علاقه شما وجود دارد',
                })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد لیست کالا های مورد علاقه لطفا ابتدا وارد حساب کاربری خود شوید',
        })


def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request: HttpRequest):
    product_brands = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brands
    }
    return render(request, 'product_module/components/product_brands_component.html', context)
