from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    # Жанры
    GENRE_CHOICES = [
        ('pop', 'Поп'),
        ('jazz', 'Джаз'),
        ('rock', 'Рок'),
        ('electronic', 'Электроника'),
    ]

    artist = models.CharField('Исполнитель', max_length=200)
    title = models.CharField('Название альбома', max_length=200)
    year = models.IntegerField('Год выпуска', null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    stock = models.IntegerField('Количество на складе', default=1)
    genre = models.CharField('Жанр', max_length=20, choices=GENRE_CHOICES, default='pop')
    image = models.ImageField('Фото', upload_to='products/', blank=True, null=True)
    image_url = models.URLField('Ссылка на фото (из интернета)', blank=True, null=True)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return f"{self.artist} - {self.title}"

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        elif self.image:
            return self.image.url
        return 'https://via.placeholder.com/300x300?text=No+Image'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершён'),
        ('cancelled', 'Отменён'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    full_name = models.CharField('ФИО', max_length=200)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    address = models.TextField('Адрес доставки')
    comment = models.TextField('Комментарий', blank=True)
    total = models.DecimalField('Итого', max_digits=10, decimal_places=2, default=0)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField('Дата заказа', auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.id} - {self.full_name}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.title} x {self.quantity}'

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'