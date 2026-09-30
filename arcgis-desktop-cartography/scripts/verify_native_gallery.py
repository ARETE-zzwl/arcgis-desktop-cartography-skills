# -*- coding: ascii -*-
"""Reopen all MXDs/LYRs in a relocated synthetic package; Python 2.7."""
from __future__ import print_function
import argparse
import glob
import json
import os


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('root')
    p.add_argument('report')
    p.add_argument('--render',action='store_true')
    args=p.parse_args()
    import arcpy
    root=os.path.normcase(os.path.abspath(args.root))
    report=dict(maps=[],layer_files=0,broken_sources=[],external_sources=[],relative_paths=True)

    def check(layer):
        assert not layer.isBroken,layer.name
        if layer.supports('DATASOURCE'):
            source=os.path.normcase(os.path.abspath(layer.dataSource))
            assert source.startswith(root+os.sep), 'External source: '+layer.name

    for path in sorted(glob.glob(os.path.join(root,'maps','M*','*.mxd'))):
        mxd=arcpy.mapping.MapDocument(path)
        try:
            assert not arcpy.mapping.ListBrokenDataSources(mxd)
            layers=arcpy.mapping.ListLayers(mxd)
            for layer in layers:check(layer)
            frames=arcpy.mapping.ListDataFrames(mxd)
            for frame in frames:assert frame.spatialReference.factoryCode==32650
            if args.render:
                arcpy.mapping.ExportToPNG(mxd,os.path.splitext(path)[0]+'-relocated.png',resolution=300)
            report['maps'].append(dict(id=os.path.basename(path)[:-4],frames=len(frames),layers=len(layers)))
        finally:del mxd
        for filename in sorted(glob.glob(os.path.join(os.path.dirname(path),'*.lyr'))):
            layer=arcpy.mapping.Layer(filename)
            check(layer);report['layer_files']+=1;del layer
    assert len(report['maps'])==10
    with open(args.report,'w') as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
