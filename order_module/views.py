import time
from datetime import datetime

from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import redirect

from product_module.models import Product
from utils.user_auth import LoggedinUser, user_login_required
from .models import Order, OrderDetail


# Create your views here.

def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    user = LoggedinUser(request)

    if count < 1:
        return JsonResponse({
            'status': 'invalid_count',
            'text': 'مقدار وارد شده معتبر نمی باشد',
        })
    if user:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
                return JsonResponse({
                    'status': 'exists',
                    'text': 'کالای مورد نظر در سبد خرید شما موجود بود و به تعداد ان افزوده شد',
                })
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()
                return JsonResponse({
                    'status': 'success',
                    'text': 'کالای مورد نظر با موفقیت به سبد خرید شما افزوده شد',
                })
        else:
            return JsonResponse({
                'status': 'not_found',
                'text': 'محصول مورد نظر یافت نشد',
            })
    else:
        return JsonResponse({
            'status': 'not_auth',
            'text': 'برای افزودن محصول به سبد خرید لطفا ابتدا وارد حساب کاربری خود شوید',
        })


@user_login_required
def payment_basket(request: HttpRequest):
    user = LoggedinUser(request)
    current_order = Order.objects.prefetch_related('orderdetail_set').filter(is_paid=False, user_id=user.id).first()
    # order_detail = current_order.orderdetail_set.all
    # order_detaill = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=user.id).first()
    total_price = current_order.calculate_total_price()
    if total_price == 0:
        return redirect('user_basket_page')

    for order_detail in current_order.orderdetail_set.all():
        order_detail.final_price = order_detail.product.price
        order_detail.save()

    current_order.is_paid = True
    current_order.payment_date = datetime.now()
    current_order.save()

    return redirect('user_panel_dashboard_page')
