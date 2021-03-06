from setuptools import setup, find_packages

setup_requires = [
        'setuptools>=35.0.2',
]

install_requires = [
        'click',
        'awscli',
        'boto3',
        'botocore',
        'pathlib',
]

tests_requires = [
        'pytest>=3.6',
        'mock',
        'pytest-cov',
        'codecov',
]

docs_requires = [
        'sphinx',
        'sphinx_rtd_theme',
]

setup(
        name='gaia-finder',
        version=open('VERSION').read().strip(),
        url='https://github.com/deadlylaid/gaia',
        author_email='deadlylaid@gmail.com',
        packages=find_packages(),
        install_requires=install_requires,
        setup_requires=setup_requires,
        tests_requires=tests_requires,
        extras_require={
                'test': tests_requires,
                'doc': docs_requires,
        },
        entry_points='''
            [console_scripts]
            gaia=gaia.gaia:cli
        '''
)
