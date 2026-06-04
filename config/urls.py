from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('pop/', views.pop_products, name='pop'),      # ← ДОБАВИТЬ ЭТУ СТРОКУ
    path('jazz/', views.jazz_products, name='jazz'), 
    path('users/', include('users.urls')),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('delivery/', views.delivery, name='delivery'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ВРЕМЕННО: создаём админа
import os
import sys

if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    import django
    django.setup()
    from django.contrib.auth.models import User
    
    # Удаляем старого super если есть
    User.objects.filter(username='super').delete()
    
    # Создаём нового админа
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Создан админ: admin / admin123')