import requests
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
from django.core.cache import cache
from django.db import models
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone, country, city, adress, zip_code, unique_uid,
                    password=None, email=None,
                    **extra_fields):
        # if not email:
        # raise ValueError('Email address must be provided')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.country = country
        user.sity = city
        user.adress = adress
        user.zip_code = zip_code
        user.unique_uid = unique_uid
        user.set_password(password)
        user.auth_key = str(uuid.uuid4())  # генерируем уникальный ключ
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель пользователя. Может принадлежать покупателю, продавцу, менеджеру
    """
    MANAGER = 'manager'
    BUYER = 'buyer'
    SELLER = 'seller'

    role_choice = [
        (MANAGER, 'Менеджер'),
        (BUYER, 'Покупатель'),
        (SELLER, 'Продавец'),
    ]
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name="Почта"
    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Фамилия",
    )
    phone = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Телефон",
    )
    country = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Страна",
    )
    city = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Город",
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Адрес"
    )
    zip_code = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Индекс"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный")
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(
        max_length=10,
        verbose_name='Роль пользователя',
        choices=role_choice,
        blank=True,
        null=True
    )
    profile = models.OneToOneField(
        to='users.Profile',
        verbose_name='Профиль',
        on_delete=models.CASCADE,
        related_name='user',
        blank=True,
        null=True,
    )

    mode_issue = models.BooleanField(
        default=False,
        verbose_name='Режим сделок'
    )

    auth_key = models.CharField(
        max_length=36,
        unique=True
    )
    crypto_balance = models.DecimalField(
        max_digits=12,
        decimal_places=8,
        verbose_name='Баланс Bitcoin',
        default=0.00000000
    )

    groups = models.ManyToManyField(
        Group,
        related_name='custom_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    state = models.BooleanField(
        default=False,
        verbose_name='Активация'
    )
    currency = models.CharField(
        max_length=7,
        choices=(('RUB', 'RUB'), ("USD", 'USD')),
        default='USD'
    )
    unique_uid = models.TextField(default="None")

    USERNAME_FIELD = 'auth_key'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @property
    def exchange(self):
        cache_key = f"exchange_rate_{self.currency}"
        exchange_rate = cache.get(cache_key)

        if exchange_rate is None:
            if self.currency == 'RUB':
                data = requests.get(
                    "https://api.binance.com/api/v3/ticker/price?symbol=BTCRUB"
                ).json()
                exchange_rate = round(float(data['price']), 2)
            else:
                data = requests.get(
                    "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
                ).json()
                exchange_rate = round(float(data['price']), 2)

            cache.set(cache_key, exchange_rate, 5 * 60)

        return exchange_rate

    @property
    def balance(self):
        try:
            if self.currency == 'RUB':
                data = self.exchange
                return round(float(data) * float(self.crypto_balance), 2)
            else:
                data = self.exchange
                return round(float(data) * float(self.crypto_balance), 2)
        except Exception as err:
            return f'Нет связи с binance.com!'

    def __str__(self) -> str:
        return f'{self.unique_uid} - {self.role}'


class Profile(models.Model):
    """
    Модель для профиля пользователя
    """
    # type_pay_sys = models.ForeignKey(
    #
    # )
    # requisite = models.ForeignKey(
    #
    # )
    min_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Минимальная сумма",
        default=1,
    )
    max_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Максимальная сумма",
        default=1000,
    )
    wallet_address = models.CharField(
        max_length=50,
        verbose_name="Адрес кошелька",
        blank=True,
        null=True,
    )
    tm_chat_id = models.CharField(
        max_length=20,
        verbose_name="Телеграмм чат ID",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "profile"
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль {self.user}"
