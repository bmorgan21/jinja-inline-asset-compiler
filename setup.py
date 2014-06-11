from setuptools import setup

setup(
    name='jiac',
    author='Brian Morgan',
    author_email='brian.s.morgan@gmail.com',
    version='0.11',
    install_requires=open('requirements.txt').readlines(),
    description='A Jinja extension (compatible with Flask) to compile and/or compress your assets inline.',
    url='https://github.com/bmorgan21/jinja-inline-asset-compressor',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
