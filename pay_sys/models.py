from django.db import models


# class TypePaySys(models.Model):
#     """
#     Тип платежной системы
#     """
#     ps_type = models.CharField(
#         max_length=120,
#         verbose_name="Тип платежной системы",
#         blank=True,
#         null=True,
#     )
#     country = models.CharField(
#         max_length=20,
#         verbose_name="Страна платежной системы",
#         default="Rus"
#     )
#
#     class Meta:
#         db_table = "type_pay_system"
#         verbose_name = "Тип платежной системы"
#         verbose_name_plural = "Типы платежных систем"
#
#     def __str__(self):
#         return f"{self.ps_type}: {self.id}"


class PaySystem(models.Model):
    """
    Модель для платежных систем
    """
    name = models.CharField(
        max_length=20,
        verbose_name="Название",
    )
    # type_pay_system = models.ForeignKey(
    #     to="pay_sys.TypePaySys",
    #     on_delete=models.CASCADE,
    #     verbose_name="Тип платежной системы",
    # )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Активная"
    )
    description = models.CharField(
        max_length=600,
        verbose_name="Описание",
    )
    type_pay_system = models.CharField(
        max_length=120,
        verbose_name="Тип платежной системы",
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=20,
        verbose_name="Страна платежной системы",
        default="Rus"
    )
    user = models.ManyToManyField(
        to="users.CustomUser",
        verbose_name="Пользователь",
        related_name="pay_systems"
    )
    as_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        db_table = "pay_system"
        verbose_name = "Платежная система"
        verbose_name_plural = "Платежные системы"

    def __str__(self):
        return f"{self.name}"


class Requisites(models.Model):
    """Модель для реквизитов"""

    payment_system = models.ForeignKey(
        to="pay_sys.PaySystem",
        on_delete=models.CASCADE,
        verbose_name="Платежная система",
        related_name="requisites"
    )
    data = models.CharField(
        max_length=120,
        verbose_name="Данные реквизитов"
    )
    user = models.ManyToManyField(
        to="users.CustomUser",
        verbose_name="Пользователь",
        related_name="requisites"
    )

    class Meta:
        db_table = "requisites"
        verbose_name = "Реквизит"
        verbose_name_plural = "Реквизиты"

    def __str__(self):
        return f"Реквизит {self.user}"
