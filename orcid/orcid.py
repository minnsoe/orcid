class Orcid(object):

    def __init__(self, client_id=None, client_secret=None, sandbox=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self._sandbox = bool(sandbox)

    @property
    def sandbox(self):
        return self._sandbox

    @sandbox.setter
    def sandbox(self, setting):
        self._sandbox = bool(setting)
