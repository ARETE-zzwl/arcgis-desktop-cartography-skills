# Target ArcGIS environment

## Discover the licensed installation

This skill has been tested with ArcMap 10.2, an ArcInfo license, 32-bit Python 2.7.18 and NumPy 1.16.6. These are reference test results, not assertions about the reader's machine. Personal installation and project paths have been removed.

Locate and verify the following, then pass them explicitly to the scripts:

|Parameter|Meaning|
|---|---|
|`--python`|The licensed 32-bit ArcMap Python 2.7 executable|
|`--com`|The installation's `com/` directory containing ArcObjects type libraries|
|`--vendor`|A task-local comtypes 1.1.7 source directory|
|`--data`, `--out`|Project-owned input and new output directories|

The example generator creates a clean A4 landscape document from scratch. When adapting an existing user template for other tasks, inspect its saved paths and historical metadata before sharing; even a vendor-supplied blank template can retain old machine-specific references.

Use a bounded worker for environment probes as well as data work. Within the licensed worker, `arcpy.GetInstallInfo()` and `arcpy.ProductInfo()` identify the product; keep logs private because installation paths may be included. Runtime parameters belong in a project-local configuration, not hardcoded into a public skill.

## Compatibility constraints

- Use Python 2.7 syntax and `arcpy.mapping`; Pro uses Python 3 and `arcpy.mp`.
- Use a standalone MXD path rather than `MapDocument("CURRENT")` outside ArcMap.
- Do not mix 64-bit background-geoprocessing Python with a 32-bit ArcObjects authoring process.
- Prefer a short ASCII staging path when diagnosing old code-page failures. Do not rewrite the installation, registry or licensing files as a speculative fix.
- Helper processes should be hidden; open a visible ArcMap window only when the user needs to inspect or edit it interactively.

## Verified behavior and known limits

The 2026-09-30 reference tests separated dataset operations from map rendering. In fresh processes, a shapefile `Describe` stalled beyond 45 seconds and `GetCount` beyond 30 seconds, while imports, map inspection, ArcObjects authoring and `arcpy.mapping` export succeeded. This isolates a failure; it does not identify its cause or prove geoprocessing is repaired.

The journal example build produced 10 native MXDs, 17 data frames and 41 LYR files. The synthetic bundle was copied to an independent directory and reopened after removing the neutral build-drive mapping; every source resolved inside the relocated bundle. See [native-gallery.md](native-gallery.md) and [validation-report.md](validation-report.md).

The reference installation emits a missing `locale/codepage/936.txt` warning. ASCII fields and labels were verified. Chinese attribute conversion and fonts remain unverified; do not invent a replacement code-page table or suppress the warning as proof of success.
