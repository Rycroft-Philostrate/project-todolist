import random

from django.db import models

SIMBOLS = "abcdefghijklmnopqrstuvwxyz1234567890"


class TgUser(models.Model):
    tg_id = models.BigIntegerField(verbose_name="tg id", unique=True)
    tg_chat_id = models.BigIntegerField(verbose_name="tg chat id")
    user = models.ForeignKey(
        "core.User",
        models.PROTECT,
        null=True,
        blank=True,
        default=None,
        verbose_name="Связанный пользователь",
    )
    username = models.CharField(
        max_length=512, verbose_name="tg username", null=True, blank=True, default=None
    )
    verification_code = models.CharField(
        max_length=32, verbose_name="Код подтверждения"
    )

    class Meta:
        verbose_name = "Telegram пользователь"
        verbose_name_plural = "Telegram пользователи"

    def set_verification_code(self):
        self.verification_code = "".join([random.choice(SIMBOLS) for _ in range(9)])
