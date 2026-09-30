# ArcMap automation patterns

## Template-first model

ArcMap automation is strongest when layout and symbology are authored ahead of time:

1. Prepare an MXD with the required page size, orientation, data frames, legend, scale bar, north arrow, text elements, and placeholders.
2. Assign unique element names.
3. Prepare `.lyr` files for important symbol systems and labels.
4. Copy the template or use `saveACopy`; never modify the system template.
5. Replace data sources, update text, set extent/scale, and export with `arcpy.mapping`.

Do not attempt to recreate every ArcMap UI operation through `arcpy.mapping`; it does not expose the entire ArcObjects surface.

If dataset inspection or geoprocessing stalls but map loading/export works, use the [tested recovery path](stalled-geoprocessing.md). Direct ArcObjects can create native feature layers, renderers and text elements without routing through `Describe`, KML conversion or geoprocessing. It is still ArcGIS authoring, not a replacement renderer.

## Minimal Python 2.7 pattern

```python
# -*- coding: utf-8 -*-
from __future__ import print_function

import arcpy
import os
import shutil

template = os.path.abspath("template.mxd")
output_mxd = os.path.abspath("output/map.mxd")
output_pdf = os.path.abspath("output/map.pdf")

if not os.path.isdir(os.path.dirname(output_mxd)):
    os.makedirs(os.path.dirname(output_mxd))

shutil.copyfile(template, output_mxd)
mxd = arcpy.mapping.MapDocument(output_mxd)
df = arcpy.mapping.ListDataFrames(mxd, "Main Map")[0]

# Prefer UpdateLayer with an authored .lyr for important symbology.
# Set df.extent or df.scale only after confirming the intended map purpose.

broken = arcpy.mapping.ListBrokenDataSources(mxd)
if broken:
    names = [item.name for item in broken]
    del df, mxd
    raise RuntimeError("Broken data sources: " + ", ".join(names))

mxd.save()
arcpy.mapping.ExportToPDF(
    mxd,
    output_pdf,
    resolution=600,
    image_quality="BEST",
    colorspace="RGB",
    compress_vectors=True,
    image_compression="DEFLATE",
    embed_fonts=True,
    georef_info=True
)

del df, mxd
print(output_pdf)
```

Check the exact ArcGIS 10.2 function signature before using optional export parameters. Remove optional arguments that the installed version does not support rather than switching Python environments.

## Layer and layout rules

- Add background and reference layers first; place the analytical layer and selection/annotation overlays above them.
- Use `AddLayer`, `InsertLayer`, or `UpdateLayer` based on whether ordering or authored symbology matters.
- Avoid relying on `ListDataFrames(...)[0]` or `ListLayoutElements(...)[0]` unless the template contract guarantees exactly one match.
- Set element names in ArcMap and address them by unique name.
- Use `findAndReplaceWorkspacePaths` or layer data-source replacement for staged/copied projects; validate every replacement.
- Do not silently skip missing inputs. Treat an optional decorative layer differently from a required analytical layer and report the omission.
- For shapefiles, require `.shp`, `.shx`, and `.dbf`; report a missing `.prj` as an unknown-CRS risk and preserve `.cpg` when present.
- Run `CheckGeometry_management` before geometry-sensitive analysis. If repair is necessary, copy the source first and run `RepairGeometry_management` only on the derived copy.
- Use `CheckExtension`, `CheckOutExtension`, and `CheckInExtension` for tools that require Spatial Analyst or another extension. Return the license in a `finally` block.

## Coordinate operations

- Inspect `Describe(path).spatialReference` before setting the data frame CRS.
- Define Projection changes CRS metadata only; use it solely when the stored coordinates' CRS is known.
- Project transforms vector geometry; Project Raster transforms rasters.
- Record the input CRS, output CRS, geographic transformation, resampling method, cell size, and snap raster where applicable.
- For overlay and raster alignment, set deliberate processing environments such as extent, cell size, snap raster, mask, and output coordinate system.

## Export choices

- Page-layout export: control detail with `resolution`.
- Data-frame export: control pixel detail with `df_export_width` and `df_export_height`; do not assume page-layout DPI behaves identically.
- PDF: prefer embedded fonts, vector compression, georeference information where useful, and lossless raster compression for publication masters.
- PNG: use as a review or screen artifact; request a world file only for a data-frame export intended as georeferenced raster output.
- TIFF: use lossless compression for journal or archive delivery and verify whether georeferencing is required.
- High transparency or rasterizing symbols can rasterize otherwise vector PDF content. Inspect the exported PDF rather than assuming it stayed vector.

## Verification contract

Before success:

1. Confirm required inputs with `arcpy.Exists` or `os.path.exists` as appropriate.
2. Check the output MXD with `ListBrokenDataSources`.
3. Reopen the saved MXD in a fresh process when practical.
4. Check output files are non-empty.
5. Render and inspect the final output at its intended physical size.
6. Compare known control locations, extent, scale, legend classes, and labels against the data.

## Official references

- [Guidelines for arcpy.mapping](https://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-mapping/guidelinesforarcpymapping.htm)
- [MapDocument](https://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-mapping/mapdocument.htm)
- [ListBrokenDataSources](https://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-mapping/listbrokendatasources.htm)
- [ExportToPDF](https://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-mapping/exporttopdf.htm)
- [ExportToPNG](https://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-mapping/exporttopng.htm)
- [Exporting your map](https://desktop.arcgis.com/en/arcmap/latest/map/map-export-and-print/exporting-your-map.htm)
