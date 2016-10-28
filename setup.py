try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='sed',
    version='0.2.9',
    description='Streaming editor toolkit',
    author='Hugh Brown',
    author_email='hughdbrown@yahoo.com',
    url='http://iwebthereforeiam.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
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
