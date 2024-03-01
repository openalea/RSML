"""
Tests for the measurements module
"""
import rsml
from rsml import hirros

def get_mtg():
    fn = 'data/61_graph_expertized.rsml'
    g = rsml.rsml2mtg(fn)
    return g

def test_hirros_read():
    g = get_mtg()    
    
    assert(len(g) == 95)
    assert(g.max_scale() == 2)
    assert(g.nb_vertices(scale=1) == 5)

def test_observations():
    g = get_mtg()
    obs = hirros.times(g)
    assert(len(obs) == 18)
    assert(max(obs) <= 102)
    assert(min(obs)>= 0)
    
    plant_ids = g.vertices(scale=1)
    prims = hirros.primaries(g, plant_ids, obs)
 


def test1():
    "Returns secondary dataframe"




