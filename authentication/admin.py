from django.contrib import admin

from .models import BlacklistedToken


@admin.register(BlacklistedToken)
class BlacklistedTokenAdmin(admin.ModelAdmin):
    """Административная панель для заблокированных токенов"""

    list_display = ('short_token', 'blacklisted_at')
    search_fields = ('token',)
    list_filter = ('blacklisted_at',)
    ordering = ('-blacklisted_at',)

    def short_token(self, obj: BlacklistedToken) -> str:
        return obj.token[:30] + '...' if len(obj.token) > 30 else obj.token

    short_token.short_description = 'Token'
