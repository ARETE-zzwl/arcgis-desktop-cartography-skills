# Recover a stalled ArcMap workflow

Use this route when ArcGIS imports and has a license but a dataset inspection or processing call stops making progress. It is not a general replacement for working ArcPy geoprocessing.

## Separate the capabilities

Probe in separate processes, with flushed stage messages and a bounded wait:

1. Import ArcPy, report `ProductInfo()` and `GetInstallInfo()`.
2. Open a known-good MXD and check `ListBrokenDataSources`.
3. Export that MXD without dataset `Describe`, `GetCount`, KML conversion or clipping.
4. Test the suspected dataset operation separately on a small local input.

Do not infer that the renderer is broken from a stuck preflight. A Python `try/except` does not put a time limit on a native call that never returns. The bundled supervisor runs only the requested worker, retains its output, and stops that child on timeout; it does not terminate user ArcMap sessions. It is intended for standalone workers that do not launch their own process trees.

The 2026-09-30 checks on this machine found:

| Probe | Observed result |
| --- | --- |
| ArcPy import, ArcInfo license | Passed |
| `arcpy.env.overwriteOutput`, EPSG:4326 construction | Passed in a fresh process |
| `arcpy.Describe` on a 42-point local shapefile | Did not return within 45 seconds |
| `GetCount` on the same shapefile without `Describe` | Did not return within 30 seconds |
| Existing eight-layer MXD export | PDF, PNG and TIFF completed in about 7 seconds |
| Native ArcObjects rebuild from shapefiles | Editable MXD and eight LYR files plus exports completed in about 9 seconds |
| Reopen after relocation and export again | Passed; MXD sources resolved in the new folder |

The failing call is isolated; these tests do not establish why its underlying native implementation hangs. Do not claim a repaired installation or that all geoprocessing tools have been restored. No registry, license, system template or ArcGIS installation files need changing for the tested map recovery.

## Existing MXD: export directly

Run the supervisor with a Python 3 interpreter. Pass the licensed ArcMap Python 2.7 executable explicitly with `--python`:

```powershell
& '<python3.exe>' '<skill-dir>\scripts\run_arcmap_checked.py' --python '<arcmap-python.exe>' --timeout 120 --log '<project>\export.log' '<skill-dir>\scripts\arcmap_export.py' '<project>\map.mxd' '<project>\exports_new' --dpi 600
```

The output directory must not already exist. The worker exports `map.pdf`, `map.png`, `map.tif` and `export_report.json`. It embeds PDF fonts, uses lossless LZW TIFF and records layer sources, display CRS, extent, scale and broken-source status. It does not modify the input MXD or perform geometry analysis. Inspect the image yourself; successful export is not a visual-quality check.

Do not add a `Describe` or `GetCount` call ahead of this exporter as a mandatory preflight when that is the operation being diagnosed.

## New layout or symbols: native ArcObjects

When the template does not already contain the required symbols or text, use ArcObjects within the same licensed 32-bit ArcGIS Python process. This avoids KML conversion solely as a way to manufacture editable symbology.

The tested bridge is `comtypes==1.1.7`, compatible with Python 2.7. Keep a verified source distribution and its license in a task-local vendor directory and add that directory to `sys.path`. Do not install a modern Python-3-only comtypes version into ArcGIS or replace system packages. Ensure the generated wrapper cache is writable. Pass the installation type-library directory explicitly; do not preserve a personal installation path.

Core calls used by the verified build:

