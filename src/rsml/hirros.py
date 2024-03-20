"""
Module that provide tools on 2D+t RSML-type MTG:
    * Get observation times : `times``
    * Extract primary lengths
    * Extract secondary lengths for each plant
"""
import argparse
from path import Path

import numpy as np
import pandas as pd

import rsml


def walk(dir: str, recursive=True):
    """ Traverse a set of directories and return rsml files.

    Notes : rsml files are defined by 61_graph*.rsml
    """
    dir = Path(dir)
    fns = []
    for rsml_file in ['61_graph_expertized.rsml', '61_graph.rsml']:
        rsmls = dir.glob(rsml_file)
        if rsmls : 
            fns.extend(rsmls)
        if recursive:
            rsmls = dir.glob('*/%s'%rsml_file)
            if rsmls : 
                fns.extend(rsmls)

    if not fns:
        print("ERROR: no rsml files found")
    
    final_fns = []
    for fn in fns:
        if (fn.parent/'80_graph_analysis.xlsx').exists():
            continue
        elif (fn.parent/'80_graph_expertized_analysis.xlsx').exists():
            continue
        else:
            final_fns.append(fn)
    return final_fns
    
def read(fn):
    g = rsml.rsml2mtg(fn)
    return g

def times(g):
    """Return Observation dates in hours."""
    obs_t = g._graph_properties['metadata']['observation-hours'].split(',')
    observations = [float(t) for t in obs_t]
    return observations

# Primary Length 

def primaries(g, plant_ids, obs):
    """ Return length of primary roots at various observation times. """
    prims = [next(g.component_roots_iter(pid)) for pid in plant_ids]
    seq = [sequence_length(g, obs, vid) for vid in prims]
    return seq


def secondary(g, pid, obs):
    """ Return the length of secondary roots through time of a given plant."""
    
    res = []
    for cid in g.components_iter(pid):
        if g.order(cid) >= 1:
            res.append(sequence_length(g, obs, cid))
    return res

def sequence_length(g, obs, vid):
    """ Return the length of a root at different observation times.
    """
    polyline = g.property('geometry')[vid]
    pos = np.array(polyline)
    time = g.property('time_hours')[vid]
    
    n = len(obs)
    obs_index = 0
    i = -1
    length_time = [] 
    
    for to in obs:
        index = -1
        for t in time:
            if t <= to:
                index+=1
            else:
                break
        
        if index == -1:
            length_time.append(0.)
        else:
            vec = np.diff(pos[:index+1],axis=0)**2
            sum_seg = vec.sum(axis=1)**.5
            length_time.append(sum_seg.sum())

    return length_time
    
def length_and_number(secondary):
    secs = np.array(secondary)
    total_length = secs.sum(axis=0)
    total_number = np.count_nonzero(secs, axis=0)

    return total_length.tolist(), total_number.tolist()


def dataframes(obs, primaries, secondaries):
    data = [obs]
    index=['time(h)']
    for i, p in enumerate(primaries):
        data.append(p)
        index.append('P%d'%(i+1))

    ps = np.array(primaries)
    _mean = ps.mean(axis=0)

    data.append(_mean)
    index.append('Mean')

    dfp = pd.DataFrame(data, index = index)

    #print(dfp)
    
    dfs= []

    for sec in secondaries:

        data = [obs]
        index=['time(h)']
        if not sec:
            continue
        #print('Secondary: ', sec)
        for i, p in enumerate(sec):
            data.append(p)
            index.append('R%d'%(i+1))

        tot_len, tot_num = length_and_number(sec)

        index.append('Total Length')
        data.append(tot_len)

        index.append('Total Number')
        data.append(tot_num)

        df = pd.DataFrame(data, index = index)
        dfs.append(df)

    return dfp, dfs

def write_xls(xls_file, dfp, dfs):


    if xls_file:
        with pd.ExcelWriter(xls_file, engine="xlsxwriter") as writer:  
            dfp.to_excel(writer, 
                        sheet_name='Prim',
                        float_format="%.2f", 
                        header = False)
            workbook  = writer.book
            bold_format = workbook.add_format({'bold': True})

            worksheet = writer.sheets['Prim']
            worksheet.set_row(0, None, bold_format)

            for i, df in enumerate(dfs):
                df.to_excel(writer, 
                            sheet_name='RP%d'%(i+1),
                            float_format="%.2f", 
                            header = False)
                worksheet = writer.sheets['RP%d'%(i+1)]
                worksheet.set_row(0, None, bold_format)

