from django.db import models


class BlacklistedToken(models.Model):
    """Модель заблокированного токена"""

    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заблокированный токен'
        verbose_name_plural = 'Заблокированные токены'

    def __str__(self) -> str:
        return f'BlacklistedToken(token={self.token[:20]}..., at={self.blacklisted_at})'
