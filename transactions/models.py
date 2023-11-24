from django.db import models


class Transactions(models.Model):
    """Модель для определния таблицы сделки"""

    DISCUSSION: str = "В споре"
    PAID: str = "Олачено"
    COMPLETED: str = "Завершена"
    IN_PROCESSING_PAID: str = "В ожидании оплаты"
    WORK_MANAGER: str = "В обработке менеджером"
    CANCELED: str = "Отменена"
    CHECK_SELLER: str = "На подтверждении у продавца"
    FOUND_BUYER: str = "В поиске продавца"

    status_choice = [
        ("discussion", DISCUSSION),
        ("paid", PAID),
        ("completed", COMPLETED),
        ("in_processing_paid", IN_PROCESSING_PAID),
        ("work_manager", WORK_MANAGER),
        ("canceled", CANCELED),
        ("check_seller", CHECK_SELLER),
        ("found_buyer", FOUND_BUYER),

    ]

    buyer = models.ForeignKey(
        to="users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Покупатель",
        related_name="transactions_buy",
    )
    seller = models.ForeignKey(
        to="users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Продавец",
        related_name="transactions_sell",
        blank=True,
        null=True
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма",
        default=100,
    )
    status = models.CharField(
        max_length=25,
        choices=status_choice,
        default=FOUND_BUYER,
    )
    buyer_yes = models.BooleanField(
        default=False,
        verbose_name="Согласие "
    )
    is_paid = models.BooleanField(
        default=False,
        verbose_name="Оплачено"
    )
    date_paid = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты"
    )
    pay_system = models.ForeignKey(
        to="pay_sys.PaySystem",
        on_delete=models.CASCADE,
        verbose_name="Платежная система продавца",
        related_name="transactions",
    )

    class Meta:
        db_table = "transactions"
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

    def __str__(self) -> str:
        return f"Сделка {self.pk}"

