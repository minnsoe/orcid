from setuptools import setup


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
	'install_requires': ['rauth']
}


setup(**_parameters)