from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register_page'),
    path('login', views.LoginView.as_view(), name='login_page'),
    path('logout', views.LogoutView.as_view(), name='logout_page'),
    path('forget-pass', views.ForgetPasswordView.as_view(),
         name='forget_password_page'),
    path('reset-pass/<reset_code>', views.ResetPasswordView.as_view(),
         name='reset_password_page'),
    path('activate-account/<email_active_code>',
         views.ActivateAccountView.as_view(), name='activate_account'),
    # ---- user Panel ----
    path('panel', views.UserPanelDashboardPage.as_view(),
         name='user_panel_dashboard_page'),
    path('edit-profile', views.EditUserProfilePage.as_view(),
         name='edit_user_profile_page'),
    path('change-pass', views.ChangePasswordPage.as_view(),
         name='change_password_page'),
    path('user-basket', views.user_basket, name='user_basket_page'),
    path('last-orders', views.LastOrders.as_view(), name='last_orders_page'),
    path('last-orders-detail/<order_id>',
         views.last_orders_detail, name='last_orders_detail_page'),
    path('remove-order-detail', views.remove_order_detail,
         name='remove_order_detail_ajax'),
    path('change-order-detail', views.change_order_detail_count,
         name='change_order_detail_count_ajax'),

]
