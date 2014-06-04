import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(name='lol_stats',
      version='0.1',
      py_modules=['lol_stats'],
      include_package_data=True,
      license='GNU AGPL v3',
      description='A Django project to collect and analyze data for League of Legends.',
      long_description=README,
      url='https://bitbucket.org/kreychek/lol_stats',
      author='Edward Chen',
      author_email='chenward.t@gmail.com',
      install_requires=[
          'Django',
      ],
      classifiers=[
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License', # example license
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
)