```python
# Python 2.7; comtypes_root is the directory containing the comtypes package.
import os
import sys
sys.path.insert(0, comtypes_root)
import arcpy
import comtypes.client as cc

com = os.path.join(arcpy.GetInstallInfo()['InstallDir'], 'com')
C = cc.GetModule(os.path.join(com, 'esriCarto.olb'))
D = cc.GetModule(os.path.join(com, 'esriDisplay.olb'))
G = cc.GetModule(os.path.join(com, 'esriGeometry.olb'))
DB = cc.GetModule(os.path.join(com, 'esriGeoDatabase.olb'))
doc = cc.CreateObject('esriCarto.MapDocument', interface=C.IMapDocument)
doc.Open(template_mxd, '')
mp = doc.Map[0]  # Only for a template verified to have one map.
factory = cc.CreateObject('esriDataSourcesFile.ShapefileWorkspaceFactory',
                          interface=DB.IWorkspaceFactory)
workspace = factory.OpenFromFile(shapefile_directory, 0).QueryInterface(DB.IFeatureWorkspace)
feature = cc.CreateObject('esriCarto.FeatureLayer', interface=C.IFeatureLayer)
feature.FeatureClass = workspace.OpenFeatureClass('observations.shp')
layer = feature.QueryInterface(C.ILayer)
layer.Name = 'Observations'
mp.AddLayer(layer)

# Author explicit renderers and layout elements before saving; default styles
# are not a publication-ready map. See the interface recipe below.
doc.SaveAs(output_mxd, True, False)  # Relative paths; do not overwrite the template.
doc.Close()
del doc, mp, feature, layer, workspace
```

Native interface recipe:

- CRS: `SpatialReferenceEnvironment` / `ISpatialReferenceFactory`; set map `SpatialReference`. For control points, assign the verified input CRS to `IGeometry`, then call `Project(output_crs)`. Changing the map display CRS does not rewrite source coordinates.
- Symbols: `ISimpleRenderer.Symbol`, assigned via `IGeoFeatureLayer.Renderer`; construct `ISimpleFillSymbol`, `ISimpleLineSymbol` or `ISimpleMarkerSymbol` explicitly. Use `RgbColor` through `IColor`.
- Layers: `ILayerFile.New`, `ReplaceContents`, `Save`, `Close`. Before saving, set `layer.QueryInterface(C.IDataLayer2).RelativeBase` to the **full destination LYR filename**, not merely its directory. The tested form is `os.path.join(out_dir, layer.Name + '.lyr')`. Leaving it unset retained absolute staging paths; supplying only the directory introduced an extra directory component on relocation. Setting the full filename passed relocation checks for all eight layers. Verify individual LYR source paths separately from the MXD when packaging.
- Layout: obtain `IGraphicsContainer` from `doc.PageLayout`; locate the map frame using `FindFrame(mp)`. Set frame geometry in the template's page units. Inspect the units rather than assuming points or millimetres.
- Text: create `ITextElement`, `ITextSymbol` and `StdFont`, set font, colour and anchor explicitly, then add the element. `esriTHALeft` and `esriTVABottom` prevent an unintended centred anchor from clipping a title against the page edge.
- Extent: project the intended geographic bounds, allow for the frame aspect ratio, then set `IActiveView.Extent`.
- Point symbols: an X with a white outline can disappear on a light background. Set both its colour and outline deliberately and inspect the export.

Close the native document before reopening it with `arcpy.mapping.MapDocument` for export. Avoid calling unrelated geoprocessing functions in between.

## Portability and acceptance

- Use a new project output folder and preserve the input MXD, data and system template.
- Keep `.shp`, `.shx`, `.dbf` and verified `.prj` companions together; retain `.cpg` when present. Stage only needed inputs under a short ASCII path if path compatibility is in question.
- A final MXD must open in a fresh process with no broken sources. After copying the project, verify every actual layer source resolves into the delivery folder, not a still-existing staging folder.
- Check LYR files independently; a working MXD does not prove each standalone LYR is portable.
- Check vector PDF content, embedded fonts, PNG/TIFF pixel dimensions and resolution, nonblank content, all intended point classes, label placement and final-size readability.
- Missing `locale/codepage/936.txt` warnings did not prevent the tested English map from rendering. They do not prove Unicode/Chinese attribute conversion works. Test actual non-ASCII attributes separately before using them; do not copy unrelated mapping files into the installation.
- Keep timeout logs alongside successful logs. Report successful map recovery separately from any remaining geoprocessing limitation.

## API references

The installed 10.2 type libraries are the runtime authority. Esri's documentation describes [IDataLayer2.RelativeBase](https://desktop.arcgis.com/en/arcobjects/10.7/net/IDataLayer2_RelativeBase.htm) and the [native layer-file lifecycle](https://desktop.arcgis.com/en/arcobjects/10.7/net/SaveLayerFile.htm); the full-filename rule above was verified on this installation rather than inferred solely from the later-version documentation.
