from urllib.parse import urlparse
from escherauth_go.escher_validator import EscherValidator, EscherValidatorError
from authorization import ValidationError


_CREDENTIAL_SCOPE = 'eu/pisti_ai-prediction-launcher/ems_request'
_KEY_DB = [{'keyId': 'love', 'secret': 'pisti', 'acceptOnly': 0}]

_escher_validator = EscherValidator(
    _CREDENTIAL_SCOPE,
    _KEY_DB,
    authHeaderName='X-Ems-Auth',
    dateHeaderName='X-Ems-Date')


def validate_request(request):
    url_to_check = _get_url_to_validate(request.url)
    try:
        return _escher_validator.validateRequest(
            request.method,
            url_to_check,
            request.data.decode('utf-8'),
            request.headers)
    except EscherValidatorError as e:
        raise ValidationError(str(e))


def _get_url_to_validate(url):
    parsed_url = urlparse(url)
    return (parsed_url.path + '?' + parsed_url.query).rstrip('?')
