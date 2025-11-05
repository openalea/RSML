#!/usr/bin/env python
# coding: utf-8

# # RSML Tutorial in Python 

# First, we activate matplotlib and qt in the Notebook

# In[2]:


# get_ipython().run_line_magic('matplotlib', 'inline')
# get_ipython().run_line_magic('gui', 'qt')
#
#
# # In[3]:
#
#
# import sys; print('Python %s on %s' % (sys.version, sys.platform))
# sys.path.extend(['../src'])


# Then, we import main modules and function to work with RSML format in Python

# In[4]:


import os
from pprint import pprint
from openalea.core.path import path
import openalea.rsml as rsml
from openalea.rsml.plot import multiple_plot
from openalea.rsml.data import data_dir


# In[5]:


arabido = data_dir/'AR570'
_generator = arabido.glob('*.rsml')
files = []
for f in _generator:
    files.append(os.path.normpath(f))
pprint(files)


# # In[6]:
#
#
# multiple_plot(files, image=False)
#
#
# # In[7]:
#
#
# multiple_plot(files, image=True)
#
#
# # In[8]:
#
#
# get_ipython().run_line_magic('run', 'demo_plot_rsml.py')
#
#
# # In[9]:
#
#
g = rsml.rsml2mtg('data/lupin_aero.rsml')
from hydroroot.hydro_io import import_rsml_to_discrete_mtg
g=import_rsml_to_discrete_mtg(g)

#
#
# # In[10]:
#
#
# from openalea.rsml.plot import plot2d, plot3d
# plot2d(g)  # requires matplotlib
# plot3d(g)  # requires openalea.plantgl


# In[11]:


# export mesurements to tabular file
from openalea.rsml.measurements import RSML_Measurements
results = RSML_Measurements()
results.add(g)
RSML_Measurements.export_csv(g, 'results.csv')


# In[12]:


labels = g.property('label')
print(labels)
for rsml_file in files: 
    g = rsml.rsml2mtg(rsml_file)
    print(g)

    for v in g.vertices(scale=2):
        labels[v]='Axis'
    g.properties()['label']=labels

    g.display(display_id=True, display_scale=True)


# In[ ]:




