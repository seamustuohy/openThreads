from setuptools import setup

setup(name='openThreads',
      version='0.2',
      description='An e-mail parser for exploring social communication',
      long_description='OpenThreads parses e-mail list-servs to identify the way that individuals impact the comunicative environment',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: GPLV3',
        'Programming Language :: Python :: 2.7',
        'Topic :: e-mail parsing',
        ],
      keywords='e-mail, list-serv',
      url='https://github.com/elationfoundation/openThreads',
      author='s2e',
      author_email='s2e@opentechinstitute.org',
      license='GPLV3',
      packages=['openThreads', 'openThreads.email', 'openThreads.email.tests'])
