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

The **rsml** package is an openalea package that can be installed using conda. After installing conda, enter the following command on your conda environment::

    conda install rsml -c openalea/label/unstable -c openalea
    

#### From the source

The **rsml** package is an openalea package and thus requires openalea.deploy to be installed. To install it, go to the rsml folder and enter the following command::

    python setup.py install
    

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


# Limit order 1(primary) order 2 (secondary)
## 4/5 different array with key : plant
- Total Length, 
- nb racine (t absolute) (P1), 
- primary length
- nude tip length 
- frequency vs IBD (P2)

# Axis : time in raw
## time is known

Plant Lateral lenght
- Length by root  (t) (question unit?)
    - time as col
    - name : Ln nth root along primary from base

Tab Position
- col : L1 ... Ln
- position on primary


- # root , position lateral (from base , distance)

script : rsmlanalysis rsmls.txt| *.rsml
TODO: define options to group all the analysis in a same file (csv) or in several files.