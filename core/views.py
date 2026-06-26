from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from decimal import Decimal
import uuid

from core.models import (
    DomainExtension, HostingPlan, Cart, CartItem, Order, 
    OrderItem, UserProfile, Notification
)


# Home & Landing Page
def home(request):
    """Landing page with domain search and hosting plans preview"""
    popular_extensions = DomainExtension.objects.filter(is_popular=True, is_active=True)[:6]
    popular_plans = HostingPlan.objects.filter(is_popular=True, is_active=True)[:3]
    
    context = {
        'popular_extensions': popular_extensions,
        'popular_plans': popular_plans,
    }
    return render(request, 'core/home.html', context)


# Domain Management
from core.truehost_service import truehost

def domain_search(request):
    """Domain availability search with TrueHost API"""
    extensions = DomainExtension.objects.filter(is_active=True)
    results = []
    
    if request.method == 'POST':
        domain_name = request.POST.get('domain_name', '').strip()
        selected_extensions = request.POST.getlist('extensions')
        
        if domain_name:
            if selected_extensions:
                exts = DomainExtension.objects.filter(name__in=selected_extensions)
            else:
                exts = extensions
            
            for ext in exts:
                # Real TrueHost API check
                is_available = truehost.check_domain(domain_name, ext.name)
                
                results.append({
                    'domain': f"{domain_name}{ext.name}",
                    'extension': ext,
                    'available': is_available,
                    'registration_price': ext.registration_price,
                })
    
    context = {
        'extensions': extensions,
        'results': results,
        'search_query': request.POST.get('domain_name', ''),
    }
    return render(request, 'core/domain_search.html', context)

def domain_details(request, domain_name, extension):
    """Detailed domain information"""
    ext = get_object_or_404(DomainExtension, name=extension)
    
    context = {
        'domain_name': domain_name,
        'extension': ext,
        'registration_price': ext.registration_price,
        'renewal_price': ext.renewal_price,
        'transfer_price': ext.transfer_price,
        'domain_full': f"{domain_name}{ext.name}",
    }
    return render(request, 'core/domain_details.html', context)


# Hosting Plans
def hosting_plans(request):
    """List all hosting plans"""
    plan_type = request.GET.get('type')
    
    if plan_type:
        plans = HostingPlan.objects.filter(plan_type=plan_type, is_active=True)
    else:
        plans = HostingPlan.objects.filter(is_active=True)
    
    plan_types = HostingPlan.objects.values_list('plan_type', flat=True).distinct()
    
    context = {
        'plans': plans,
        'plan_types': plan_types,
        'selected_type': plan_type,
    }
    return render(request, 'core/hosting_plans.html', context)


def hosting_plan_detail(request, plan_id):
    """Detailed hosting plan view"""
    plan = get_object_or_404(HostingPlan, id=plan_id)
    
    context = {
        'plan': plan,
    }
    return render(request, 'core/hosting_plan_detail.html', context)


# Shopping Cart
@login_required
def view_cart(request):
    """View shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    total = cart.get_total()
    
    context = {
        'cart': cart,
        'items': items,
        'total': total,
    }
    return render(request, 'core/cart.html', context)


@login_required
@require_POST
def add_to_cart(request):
    """Add item to cart (AJAX)"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    item_type = request.POST.get('item_type')
    
    if item_type == 'domain':
        domain_name = request.POST.get('domain_name')
        extension_id = request.POST.get('extension_id')
        ext = get_object_or_404(DomainExtension, id=extension_id)
        
        CartItem.objects.create(
            cart=cart,
            item_type='domain',
            domain_name=domain_name,
            domain_extension=ext,
            price=ext.registration_price,
        )
    
    elif item_type == 'hosting':
        plan_id = request.POST.get('plan_id')
        duration = request.POST.get('duration', 'monthly')
        plan = get_object_or_404(HostingPlan, id=plan_id)
        
        price = plan.price_monthly if duration == 'monthly' else plan.price_annual
        
        CartItem.objects.create(
            cart=cart,
            item_type='hosting',
            hosting_plan=plan,
            hosting_duration=duration,
            price=price,
        )
    
    return JsonResponse({
        'success': True,
        'message': 'Item added to cart',
        'cart_count': cart.items.count(),
        'cart_total': str(cart.get_total()),
    })


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = item.cart
    item.delete()
    
    return JsonResponse({
        'success': True,
        'message': 'Item removed from cart',
        'cart_count': cart.items.count(),
        'cart_total': str(cart.get_total()),
    })


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        item.quantity = quantity
        item.save()
    
    cart = item.cart
    return JsonResponse({
        'success': True,
        'subtotal': str(item.get_subtotal()),
        'cart_total': str(cart.get_total()),
    })


