#!/bin/bash
# BrandHostest Installation Script

set -e

echo "╔════════════════════════════════════════════════════════╗"
echo "║         BrandHostest - Setup & Installation           ║"
echo "║      Domain & Hosting Reseller Platform              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check Python
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
python_version=$(python3 --version | awk '{print $2}')
echo "  Found Python $python_version"

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate || . venv\Scripts\activate

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
echo ""
echo "✓ Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "  Created .env file - please edit with your settings"
fi

# Run migrations
echo ""
echo "✓ Setting up database..."
python manage.py migrate

# Create superuser
echo ""
echo "✓ Creating superuser account..."
python manage.py createsuperuser

# Collect static files
echo ""
echo "✓ Collecting static files..."
python manage.py collectstatic --noinput

# Success message
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║          Installation Complete! ✓                     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate  (Linux/Mac)"
echo "   venv\\Scripts\\activate     (Windows)"
echo ""
echo "2. Start development server:"
echo "   python manage.py runserver"
echo ""
echo "3. Access the application:"
echo "   http://localhost:8000"
echo "   Admin: http://localhost:8000/admin"
echo ""
echo "4. For production deployment, see README.md"
echo ""
