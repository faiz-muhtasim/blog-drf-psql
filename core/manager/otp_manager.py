import random
from datetime import timedelta
from django.db import models
from django.utils import timezone
from .base import _soft_delete
from django.core.mail import send_mail
from django.conf import settings

OTP_EXPIRY_MINUTES = 2

class OTPManager(models.Manager):
    def get_all_otps(self):
        return self.filter(is_deleted=False)

    def get_otp_by_id(self, pk):
        try:
            return self.get(pk=pk, is_deleted=False)
        except self.model.DoesNotExist:
            return None

    def create_otp(self, validated_data):
        otp_value = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        return self.create(
            otp=otp_value,
            has_used=False,
            task_type=validated_data['task_type'],
            expired_at=expires_at,
        )

    def create_otp_for_user(self, user, task_type):
        otp_value = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        otp = self.create(
            user=user,
            otp=otp_value,
            has_used=False,
            task_type=task_type,
            expired_at=expires_at,
        )
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is: {otp_value}. It expires in {OTP_EXPIRY_MINUTES} minutes.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return otp

    @staticmethod
    def is_otp_expired(instance):
        if not instance.expired_at:
            return False
        return timezone.now() > instance.expired_at

    def get_otp_by_code(self, otp_code, task_type=None):
        now = timezone.now()
        qs = self.select_related('user').filter(
            otp=otp_code,
            has_used=False,
            is_deleted=False,
            expired_at__gt=now,
        )
        if task_type is not None:
            qs = qs.filter(task_type=task_type)
        return qs.first()

    def mark_otp_used(self, pk):
        instance = self.get_otp_by_id(pk)
        if instance is None:
            return None
        instance.has_used = True
        instance.save()
        return instance

    def delete_otp(self, pk):
        instance = self.get_otp_by_id(pk)
        if instance is None:
            return False
        _soft_delete(instance)
        return True