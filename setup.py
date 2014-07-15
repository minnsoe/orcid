from setuptools import setup, Command


class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


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
	'cmdclass': {'test': PyTest}
}


setup(**_parameters)