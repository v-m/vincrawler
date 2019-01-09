from setuptools import setup
from vmusco import __VERSION__

setup(name='vincrawler',
      version=__VERSION__,
      description='Simple URL Crawlers',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      python_requires='>=3',
      keywords='scrapping crawler',
      url='https://github.com/v-m/vincrawler',
      author='Vincenzo Musco',
      author_email='muscovin@gmail.com',
      license='MIT',
      packages=['vmusco'],
      install_requires=['bs4', 'html5lib'],
      scripts=['bin/vincrawler'],
      zip_safe=False)


