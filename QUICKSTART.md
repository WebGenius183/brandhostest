# BrandHostest - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
python manage.py migrate
```

### 3. Create Admin User
```bash
python manage.py createsuperuser
```

### 4. Add Sample Data (Optional)
```bash
python manage.py shell << EOF
from core.models import DomainExtension, HostingPlan

# Domain Extensions
extensions = ['.com', '.net', '.org', '.io', '.co', '.info']
for ext in extensions:
    DomainExtension.objects.get_or_create(
        name=ext,
        defaults={
            'registration_price': 8.99,
            'renewal_price': 8.99,
            'transfer_price': 8.99,
            'is_popular': ext in ['.com', '.net'],
            'is_active': True
        }
    )

# Hosting Plans
plans = [
    {
        'name': 'Starter',
        'plan_type': 'shared',
        'price_monthly': 2.99,
        'price_annual': 29.99,
        'storage': '50 GB',
        'bandwidth': 'Unlimited',
        'email_accounts': '50',
        'databases': '5',
        'addon_domains': '1',
        'description': 'Perfect for getting started',
        'is_popular': True,
    },
    {
        'name': 'Professional',
        'plan_type': 'shared',
        'price_monthly': 5.99,
        'price_annual': 59.99,
        'storage': '250 GB',
        'bandwidth': 'Unlimited',
        'email_accounts': 'Unlimited',
        'databases': 'Unlimited',
        'addon_domains': 'Unlimited',
        'description': 'For growing websites',
        'is_popular': True,
    },
]

for plan_data in plans:
    HostingPlan.objects.get_or_create(
        name=plan_data['name'],
        defaults=plan_data
    )

print("Sample data created successfully!")
EOF
```

### 5. Run Server
```bash
python manage.py runserver
```

### 6. Access Application
- **Home**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Login with your created superuser**

## 📋 First Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] Database migrated (python manage.py migrate)
- [ ] Superuser created (python manage.py createsuperuser)
- [ ] Server running (python manage.py runserver)
- [ ] Visited http://localhost:8000

## 🎯 First Steps

1. **Create Domains**
   - Go to Admin Panel
   - Add Domain Extensions (.com, .net, etc.)
   - Set pricing for each

2. **Create Hosting Plans**
   - Go to Admin Panel
   - Add Hosting Plans
   - Configure features and pricing

3. **Register User Account**
   - Go to Sign Up page
   - Create account
   - Login and explore

4. **Test Shopping Flow**
   - Search for domain
   - Add to cart
   - View hosting plans
   - Complete checkout

## 💡 Configuration Options

### Edit Settings
File: `config/settings.py`

```python
# Debug Mode
DEBUG = True  # Set to False in production

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Environment Variables
Copy `.env.example` to `.env` and edit:

```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🔧 Common Commands

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Admin panel
python manage.py createsuperuser
python manage.py changepassword username

# Clear cache/static
python manage.py clear_cache
python manage.py collectstatic

# Interactive shell
python manage.py shell

# Run tests
python manage.py test

# Get help
python manage.py help
```

## 📁 Customize Branding

### Change Site Name
File: `templates/base.html`
```html
<span class="font-display text-xl font-bold gradient-text">Your Brand Name</span>
```

### Change Colors
File: `templates/base.html`
```css
:root {
    --primary: #0f172a;
    --secondary: #1e293b;
    --accent: #06b6d4;  /* Change cyan to your color */
}
```

### Change Logo
Replace with your logo image

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Database Errors
```bash
python manage.py migrate --run-syncdb
```

### Clear All Data
```bash
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

## 📚 Next Steps

1. Explore the Django admin panel
2. Customize domain and hosting data
3. Test the full user journey
4. Integrate payment processing
5. Deploy to production
6. Set up email notifications
7. Configure SSL certificate

## 🎓 Learning Path

1. Django Basics: Understand models, views, URLs
2. Templates: Learn Tailwind CSS and HTML
3. Database: Add custom fields and models
4. API: Create REST endpoints
5. Payments: Integrate Stripe
6. Deployment: Deploy to production

## 🚀 Production Checklist

- [ ] Set DEBUG=False
- [ ] Change SECRET_KEY
- [ ] Setup HTTPS/SSL
- [ ] Configure allowed hosts
- [ ] Setup email backend
- [ ] Configure database (PostgreSQL)
- [ ] Setup Stripe keys
- [ ] Configure static files
- [ ] Setup monitoring
- [ ] Backup database regularly

## 💬 Support

For issues:
1. Check Django documentation
2. Review error logs
3. Search Stack Overflow
4. Review code comments in project files

---

**Happy Building! 🎉**

BrandHostest is ready to be customized and deployed. Start by exploring the admin panel and adding your own domain and hosting data.
