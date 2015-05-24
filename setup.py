import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'pyramid',
]

tests_require = install_requires + [
    'nose',
    'pyramid_chameleon',
    'webtest',
]


setup(
    name='djed.templates',
    version='0.0',
    description='djed.templates',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Djed developers',
    author_email='djedproject@googlegroups.com',
    url='https://github.com/djedproject/djed.templates',
    license='ISC License (ISCL)',
    keywords='web pyramid pylons',
    packages=['djed.templates'],
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
    },
    test_suite='nose.collector',
)
