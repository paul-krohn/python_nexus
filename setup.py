from distutils.core import setup
setup(
    name='nexus_client',
    packages=['nexus_client'], # this must be the same as the name above
    version='0.1.2',
    description='Python client for Nexus.',
    author='Paul Krohn',
    author_email='paul@daemonize.com',
    url='https://github.com/paul-krohn/python-nexus',
    download_url='https://github.com/paul-krohn/python-nexus/tarball/0.1',
    keywords=['nexus'],
    classifiers=[],
    install_requires=['requests>=1.0', 'lxml']
)
