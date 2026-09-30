"""Create deterministic SYNTHETIC cartography fixtures (Python 3; no ArcPy).

All geometry and values are invented. The UTM coordinates provide metric map
units for software tests, not a real catchment or environmental observation.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.features import shapes
from rasterio.transform import from_origin
import shapefile

CRS_CODE = 32650
X0, Y0, SPAN = 470000, 3870000, 60000
NODATA = -9999.0


def in_domain(x,y):
    angle=np.arctan2((y-.5)/.40,(x-.49)/.39)
    radius=1+.10*np.sin(3*angle)+.055*np.cos(5*angle)
    return ((x-.49)/.39)**2+((y-.5)/.40)**2<radius**2


def fields(n):
    coord = (np.arange(n) + .5) / n
    x, y = np.meshgrid(coord, coord[::-1])
    inside = in_domain(x,y)
    channel = .46 + .13 * np.sin(y * 7)
    dem = 160 + 1800 * (x - channel) ** 2 + 1000 * y + 440 * np.sin(x * 8) ** 2 * y
    dem += 70*np.sin(35*x+12*y)*np.cos(28*y-8*x)*y
    rain = 200 + 600 * y + 500 * np.exp(-((x - .68)**2 + (y - .65)**2) / .05)
    late = rain + 140 * np.sin(x * 7) * np.cos(y * 5)
    score = np.clip(.72 * np.exp(-((x - channel) / .16) ** 2) + .28 * (1 - y), 0, 1)
    cover = np.where(abs(x-channel)<.035, 0, np.where(y>.56, 1, np.where(x<.5, 2, 3)))
    future = np.where((x>.49)&(x<.74)&(y>.25)&(y<.46), 4, cover)
    delta = 300 * np.sin(x * 7) * np.cos(y * 5)
    flood = abs(x-channel)<.11
    slide = (y>.53)&(x>.39)
    erosion = (x<.45)&(y<.68)
    overlap = flood.astype(int) + 2*slide.astype(int) + 4*erosion.astype(int)
    month = ((np.arctan2(y-.5,x-.49)+np.pi)/(2*np.pi)*12).astype(int)+1
    gy,gx=np.gradient(dem,SPAN/n)
    slope=np.degrees(np.arctan(np.hypot(gx,gy)))
    return inside,dict(dem=dem,rain=rain,rain_late=late,anomaly=delta,slope=slope,
                       risk=np.minimum((score*5).astype(int),4),cover=cover,
                       cover_late=future,overlap=overlap,month=month)


def writer(path,kind):
    w=shapefile.Writer(str(path),shapeType=kind)
    w.field('CLASS','N',4,0)
    return w


def finish(w,path):
    w.close()
    path.with_suffix('.prj').write_text(CRS.from_epsg(CRS_CODE).to_wkt(version='WKT1_ESRI'),encoding='ascii')
    path.with_suffix('.cpg').write_text('UTF-8',encoding='ascii')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    args=p.parse_args(); out=args.output
    out.mkdir(parents=True,exist_ok=False)
    inside,data=fields(200)
    for name in ('dem','rain','rain_late','anomaly','slope'):
        values=np.where(inside,data[name],NODATA).astype('float32')
        with rasterio.open(out/(name+'.tif'),'w',driver='GTiff',height=200,width=200,
                           count=1,dtype='float32',crs=CRS_CODE,nodata=NODATA,
                           transform=from_origin(X0,Y0+SPAN,300,300),compress='deflate') as dst:
            dst.write(values,1)
            valid=values[inside]
            dst.update_tags(1,STATISTICS_MINIMUM=str(valid.min()),STATISTICS_MAXIMUM=str(valid.max()),
                            STATISTICS_MEAN=str(valid.mean()),STATISTICS_STDDEV=str(valid.std()))
    # Area-mean aggregation preserves support; no invented fine detail.
    fine=np.where(inside,data['rain'],np.nan)
    blocks=fine.reshape(20,10,20,10)
    count=np.isfinite(blocks).sum(axis=(1,3))
    coarse=np.divide(np.nansum(blocks,axis=(1,3)),count,out=np.full((20,20),NODATA),where=count>0)
    with rasterio.open(out/'rain_coarse.tif','w',driver='GTiff',height=20,width=20,count=1,
                       dtype='float32',crs=CRS_CODE,nodata=NODATA,
                       transform=from_origin(X0,Y0+SPAN,3000,3000)) as dst:
        dst.write(coarse.astype('float32'),1)
    with rasterio.open(out/'rain_coarse_valid_count.tif','w',driver='GTiff',height=20,width=20,count=1,
                       dtype='uint16',crs=CRS_CODE,nodata=0,
                       transform=from_origin(X0,Y0+SPAN,3000,3000)) as dst:
        dst.write(count.astype('uint16'),1)
    mask,cells=fields(60)
    for name in ('risk','cover','cover_late','overlap','month'):
        path=out/name; w=writer(path,shapefile.POLYGON)
        # Merge adjacent equal cells without smoothing their boundaries. This
        # avoids PDF anti-alias seams between thousands of same-color cells.
        for geometry,value in shapes(cells[name].astype('int16'),mask=mask,
                                     transform=from_origin(X0,Y0+SPAN,1000,1000)):
            rings=[]
            for i,ring in enumerate(geometry['coordinates']):
                area=sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]))
                if (i==0 and area>0) or (i>0 and area<0):ring=ring[::-1]
                rings.append(ring)
            w.poly(rings);w.record(int(value))
        finish(w,path)
    path=out/'boundary';w=writer(path,shapefile.POLYLINE)
    theta=np.linspace(0,2*np.pi,201)
    radius=1+.10*np.sin(3*theta)+.055*np.cos(5*theta)
    w.line([list(zip(X0+SPAN*(.49+.39*radius*np.cos(theta)),Y0+SPAN*(.5+.40*radius*np.sin(theta))))]);w.record(0);finish(w,path)
    path=out/'detail';w=writer(path,shapefile.POLYLINE)
    w.line([[(491000,3900000),(509000,3900000),(509000,3911000),(491000,3911000),(491000,3900000)]]);w.record(0);finish(w,path)
    path=out/'streams';w=writer(path,shapefile.POLYLINE)
    y=np.linspace(.08,.89,80);x=.46+.13*np.sin(y*7)
    keep=in_domain(x,y)
    w.line([list(zip(X0+SPAN*x[keep],Y0+SPAN*y[keep]))]);w.record(3)
    for y0 in [.22,.4,.58,.73]:
        for side in [-1,1]:
            yy=np.linspace(y0,y0+.1,20);xx=.46+.13*np.sin(yy[0]*7)+side*np.linspace(0,.18,20)
            keep=in_domain(xx,yy)
            w.line([list(zip(X0+SPAN*xx[keep],Y0+SPAN*yy[keep]))]);w.record(1 if side<0 else 2)
    finish(w,path)
    rng=np.random.default_rng(20260930)
    path=out/'stations';w=writer(path,shapefile.POINT)
    for i in range(28):
        while True:
            x,y=rng.uniform(.12,.85,2)
            if in_domain(x,y):break
        w.point(X0+SPAN*x,Y0+SPAN*y);w.record(i%3)
    finish(w,path)
    path=out/'uncertain';w=writer(path,shapefile.POINT)
    for y in np.arange(.2,.83,.045):
        for x in np.arange(.16,.84,.045):
            if in_domain(x,y) and abs(np.sin(x*7)*np.cos(y*5))<.3:
                w.point(X0+SPAN*x,Y0+SPAN*y);w.record(0)
    finish(w,path)
    meta=dict(status='SYNTHETIC DESIGN RECONSTRUCTION; NOT RESEARCH RESULTS',seed=20260930,
              crs_epsg=CRS_CODE,units='metre',bounds=[X0,Y0,X0+SPAN,Y0+SPAN],
              raster_cell_m=300,category_cell_m=1000,coarse_cell_m=3000,nodata=NODATA,
              category_geometry='contiguous equal cells merged; original cell support retained',
              vertical_datum='not applicable: invented elevations',
              time='illustrative scenarios A and B, not real dates',
              uncertainty='deterministic visual mask; not p-values or confidence intervals',
              license='CC0-1.0 for generated synthetic data',
              files=sorted(f.name for f in out.iterdir() if f.is_file()))
    (out/'data-provenance.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    print('Created synthetic fixtures:',out)


if __name__=='__main__':main()
