---
name: arcgis-desktop-cartography
description: Create, inspect, repair and export ArcMap/ArcGIS Desktop scientific maps with native MXD/LYR files and Python 2.7 ArcPy. Covers DEM, coordinate checks, thematic and journal map design, relative-path handoffs and stalled geoprocessing recovery. Includes a 30-paper design index and 10 native synthetic map examples. Do not treat legacy ArcMap as ArcGIS Pro.
---

# ArcGIS Desktop Cartography

Produce reproducible ArcMap 10.2 maps without confusing legacy ArcPy with ArcGIS Pro. Protect source data, make coordinate decisions explicit, use template-driven automation, and verify both GIS correctness and visual quality.

## Route the task

1. Decide whether geography is part of the reasoning. Use a chart or table when the task is mainly ranking, distribution, model skill, or time-series comparison.
2. Use the local ArcMap path for MXD, ArcGIS Desktop 10.x, `arcpy.mapping`, legacy ArcToolbox, or the existing licensed installation.
3. For an explicit ArcGIS Pro/APRX request, first locate ArcGIS Pro and its conda environment. Use `arcpy.mp` and Python 3 only if Pro is actually installed. Never run Pro code in the ArcMap Python environment.
4. Prefer GeoPandas/GDAL/QGIS for portable or modern batch processing only when the user asks for portability, ArcMap cannot perform the task reliably, or no ArcGIS license is available. Do not install or migrate tools without authorization.
5. Use Cartopy/Matplotlib or R for publication statistical panels and meteorological fields when editable GIS objects are not needed.

Read [references/local-environment.md](references/local-environment.md) before using the target licensed ArcGIS installation. Read [references/arcmap-automation.md](references/arcmap-automation.md) when creating or editing MXD/LYR files or writing ArcPy. Read [references/cartography-quality.md](references/cartography-quality.md) whenever designing, styling, or reviewing a map.

For paper-inspired maps, read [journal-map-recipes.md](references/journal-map-recipes.md) and select M01–M10. Use [literature-30.md](references/literature-30.md) for figure-level provenance: 28 direct software statements and 2 explicitly limited mixed/resource records. Do not attribute every chart in a paper to ArcGIS. The companion JSON/BibTeX support citation reuse; publisher figures and full texts are not bundled.

To reproduce the editable examples, follow [native-gallery.md](references/native-gallery.md). Check [data-contracts-and-review.md](references/data-contracts-and-review.md) before adapting them to real data. All bundled surfaces, points and networks are synthetic design fixtures, not observations or reproduced research results. Read [release-hygiene.md](references/release-hygiene.md) before sharing binary MXD/LYR files.

If a preflight, `Describe`, or geoprocessing call stalls, read [references/stalled-geoprocessing.md](references/stalled-geoprocessing.md). Test map export separately before concluding that ArcGIS cannot draw. The reference environment has a verified native ArcObjects authoring plus `arcpy.mapping` export path that does not require the stalled dataset calls.

For a DEM background with an editable elevation colorbar, read [references/dem-rendering.md](references/dem-rendering.md). It covers verified native raster rendering, continuous ramps, and colorbar consistency checks.

## Execute the workflow

### 1. Define the result

- State assumptions that affect data, extent, projection, symbology, or output.
- Convert the request into a short plan with verifiable success criteria.
- Identify the map's purpose, audience, medium, page size, required layers, target CRS, extent, and deliverables.
- Ask only when a missing choice would materially change the map or analysis.

### 2. Inventory before modification

- Verify executable, Python, ArcPy, template, input, and output paths.
- Check out only the ArcGIS extensions required by the requested tools, verify availability first, and check them back in from a `finally` block.
- Run the bundled preflight in a bounded worker. The supervisor uses Python 3; the worker still uses the licensed ArcGIS Python 2.7. Use a fresh log path for each attempt:

```powershell
& '<python3.exe>' '<skill-dir>\scripts\run_arcmap_checked.py' --python '<arcmap-python.exe>' --timeout 60 --log '<project>\preflight.log' '<skill-dir>\scripts\arcmap_preflight.py' '<input.mxd>'
```

