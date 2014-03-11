try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='sed',
    version='0.1',
    description='Streaming editor toolikit',
    author='Hugh Brown',
    author_email='hughdbrown@yahoo.com',
    url='iwebthereforeiam.com',
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
    ],
    tests_require=[
        'nose',
    ],
    setup_requires=[],
    packages=[
        'sed',
        'sed.engine',
    ],
    test_suite='nose.collector',
    zip_safe=False,
)
