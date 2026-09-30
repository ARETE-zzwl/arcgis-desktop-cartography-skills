# -*- coding: utf-8 -*-
"""Read-only ArcGIS Desktop 10.x environment and dataset preflight.

Run with the ArcGIS Python 2.7 interpreter, not system Python 3:
    <arcmap-python.exe> arcmap_preflight.py [PATH ...]
"""
from __future__ import print_function

import json
import os
import platform
import sys
import traceback

import arcpy


def safe_attr(value, attribute, default=None):
    try:
        return getattr(value, attribute)
    except Exception:
        return default


def safe_text(value):
    if value is None:
        return None
    try:
        if isinstance(value, unicode):
            return value
        if isinstance(value, str):
            try:
                return value.decode("mbcs")
            except UnicodeDecodeError:
                return value.decode("utf-8", "replace")
        return unicode(value)
    except NameError:
        return str(value)
    except Exception:
        return repr(value)


def has_non_ascii(path):
    try:
        if isinstance(path, unicode):
            path.encode("ascii")
        else:
            path.decode("ascii")
        return False
    except (UnicodeEncodeError, UnicodeDecodeError):
        return True


def spatial_reference_info(spatial_reference):
    if spatial_reference is None:
        return None
    return {
        "name": safe_text(safe_attr(spatial_reference, "name")),
        "type": safe_text(safe_attr(spatial_reference, "type")),
        "factory_code": safe_attr(spatial_reference, "factoryCode"),
        "linear_unit": safe_text(safe_attr(spatial_reference, "linearUnitName")),
        "angular_unit": safe_text(safe_attr(spatial_reference, "angularUnitName")),
    }


def extent_info(extent):
    if extent is None:
        return None
    return {
        "xmin": safe_attr(extent, "XMin"),
        "ymin": safe_attr(extent, "YMin"),
        "xmax": safe_attr(extent, "XMax"),
        "ymax": safe_attr(extent, "YMax"),
    }


def inspect_mxd(path):
    mxd = arcpy.mapping.MapDocument(path)
    try:
        frames = []
        layer_count = 0
        for frame in arcpy.mapping.ListDataFrames(mxd):
            layers = arcpy.mapping.ListLayers(mxd, "", frame)
            layer_count += len(layers)
            frames.append({
                "name": safe_text(safe_attr(frame, "name")),
                "scale": safe_attr(frame, "scale"),
                "spatial_reference": spatial_reference_info(safe_attr(frame, "spatialReference")),
                "extent": extent_info(safe_attr(frame, "extent")),
                "layers": [safe_text(safe_attr(layer, "name")) for layer in layers],
            })
        broken = [safe_text(item.name) for item in arcpy.mapping.ListBrokenDataSources(mxd)]
        return {
            "kind": "mxd",
            "data_frames": frames,
            "layer_count": layer_count,
            "broken_data_sources": broken,
        }
    finally:
        del mxd


def inspect_dataset(path):
    desc = arcpy.Describe(path)
    item = {
        "kind": "dataset",
        "data_type": safe_text(safe_attr(desc, "dataType")),
        "catalog_path": safe_text(safe_attr(desc, "catalogPath", path)),
        "spatial_reference": spatial_reference_info(safe_attr(desc, "spatialReference")),
        "extent": extent_info(safe_attr(desc, "extent")),
    }

    for attribute in ("shapeType", "bandCount", "width", "height", "meanCellWidth", "meanCellHeight"):
        if hasattr(desc, attribute):
            item[attribute] = safe_attr(desc, attribute)

    try:
        fields = [
            {"name": safe_text(field.name), "type": safe_text(field.type)}
            for field in arcpy.ListFields(path)
        ]
        item["field_count"] = len(fields)
        item["fields"] = fields[:50]
        item["fields_truncated"] = max(0, len(fields) - 50)
    except Exception:
        pass

    try:
        item["count"] = int(arcpy.GetCount_management(path).getOutput(0))
    except Exception:
        pass

    if path.lower().endswith(".shp"):
        base = path[:-4]
        components = {}
        for extension in (".shp", ".shx", ".dbf", ".prj", ".cpg"):
            components[extension] = os.path.exists(base + extension)
        item["shapefile_components"] = components
        item["required_components_missing"] = [
            extension for extension in (".shp", ".shx", ".dbf")
            if not components[extension]
        ]
        item["projection_file_missing"] = not components[".prj"]

    return item


def inspect_path(path):
    result = {
        "path": safe_text(os.path.abspath(path)),
        "non_ascii_path": has_non_ascii(path),
        "exists": bool(os.path.exists(path) or arcpy.Exists(path)),
    }
    if not result["exists"]:
        result["error"] = "Path does not exist"
        return result

    try:
        if path.lower().endswith(".mxd"):
            result.update(inspect_mxd(path))
        else:
            result.update(inspect_dataset(path))
    except Exception as exc:
        result["error"] = safe_text(exc)
        result["traceback"] = traceback.format_exc()
    return result


def main(argv):
    install_info = arcpy.GetInstallInfo()
    report = {
        "environment": {
            "python_executable": safe_text(sys.executable),
            "python_version": safe_text(platform.python_version()),
            "architecture": safe_text(platform.architecture()[0]),
            "arcgis_product_info": safe_text(arcpy.ProductInfo()),
            "arcgis_install_info": dict((safe_text(key), safe_text(value)) for key, value in install_info.items()),
        },
        "inputs": [inspect_path(path) for path in argv],
    }

    print(json.dumps(report, ensure_ascii=True, indent=2, sort_keys=True))

    failed = False
    for item in report["inputs"]:
        if (not item.get("exists") or item.get("error") or
                item.get("broken_data_sources") or item.get("required_components_missing")):
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
