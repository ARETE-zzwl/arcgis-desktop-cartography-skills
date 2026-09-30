# -*- coding: ascii -*-
"""Export an existing MXD without dataset Describe or geoprocessing calls."""
from __future__ import print_function
import argparse
import json
import os
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mxd')
    parser.add_argument('output_directory')
    parser.add_argument('--dpi', type=int, default=600)
    args = parser.parse_args()
    path = os.path.abspath(args.mxd)
    out = os.path.abspath(args.output_directory)
    if not os.path.isfile(path) or args.dpi <= 0:
        parser.error('MXD must exist and DPI must be positive')
    if os.path.exists(out):
        parser.error('Use a new export directory; existing outputs are not overwritten')
    os.makedirs(out)
    started = time.time()

    def stage(value):
        print('%.3fs %s' % (time.time() - started, value))
        sys.stdout.flush()

    stage('BEFORE_IMPORT')
    import arcpy
    stage('BEFORE_MAP_OPEN')
    mxd = arcpy.mapping.MapDocument(path)
    try:
        broken = [layer.name for layer in arcpy.mapping.ListBrokenDataSources(mxd)]
        if broken:
            raise RuntimeError('Broken sources: ' + ', '.join(broken))
        frames = []
        for frame in arcpy.mapping.ListDataFrames(mxd):
            layers = []
            for layer in arcpy.mapping.ListLayers(mxd, '', frame):
                layers.append(dict(name=layer.name, visible=layer.visible,
                                   source=layer.dataSource if layer.supports('DATASOURCE') else None))
            frames.append(dict(name=frame.name, scale=frame.scale,
                               crs=frame.spatialReference.name,
                               epsg=frame.spatialReference.factoryCode,
                               extent=[frame.extent.XMin, frame.extent.YMin,
                                       frame.extent.XMax, frame.extent.YMax], layers=layers))
        outputs = []
        for extension, export in [('pdf', arcpy.mapping.ExportToPDF),
                                  ('png', arcpy.mapping.ExportToPNG),
                                  ('tif', arcpy.mapping.ExportToTIFF)]:
            stage('BEFORE_EXPORT_' + extension)
            destination = os.path.join(out, 'map.' + extension)
            options = dict(resolution=args.dpi)
            if extension == 'pdf':
                options.update(embed_fonts=True, georef_info=True)
            if extension == 'tif':
                options.update(tiff_compression='LZW')
            export(mxd, destination, **options)
            size = os.path.getsize(destination)
            if not size:
                raise RuntimeError('Empty export: ' + destination)
            outputs.append(dict(file=destination, bytes=size))
            stage('EXPORTED_' + extension)
    finally:
        del mxd
    fresh = arcpy.mapping.MapDocument(path)
    try:
        if arcpy.mapping.ListBrokenDataSources(fresh):
            raise RuntimeError('Sources broken after reopening')
    finally:
        del fresh
    report = dict(source_mxd=path, software=arcpy.GetInstallInfo(),
                  license=arcpy.ProductInfo(), frames=frames, broken_sources=[],
                  dpi=args.dpi, exports=outputs,
                  visual_inspection='Required separately; this script does not assess appearance.')
    with open(os.path.join(out, 'export_report.json'), 'w') as stream:
        json.dump(report, stream, indent=2)
    stage('ARCMAP_EXPORT_COMPLETE')
    return 0


if __name__ == '__main__':
    sys.exit(main())
