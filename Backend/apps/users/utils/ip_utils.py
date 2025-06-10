from typing import Optional
from django.http import HttpRequest
import logging



logger = logging.getLogger(__name__)

def get_client_ip(request: HttpRequest) -> Optional[str]:
    """
    Get the client's IP address from request headers.
    Handles cases where the request might be behind a proxy.
    
    Args:
        request: Django HttpRequest object
    
    Returns:
        str: IP address if found, None otherwise
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
        logger.debug(f"Got IP from X-Forwarded-For: {ip}")
    else:
        ip = request.META.get('REMOTE_ADDR')
        logger.debug(f"Got IP from REMOTE_ADDR: {ip}")
    return ip if ip else None