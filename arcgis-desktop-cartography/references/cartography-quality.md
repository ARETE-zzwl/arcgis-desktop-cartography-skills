# Cartography quality guide

## Decide whether to map

Use a map when location, adjacency, direction, distance, terrain, spatial pattern, or regional context is part of the claim. Prefer a chart when the main task is comparing magnitudes, ranks, distributions, model skill, or time series across named places.

## Define the visual argument

Before styling, state:

- the single main claim;
- intended audience and final physical size;
- analytical layer versus contextual layers;
- projection and why it fits the claim;
- units, classification, normalization, and uncertainty;
- source date, coverage gaps, and provenance;
- which content is measured, derived, modeled, inferred, schematic, or decorative.

## Choose the map family intentionally

- Choropleth: normalized rates, ratios, or densities tied to areas; do not map raw totals when area/population differences make them misleading.
- Graduated symbols: magnitude at locations or regions when preserving totals matters.
- Dot/point map: locations or counts when overlap is manageable.
- Isoline/raster field: continuous environmental or atmospheric surfaces.
- Flow map: origin-destination or directional movement; control occlusion and explain width/direction encoding.
- Small multiples: comparison across time, scenario, model, or variable when one map would overload the legend.

## Establish hierarchy

Typical bottom-to-top order:

1. page/background;
2. land/water or quiet reference surface;
3. terrain/hillshade or imagery;
4. minor contextual boundaries and hydrography;
5. major boundaries and reference features;
6. primary analytical raster or polygons;
7. primary lines, points, study areas, and selections;
8. labels and annotations;
9. layout surrounds.

Adjust order to the claim. The primary analytical layer must remain visible; a decorative basemap must not compete with it.

## Color and symbols

- Use sequential schemes for ordered magnitude, diverging schemes around a meaningful midpoint, and qualitative schemes for unordered categories.
- Avoid rainbow palettes for ordered data.
- Do not use hue for a variable that is only magnitude unless the legend makes the order unambiguous.
- Avoid red/green-only critical distinctions; add shape, line pattern, outline, or direct labels when feasible.
- Keep polygon boundary weight subordinate to fill unless boundaries are the subject.
- Use transparency carefully: it can obscure color meaning and force vector exports to rasterize.
- Ensure uncertainty is visible rather than hidden in the caption alone.

## Labels and typography

- Establish a label priority order and remove labels that do not support the map's purpose.
- Use a legible font family with a small number of weights and sizes.
- Apply halos selectively over complex backgrounds.
- Keep units and significant digits consistent.
- Direct-label important features when it reduces legend lookup.
- Inspect collisions, clipping, ambiguous leader lines, and text at final print size.

## Projection and scale

- Choose equal-area projections for area comparisons, conformal projections when local shape/angle matters, and local projected CRSs for metric analysis.
- Avoid Web Mercator for area comparison.
- State when distortion is material to interpretation.
- Use scale-dependent generalization and label density. Detail appropriate at one scale may be clutter at another.

## Layout and context

- Use a concise title that states subject, place, and time where needed.
- Include legend, scale bar, north arrow, graticule, inset, and source note only when they add information.
- Keep legend order consistent with layer order and visual order.
- Mark the mapped extent in an inset only when the audience lacks geographic context.
- Reserve margins and whitespace; avoid filling every area of the page.

## Review checklist

- Is a map necessary for this claim?
- Is the projection appropriate and documented?
- Are values normalized correctly?
- Does the visual hierarchy reveal the intended message first?
- Can important categories be distinguished without color alone?
- Are sources, time, units, missing data, and uncertainty visible?
- Are labels and legend readable at final size?
- Are map extent, scale, and known locations correct?
- Did export change fonts, symbols, colors, transparency, or vector content?
- Does the editable MXD reproduce the delivered output without broken sources?

## External skill patterns consulted

- [OpenAI geospatial and cartographic visualization skill](https://github.com/openai/plugins/blob/main/plugins/build-web-data-visualization/skills/geospatial-and-cartographic-visualization/SKILL.md): map-or-not decision, source/method ledger, projection and normalization checks.
- [Mapbox cartography skill](https://github.com/mapbox/mapbox-agent-skills/blob/main/skills/mapbox-cartography/SKILL.md): visual hierarchy, layer ordering, color accessibility, typography, and medium-specific review.

Apply the cartographic principles without importing their WebGIS or Mapbox-specific implementation stack into ArcMap.
