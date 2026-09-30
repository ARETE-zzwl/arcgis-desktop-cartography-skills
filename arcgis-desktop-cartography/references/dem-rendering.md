# DEM rendering in ArcMap 10.2

Verified on 2026-09-30 with the native ArcObjects bridge described in `stalled-geoprocessing.md`. ArcMap rendered a float32 LZW GeoTIFF plus eight vector layers and editable page elements at 600 dpi. No Spatial Analyst extension or dataset geoprocessing calls were needed.

## Native raster layer

- Create `esriCarto.RasterLayer` as `IRasterLayer`; call `CreateFromFilePath` with the DEM path; add its `ILayer` to the map before vector context and samples.
- Use `RasterStretchColorRampRenderer`; set `IRasterRenderer.Raster`, call `Update`, select band 0, and assign an `IColorRamp`.
- Set `IRasterStretch.StretchType = esriRasterStretch_MinimumMaximum`, `Invert = False`; turn `IRasterStretch3.UseGamma` off for a linear elevation legend.
- Use `IRasterStretchMinMax.CustomStretchMin/Max` and `UseCustomStretchMinMax = True` for explicit limits. Choose limits from the displayed map extent, not distant elevations in a larger source mosaic. Call `Update` and assign `IRasterLayer.Renderer`.
- Province polygons must use a null fill (`esriSFSNull`) when they sit above the DEM; otherwise they obscure the terrain.
- Keep NoData distinct from zero elevation. If negative values share the lowest display color, label the endpoint accordingly and preserve the actual source values. Record source anomalies rather than silently treating them as valid relief or filling them for appearance.

## Continuous ramp and colorbar

`IPresetColorRamp` with 13 anchor colors produced 13 visible color bands on this installation, even with `Size = 256`. Use `IMultiPartColorRamp` containing adjacent `IAlgorithmicColorRamp` segments for a continuous ramp. A CIELab algorithm produced a smooth, low-saturation elevation scale.

```python
ramp = cc.CreateObject('esriDisplay.MultiPartColorRamp', interface=D.IMultiPartColorRamp)
for first, last in zip(anchors[:-1], anchors[1:]):
    part = cc.CreateObject('esriDisplay.AlgorithmicColorRamp', interface=D.IAlgorithmicColorRamp)
    part.FromColor, part.ToColor = colour(first), colour(last)
    part.Algorithm = D.esriCIELabAlgorithm
    part.Size = 32
    ramp.AddRamp(part.QueryInterface(D.IColorRamp))
ramp.Size = 256
assert ramp.CreateRamp()
```

CIELab ramp colors may not support `QueryInterface(IRgbColor)`. Convert with a separate `RgbColor` object's `RGB` property:

```python
rgb = cc.CreateObject('esriDisplay.RgbColor', interface=D.IRgbColor)
rgb.RGB = ramp.Color[i].RGB
channels = [rgb.Red, rgb.Green, rgb.Blue]
```

Build an editable page colorbar from the renderer's actual RGB entries, using `RectangleElement` / `IFillShapeElement` fills with null outlines. Use the same numeric limits for their positions and for tick labels. This is an elevation legend; do not replace it with a visually similar but differently normalized gradient image.

PDF renderers can show white antialiasing seams between adjacent rectangles even when PNG looks correct. A small overlap was insufficient in the tested PDF. The verified solution is to paint nested opaque rectangles in low-to-high color order: each begins at its own elevation position and extends to the common colorbar top. Later rectangles cover the preceding fill, so boundaries blend against the preceding color rather than the white page. Render the PDF itself to check this, not only the native PNG.

## Reopening and verification

- A reopened color ramp can report `Size = 0`, although ArcMap exports the DEM correctly. For a read-only palette check, set the in-memory ramp `Size = 256` before calling `CreateRamp`. Do not save this inspection document.
- CIELab colors changed by at most one 8-bit RGB channel level after persistence. Record that tolerance explicitly; do not claim bit-exact palette persistence. In the verified example, a relocated MXD nevertheless exported an identical PNG.
- Check custom limits, gamma, CRS, actual source paths, and standalone raster/vector LYR portability in a new process. Save each LYR with `IDataLayer2.RelativeBase` equal to its full output filename, as for vectors.
- DEM PDF exports correctly contain raster terrain plus vector overlays and embedded text. An all-vector requirement would be inappropriate.

## Terrain sources and resolution

Record tile URLs, HTTP source identifiers, download date, hashes, CRS, units, crop, land mask, and resampling. Mapzen Terrain Tiles GeoTIFFs are 512-pixel Web Mercator tiles; derive pixel size from the GeoTIFF transform rather than applying a 256-pixel slippy-map formula unmodified. The tested zoom-7 tiles list SRTM and GMTED in their source headers. A 500 m output grid is a cartographic resampling, not a claim that the underlying dataset is a native 500 m DEM.

Official references: [AWS Terrain Tiles](https://registry.opendata.aws/terrain-tiles/), [formats](https://github.com/tilezen/joerd/blob/master/docs/formats.md), [source attribution](https://github.com/tilezen/joerd/blob/master/docs/attribution.md).
