from setuptools import setup
 
setup(
    name = 'easymlserver',
    packages = ['easymlserver'],
    entry_points = {
        'console_scripts': [
            'easyml-server = easymlserver.server:main'
            ]
        },
    license='Modified BSD',
    version = '0.1.2',
    description = 'Server package for EasyML-lib (Android machine learning)',
    author='Delvv, Inc.',
    author_email='info@delvv.com',
    url='https://github.com/delvv/easyML-lib',
    platforms = ["any"],
    package_dir={'easymlserver':'easymlserver'},
    install_requires = ["flask", "python-recsys", "numpy", "scipy", "divisi2", "csc-pysparse"],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
    ]
)
