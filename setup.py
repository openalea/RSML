# -*- coding: utf-8 -*-
__revision__ = "$Id: $"

import sys

from setuptools import setup, find_packages

# Reads the metainfo file
version = '1.1.0'
release = '1.1'
name = 'RSML'
package = name
description= 'RSML package provide IO functionality between .rsml file and MTG'
long_description=  'RSML package provide IO functionality between .rsml file and MTG, as well as ploting and standard measurements. '
authors= 'C. Pradal, J. Diener'
authors_email = 'christophe.pradal@inria.fr, julien.diener@inria.fr'
url = 'https://github.com/RootSystemML/RSML-conversion-tools'
license = 'Cecill-C'

# Packages list, namespace and root directory of packages

pkgs = [pkg for pkg in find_packages('src')]
packages = pkgs
package_dir = dict([('', 'src')] + [(pkg, "src/" + pkg) for pkg in pkgs])

# dependencies to other eggs
setup_requires = ['openalea.deploy']

# web sites where to find eggs
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords='rsml',

    # package installation
    packages=packages,
    package_dir=package_dir,

    # Namespace packages creation by deploy
    #namespace_packages = [namespace],
    #create_namespaces = False,
    zip_safe=False,

    # Dependencies
    setup_requires=setup_requires,
    install_requires=[],
    #dependency_links=dependency_links,



    # Eventually include data in your package
    # (folowing is to include all versioned files other than .py)
    include_package_data=True,
    # (you can provide an exclusion dictionary named exclude_package_data to remove parasites).
    # alternatively to global inclusion, list the file to include
    #package_data = {'' : ['*.pyd', '*.so'],},
    share_dirs = {'share': 'share'},
    # postinstall_scripts = ['',],

    # Declare scripts and wralea as entry_points (extensions) of your package
    entry_points={
        'wralea': ['rsml = rsml_wralea'],
    },
)
