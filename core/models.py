from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class DomainExtension(models.Model):
    """Model for domain extensions (.com, .net, etc.)"""
    name = models.CharField(max_length=10, unique=True)
    registration_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    renewal_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    transfer_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_popular', 'name']
    
    def __str__(self):
        return f"{self.name}"

class HostingPlan(models.Model):
    """Model for hosting plans offered"""
    PLAN_TYPES = (
        ('shared', 'Shared Hosting'),
        ('reseller', 'Reseller Hosting'),
        ('vps', 'VPS'),
        ('dedicated', 'Dedicated Server'),
    )
    
    name = models.CharField(max_length=100)
    whm_package = models.CharField(max_length=100,unique=True,help_text="WHM package name")
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    price_monthly = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price_annual = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Plan Features
    storage = models.CharField(max_length=100, help_text="e.g., 100 GB")
    bandwidth = models.CharField(max_length=100, help_text="e.g., Unlimited")
    email_accounts = models.CharField(max_length=100, help_text="e.g., 100")
    databases = models.CharField(max_length=100, help_text="e.g., Unlimited")
    addon_domains = models.CharField(max_length=100, help_text="e.g., Unlimited")
    
    description = models.TextField()
    features = models.JSONField(default=list, help_text="List of features as JSON array")
    
    is_popular = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['plan_type', 'price_monthly']
    
    def __str__(self):
        return f"{self.name} - ${self.price_monthly}/mo"

class Cart(models.Model):
    """Shopping cart for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())
    
    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    """Items in a shopping cart"""
    ITEM_TYPES = (
        ('domain', 'Domain Registration'),
        ('hosting', 'Hosting Plan'),
        ('addon', 'Add-on Service'),
    )
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES)
    
    # For domain items
    domain_name = models.CharField(max_length=255, null=True, blank=True)
    domain_extension = models.ForeignKey(DomainExtension, on_delete=models.SET_NULL, null=True, blank=True)
    
    # For hosting items
    hosting_plan = models.ForeignKey(HostingPlan, on_delete=models.SET_NULL, null=True, blank=True)
    hosting_duration = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('annual', 'Annual')])
    
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_subtotal(self):
        return self.price * self.quantity
    
    def __str__(self):
        if self.item_type == 'domain':
            return f"{self.domain_name}{self.domain_extension.name if self.domain_extension else ''}"
        return f"{self.hosting_plan.name}" if self.hosting_plan else "Unknown Item"

class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    )
    
    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment Details
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    
    # Customer Details
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Billing Address
    billing_address = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.user.username}"
    
    def mark_completed(self):
        self.status = 'completed'
        self.payment_status = 'completed'
        self.completed_at = timezone.now()
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    item_type = models.CharField(max_length=20)

    hosting_plan = models.ForeignKey(
        HostingPlan,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    domain_extension = models.ForeignKey(
        DomainExtension,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    domain_name = models.CharField(
        max_length=255,
        blank=True
    )

    item_name = models.CharField(max_length=255)
    description = models.TextField()

    quantity = models.IntegerField(default=1)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.item_name} x {self.quantity}"

class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    company_website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"

class Notification(models.Model):
    """System notifications for users"""
    NOTIFICATION_TYPES = (
        ('order', 'Order Update'),
        ('domain', 'Domain Update'),
        ('billing', 'Billing Update'),
        ('security', 'Security Alert'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

class HostingAccount(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True
    )

    plan = models.ForeignKey(
        HostingPlan,
        on_delete=models.PROTECT
    )

    domain = models.CharField(max_length=255)

    cpanel_username = models.CharField(max_length=30)

    cpanel_login_url = models.URLField()

    status = models.CharField(
        max_length=20,
        default="active"
    )

    created_at = models.DateTimeField(auto_now_add=True)