from setuptools import setup

setup(
    name='jiac',
    packages=['jiac'],
    version='0.2.0',
    description='A Jinja extension (compatible with Flask) to compile and/or compress your assets inline.',
    author='Brian Morgan',
    author_email='brian.s.morgan@gmail.com',
    install_requires=[
        'Jinja2',
        'beautifulsoup4>=4.3.2'
    ],
    url='https://github.com/bmorgan21/jinja-inline-asset-compressor',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
