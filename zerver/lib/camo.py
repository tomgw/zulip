import binascii
import hashlib
import hmac

from django.conf import settings


def generate_camo_url(url: str) -> str:
    encoded_url = url.encode("utf-8")
    encoded_camo_key = settings.CAMO_KEY.encode("utf-8")
    digest = hmac.new(encoded_camo_key, encoded_url, hashlib.sha1).hexdigest()
    hex_encoded_url = binascii.b2a_hex(encoded_url)
    return "{}/{}".format(digest, hex_encoded_url.decode("utf-8"))

# Encodes the provided URL using the same algorithm used by the camo
# caching https image proxy
def get_camo_url(url: str) -> str:
    # Only encode the url if Camo is enabled
    if settings.CAMO_URI == '':
        return url
    return f"{settings.CAMO_URI}{generate_camo_url(url)}"

def is_camo_url_valid(digest: str, url: str) -> bool:
    camo_url = generate_camo_url(url)
    camo_url_digest = camo_url.split('/')[0]
    return camo_url_digest == digest
