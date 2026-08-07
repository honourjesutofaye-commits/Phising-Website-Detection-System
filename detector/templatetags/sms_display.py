"""Display-only template helpers for SMS results."""
import re

from django import template

register = template.Library()


@register.filter
def mask_sms_sender(value):
    """Mask the middle of a phone number while retaining useful context."""
    raw_value = str(value or "").strip()
    digits = re.sub(r"\D", "", raw_value)
    if not digits or raw_value.lower() in {"none", "not applicable"}:
        return "None"
    if len(digits) <= 7:
        return f"{digits[:2]}***{digits[-2:]}"
    prefix_length = 6 if len(digits) >= 11 else 4
    suffix_length = 3
    masked_length = len(digits) - prefix_length - suffix_length
    prefix = digits[:prefix_length]
    prefix = "+" + prefix if raw_value.startswith("+") else prefix
    return f"{prefix}{'*' * masked_length}{digits[-suffix_length:]}"
