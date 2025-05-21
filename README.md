# RSML

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

    mamba create -n rsml -c conda-forge -c openalea3 rsml
    mamba activate rsml
    

#### From the source

To install it, go to the rsml folder and enter the following command::

    pip install .
    

### Use

```python
    import rsml
    
    # load rsml
    g = rsml.rsml2mtg( filename )
    
    # plot
    plot2d(g)  # requires matplotlib
    plot3d(g)  # requires openalea.plantgl

    # save mtg into rsml
    rsml.mtg2rsml(g, filename)
    
    # export mesurements to tabular file
    from rsml import measurements
    measurements.export(g, filename[:-5]+'.csv')
```    

### Tutorial

[RSML tutorial in Python](http://nbviewer.ipython.org/github/RootSystemML/RSML-conversion-tools/blob/master/python/rsml/example/RSML%20tutorial%20in%20Python.ipynb)
