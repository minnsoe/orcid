from setuptools import setup
from setuptools.command.test import test as TestCommand

class Tox(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
    def finalize_options(self):
	TestCommand.finalize_options(self)
	self.test_args = []
	self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline()
        sys.exit(errno)

_parameters = {
    'name': 'orcid',
    'version': '0.1.1',
    'description': 'ORCID API Client.',
    'author': 'Minn Soe',
    'maintainer': 'Minn Soe',
    'maintainer_email': 'contributions@minn.so',
    'license': 'BSD',
    'packages': ['orcid'],
    'classifiers': [
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7'
    ],
    'install_requires': ['rauth'],
    'tests_require': ['tox'],
    'cmdclass' : {'test' : Tox}
}


setup(**_parameters)
