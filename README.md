# RSML

[![Docs](https://readthedocs.org/projects/rsml/badge/?version=latest)](https://rsml.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://github.com/openalea/RSML/actions/workflows/openalea_ci.yml/badge.svg)](https://github.com/openalea/RSML/actions/workflows/openalea_ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/openalea.rsml/badges/version.svg)](https://anaconda.org/openalea3/openalea.rsml)
[![License](https://img.shields.io/badge/License--CeCILL-C-blue)](https://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html)

**Authors** : C. Pradal and J. Diener

**Institutes** : INRIA / CIRAD

**Status** : Python package 

**License** : Cecill-C

**URL** : http://rootsystemml.github.io/

### About

The **rsml** python package provides:

 - import/export between .rsml files and MTG
 - plot
 - standard root system measurements
 - export to table file


### Installation

#### Conda 

The **rsml** package is an openalea package that can be installed using conda or mamba:

    mamba create -n rsml -c conda-forge -c openalea3 openalea.rsml
    mamba activate rsml
    

#### From the source

To install it, go to the rsml folder and enter the following command::

    pip install .
    

### Use

```python
    import openalea.rsml as rsml
    
    # load rsml
    g = rsml.rsml2mtg( filename )
    
    # plot
    plot2d(g)  # requires matplotlib
    plot3d(g)  # requires openalea.plantgl

    # save mtg into rsml
    rsml.mtg2rsml(g, filename)
    
    # export mesurements to tabular file
    from openalea.rsml import measurements
    measurements.export(g, filename[:-5]+'.csv')
```    

### Tutorial

[RSML tutorial in Python](https://github.com/openalea/RSML/blob/master/example/RSML_tutorial_in_Python.ipynb)
