#!/usr/bin/evn python

try: 
    from setuptools import setup
except ImportError:
    print('setuptools not found, using distutils')
    from distutils.core import setup


setup(name='pyric',
      version='0.1',
      description='Event driven Python IRC framework',
      author='Vegard Veiset',
      author_email='veiset@gmail.com',
      url='http://github.com/veiset/pyric/',
      packages=['pyric', 'ircparser'],
#      scripts=['scripts/pyric_install.py'], #'scripts/ircparser_install'],
      #install_requires=['beautifulsoup'],
      classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English'
     ]
)
