import sys

from django.conf import settings
from model_utils import Choices


PLATFORM_CODES = Choices(
    ('twilio', 'Twilio'),
    ('info', 'Information'),
    ('danger', 'Danger'),
    ('success', 'Success'),
)

ROLE_TYPES = Choices(
    ('provider', 'Provider'),
    ('manager', 'Manager'),
    ('user', 'User'),
    ('association', 'Association'),
    ('control_panel', 'Control Panel'),
)


LEVEL_TYPES = Choices(
    ('warning', 'Warning'),
    ('info', 'Information'),
    ('danger', 'Danger'),
    ('success', 'Success'),
)

DEVICE_TYPES = Choices(
    ('mobile', 'Mobile'),
    ('tablet', 'Tablet'),
    ('touch_capable', 'Touch Capable'),
    ('pc', 'PC'),
    ('bot', 'Bot'),
    ('unknown', 'Unknown')
)

COMPONENT_TYPE = Choices(
    ('')
)

try:
    from django.core.cache import caches, DEFAULT_CACHE_ALIAS


    def get_cache(backend, **kwargs):
        return caches[backend]
except ImportError:
    from django.core.cache import get_cache


# Small snippet from the `six` library to help with Python 3 compatibility
if sys.version_info[0] == 3:
    text_type = str
else:
    text_type = unicode

USER_AGENTS_CACHE = getattr(settings, 'USER_AGENTS_CACHE', DEFAULT_CACHE_ALIAS)

if USER_AGENTS_CACHE:
    cache = get_cache(USER_AGENTS_CACHE)
else:
    cache = None