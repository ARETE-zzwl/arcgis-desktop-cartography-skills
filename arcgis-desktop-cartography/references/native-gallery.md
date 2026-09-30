# 原生示例的运行与修改

## 已提供的成果

`assets/synthetic/maps/` 内的 M01–M10 每个目录都有原生MXD、独立LYR、PDF、PNG和不含本机路径的渲染记录。总计10个MXD、17个数据框、41个LYR。它们由ArcObjects创建、ArcMap 10.2导出；不是把其他软件生成的PNG贴入MXD。数据在同级 `data/`，整个 `synthetic/` 目录需要一起移动。

页面为A4横向，PDF/PNG导出300 dpi。图例、色标和比例尺为可编辑的原生图形，但不是随任意用户编辑自动更新的智能图例；更改范围、数据或符号后应重新运行生成器。色带来自实际渲染器RGB，避免图例与栅格各用一套渐变。

## 两套运行环境

- **Python 3**：`prepare_gallery.py` 使用NumPy、rasterio、pyshp构造合成GeoTIFF/SHP；`run_arcmap_checked.py` 监督独立工作进程；离线测试也在Python 3运行。
- **授权的32位ArcMap Python 2.7**：`arcmap_gallery.py`、`verify_native_gallery.py` 和既有导出脚本使用ArcPy/ArcObjects。参考实测环境为ArcMap 10.2、ArcInfo、Python 2.7.18、NumPy 1.16.6。
- **COM桥接**：任务本地 `comtypes==1.1.7` 源码目录及可写包装缓存；不要把现代comtypes安装进ArcGIS旧环境。该第三方库及ArcGIS软件均不随包分发。

## 最小命令

先把下列占位符替换为自己的路径。各输出目录和日志使用新名称，脚本不会覆盖已有项目。

```powershell
& '<python3.exe>' scripts/prepare_gallery.py '<new-project>/data'

& '<python3.exe>' scripts/run_arcmap_checked.py `
  --python '<arcmap-python.exe>' --timeout 120 --log '<new-log>.txt' `
  scripts/arcmap_gallery.py `
  --data '<new-project>/data' --out '<new-project>/maps' `
  --com '<arcgis-home>/com' --vendor '<comtypes-1.1.7-folder>' --dpi 300
```

`--only M03` 可以只生成一类图；`--dpi 600` 用于需要更高分辨率的出口。改变 `assets/gallery-specs.json` 的标题、框尺寸、色限和颜色可修改示例；它不是任意业务GIS数据的通用制图框架。

```powershell
& '<python3.exe>' scripts/run_arcmap_checked.py `
  --python '<arcmap-python.exe>' --timeout 90 --log '<new-check-log>.txt' `
  scripts/verify_native_gallery.py '<relocated-project>' '<report.json>' --render

& '<python3.exe>' -B -m unittest discover -s scripts -p 'test_*.py'
```

## 本轮新增的非显然经验

1. 新建 `IMapFrame` 时，先关联 `Map`、设置CRS和非空页面Geometry，再调用 `IGraphicsContainer.AddElement`；空Geometry会报参数错误。
2. 页面毫米与数据米的比例必须浮点计算。Python 2整数除法会把短比例尺算成零；本轮已由数值和实际渲染共同检查。
3. `esriSMSX` 为3、菱形 `esriSMSDiamond` 为4；X形符号配白色描边可能在浅底上消失，示例采用圆/方/菱形。
4. 相对路径能让图件迁移，却不保证原生二进制完全不含构建目录；公开发布需要额外扫描并采用中性路径构建。
5. 不要在导出阶段调用已知会挂起的Dataset Describe/GetCount。MXD/LYR检查和地图导出与地理处理可分开验证。
6. 不将ArcGIS读取数据后生成的锁文件、临时缓存、绝对路径日志或整个COM包装缓存打包。具体边界见 [发布清理](release-hygiene.md)。
7. 相邻同类网格逐个作为面要素导出时，PDF阅读器可能显示抗锯齿白缝；合并相邻同类格网，保留原有阶梯边界，并回栅格化逐像元验证类别未改变。
8. 图例线宽与地图范围宽度使用不同变量；比例尺必须用重新打开的MXD范围核对，不能仅凭“看起来正常”验收。
9. 系统自带的空白MXD模板也可能含历史个人目录、样式文件和VBA库引用。本生成器使用 `IMapDocument.New` 和 `IPage.PutCustomSize(297,210)` 从空白创建，不依赖模板。初始化页面与各地图的 ActiveView、范围和 AreaOfInterest 后保存，避免空几何错误。参考 [Esri IMapDocument.New](https://resources.arcgis.com/en/help/arcobjects-net/componentHelp/0012/0012000008n0000000.htm) 与 [IPage](https://desktop.arcgis.com/en/arcobjects/10.7/net/IPage.htm)。