- Record for each input: source/provenance, license if relevant, date/version, units, data type, CRS, extent, resolution or scale, NoData/missing values, and whether the layer is measured, derived, inferred, or decorative.
- Preserve source files. Write derived data and maps to a project output or English-only staging directory.
- Check shapefile companion files and vector geometry. Repair geometry only on a derived copy after reporting what will change.
- Dataset preflight calls `Describe` and `GetCount`; MXD preflight does not. On timeout, retain the log and isolate the failing operation. Do not run repeated unbounded retries or kill unrelated ArcMap/Python processes.

### 3. Resolve coordinate systems safely

- Never assign EPSG:4326 merely because coordinates look like longitude/latitude.
- Use Define Projection only to attach a CRS that is already known to describe the stored coordinates. It does not transform geometry.
- Use Project for vector coordinate transformation and Project Raster for rasters. Select and document any required geographic transformation.
- Use a suitable projected CRS for distance, area, buffering, density, and scale-sensitive analysis. Do not calculate metric results in degrees.
- Check several known locations or bounds after transformation.

### 4. Build with templates and styles

- Copy an existing MXD template; never overwrite the system template or an input MXD.
- Prefer a pre-authored MXD/LYR containing layout elements and approved symbols. `arcpy.mapping` manipulates existing objects but cannot fully author every ArcMap layout or symbol property.
- Give data frames, layers, legends, titles, scale bars, north arrows, and other layout elements unique names before automation.
- Use project-specific Python 2.7 code with absolute paths and `os.path`. Set processing environments only when the requested geoprocessing requires them; exporting an MXD does not require `arcpy.env.overwriteOutput`. Do not use f-strings, `pathlib`, type annotations, or `arcpy.mp` in the ArcMap worker.
- Add layers in an intentional bottom-to-top hierarchy. Apply `.lyr` symbology or `UpdateLayer` when visual consistency matters.
- Use `saveACopy` or copy the template first. Release `MapDocument`, cursors, and layer references with `del`.

### 5. Design the map

- Make the analytical layer visually dominant and keep the basemap quiet.
- Choose the map family and projection to match the claim; document classification and normalization for choropleths.
- Encode important distinctions with at least one non-color cue when feasible. Avoid red/green-only distinctions.
- Limit labels to information that supports the claim; establish label priority and inspect overlap at final size.
- Include only meaningful context and surrounds. Do not add a north arrow, graticule, inset, or scale bar by habit.
- Separate measured, modeled, uncertain, and schematic content visibly.

### 6. Export deliberately

- Preserve an editable MXD and any `.lyr` files needed to reproduce styling.
- Export the page layout to PDF for vector-friendly publication output. Embed fonts and retain georeferencing when appropriate.
- Use RGB for screens and ordinary office output; use CMYK only when the print workflow requires it.
- Export PNG for preview and TIFF for raster publication delivery. Use lossless compression when required.
- Treat 300 dpi as a normal print baseline and 600 dpi as a common journal-map target, not a substitute for correct page size or legible symbols.
- For an existing MXD, `scripts/arcmap_export.py` exports PDF/PNG/TIFF, records frame/layer sources and reopens the project without calling dataset `Describe` or geoprocessing. Run it through the bounded supervisor and choose a new output directory. See the recovery reference for the tested command.

### 7. Verify the result

- Require a zero script exit code and non-empty outputs.
- Re-run preflight on the output MXD and fail validation if `ListBrokenDataSources` returns any layer.
- Confirm layer count/order, CRS, extent, scale, units, field use, classification, output dimensions, fonts, and expected formats.
- When delivering standalone `.lyr` files, relocate and inspect them as well as the MXD. Native layer-file saves need an explicit relative base; see the recovery reference for the tested full-filename setting.
- Render and inspect at least one final export. Check blank output, clipping, rasterization, missing symbols, mojibake, label collisions, legend mismatch, weak hierarchy, color ambiguity, and small-text readability.
- Compare several known geographic locations against a trusted reference.
- Keep the editable MXD and list remaining manual ArcMap refinements instead of claiming publication readiness when only default symbology was produced.

## Deliver the handoff

Report:

- the ArcGIS/Python environment actually used;
- source inputs and any English-path staging copies;
- script, MXD, LYR, and exported-file paths;
- CRS and transformation decisions;
- classification, normalization, and symbology decisions;
- validation results and any manual refinements still required.

Do not report success until the artifacts exist and both technical and visual checks pass.
