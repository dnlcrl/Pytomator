from setuptools import setup
import io
import os

import pytomator

here = os.path.abspath(os.path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md')


setup(name='pytomator',
      version='0.1',
      description='Automate any task on os x',
      long_description=long_description,

      url='https://github.com/danieleciriello/Pytomator',
      author='Daniele Ciriello',
      author_email='ciriello.daniele@gmail.com',
      license='GPL2',
      packages=['pytomator'],
      include_package_data=True,
      platforms='darwin',
      zip_safe=False)
