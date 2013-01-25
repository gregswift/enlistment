from setuptools import setup

setup(name='HIREme',
      version='1.0',
      description='Rackspace HIRE',
      author='Greg Swift',
      author_email='greg.swift@rackspace.com',
      url='http://hire.nytefyre.net',
      install_requires=['Flask>=0.9',
                        'Flask-Login>=0.1.3',
                        'Flask-Restless>=0.9.1',
                        'Flask-Shelve>=0.1.1'],
     ),
