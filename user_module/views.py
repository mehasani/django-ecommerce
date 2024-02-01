from django.http import HttpRequest, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password, check_password
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from utils.user_auth import LoggedinUser, user_login_required
from order_module.models import Order, OrderDetail
from utils.email_service import send_email
from .models import User
from django.views import View
from .forms import LoginForm, RegisterForm, ForgotPasswordForm, ResetPasswordForm, EditProfileModelForm, \
    ChangePasswordForm


# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'user_module/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_first_name = register_form.cleaned_data.get('first_name')
            user_last_name = register_form.cleaned_data.get('last_name')
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error(
                    'email', 'ایمیل وارد شده تکراری میباشد')
            else:
                new_user = User(
                    first_name=user_first_name,
                    last_name=user_last_name,
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    password=make_password(user_password)
                )

                new_user.save()

                send_email('فعال سازی حساب کاربری', new_user.email, {
                    'user': new_user}, 'emails/active_account.html')

                return redirect(reverse('login_page'))

        context = {
            'register_form': register_form
        }
        return render(request, 'user_module/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }

        return render(request, 'user_module/login.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error(
                        'email', 'حساب کاربری شما فعال نشده است')
                else:
                    if check_password(user_pass, user.password):
                        request.session["user_id"] = user.id
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('password', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error(
                    'email', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'login_form': login_form
        }

        return render(request, 'user_module/login.html', context)


class LogoutView(View):
    def get(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            del request.session['user_id']
        return redirect(reverse('login_page'))


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(
            email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                return redirect(reverse('login_page'))
            else:
                pass
        raise Http404


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'user_module/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور', user.email, {
                    'user': user}, 'emails/forgot_password.html')
                return redirect(reverse('home_page'))

        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'user_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, reset_code):
        user: User = User.objects.filter(
            email_active_code__iexact=reset_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_pass_form = ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'user_module/reset_password.html', context)

    def post(self, request: HttpRequest, reset_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(
            email_active_code__iexact=reset_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            user.password = make_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'user_module/reset_password.html', context)


# ------ User Panel ------

@method_decorator(user_login_required, name='dispatch')
class UserPanelDashboardPage(TemplateView):
    template_name = 'user_module/user_dashboard.html'


@method_decorator(user_login_required, name='dispatch')
class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        user = LoggedinUser(request)
        edit_form = EditProfileModelForm(instance=user)
        context = {
            'form': edit_form
        }
        return render(request, 'user_module/edit_user_profile_page.html', context)

    def post(self, request: HttpRequest):
        user = LoggedinUser(request)
        edit_form = EditProfileModelForm(request.POST, instance=user)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'form': edit_form
        }
        return render(request, 'user_module/edit_user_profile_page.html', context)


@method_decorator(user_login_required, name='dispatch')
class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        context = {
            'change_pass_form': ChangePasswordForm()
        }
        return render(request, 'user_module/change_password_page.html', context)

    def post(self, request: HttpRequest):
        change_pass_form = ChangePasswordForm(request.POST)
        if change_pass_form.is_valid():
            user_pass = change_pass_form.cleaned_data.get('current_password')
            current_user = LoggedinUser(request)
            if check_password(user_pass, current_user.password):
                user_new_pass = change_pass_form.cleaned_data.get('password')
                current_user.password = make_password(user_new_pass)
                current_user.save()
                del request.session['user_id']
                return redirect(reverse('login_page'))
            else:
                change_pass_form.add_error('current_password', 'کلمه عبور فعلی اشتباه است')

        context = {
            'change_pass_form': change_pass_form
        }
        return render(request, 'user_module/change_password_page.html', context)


@method_decorator(user_login_required, name='dispatch')
class LastOrders(ListView):
    model = Order
    template_name = 'user_module/user_last_orders.html'

    def get_queryset(self):
        user = LoggedinUser(self.request)
        request: HttpRequest = self.request
        queryset = super().get_queryset()
        queryset = queryset.filter(user_id=user.id, is_paid=True)
        return queryset


@user_login_required
def last_orders_detail(request: HttpRequest, order_id):
    user = LoggedinUser(request)
    order = Order.objects.prefetch_related('orderdetail_set').filter(id=order_id, user_id=user.id).first()
    if order is None:
        raise Http404('سفارش مورد نظر یافت نشد')

    context = {
        'order': order
    }
    return render(request, 'user_module/user_last_orders_detail.html', context)


@user_login_required
def user_basket(request: HttpRequest):
    user = LoggedinUser(request)
    current_order = Order.objects.prefetch_related('orderdetail_set').filter(is_paid=False, user_id=user.id).first()

    if current_order:
        total_amount = current_order.calculate_total_price()
    else:
        total_amount = 0

    context = {
        'order': current_order,
        'sum': total_amount
    }
    return render(request, 'user_module/user_basket.html', context)


def remove_order_detail(request: HttpRequest):
    user = LoggedinUser(request)
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })
    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=user.id).delete()
    if deleted_count == 0:
        return JsonResponse({
            'status': 'not_found_detail'
        })

    current_order = Order.objects.prefetch_related('orderdetail_set').filter(is_paid=False, user_id=user.id).first()
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_module/includes/user_basket_content.html', context)
    })


def change_order_detail_count(request: HttpRequest):
    user = LoggedinUser(request)
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_id_or_state'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__is_paid=False, order__user_id=user.id).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'not_found_detail'
        })

    if state == 'increase':
        order_detail.count += 1
        order_detail.save()
    elif state == 'decrease':
        if order_detail.count == 1:
            order_detail.delete()
        else:
            order_detail.count -= 1
            order_detail.save()
    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order = Order.objects.prefetch_related('orderdetail_set').filter(is_paid=False, user_id=user.id).first()
    total_amount = current_order.calculate_total_price()

    context = {
        'order': current_order,
        'sum': total_amount
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_module/includes/user_basket_content.html', context)
    })
