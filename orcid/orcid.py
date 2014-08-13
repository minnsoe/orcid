# standard library
from datetime import datetime

# third party
from rauth import OAuth2Service

# local
import constants
from exceptions import AuthError
from utils import Tokens


class Orcid(object):
    """ORCID Public API Service

    Provides methods to upgrade API access using OAuth2 Three-Legged
    authentication.
    """

    def __init__(self, client_id=None, client_secret=None, sandbox=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sandbox = sandbox

    @property
    def sandbox(self):
        return self._sandbox

    @sandbox.setter
    def sandbox(self, setting):
        self._sandbox = bool(setting)

    def _check_if_credentials_are_set(self):
        """Checks if client_id and client_secret are set."""
        if self.client_id is None:
            raise AuthError('authentication requires a client_id')
        if self.client_secret is None:
            raise AuthError('authentication requires a client_secret')

    def _check_redirect_uri(self, redirect_uri):
        """Checks if redirect_uri is valid."""
        if redirect_uri == '':
            raise ValueError('redirect_uri must not be empty')

    def _get_authorize_url_endpoint(self):
        """Provides the appropriate authorize_url for prod/sandbox."""
        if self.sandbox:
            return constants.AUTHORIZE_URL_SANDBOX
        else:
            return constants.AUTHORIZE_URL

    def _get_access_token_url_endpoint(self):
        """Provides the appropriate token_url for prod/sandbox."""
        if self.sandbox:
            return constants.TOKEN_URL_SANDBOX
        else:
            return constants.TOKEN_URL

    def _add_optional_state_to_params(self, state, params):
        """Mutates params to add optional CSRF state."""
        if state is not None:
            params['state'] = state

    def _create_service(self):
        self._check_if_credentials_are_set()
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'authorize_url': self._get_authorize_url_endpoint(),
            'access_token_url': self._get_access_token_url_endpoint()
        }
        return OAuth2Service(**params)

    def create_authorization_url(self, scope, redirect_uri, state=None):
        """Provides a URL to request an ORCID authorization code.

        Client credentials (client_id and client_secret) must be set
        before attempting to obtain an authorization_url.
        :exc:`AuthError` will be thrown if there are no credentials.

        :param scope: ORCID access scope delimited with spaces
        :type scope: str
        :param redirect_uri: redirection uri after authorization
        :type redirect_uri: str
        :returns: str -- url to request authorization code from ORCID
        :raises: AuthError, ValueError
        """
        self._check_redirect_uri(redirect_uri)
        service = self._create_service()
        url_params = {
            'scope': scope,
            'redirect_uri': redirect_uri,
            'response_type': 'code'
        }
        self._add_optional_state_to_params(state, url_params)
        url = service.get_authorize_url(**url_params)
        return url

    def authorize_with_code(self, code):
        tokens = Tokens('ACCESS','REFRESH', '10', datetime(2000,1,1,0,0,0,0))
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'sandbox': self.sandbox,
            'tokens': tokens
        }
        return AuthorizedOrcid(**params)


class AuthorizedOrcid(Orcid):

    def __init__(self, client_id, client_secret, sandbox, tokens):
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'sandbox': sandbox
        }
        super(AuthorizedOrcid, self).__init__(**params)
        self.tokens = tokens
