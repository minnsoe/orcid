# third party
from rauth import OAuth2Service

# local
import constants
from exceptions import AuthError


class Orcid(object):

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
        if self.client_id is None:
            raise AuthError('authentication requires a client_id')
        if self.client_secret is None:
            raise AuthError('authentication requires a client_secret')

    def _check_redirect_uri(self, redirect_uri):
        if redirect_uri == '':
            raise ValueError('redirect_uri must not be empty')

    def _authorize_url_endpoint(self):
        if self.sandbox:
            return constants.AUTHORIZE_URL_SANDBOX
        else:
            return constants.AUTHORIZE_URL

    def _add_optional_state_to_params(self, state, params):
        if state is not None:
            params['state'] = state

    def authorization_url(self, scope, redirect_uri, state=None):
        """Provides a URL to request an ORCID authorization code.

        Client credentials (client_id and client_secret) must be set
        before attempting to obtain an authorization_url.
        :class:`AuthError` will be thrown if there are no credentials.

        :param scope: ORCID access scope delimited with spaces
        :type scope: str
        :param redirect_uri: redirection uri after authorization
        :type redirect_uri: str
        :returns: str -- url to request authorization code from ORCID
        :raises: AuthError, ValueError
        """
        self._check_if_credentials_are_set()
        self._check_redirect_uri(redirect_uri)
        AUTHORIZE_URL = self._authorize_url_endpoint()
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'authorize_url': AUTHORIZE_URL
        }
        service = OAuth2Service(**params)
        url_params = {
            'scope': scope,
            'redirect_uri': redirect_uri,
            'response_type': 'code'
        }
        self._add_optional_state_to_params(state, url_params)
        url = service.get_authorize_url(**url_params)
        return url
