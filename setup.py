from setuptools import setup, find_packages

import explor

with open("README.md", encoding="utf8") as file:
    description = file.read()

setup(
    name='explor',
    version=explor.__version__,
    description='Powerful human-readable version of dir().',
    long_description=description,
    long_description_content_type="text/markdown",
    url='https://github.com/Talon24/explore',
    author='Talon24',
    author_email='talontalon24@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_dir={"": "."},
    py_modules=["explor"],
    # package_data={'explore': ['mapping.json']},
    # include_package_data=True,
    install_requires=['terminaltables>=3.1.0',
                      'colorama>=0.4',
                      ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
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
