#!/usr/bin/evn python
from distutils.core import setup
setup(name='pyric',
      version='0.1',
      description='Event driven Python IRC framework',
      author='Vegard Veiset',
      author_email='veiset@gmail.com',
      url='http://github.com/veiset/pyric/',
      packages=['pyric'],
      package_dir={'pyric' : '.'},
)
