from setuptools import setup

setup(
    name='explore',
    version='0.1.0',
    description='Powerful human readable version of dir().',
    url='https://github.com/Talon24/explore',
    author='Talon24',
    author_email='talontalon24@gmail.com',
    license='MIT',
    packages=['explore'],
    install_requires=['terminaltables>=3.1.0',
                      'colorama>=0.4.3',
                      'six',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)