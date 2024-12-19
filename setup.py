from setuptools import setup, find_packages


setup(
    author='Dmitry Banny',
    author_email='dima.benny88@gmail.com',
    name='linkedin_scrapper',
    version='0.1',
    packages=find_packages(
        include=['linkedin_scrapper']
    ),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'urllib3',
        'pandas',
    ]
)
