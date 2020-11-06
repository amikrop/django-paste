import re
from pathlib import Path

from setuptools import setup


init_path = Path('paste') / '__init__.py'
with init_path.open() as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with open('README.rst') as f:
    long_description = f.read()


setup(
    name='django-paste',
    version=version,
    description='Pluggable, configurable, pastebin HTTP REST API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Aristotelis Mikropoulos',
    author_email='amikrop@gmail.com',
    url='https://github.com/amikrop/django-paste',
    packages=['paste'],
    license='MIT',
    install_requires=[
        'Django',
        'djangorestframework',
        'Pygments',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
