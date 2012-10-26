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
    install_requires=[
        'nose',
    ],
    tests_require=[
    ],
    setup_requires=[],
    packages=find_packages(exclude=['apps', 'test']),
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
)
