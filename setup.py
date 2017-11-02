from setuptools import setup

setup(name='coinwars',
      version='0.1',
      description='Play Coin Wars in your terminal.',
      url='http://github.com/geluso/ascii_coinwars',
      author='Steve Geluso',
      author_email='stevegeluso@gmail.com',
      license='MIT',
      packages=['coinwars'],
      scripts=['bin/coinwars'],
      zip_safe=False)
