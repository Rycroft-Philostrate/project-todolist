from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = TgUser
        read_only_fields = ("tg_id", "username", "user_id")
        fields = ("tg_id", "username", "verification_code", "user_id")

    def validate(self, attrs: dict):
        verification_code = attrs.get("verification_code")
        tg_user = TgUser.objects.filter(verification_code=verification_code).first()
        if not tg_user:
            raise ValidationError({"verification_code": "incorrect"})
        attrs["tg_user"] = tg_user
        return attrs