from django.contrib import admin
from django.utils.html import format_html
from core.models import (
    DomainExtension, HostingPlan, Cart, CartItem, Order,
    OrderItem, UserProfile, Notification
)

@admin.register(DomainExtension)
class DomainExtensionAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_price', 'renewal_price', 'is_popular', 'is_active']
    list_filter = ['is_popular', 'is_active', 'created_at']
    search_fields = ['name']
    list_editable = ['is_popular', 'is_active']
    
    fieldsets = (
        ('Extension Details', {
            'fields': ('name',)
        }),
        ('Pricing', {
            'fields': ('registration_price', 'renewal_price', 'transfer_price')
        }),
        ('Status', {
            'fields': ('is_popular', 'is_active')
        }),
    )

@admin.register(HostingPlan)
class HostingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price_monthly', 'price_annual', 'is_popular', 'is_active']
    list_filter = ['plan_type', 'is_popular', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_popular', 'is_active']
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('name', 'plan_type', 'description')
        }),
        ('Pricing', {
            'fields': ('price_monthly', 'price_annual')
        }),
        ('Resources', {
            'fields': ('storage', 'bandwidth', 'email_accounts', 'databases', 'addon_domains')
        }),
        ('Features', {
            'fields': ('features',)
        }),
        ('Status', {
            'fields': ('is_popular', 'is_active')
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'total', 'updated_at']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]
    readonly_fields = ['created_at', 'updated_at']
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'
    
    def total(self, obj):
        return f"${obj.get_total()}"
    total.short_description = 'Total'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['get_item_name', 'cart_user', 'quantity', 'price', 'added_at']
    list_filter = ['item_type', 'added_at']
    search_fields = ['domain_name', 'hosting_plan__name']
    readonly_fields = ['added_at']
    
    def get_item_name(self, obj):
        if obj.item_type == 'domain':
            return f"{obj.domain_name}{obj.domain_extension.name}"
        return obj.hosting_plan.name
    get_item_name.short_description = 'Item'
    
    def cart_user(self, obj):
        return obj.cart.user.username
    cart_user.short_description = 'User'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item_name', 'description', 'total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status_badge', 'total_amount', 'payment_status_badge', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'completed_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'created_at', 'completed_at')
        }),
        ('Customer Details', {
            'fields': ('email', 'phone', 'billing_address')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_status', 'transaction_id', 'total_amount')
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#fbbf24',
            'processing': '#60a5fa',
            'completed': '#10b981',
            'cancelled': '#ef4444',
            'failed': '#ef4444'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, '#6b7280'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': '#fbbf24',
            'completed': '#10b981',
            'failed': '#ef4444'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.payment_status, '#6b7280'),
            obj.payment_status.title()
        )
    payment_status_badge.short_description = 'Payment'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'order_number', 'quantity', 'unit_price', 'total_price']
    list_filter = ['item_type', 'order__created_at']
    search_fields = ['item_name', 'order__order_number']
    readonly_fields = ['order']
    
    def order_number(self, obj):
        return obj.order.order_number
    order_number.short_description = 'Order'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'city', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['user__username', 'user__email', 'company_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at']

# Customize Admin Site
admin.site.site_header = "BrandHostest Admin"
admin.site.site_title = "BrandHostest Administration"
admin.site.index_title = "Welcome to BrandHostest Admin"
