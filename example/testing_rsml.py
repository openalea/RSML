###############################################################################
# F. Bauget 2020-06-12
# testing import of rsml file
###############################################################################

# from random import _hexlify, _urandom

import numpy as np
import rsml
from rsml.continuous import *
from openalea.mtg import MTG, traversal


def my_toporder(g, scale):
  # F. Bauget 2020-03-18 : testing RSML continuous from rsml2mtg()  to hydroroot disctrete copied from rsml.continuous
    """ Return the list of `g` vertices at scale `scale` in topological order """
    axes = []
    list(map(axes.extend,(traversal.pre_order2(g,vid)
                          for vid in g.vertices(scale=scale)
                          if not g.parent(vid))))
    return axes

def my_continuous_to_discrete(g_c, segment_length = 1.0e-4, resolution = 1.0e-3):
    # F. Bauget 2020-03-18 : testing RSML continuous from rsml2mtg()  to hydroroot disctrete copied from rsml.continuous
    """ Convert mtg `g` from continuous to discrete form **in-place**

    Does the reverse of `discrete_to_continuous`:
      - Add a sequence of segments to all axes from their `geometry` attribute

    todo:
      - functions
    """


    geometry = g_c.property('geometry')
    parent_node = g_c.property('parent-node')
    _order = 0 # _order = 0 => 1st axe <=> primary root

    g = MTG()
    rid = seg = g.add_component(g.root)

    rnid = g.node(rid)
    rnid.base_length = 0.
    rnid.length = segment_length
    rnid.label = 'S'
    rnid.order = _order


    axe_segments = {}

    for axe in my_toporder(g_c, g_c.max_scale()):
        # get segment on parent branch
        p_axe = g_c.parent(axe)
        v = axe
        _order = 0
        while g_c.parent(v) is not None:
            v = g_c.parent(v)
            _order += 1

        # create 1st segment
        # position = geometry[axe]

        if p_axe is not None:
            pos_axe = np.array(geometry[p_axe])
            vec_axe = np.diff(pos,axis=0)**2
            _length_axe = np.sqrt(np.sum(vec_axe, axis = 1))*resolution
        pos = np.array(geometry[axe])
        vec = np.diff(pos,axis=0)**2
        _length = np.sqrt(np.sum(vec, axis = 1))*resolution

        if axe in parent_node:
            # p_seg = axe_segments[(p_axe, parent_node[axe])]
            # seg = g.add_component(axe, edge_type = '/', position = position[1])
            # g.add_child(p_seg, seg, edge_type = '+')
            # axe_segments[(axe, 0)] = p_seg
            shift = 1
        else:
            if _order == 0:
                for j in range(int(_length[0]/segment_length)):
                    seg = g.add_child(seg, edge_type='<', label = 'S', length = segment_length, order = _order)
            else:
                min = 1.0e10
                for i, p in enumerate(pos_axe):
                    # search for the smallest distance between each nodes of p_axe and the 1st node of the child
                    distance = np.sqrt((p[0] - pos[0][0])**2.0+(p[1] - pos[0][1])**2.0)
                    if distance < min:
                        min = distance
                    elif i > 1:
                        break

                seg = axe_segments[(p_axe, i - 1)] # branching vertex on parent axe

                seg = g.add_child(seg, edge_type='+', label = 'S', length = segment_length, order = _order)
                for j in range(int(_length[0]/segment_length)-1):
                    seg = g.add_child(seg, edge_type='<', label = 'S', length = segment_length, order = _order)
            # if first:
            #     seg = g.add_component(axe, edge_type = '>', position = position[0])
            #     first = False
            # else:
            #     seg, u2 = g.add_child_and_complex(axe, edge_type='+', position=position[0])
            #     g.node(u2).label = 'I'+str(axe)
            #     g.node(u2).edge_type = '+'
            shift = 0
        axe_segments[(axe, shift)] = seg

        # create the other segments
        for i, l in enumerate(_length[(1 + shift):]):
            for j in range(int(l/segment_length)):
                seg = g.add_child(seg, edge_type = '<', label = 'S', length = segment_length, order = _order)
            axe_segments[(axe, i + 1)] = seg

        shift = 0

        # geometry.pop(axe)
        # parent_node.pop(axe, None)

    return g

if __name__ == '__main__':
    g_c = rsml.rsml2mtg('data/arabidopsis-simple.rsml')
    g = my_continuous_to_discrete(g_c)
    # g = continuous_to_discrete(g_c)