# Checkout & Orders
@login_required
def checkout(request):
    """Checkout process"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    
    if not items.exists():
        messages.warning(request, 'Your cart is empty')
        return redirect('view_cart')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        billing_address = request.POST.get('billing_address')
        payment_method = request.POST.get('payment_method', 'card')
        
        # Create order
        order_number = f"BH-{uuid.uuid4().hex[:8].upper()}"
        order = Order.objects.create(
            order_number=order_number,
            user=request.user,
            email=email,
            phone=phone,
            billing_address=billing_address,
            payment_method=payment_method,
            total_amount=cart.get_total(),
            status='pending',
        )
        
        # Add order items
        for item in items:
            if item.item_type == 'domain':
                item_name = f"{item.domain_name}{item.domain_extension.name}"
                description = f"Domain Registration for 1 year"
            else:
                item_name = item.hosting_plan.name
                description = f"Hosting Plan - {item.hosting_duration}"
            
            OrderItem.objects.create(
                order=order,
                item_type=item.item_type,
                item_name=item_name,
                description=description,
                quantity=item.quantity,
                unit_price=item.price,
                total_price=item.get_subtotal(),
            )
        
        # Clear cart
        cart.items.all().delete()
        
        # Redirect to payment
        return redirect('payment', order_id=order.id)
    
    context = {
        'cart': cart,
        'items': items,
        'total': cart.get_total(),
    }
    return render(request, 'core/checkout.html', context)


@login_required
def payment(request, order_id):
    """Payment processing"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        # Process payment (simulated - integrate with Stripe in production)
        order.payment_status = 'completed'
        order.mark_completed()
        
        # Create notification
        Notification.objects.create(
            user=request.user,
            notification_type='order',
            title='Order Completed',
            message=f'Your order {order.order_number} has been processed successfully.',
        )
        
        messages.success(request, f'Payment successful! Order number: {order.order_number}')
        return redirect('order_confirmation', order_id=order.id)
    
    context = {
        'order': order,
    }
    return render(request, 'core/payment.html', context)


@login_required
def order_confirmation(request, order_id):
    """Order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'core/order_confirmation.html', context)


# User Dashboard
@login_required
def dashboard(request):
    """User dashboard"""

    all_orders = request.user.orders.all()

    recent_orders = all_orders.filter(status='completed').count()

    total_spent = sum(
        order.total_amount
        for order in all_orders.filter(status='completed')
    )

    latest_orders = all_orders.order_by('-created_at')[:5]

    notifications = request.user.notifications.all()[:5]
    unread_count = request.user.notifications.filter(is_read=False).count()

    context = {
        'orders': latest_orders,
        'recent_orders': recent_orders,
        'total_spent': total_spent,
        'notifications': notifications,
        'unread_count': unread_count,
    }

    return render(request, 'core/dashboard.html', context)
    
@login_required
def my_orders(request):
    """User's orders history"""
    orders = request.user.orders.all()
    status_filter = request.GET.get('status')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
    }
    return render(request, 'core/my_orders.html', context)


@login_required
def order_detail(request, order_id):
    """Order detail view"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'core/order_detail.html', context)


@login_required
def my_domains(request):
    """User's registered domains"""
    # This would pull from actual domain management system
    orders = request.user.orders.filter(status='completed')
    domains = []
    
    for order in orders:
        for item in order.items.filter(item_type='domain'):
            domains.append(item)
    
    context = {
        'domains': domains,
    }
    return render(request, 'core/my_domains.html', context)


@login_required
def my_hosting(request):
    """User's hosting services"""
    orders = request.user.orders.filter(status='completed')
    hosting_services = []
    
    for order in orders:
        for item in order.items.filter(item_type='hosting'):
            hosting_services.append(item)
    
    context = {
        'hosting_services': hosting_services,
    }
    return render(request, 'core/my_hosting.html', context)


@login_required
def profile(request):
    """User profile management"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.city = request.POST.get('city', '')
        profile.state = request.POST.get('state', '')
        profile.zipcode = request.POST.get('zipcode', '')
        profile.country = request.POST.get('country', '')
        profile.company_name = request.POST.get('company_name', '')
        profile.company_website = request.POST.get('company_website', '')
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'core/profile.html', context)


# Authentication
def register(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
    
    return render(request, 'core/register.html')


def login_view(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_page = request.GET.get('next', 'dashboard')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'core/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')
