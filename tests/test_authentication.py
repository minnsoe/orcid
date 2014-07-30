# third party
import pytest
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
        url = orcid_with_params.authorization_url('', '')
        assert url is not None
        assert url != ''

    def test_obtain_url_without_client_id(self, orcid_without_params):
        with pytest.raises(exceptions.AuthError):
            url = orcid_without_params.authorization_url('', '')

    def test_obtain_url_without_client_secret(self, orcid_without_params):
        orcid_without_params.client_id = 'daphne'

        with pytest.raises(exceptions.AuthError):
            url = orcid_without_params.authorization_url('', '')

    def test_if_url(self, orcid_with_params):
        url = orcid_with_params.authorization_url('', '')
        scheme, netloc, _, _, _, _ = urlparse(url)

        assert scheme != ''
        assert netloc != ''

    @pytest.mark.parametrize("service,auth_endpoint", [
        (orcid_with_params(), constants.AUTHORIZE_URL),
        (orcid_with_params_sandbox(), constants.AUTHORIZE_URL_SANDBOX)
    ])
    def test_if_orcid_endpoint_url(self, service, auth_endpoint):
        url = service.authorization_url('', '')
        scheme, netloc, path, _, _, _ = urlparse(url)
        o_scheme, o_netloc, o_path, _, _, _ = urlparse(auth_endpoint)

        assert scheme == o_scheme
        assert netloc == o_netloc
        assert path == o_path

    def test_if_url_contains_scope(self, orcid_with_params):
        url = orcid_with_params.authorization_url('SCOPE', '')
        _, _, _, _, query, _ = urlparse(url)

        assert 'scope=SCOPE' in query

    def test_if_url_contains_redirect_uri(self, orcid_with_params):
        url = orcid_with_params.authorization_url('', 'URL')
        _, _, _, _, query, _ = urlparse(url)

        assert 'redirect_uri=URL' in query
