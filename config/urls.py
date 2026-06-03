from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home & Landing
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Domains
    path('domains/', views.domain_search, name='domain_search'),
    path('domains/<str:domain_name>/<str:extension>/', views.domain_details, name='domain_details'),
    
    # Hosting
    path('hosting/', views.hosting_plans, name='hosting_plans'),
    path('hosting/<int:plan_id>/', views.hosting_plan_detail, name='hosting_plan_detail'),
    
    # Shopping Cart
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('my-domains/', views.my_domains, name='my_domains'),
    path('my-hosting/', views.my_hosting, name='my_hosting'),
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