def write_xls_all(xls_file, primaries, secondaries):

    with pd.ExcelWriter(xls_file, engine="xlsxwriter") as writer:  
        startrow = 0
        for dfp in primaries:

            dfp.to_excel(writer, 
                        sheet_name='Prim',
                        float_format="%.2f", 
                        header = False,
                        startrow=startrow)
            workbook  = writer.book
            bold_format = workbook.add_format({'bold': True})

            worksheet = writer.sheets['Prim']
            worksheet.set_row(startrow, None, bold_format)

            startrow += len(dfp)+2

        for i in secondaries: 
            dfs = secondaries[i]
            startrow = 0
            for df in dfs:
                df.to_excel(writer, 
                            sheet_name='RP%d'%(i+1),
                            float_format="%.2f", 
                            header = False,
                            startrow=startrow)
                worksheet = writer.sheets['RP%d'%(i+1)]
                worksheet.set_row(startrow, None, bold_format)
                startrow += len(df)+2

def process(g):
    obs = times(g)

    plant_ids = g.vertices(scale=1)

    prims = primaries(g, plant_ids, obs)


    secondaries = []
    for pid in plant_ids:
        s2 = secondary(g, pid, obs)
        secondaries.append(s2)

    df_primary, df_secondaries = dataframes(obs, prims, secondaries)
    return df_primary, df_secondaries

def run(fn):
    g = read(fn)
    dfp, dfs =  process(g)

    # Write in xlsx
    if 'expertized' in fn:
        xlsx_file = fn.parent/'80_graph_expertized_analysis.xlsx'
    else: 
        xlsx_file = fn.parent/'80_graph_analysis.xlsx'
    write_xls(xlsx_file, dfp, dfs)

    print('WRITE %s'%xlsx_file)

def run_all(fns):

    prims = []
    secondaries = {}

    for fn in fns:
        g = read(fn)
        dfp, dfs =  process(g)
        prims.append(dfp)
        for i, df in enumerate(dfs):
            secondaries.setdefault(i, []).append(df)

    write_xls_all('gxe_results.xlsx', prims, secondaries)
    print('WRITE gxe_results.xlsx')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', default='.', help='directory to process')
    parser.add_argument('-r', default=True, type=bool, help='traverse the directories recursively')
    parser.add_argument('-f',  help='text file containing the list of directories to process')
    
    args = parser.parse_args()

    dir = args.d
    recursive = args.r
    gxe_file = args.f

    fns = []
    if gxe_file:
        print('GxE file to process', gxe_file)
        dirs = []
        with open('gxe.txt', 'r') as gxe:
            dirs = [d.strip() for d in gxe]
            dirs = [d for d in dirs if Path(d).exists()]

        for d in dirs: 
            rsml_files = walk(dir=d, recursive=recursive)
            fns.extend(rsml_files)

        print('Process files %s'%(' '.join(fns)))
        run_all(fns)
    else:
        fns = walk(dir=dir, recursive=recursive)
    
        if not fns:
            return
        
        if len(fns) == 1:
            fn = fns[0]
            print('Process file %s'%(fns[0]))
            run(fn)

        else:
            for fn in fns:
                print('Process file %s'%(fns[0]))
                run(fn)

    
    
if __name__=='__main__':
    fns = walk('set_de_5/230403VS004')
    g = read(fns[0])
    obs = times(g)

    plant_ids = g.vertices(scale=1)

    prims = primaries(g, plant_ids, obs)


    
    secondaries = []
    for pid in plant_ids:
        s2 = secondary(g, pid, obs)
        secondaries.append(s2)

    for s in secondaries:
        secs = np.array(s)
        total_length = secs.sum(axis=0)
        total_secs = np.count_nonzero(secs, axis=0)
        print(total_length)
        print(total_secs)
        print()

    # Write in xlsx
    write_xls('80_graph_analysis.xlsx', 
              obs, primaries=prims, secondaries=secondaries)