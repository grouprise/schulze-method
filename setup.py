from setuptools import setup, find_packages

setup(
    name='schulze',
    description='Implementation of the Schulze method for ranking candidates',
    url='https://github.com/stadtgestalten/schulze-method',
    version='0.1',
    packages=find_packages(),
    author=', '.join([
        'Konrad Mohrfeldt <konrad.mohrfeldt@farbdev.org>',
        'Michael G. Parker'
    ]),
    license='Apache Software License',
    keywords='schulze ranking vote election',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
    ],
)
