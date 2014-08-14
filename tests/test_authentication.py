# standard library
from datetime import datetime, timedelta

# third party
import pytest
import responses
from requests.utils import urlparse

# local
from test_orcid import orcid_without_params
from orcid import Orcid, exceptions, constants


@pytest.fixture
def orcid_with_params():
    return Orcid(client_id='daphne', client_secret='mystery_machine')


@pytest.fixture
def orcid_with_params_sandbox():
    return Orcid(client_id='daphne',
                 client_secret='mystery_machine',
                 sandbox=True)


class TestAuthorizationURL(object):

    def test_obtain_url_with_params(self, orcid_with_params):
        url = orcid_with_params.create_authorization_url('SCOPE', 'URL')
        assert url is not None
        assert url != ''

    def test_obtain_url_without_client_id(self, orcid_without_params):
        with pytest.raises(exceptions.AuthError):
            url = orcid_without_params.create_authorization_url('SCOPE', 'URL')

    def test_obtain_url_without_client_secret(self, orcid_without_params):
        orcid_without_params.client_id = 'daphne'

        with pytest.raises(exceptions.AuthError):
            url = orcid_without_params.create_authorization_url('SCOPE', 'URL')

    def test_if_url(self, orcid_with_params):
        url = orcid_with_params.create_authorization_url('SCOPE', 'URL')
        scheme, netloc, _, _, _, _ = urlparse(url)

        assert scheme != ''
        assert netloc != ''

    @pytest.mark.parametrize("service,auth_endpoint", [
        (orcid_with_params(), constants.AUTHORIZE_URL),
        (orcid_with_params_sandbox(), constants.AUTHORIZE_URL_SANDBOX)
    ])
    def test_if_orcid_endpoint_url(self, service, auth_endpoint):
        url = service.create_authorization_url('SCOPE', 'URL')
        scheme, netloc, path, _, _, _ = urlparse(url)
        o_scheme, o_netloc, o_path, _, _, _ = urlparse(auth_endpoint)

        assert scheme == o_scheme
        assert netloc == o_netloc
        assert path == o_path

    def test_if_url_contains_scope(self, orcid_with_params):
        url = orcid_with_params.create_authorization_url('SCOPE', 'URL')
        _, _, _, _, query, _ = urlparse(url)

        assert 'scope=SCOPE' in query

    def test_if_url_contains_redirect_uri(self, orcid_with_params):
        url = orcid_with_params.create_authorization_url('SCOPE', 'URL')
        _, _, _, _, query, _ = urlparse(url)

        assert 'redirect_uri=URL' in query

    def test_if_url_contains_optional_state(self, orcid_with_params):
        url = orcid_with_params.create_authorization_url(
            'SCOPE',
            'URL',
            state='STATE'
        )
        _, _, _, _, query, _ = urlparse(url)
        assert 'state=STATE' in query

    def test_url_optional_state_with_spaces(self, orcid_with_params):
        url = orcid_with_params.create_authorization_url(
            'SCOPE',
            'URL',
            state='STATE WITH SPACES'
        )
        _, _, _, _, query, _ = urlparse(url)
        assert 'state=STATE+WITH+SPACES' in query

    def test_if_raises_for_bad_redirect_uri(self, orcid_with_params):
        with pytest.raises(ValueError):
            orcid_with_params.create_authorization_url('SCOPE', '')


BASE_RESPONSE_DATETIME = datetime(2000, 1, 1, 0, 0, 0, )


@pytest.fixture
def authorize_response_mock(orcid_with_params):

    @responses.activate
    def run():
        responses.add(responses.POST, constants.TOKEN_URL,
                      body='{"access_token":"ACCESS",\
                             "refresh_token":"REFRESH",\
                             "expires_in":3600,\
                             "scope":"SCOPE",\
                             "orcid":"ORCID"}',
                      status=200)
        return orcid_with_params.authorize_with_code('CODE')

    return orcid_with_params, run()


class TestAuthorize(object):

    def test_authorize_code_returns_something(self, authorize_response_mock):
        service, auth = authorize_response_mock
        assert auth is not None

    def test_authorize_code_provides_copy(self, authorize_response_mock):
        original, auth = authorize_response_mock
        assert id(original) != id(auth)

    def test_authorize_code_provides_subclass(self, authorize_response_mock):
        service, auth = authorize_response_mock
        assert issubclass(type(auth), Orcid)

    def test_authorize_with_code_tokens(self, authorize_response_mock):
        service, auth = authorize_response_mock
        assert auth.access_token == 'ACCESS'
        assert auth.refresh_token == 'REFRESH'
        assert auth.expires_in == 3600
        assert isinstance(auth.expires_on, datetime)

    def test_expires_on_calc(self, authorize_response_mock):
        service, auth = authorize_response_mock
        expected = BASE_RESPONSE_DATETIME + timedelta(seconds=60)
        actual = auth._get_expires_on(BASE_RESPONSE_DATETIME, 60)
        assert actual == expected
        assert auth.expires_on > datetime.now()
