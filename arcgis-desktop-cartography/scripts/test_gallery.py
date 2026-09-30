"""Offline scientific and release invariants. Native GIS checks run separately."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_origin
import shapefile
from prepare_gallery import fields, in_domain, X0, Y0, SPAN

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets/synthetic/data'
SPECS=json.loads((ROOT/'assets/gallery-specs.json').read_text(encoding='utf-8'))


class GalleryContracts(unittest.TestCase):
    def test_crs_and_missing_not_zero(self):
        with rasterio.open(DATA/'rain.tif') as src:
            self.assertEqual(src.crs.to_epsg(),32650)
            self.assertEqual(src.res,(300,300))
            self.assertEqual(src.nodata,-9999)
            values=src.read(1,masked=True)
            self.assertTrue(values.mask.any())
            self.assertGreater(values.min(),0)

    def test_categories_complete(self):
        for name,codes in [('risk',set(range(5))),('overlap',set(range(8))),('month',set(range(1,13)))]:
            with shapefile.Reader(str(DATA/name)) as src:
                self.assertEqual({int(r[0]) for r in src.records()},codes)

    def test_nominal_color_dictionary_stable(self):
        a,b=SPECS[3]['panels']
        self.assertEqual(a['colors'],b['colors'])
        self.assertEqual(a['labels'],b['labels'])

    def test_merged_polygons_preserve_category_cells(self):
        mask,cells=fields(60)
        for name in ['risk','cover','cover_late','overlap','month']:
            with shapefile.Reader(str(DATA/name)) as src:
                geoms=[(s.shape.__geo_interface__,int(s.record[0])) for s in src.iterShapeRecords()]
            actual=rasterize(geoms,out_shape=(60,60),fill=-1,
                             transform=from_origin(X0,Y0+SPAN,1000,1000),dtype='int16')
            np.testing.assert_array_equal(actual,np.where(mask,cells[name],-1))

    def test_comparison_limits_fixed(self):
        for index in [1,9]:
            a,b=SPECS[index]['panels']
            self.assertEqual(a['limits'],b['limits'])
            self.assertEqual(a['colors'],b['colors'])
            self.assertEqual(a['units'],b['units'])

    def test_zero_centered_change(self):
        panel=SPECS[4]['panels'][0]
        self.assertEqual(-panel['limits'][0],panel['limits'][1])
        self.assertEqual(len(panel['colors']),3)

    def test_all_point_and_stream_vertices_inside_domain(self):
        for name in ['stations','uncertain','streams']:
            with shapefile.Reader(str(DATA/name)) as src:
                for shape in src.shapes():
                    points=np.asarray(shape.points)
                    self.assertTrue(np.all(in_domain((points[:,0]-X0)/SPAN,(points[:,1]-Y0)/SPAN)),name)

    def test_coarse_mean_and_valid_area(self):
        with rasterio.open(DATA/'rain.tif') as src:
            values=src.read(1).astype(float);values[values==src.nodata]=np.nan
        blocks=values.reshape(20,10,20,10)
        count=np.isfinite(blocks).sum(axis=(1,3))
        with rasterio.open(DATA/'rain_coarse_valid_count.tif') as src:
            np.testing.assert_array_equal(src.read(1),count)
        with rasterio.open(DATA/'rain_coarse.tif') as src:
            coarse=src.read(1)
            expected=np.nansum(blocks,axis=(1,3))[count>0]/count[count>0]
            np.testing.assert_allclose(coarse[count>0],expected,rtol=1e-6)
            self.assertTrue(np.all(coarse[count==0]==src.nodata))

    def test_thirty_unique_traceable_records(self):
        records=json.loads((ROOT/'references/literature-30.json').read_text(encoding='utf-8'))['papers']
        self.assertEqual(len(records),30)
        self.assertEqual(len({p['doi'] for p in records}),30)
        mapped={p for s in SPECS for p in s['papers']}
        self.assertEqual(mapped,{p['id'] for p in records})
        for p in records:
            self.assertTrue(p['figure_url'].endswith('#'+p['figure']))
            self.assertTrue(p['evidence'] and p['improvement'] and p['limit'])

    def test_native_scales_and_frames(self):
        paths=sorted((ROOT/'assets/synthetic/maps').glob('M*/native-report.json'))
        self.assertEqual(len(paths),len(SPECS))
        for path in paths:
            r=json.loads(path.read_text())
            self.assertEqual(r['broken_sources'],[])
            frames={frame['name']:frame for frame in r['reopened_frames']}
            self.assertEqual(len(frames),len(r['panels']))
            for panel in r['panels']:
                self.assertEqual(panel['epsg'],32650)
                frame=frames[panel['label']]
                self.assertEqual(frame['epsg'],32650)
                np.testing.assert_allclose(frame['extent'],panel['extent'],rtol=0,atol=.01)
                length=panel['scale_bar_mm']
                self.assertGreater(length,1)
                self.assertLess(length,panel['frame_mm'][2])
                calculated=panel['scale_km']*1000.0/(panel['extent'][2]-panel['extent'][0])*panel['frame_mm'][2]
                self.assertAlmostEqual(length,calculated,places=8)


class BoundedWorker(unittest.TestCase):
    def test_timeout_stops_only_own_worker(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);worker=root/'worker.py';log=root/'worker.log'
            worker.write_text('import time\nprint("started",flush=True)\ntime.sleep(10)\n')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/run_arcmap_checked.py'),
                                   '--python',sys.executable,'--timeout','.2','--log',str(log),str(worker)],
                                  capture_output=True,timeout=5)
            self.assertEqual(result.returncode,124)
            report=json.loads(log.with_suffix('.log.json').read_text())
            self.assertTrue(report['timed_out'])

    def test_existing_log_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);worker=root/'worker.py';log=root/'worker.log'
            worker.write_text('raise SystemExit(0)\n');log.write_text('prior evidence')
            result=subprocess.run([sys.executable,str(ROOT/'scripts/run_arcmap_checked.py'),
                                   '--python',sys.executable,'--log',str(log),str(worker)],
                                  capture_output=True,timeout=5)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual(log.read_text(),'prior evidence')


if __name__=='__main__':unittest.main()
