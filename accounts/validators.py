import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordValidator:
    """
    Custom password validator to enforce specific password rules.
    """

    def validate(self, password, user=None):
        if len(password) < 4:
            raise ValidationError(
                _("Пароль должен содержать не менее 4 символов."),
                code='password_too_short',
            )
        
        if len(password) > 16:
            raise ValidationError(
                _("Пароль не должен превышать 16 символов."),
                code='password_too_long',
            )
        
        forbidden_chars = set('*&{}|+')
        if any(char in forbidden_chars for char in password):
            raise ValidationError(
                _("Пароль не должен содержать следующие символы: * & { } | +"),
                code='forbidden_characters',
            )
        
        if not re.search(r'[A-ZА-Я]', password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну заглавную букву."),
                code='no_uppercase_letter',
            )
        
        if not re.search(r'\d', password):
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну цифру."),
                code='no_digit',
            )
        
        def get_help_text(self):
            return _(
                "Ваш пароль должен соответствовать следующим требованиям:\n"
                "- От 4 до 16 символов в длину.\n"
                "- Не должен содержать следующие символы: * & { } | +\n"
                "- Должен содержать хотя бы одну заглавную букву.\n"
                "- Должен содержать хотя бы одну цифру."
            )