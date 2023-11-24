from django.db import models


class Discussion(models.Model):
    """Модель для опрделения таблицы споры"""
    transactions = models.ForeignKey(
        to="transactions.Transactions",
        on_delete=models.CASCADE,
        verbose_name="Транзакция",
    )
    # request_check = models.ImageField(
    #     verbose_name="Запрошенный менеджером чек"
    # )
    request_data = models.CharField(
        max_length=1000,
        verbose_name="Зпрошенные данные менеджером",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания спора"
    )
    # p = models.CharField()
    comment = models.CharField(
        max_length=1000,
        verbose_name="Комментарий",
        blank=True,
        null=True,
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="Разрешено"
    )
    date_completed = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата разрешения"
    )

    class Meta:
        db_table = "discussions"
        verbose_name = "Спор"
        verbose_name_plural = "Споры"

    def __str__(self) -> str:
        return f"Спор {self.pk}"
