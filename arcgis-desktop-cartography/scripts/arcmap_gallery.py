# -*- coding: ascii -*-
"""Native ArcObjects map authoring and ArcMap export; Python 2.7 only.

Uses the explicitly synthetic fixtures from prepare_gallery.py. Supply an
existing licensed ArcGIS installation and a local
comtypes 1.1.7 distribution. Never installs software or edits source data.
"""
from __future__ import print_function
import argparse
import ctypes
import json
import os
import sys


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data', required=True)
    p.add_argument('--out', required=True)
    p.add_argument('--com', required=True)
    p.add_argument('--vendor', required=True)
    p.add_argument('--only', default='all')
    p.add_argument('--dpi', type=int, default=300)
    args = p.parse_args()
    if os.path.exists(args.out):
        p.error('Use a new output directory')
    sys.path.insert(0, os.path.abspath(args.vendor))
    import arcpy
    import comtypes.client as cc
    C = cc.GetModule(os.path.join(args.com, 'esriCarto.olb'))
    D = cc.GetModule(os.path.join(args.com, 'esriDisplay.olb'))
    G = cc.GetModule(os.path.join(args.com, 'esriGeometry.olb'))
    DB = cc.GetModule(os.path.join(args.com, 'esriGeoDatabase.olb'))
    S = cc.GetModule(os.path.join(args.com, 'esriSystem.olb'))
    specs = json.load(open(os.path.join(os.path.dirname(__file__), '..', 'assets', 'gallery-specs.json')))
    selected = [s for s in specs if args.only in ('all', s['id'])]
    if not selected or args.dpi < 72:
        p.error('Unknown map ID or invalid DPI')
    os.makedirs(args.out)
    data = os.path.abspath(args.data)
    out = os.path.abspath(args.out)
    factory = cc.CreateObject('esriGeometry.SpatialReferenceEnvironment', interface=G.ISpatialReferenceFactory)
    crs = factory.CreateProjectedCoordinateSystem(32650).QueryInterface(G.ISpatialReference)
    wf = cc.CreateObject('esriDataSourcesFile.ShapefileWorkspaceFactory', interface=DB.IWorkspaceFactory)
    workspace = wf.OpenFromFile(data, 0).QueryInterface(DB.IFeatureWorkspace)

    def color(rgb):
        c = cc.CreateObject('esriDisplay.RgbColor', interface=D.IRgbColor)
        c.Red, c.Green, c.Blue = rgb
        return c.QueryInterface(D.IColor)

    def line(rgb, width=.6):
        s = cc.CreateObject('esriDisplay.SimpleLineSymbol', interface=D.ISimpleLineSymbol)
        s.Color, s.Width = color(rgb), width
        return s

    def fill(rgb):
        s = cc.CreateObject('esriDisplay.SimpleFillSymbol', interface=D.ISimpleFillSymbol)
        s.Color = color(rgb)
        edge = line(rgb, 0); edge.Style = D.esriSLSNull
        s.Outline = edge.QueryInterface(D.ILineSymbol)
        return s

    def marker(rgb, size, shape=0):
        s = cc.CreateObject('esriDisplay.SimpleMarkerSymbol', interface=D.ISimpleMarkerSymbol)
        s.Color, s.Size, s.Style = color(rgb), size, shape
        s.Outline, s.OutlineColor, s.OutlineSize = True, color((255,255,255)), .5
        return s

    def envelope(box):
        e = cc.CreateObject('esriGeometry.Envelope', interface=G.IEnvelope)
        e.PutCoords(*box)
        return e

    def vector(mp, name, styles, kind='fill'):
        fl = cc.CreateObject('esriCarto.FeatureLayer', interface=C.IFeatureLayer)
        fl.FeatureClass = workspace.OpenFeatureClass(name + '.shp')
        r = cc.CreateObject('esriCarto.UniqueValueRenderer', interface=C.IUniqueValueRenderer)
        r.FieldCount = 1; r.Field[0] = 'CLASS'; r.UseDefaultSymbol = False
        for val, rgb, size, shape, label in styles:
            s = fill(rgb) if kind == 'fill' else line(rgb,size) if kind == 'line' else marker(rgb,size,shape)
            r.AddValue(str(val), '', s.QueryInterface(D.ISymbol))
            r.Label[str(val)] = label
        fl.QueryInterface(C.IGeoFeatureLayer).Renderer = r.QueryInterface(C.IFeatureRenderer)
        layer = fl.QueryInterface(C.ILayer); layer.Name = name
        mp.AddLayer(layer)
        return layer

    def raster(mp, panel):
        layer = cc.CreateObject('esriCarto.RasterLayer', interface=C.IRasterLayer)
        layer.CreateFromFilePath(os.path.join(data, panel['data']+'.tif'))
        layer.QueryInterface(C.ILayer).Name = panel['label']
        mp.AddLayer(layer.QueryInterface(C.ILayer))
        ramp = cc.CreateObject('esriDisplay.MultiPartColorRamp', interface=D.IMultiPartColorRamp)
        colors = panel['colors']
        for first,last in zip(colors[:-1],colors[1:]):
            part = cc.CreateObject('esriDisplay.AlgorithmicColorRamp', interface=D.IAlgorithmicColorRamp)
            part.FromColor,part.ToColor = color(first),color(last)
            part.Algorithm,part.Size = D.esriCIELabAlgorithm,32
            ramp.AddRamp(part.QueryInterface(D.IColorRamp))
        ramp.Size=256
        assert ramp.CreateRamp()
        stretch = cc.CreateObject('esriCarto.RasterStretchColorRampRenderer', interface=C.IRasterStretchColorRampRenderer)
        rr = stretch.QueryInterface(C.IRasterRenderer); rr.Raster = layer.Raster; rr.Update()
        stretch.BandIndex,stretch.ColorRamp = 0,ramp.QueryInterface(D.IColorRamp)
        st = stretch.QueryInterface(C.IRasterStretch)
        st.StretchType,st.Invert = C.esriRasterStretch_MinimumMaximum,False
        stretch.QueryInterface(C.IRasterStretch3).UseGamma = False
        limits = stretch.QueryInterface(C.IRasterStretchMinMax)
        limits.CustomStretchMin,limits.CustomStretchMax = panel['limits']
        limits.UseCustomStretchMinMax = True
        rr.Update();layer.Renderer=rr
        actual=[]
        for i in range(256):
            rgb=cc.CreateObject('esriDisplay.RgbColor',interface=D.IRgbColor)
            rgb.RGB=ramp.Color[i].RGB
            actual.append([rgb.Red,rgb.Green,rgb.Blue])
        return actual

    reports=[]
    for spec in selected:
        print('BUILD',spec['id']);sys.stdout.flush()
        dest=os.path.join(out,spec['id']);os.makedirs(dest)
        doc=cc.CreateObject('esriCarto.MapDocument',interface=C.IMapDocument)
        path=os.path.join(dest,spec['id']+'.mxd')
        doc.New(path)
        view=doc.PageLayout.QueryInterface(C.IActiveView)
        view.Activate(ctypes.windll.user32.GetDesktopWindow())
        page=doc.PageLayout.Page
        page.Units=S.esriMillimeters
        page.PutCustomSize(297,210)
        view.Extent=envelope([0,0,297,210])
        graphics=doc.PageLayout.QueryInterface(C.IGraphicsContainer)

        def add_element(element, geometry):
            e=element.QueryInterface(C.IElement);e.Geometry=geometry
            graphics.AddElement(e,0)

        def text(value,x,y,size=10,bold=False):
            el=cc.CreateObject('esriCarto.TextElement',interface=C.ITextElement)
            symbol=cc.CreateObject('esriDisplay.TextSymbol',interface=D.ITextSymbol)
            font=cc.CreateObject('StdFont');font.Name='Arial';font.Size=size;font.Bold=bold
            symbol.Font,symbol.Color=font,color((40,48,54))
            symbol.HorizontalAlignment,symbol.VerticalAlignment=D.esriTHALeft,D.esriTVABottom
            el.Symbol,el.Text=symbol,value
            pt=cc.CreateObject('esriGeometry.Point',interface=G.IPoint);pt.PutCoords(x,y)
            add_element(el,pt.QueryInterface(G.IGeometry))

        def rect(x0,y0,x1,y1,rgb):
            el=cc.CreateObject('esriCarto.RectangleElement',interface=C.IFillShapeElement)
            el.Symbol=fill(rgb).QueryInterface(D.IFillSymbol)
            add_element(el,envelope([x0,y0,x1,y1]).QueryInterface(G.IGeometry))

        def swatch_marker(x,y,rgb,shape):
            el=cc.CreateObject('esriCarto.MarkerElement',interface=C.IMarkerElement)
            el.Symbol=marker(rgb,5,shape).QueryInterface(D.IMarkerSymbol)
            pt=cc.CreateObject('esriGeometry.Point',interface=G.IPoint);pt.PutCoords(x,y)
            add_element(el,pt.QueryInterface(G.IGeometry))

        text(spec['id']+'  '+spec['title'],14,195,16,True)
        text('SYNTHETIC DESIGN RECONSTRUCTION  |  Not research results',14,186,9)
        text(spec['subtitle'],14,178,10)
        panel_reports=[]
        for i,panel in enumerate(spec['panels']):
            box=panel['box'];x,y,w,h=box
            if i==0:
                mp=doc.Map[0];mf=graphics.FindFrame(mp).QueryInterface(C.IMapFrame)
            else:
                mp=cc.CreateObject('esriCarto.Map',interface=C.IMap)
                mf=cc.CreateObject('esriCarto.MapFrame',interface=C.IMapFrame);mf.Map=mp
            mp.Name=panel['label'];mp.SpatialReference=crs
            mf.QueryInterface(C.IElement).Geometry=envelope([x,y,x+w,y+h]).QueryInterface(G.IGeometry)
            if i>0:graphics.AddElement(mf.QueryInterface(C.IElement),0)
            actual=None
            if panel['kind']=='raster':actual=raster(mp,panel)
            elif panel['kind']=='category':
                styles=[[j,panel['colors'][j],0,0,label] for j,label in enumerate(panel['labels'])]
                if panel.get('start',0):
                    for style in styles:style[0]+=panel['start']
                vector(mp,panel['data'],styles)
            vector(mp,'boundary',[[0,[89,99,100],.7,0,'Synthetic boundary']],'line')
            if panel.get('streams'):
                vector(mp,'streams',[[1,[111,169,185],.6,0,'Order 1'],[2,[61,132,160],1.2,0,'Order 2'],[3,[17,87,118],2.1,0,'Order 3']],'line')
            if panel.get('stations'):
                vector(mp,'stations',[[0,[16,82,118],5.5,0,'Type A'],[1,[185,93,25],6,1,'Type B'],[2,[90,47,128],6,4,'Type C']],'marker')
            if panel.get('detail_box'):
                vector(mp,'detail',[[0,[55,55,65],.9,0,'Detail view extent']],'line')
            if panel.get('uncertain'):
                vector(mp,'uncertain',[[0,[45,45,45],1.8,0,'Illustrative uncertainty mask']],'marker')
            bounds=panel.get('extent',[470000,3870000,530000,3930000])
            cx,cy=(bounds[0]+bounds[2])/2,(bounds[1]+bounds[3])/2
            width=max(bounds[2]-bounds[0],(bounds[3]-bounds[1])*float(w)/h);height=width*float(h)/w
            extent=[cx-width/2,cy-height/2,cx+width/2,cy+height/2]
            map_view=mp.QueryInterface(C.IActiveView)
            map_view.Activate(ctypes.windll.user32.GetDesktopWindow())
            mp.AreaOfInterest=envelope(extent)
            map_view.Extent=envelope(extent)
            text(panel['label'],x,y+h+1.5,10,True)
            lx,ly,lw=panel['legend']
            if actual and not panel.get('skip_legend'):
                for j,rgb in enumerate(actual):rect(lx+lw*j/256.0,ly,lx+lw,ly+3.4,rgb)
                lo,hi=panel['limits']
                for t in [0,.5,1]:text('%g'%(lo+t*(hi-lo)),lx+lw*t-2,ly-4.5,8)
                text(panel['units'],lx,ly+4.5,8)
            elif panel['kind']=='category':
                for j,label in enumerate(panel['labels']):
                    xx=lx+(j%3)*40 if panel.get('horizontal_legend') else lx
                    yy=ly-(j//3)*6 if panel.get('horizontal_legend') else ly-j*5.2
                    rect(xx,yy,xx+3,yy+3,panel['colors'][j]);text(label,xx+5,yy-.5,8)
            elif panel['kind']=='network':
                for j,(rgb,stroke_width) in enumerate([([111,169,185],.6),([61,132,160],1.2),([17,87,118],2.1)]):
                    yy=ly-j*9;rect(lx,yy,lx+14,yy+stroke_width*.3528,rgb)
                    text('Order '+str(j+1),lx+18,yy-1,9)
            # Graphic scale is calculated from this exact projected extent and frame.
            km=10 if width<90000 else 20
            length=km*1000.0/width*w
            sx,sy=x+2,y+3
            rect(sx,sy,sx+length/2,sy+.8,[35,40,43]);rect(sx+length/2,sy,sx+length,sy+.8,[160,165,168])
            text('0',sx,sy+1,7);text(str(km)+' km',sx+length-4,sy+1,7)
            layer_reports=[]
            for k in range(mp.LayerCount):
                lyr=mp.Layer[k]
                lyrfile=os.path.join(dest,'panel%d_layer%d.lyr'%(i+1,k+1))
                lyr.QueryInterface(C.IDataLayer2).RelativeBase=lyrfile
                lf=cc.CreateObject('esriCarto.LayerFile',interface=C.ILayerFile)
                lf.New(lyrfile);lf.ReplaceContents(lyr);lf.Save();lf.Close()
                layer_reports.append({'name':lyr.Name,'file':os.path.basename(lyrfile)})
            panel_reports.append(dict(label=panel['label'],extent=extent,frame_mm=box,epsg=32650,
                                      limits=panel.get('limits'),palette=actual,scale_km=km,
                                      scale_bar_mm=length,layers=layer_reports))
        for j,(label,rgb,shape) in enumerate(spec.get('marker_legend',[])):
            swatch_marker(206,91-j*7,rgb,shape);text(label,211,89-j*7,9)
        for j,note in enumerate(spec.get('notes',[])):text(note,202,52-j*5,8)
        text('Design sources: '+', '.join(spec['papers'])+'  |  See literature-30.md for figure-level evidence.',14,18,8)
        text('WGS 84 / UTM 50N (metres)  |  Grid north up  |  White outside domain = NoData',14,12,8)
        text('Native ArcMap 10.2; legends and scale graphics are editable but must be rebuilt after data/extent changes.',14,6,7)
        doc.SetActiveView(view)
        doc.Save(True,False);doc.Close()
        del doc,mp,mf
        graphics=None
        mxd=arcpy.mapping.MapDocument(path)
        try:
            broken=[l.name for l in arcpy.mapping.ListBrokenDataSources(mxd)]
            assert not broken,broken
            frames=arcpy.mapping.ListDataFrames(mxd)
            assert len(frames)==len(spec['panels'])
            arcpy.mapping.ExportToPDF(mxd,os.path.join(dest,spec['id']+'.pdf'),resolution=args.dpi,embed_fonts=True,georef_info=True)
            arcpy.mapping.ExportToPNG(mxd,os.path.join(dest,spec['id']+'.png'),resolution=args.dpi)
            for df,pr in zip(frames,panel_reports):
                assert df.spatialReference.factoryCode==32650
            native_frames=[dict(name=df.name,epsg=df.spatialReference.factoryCode,
                                extent=[df.extent.XMin,df.extent.YMin,df.extent.XMax,df.extent.YMax]) for df in frames]
        finally:del mxd
        report=dict(map_id=spec['id'],synthetic=True,software='ArcMap '+arcpy.GetInstallInfo()['Version'],
                    papers=spec['papers'],broken_sources=[],panels=panel_reports,reopened_frames=native_frames,
                    dpi=args.dpi,relative_paths=True,visual_review='Required separately')
        with open(os.path.join(dest,'native-report.json'),'w') as f:json.dump(report,f,indent=2)
        reports.append(report)
        print('EXPORTED',spec['id']);sys.stdout.flush()
    print('NATIVE_GALLERY_COMPLETE',len(reports))


if __name__=='__main__':main()
