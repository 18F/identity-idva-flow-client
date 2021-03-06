import datetime
from urllib import parse

from jose import constants, jwk, jwt

from flow_client import oidc, settings


def test_gen_sig_url() -> None:
    """test url signature"""
    ipd_url = "https://example.com"
    valid_for = datetime.timedelta(days=1, seconds=0)
    request = oidc.gen_sig_url(ipd_url, valid_for)
    url = parse.urlparse(request.url)
    query = parse.parse_qs(url.query)
    request_jwt = query["request"][0]
    key = jwk.construct(settings.KEYS[0], constants.ALGORITHMS.RS256)
    validation_options = {
        "require_aud": True,
        "require_exp": True,
        "require_iss": True,
    }
    jwt.decode(
        request_jwt, key, audience=settings.FLOW_ISSUER, options=validation_options
    )
