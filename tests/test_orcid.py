import pytest
from mock import patch
from orcid import Orcid


@pytest.fixture
def orcid_no_params():
    return Orcid()


class TestOrcid(object):

    def test_constructor_defaults(self, orcid_no_params):
        assert orcid_no_params.client_id is None
        assert orcid_no_params.client_secret is None
        assert orcid_no_params.sandbox is False

    def test_constructor_kwargs(self):
        service = Orcid(client_id='daphne', client_secret='mystery_machine', sandbox=True)

        assert service.client_id == 'daphne'
        assert service.client_secret == 'mystery_machine'
        assert service.sandbox == True

    def test_constructor_bad_sandbox_kwarg(self):
        service = Orcid(sandbox='trololo')
        assert service.sandbox is True

    def test_property_sandbox(self, orcid_no_params):
        orcid_no_params.sandbox = True
        assert orcid_no_params.sandbox is True

    def test_property_sandbox_cast(self, orcid_no_params):
        orcid_no_params.sandbox = 123
        assert orcid_no_params.sandbox is True
        assert not orcid_no_params.sandbox == 123
