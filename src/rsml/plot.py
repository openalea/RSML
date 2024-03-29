""" Visualisation of an MTG computed from RSML

Visualisation:
1. PlantGL and Matplotlib
2. Time-series
3. Annotations

"""


def plot3d(g, color=None, img_dir='.'):
    import openalea.plantgl.all as pgl
    from copy import copy

    default_color = (177, 123, 6)
    colors = {}
    colors[0] = pgl.Color3.RED
    colors[1] = pgl.Color3.GREEN
    colors[2] = pgl.Color3.BLUE
    colors[3] = pgl.Color3.YELLOW
    colors[4] = pgl.Color3.CYAN
    colors[5] = pgl.Color3.WHITE
    colors[6] = pgl.Color3.BLACK

    if color is None:
        def my_color(vid):
            order = g.order(vid)
            return colors.get(order, default_color)
        color = my_color
    elif not callable(color):
        _color = copy(color)
        color = lambda x: _color

    section = pgl.Polyline2D([(0.5, 0), (0, 0.5), (-0.5, 0), (0, -0.5), (0.5, 0)])
    geoms = g.property('geometry')
    diams = g.property('diameter')

    def sweep(vid):
        _color = pgl.Material(color(vid))
        if diams and (vid in diams):
            diameters = diams[vid]
            if isinstance(diameters, (list, tuple)):
                _geom = pgl.Extrusion(
                    pgl.Polyline(list(map(pgl.Vector3, geoms[vid]))), 
                    section, 
                    pgl.Point2Array(list(zip(diams[vid], diams[vid])))
                )
            else:
                _geom = pgl.Extrusion(
                    pgl.Polyline(list(map(pgl.Vector3, geoms[vid]))), 
                    section,
                    pgl.Point2Array([(diameters, diameters) for i in range(len(geoms))])
                )

        else:
            _geom = pgl.Extrusion(
                pgl.Polyline(list(map(pgl.Vector3, geoms[vid]))), 
                section)

        return pgl.Shape(_geom, _color)
    scene = pgl.Scene([sweep(i) for i in geoms])
    pgl.Viewer.display(scene)
    return scene


def plot2d(g, img_file=None, axis=None, root_id=None, color=None, order=None, clear=True, **args):
    """ Plot MTG with grains on the initial image.

    :Parameters:
        - g : MTG with properties like 2D coordinates and grains.

    :Optional Parameters:
        - img_file : an array, or the filename, of an image to display in background
        - axis : matplotlib axis to display several plot in the same figure
        - root_id : if None, root_id is the first root of the MTG at scale=max_scale .
          Draw all the descendants of root_id. 
          root_id can also be a list of vertices.
        - order : draw only vertices of order 'order'
        - color: function or dict to define the color of each vertex. 
          Format is matplotlib colors (e.g. 'b', 'g', 'y', 'r')
    """  
    import numpy as np  
    from collections import Iterable
    from matplotlib import pyplot as plt

    if img_file is not None:
        if isinstance(img_file, str):
            image = plt.imread(img_file)
        else:
            image = img_file
        if axis:
            ax_img = axis.imshow(image) 
            axis.autoscale(enable=False)
        else:
            ax_img = plt.imshow(image) 
            plt.gca().autoscale(enable=False)

    ##{0:'r', 1:'g', 2:'b', 3:'y', 4:'c', 5: 'm', 6:'y', 7:'k'}
    colors = 'rgbycmyk'

    root_scale = g.max_scale()
    polylines = g.property('geometry')

    if root_id is None:
        vertices = list(polylines.keys())
    elif isinstance(root_id, Iterable):
        vertices = [v for r in root_id
                    for vr in g.component_roots_at_scale(r, scale=root_scale) 
                    for v in g.Descendants(vr)]
    else:
        vid = g.component_roots_at_scale(root_id, scale=root_scale)
        vertices = g.Descendants(vid)

    check_order = order is not None

    if axis: 
        plot_fct = axis.plot
    else:    
        plot_fct = plt.plot

    for v in vertices:
        _order = g.order(v)
        if check_order and _order != order:
            continue         

        _color = color(v) if color else colors[_order % len(colors)]  # .get(_order,'r')
        poly = np.array(polylines[v])          
        plot_fct(poly[:, 0], poly[:, 1], color=_color, marker='.')

    if img_file is None:
        if axis:
            ax = axis
        else:
            ax = plt.gca()
            ax.set_ylim(sorted(ax.get_ylim(), reverse=True))
        ax.axis('equal')


def multiple_plot(files, image=True):
    from openalea.core.path import path
    from matplotlib import pyplot as plt
    import rsml

    def get_file(f):    
        exts = ['.png', '.jpg', '.tif']
        fn = f.splitext()[0]
        for ext in exts:
            _f = path(fn + ext)
            if _f.exists():
                return _f 

    n = len(files)
    f, axes = plt.subplots(1, n, sharex=True, sharey=True)
    f.set_size_inches(7 * n, 5)
    for i in range(n):
        fn = files[i]
        g = rsml.rsml2mtg(fn)
        if image:
            plot2d(g, img_file=get_file(fn), axis=axes[i], ms=1)
        else:
            plot2d(g, axis=axes[i], ms=1)
    if not image:
        ax = axes[0]
        ax.set_ylim(ax.get_ylim()[::-1])
