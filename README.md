# BrandHostest - Domain & Hosting Reseller Platform

A premium, fully-functional domain and web hosting reseller platform built with **Django**, **HTML**, and **Tailwind CSS**. BrandHostest provides a modern, professional interface for managing domain registrations, hosting plans, and customer orders.

## ✨ Features

### 🏪 Core Functionality
- **Domain Registration**: Search, register, and manage domains with support for multiple TLDs
- **Hosting Plans**: Multiple hosting plan types (Shared, Reseller, VPS, Dedicated)
- **Shopping Cart**: Full e-commerce cart system with add/remove functionality
- **Order Management**: Complete order processing and management system
- **Payment Processing**: Integration-ready payment gateway support (Stripe, PayPal, Bank Transfer)
- **User Authentication**: Secure user registration and login system

### 👥 User Dashboard
- View order history and status
- Manage registered domains
- Track active hosting services
- Profile management and preferences
- Real-time notifications

### 🎨 Design & UX
- **Modern Dark Theme**: Premium dark interface with cyan accents
- **Responsive Design**: Fully mobile-responsive layouts
- **Smooth Animations**: CSS animations and transitions throughout
- **Professional Typography**: Custom fonts (Space Grotesk + Sora)
- **Interactive Components**: Hover effects, cards, badges, and modals
- **Accessibility**: Semantic HTML and keyboard navigation

### ⚙️ Admin Features
- Complete Django admin interface
- Domain extension management
- Hosting plan management
- Order and customer management
- User profile management
- Notification system

## 🛠️ Tech Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, Tailwind CSS
- **Database**: SQLite (configurable to PostgreSQL)
- **Authentication**: Django built-in auth
- **Payment Ready**: Stripe integration template
- **APIs**: Django REST Framework ready

## 📋 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Extract & Navigate
```bash
cd BrandHostest
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your configuration
# Minimum required: SECRET_KEY (generate a new one)
```

### Step 5: Generate Secret Key
```python
# In Python shell:
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Step 6: Database Migration
```bash
python manage.py migrate
```

### Step 7: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 8: Load Sample Data
```bash
python manage.py shell < load_sample_data.py
```

### Step 9: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 10: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://localhost:8000`
Admin: `http://localhost:8000/admin`

## 📁 Project Structure

```
BrandHostest/
├── config/                    # Project configuration
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI application
├── core/                      # Main application
│   ├── models.py             # Database models
│   ├── views.py              # Request handlers
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App configuration
│   └── context_processors.py # Template context
├── templates/                # HTML templates
│   ├── base.html             # Base template
│   └── core/
│       ├── home.html         # Homepage
│       ├── domain_search.html
│       ├── hosting_plans.html
│       ├── cart.html
│       ├── checkout.html
│       ├── payment.html
│       ├── order_confirmation.html
│       ├── login.html
│       └── register.html
├── static/                   # Static files (CSS, JS, images)
├── manage.py                 # Django management
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🗄️ Database Models

### DomainExtension
- Domain TLDs (.com, .net, etc.)
- Registration/renewal pricing
- Popularity flags

### HostingPlan
- Multiple hosting types
- Resource specifications
- Feature lists
- Monthly/annual pricing

### Cart & CartItem
- User shopping carts
- Cart items management
- Price tracking

### Order & OrderItem
- Order creation and tracking
- Payment status
- Order item details
- Customer information

### UserProfile
- Extended user information
- Profile customization
- Company details

### Notification
- User notifications
- Order updates
- System alerts

## 🔐 Security Features

- CSRF protection on all forms
- Secure password hashing
- SQL injection prevention
- XSS protection
- Secure session handling
- SSL-ready configuration

## 🚀 Deployment

### For Production:

1. **Generate Secret Key**:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

2. **Update Settings**:
```python
# In settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

3. **Use PostgreSQL**:
```bash
pip install psycopg2-binary
```

4. **Use Gunicorn**:
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

5. **Use Whitenoise for Static Files**:
```bash
python manage.py collectstatic
```

## 💳 Payment Integration

### Stripe (Ready to integrate)
1. Get API keys from Stripe dashboard
2. Add to .env:
```
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

3. Update payment view in `core/views.py`

## 📊 Admin Dashboard

Access admin at `/admin` with superuser credentials.

### Manage:
- Domain extensions and pricing
- Hosting plans and features
- User accounts and profiles
- Orders and transactions
- Notifications and support tickets

## 🎯 Customization

### Branding
- Edit `templates/base.html` for logo/name
- Update CSS variables in `<style>` section
- Modify color scheme (cyan, slate, etc.)

### Features
- Add more domain extensions via admin
- Create custom hosting plans
- Extend user profile fields
- Add custom notification types

### Email
- Configure SMTP in settings.py
- Customize email templates
- Add email notifications

## 🤝 API Integration Ready

The project structure supports Django REST Framework:
```bash
pip install djangorestframework
```

Create API views for:
- Domain search and availability
- Order management
- Account information
- Pricing

## 📝 Sample Admin Data

To add sample data for testing:

```bash
python manage.py shell
```

```python
from core.models import DomainExtension, HostingPlan

# Add domain extensions
DomainExtension.objects.create(
    name='.com',
    registration_price=8.99,
    renewal_price=8.99,
    transfer_price=8.99,
    is_popular=True,
    is_active=True
)

# Add hosting plans
HostingPlan.objects.create(
    name='Starter',
    plan_type='shared',
    price_monthly=2.99,
    price_annual=29.99,
    storage='50 GB',
    bandwidth='Unlimited',
    email_accounts='50',
    databases='5',
    addon_domains='1',
    description='Perfect for getting started',
    is_popular=True,
    is_active=True
)
```

## 🐛 Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database errors
```bash
python manage.py migrate --run-syncdb
```

### Permission denied on manage.py
```bash
chmod +x manage.py
```

### Module not found
```bash
pip install -r requirements.txt
```

## 📚 Documentation

For Django documentation: https://docs.djangoproject.com/
For Tailwind CSS: https://tailwindcss.com/docs

## 📄 License

This project is provided as-is for reseller platform implementation.

## 🤝 Support

For issues or questions:
1. Check Django documentation
2. Review code comments in views.py and models.py
3. Check admin panel for configuration

## 🎓 Learning Resources

- Django Official Docs: https://docs.djangoproject.com/
- Tailwind CSS Docs: https://tailwindcss.com/
- HTML/CSS Best Practices: https://developer.mozilla.org/

## 🚀 Next Steps

1. Customize branding and colors
2. Add real domain registrar API integration
3. Implement Stripe payment processing
4. Add SSL certificate management
5. Create email notification system
6. Add API endpoints with DRF
7. Deploy to production server
8. Set up monitoring and analytics

## 💡 Tips

- Use Django debug toolbar for development
- Enable caching for production
- Set up periodic tasks with Celery
- Implement rate limiting on critical views
- Add comprehensive logging
- Use CDN for static files
- Implement caching strategies

---

**BrandHostest v1.0** - Premium Domain & Hosting Reseller Platform
Built with Django, Tailwind CSS, and modern web technologies.
"# brandhostest" 
