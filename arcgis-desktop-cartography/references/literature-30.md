# 30篇期刊图件学习记录

检索/核验日期：2026-09-30。通过出版商页面检索图注及相关方法，逐图查看设计，并用 Crossref 核对 DOI、题名、期刊、作者和日期。研究覆盖2016—2026年。属于**围绕制图的定向阅读**，不是系统综述、论文全文翻译或科研结果复现。

**证据分级：A（28篇）**为图注/方法明确说明 ArcGIS/ArcMap 制图；**B（2篇）**为混合软件工作流或作者提供 ArcGIS 图层样式，不能独立确认最终排版完全由 ArcGIS 完成。B级仍有可复用价值，明确保留限制。ArcGIS Pro 来源只迁移制图设计，不宣称其 Python 3 API 可在 ArcMap 10.2 运行。

30个图件观察归纳为10个原生示例。示例采用合成数据，复刻的是地图结构和编码规则，**不逐像元重现原图，不复现原研究计算**。观察与改进建议分栏；原图色彩、比例尺或统计解释不自动视为最佳实践。论文全文和原图均不分发。

|ID|期刊/年份|目标图|证据|示例|
|---|---|---|---|---|
|[A01](#a01)|Scientific Reports / 2018|[Fig4](https://www.nature.com/articles/s41598-018-33755-7#Fig4)|A|M03|
|[A02](#a02)|Nature Communications / 2018|[Fig3](https://www.nature.com/articles/s41467-018-06837-3#Fig3)|A|M02|
|[A03](#a03)|Nature Communications / 2022|[Fig1](https://www.nature.com/articles/s41467-022-31558-z#Fig1)|A|M05|
|[A04](#a04)|Nature Communications / 2024|[Fig3](https://www.nature.com/articles/s41467-024-44888-x#Fig3)|A|M10|
|[A05](#a05)|Nature Communications / 2025|[Fig1](https://www.nature.com/articles/s41467-025-67617-4#Fig1)|A|M10|
|[A06](#a06)|Communications Biology / 2026|[Fig2](https://www.nature.com/articles/s42003-026-09803-8#Fig2)|A|M04|
|[A07](#a07)|Communications Earth & Environment / 2026|[Fig3](https://www.nature.com/articles/s43247-026-03221-8#Fig3)|A|M05|
|[A08](#a08)|Scientific Data / 2018|[Fig1](https://www.nature.com/articles/sdata2018127#Fig1)|B|M07|
|[A09](#a09)|Scientific Reports / 2016|[Fig1](https://www.nature.com/articles/srep33708#Fig1)|A|M01|
|[A10](#a10)|Scientific Reports / 2020|[Fig1](https://www.nature.com/articles/s41598-020-75273-5#Fig1)|A|M02|
|[A11](#a11)|Scientific Reports / 2020|[Fig5](https://www.nature.com/articles/s41598-020-67423-6#Fig5)|A|M02|
|[A12](#a12)|Scientific Reports / 2024|[Fig4](https://www.nature.com/articles/s41598-024-59019-1#Fig4)|A|M09|
|[A13](#a13)|Scientific Reports / 2021|[Fig9](https://www.nature.com/articles/s41598-021-03585-1#Fig9)|A|M03|
|[A14](#a14)|Scientific Reports / 2019|[Fig7](https://www.nature.com/articles/s41598-019-48773-2#Fig7)|B|M10|
|[A15](#a15)|Scientific Reports / 2022|[Fig1](https://www.nature.com/articles/s41598-022-21499-4#Fig1)|A|M01|
|[A16](#a16)|Scientific Reports / 2022|[Fig4](https://www.nature.com/articles/s41598-022-21795-z#Fig4)|A|M01|
|[A17](#a17)|Scientific Reports / 2021|[Fig1](https://www.nature.com/articles/s41598-021-93328-z#Fig1)|A|M01|
|[A18](#a18)|Scientific Reports / 2021|[Fig7](https://www.nature.com/articles/s41598-021-99693-z#Fig7)|A|M04|
|[A19](#a19)|Scientific Reports / 2025|[Fig4](https://www.nature.com/articles/s41598-025-10948-5#Fig4)|A|M03|
|[A20](#a20)|Scientific Reports / 2025|[Fig3](https://www.nature.com/articles/s41598-025-13829-z#Fig3)|A|M08|
|[A21](#a21)|Scientific Reports / 2021|[Fig8](https://www.nature.com/articles/s41598-021-85862-7#Fig8)|A|M06|
|[A22](#a22)|Scientific Reports / 2025|[Fig16](https://www.nature.com/articles/s41598-025-12125-0#Fig16)|A|M03|
|[A23](#a23)|Scientific Reports / 2025|[Fig7](https://www.nature.com/articles/s41598-025-02338-8#Fig7)|A|M01|
|[A24](#a24)|Scientific Reports / 2026|[Fig2](https://www.nature.com/articles/s41598-026-39257-1#Fig2)|A|M01|
|[A25](#a25)|Scientific Reports / 2026|[Fig3](https://www.nature.com/articles/s41598-026-53019-z#Fig3)|A|M03|
|[A26](#a26)|Scientific Reports / 2026|[Fig4](https://www.nature.com/articles/s41598-026-65412-9#Fig4)|A|M02|
|[A27](#a27)|Scientific Reports / 2026|[Fig3](https://www.nature.com/articles/s41598-026-51218-2#Fig3)|A|M07|
|[A28](#a28)|Scientific Reports / 2025|[Fig1](https://www.nature.com/articles/s41598-025-13788-5#Fig1)|A|M01|
|[A29](#a29)|Scientific Reports / 2025|[Fig5](https://www.nature.com/articles/s41598-025-16056-8#Fig5)|A|M08|
|[A30](#a30)|Scientific Reports / 2026|[Fig7](https://www.nature.com/articles/s41598-026-42914-0#Fig7)|A|M05|

<a id="a01"></a>
## A01 · Novel Hybrid Evolutionary Algorithms for Spatial Prediction of Floods

Scientific Reports (2018) · [DOI](https://doi.org/10.1038/s41598-018-33755-7) · [目标图](https://www.nature.com/articles/s41598-018-33755-7#Fig4)

- **软件证据（A）**：ArcGIS 10.2 + MATLAB。方法明确把像元易发性指数导入 Arc GIS 10.2 制成最终图，并讨论分级方法。 定位：Methods: Preparation of flood susceptibility mapping using ANFIS ensemble models。
- **图件观察**：Fig.4 用主图、黑色洪水点和矩形放大区展示易发性等级与事件的空间关系。
- **拟写入技能的改进**：借鉴局部放大与点叠加；五级改为亮度有序色，不把易发性指数直接称作校准概率。
- **复刻映射**：M03；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：只复刻图形组织；不重训 ANFIS，也不复现该流域指数。

<a id="a02"></a>
## A02 · Identifying long-term stable refugia for relict plant species in East Asia

Nature Communications (2018) · [DOI](https://doi.org/10.1038/s41467-018-06837-3) · [目标图](https://www.nature.com/articles/s41467-018-06837-3#Fig3)

- **软件证据（A）**：ArcGIS 10.5 + Canvas 12。图注明确 ArcGIS 出图后在 Canvas 12 排版。 定位：Fig.3 caption; Methods: Ecological niche modelling。
- **图件观察**：Fig.3 以行列组织时期和气候模型，两个物种组各有一组图；当前与过去的低值颜色并不完全一致。
- **拟写入技能的改进**：保留模型×时期矩阵，把同一变量的范围、分级和颜色锁定；图注单列物种组与情景。
- **复刻映射**：M02；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：借鉴排版不代表认可跨时期颜色替换；未复现物种分布模型。

<a id="a03"></a>
## A03 · Albedo changes caused by future urbanization contribute to global warming

Nature Communications (2022) · [DOI](https://doi.org/10.1038/s41467-022-31558-z) · [目标图](https://www.nature.com/articles/s41467-022-31558-z#Fig1)

- **软件证据（A）**：ArcGIS 10.6 + R 3.6.1。方法明确 ArcGIS 用于空间变量地图，R 用于辐射强迫计算。 定位：Methods: Estimation of albedo change and RF。
- **图件观察**：Fig.1 三张全球变化图配一个分布直方图；正负变化通过两侧色系表达。
- **拟写入技能的改进**：差值色标以零为中心，写清基准期；全球图比例尺不可解释为所有纬度通用。
- **复刻映射**：M05；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：示例为区域投影图和合成差值，不计算反照率或辐射强迫。

<a id="a04"></a>
## A04 · Revealing the hidden carbon in forested wetland soils

Nature Communications (2024) · [DOI](https://doi.org/10.1038/s41467-024-44888-x) · [目标图](https://www.nature.com/articles/s41467-024-44888-x#Fig3)

- **软件证据（A）**：ArcGIS Pro 3.2.1 + R 4.3.0。方法明确所有地图图件由 ArcGIS Pro 制作，预测分析在 R 中进行。 定位：Methods: Statistical analysis; Fig.3 caption。
- **图件观察**：Fig.3 用同一局部范围对照湿地概率、面积类别和不同深度/产品的碳储量，配半透明地形阴影。
- **拟写入技能的改进**：对相同深度和单位共享色标；不同深度不能直接共用范围暗示等价；降低阴影遮色。
- **复刻映射**：M10；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M10 只复刻空间支持对照，不复现碳储量产品或深度换算。

<a id="a05"></a>
## A05 · Gaps in tropical science from unrepresentative distribution of sampling and citation across natural terrestrial environments

Nature Communications (2025) · [DOI](https://doi.org/10.1038/s41467-025-67617-4) · [目标图](https://www.nature.com/articles/s41467-025-67617-4#Fig1)

- **软件证据（A）**：ArcGIS Pro 3.0.3 + R ggplot2。方法区分统计图用 ggplot2、地图用 ArcGIS Pro。 定位：Methods: Statistical analyses and visualization; Fig.1 caption。
- **图件观察**：Fig.1 以两张全球格网密度图对照采样与引用，并明确约3度空间支持；两图数值上限不同。
- **拟写入技能的改进**：密度标注分母与单位；经纬度格网面积不同，不能将原始点数误当每平方公里密度。
- **复刻映射**：M10；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M10 演示投影格网空间支持；未复现全球文献数据库或密度计算。

<a id="a06"></a>
## A06 · The effects of human activity and snow cover on the distribution of mammals and terrestrial birds in the Altai Mountains under climate change

Communications Biology (2026) · [DOI](https://doi.org/10.1038/s42003-026-09803-8) · [目标图](https://www.nature.com/articles/s42003-026-09803-8#Fig2)

- **软件证据（A）**：ArcGIS 10.4.1。图注明确使用 ArcGIS 10.4.1，底图来自 Natural Earth。 定位：Fig.2 caption。
- **图件观察**：Fig.2 以物种小多图展示橙色收缩、灰色持续、蓝色扩张与白色不适生四类。
- **拟写入技能的改进**：类别语义和配色跨面板固定；变更类别保留从旧类到新类的转移表。
- **复刻映射**：M04；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M04 展示稳定类别对照；未计算生态位阈值或物种迁移。

<a id="a07"></a>
## A07 · Machine learning uncovers dominant fractions of heavy metal(loid)s in global soils

Communications Earth & Environment (2026) · [DOI](https://doi.org/10.1038/s43247-026-03221-8) · [目标图](https://www.nature.com/articles/s43247-026-03221-8#Fig3)

- **软件证据（A）**：ArcGIS Desktop 10.8.2 + Origin + Python。统计方法明确地图使用 ArcGIS Desktop 并涉及经验贝叶斯克里金，其他图件分开处理。 定位：Methods: Statistical methods; Fig.3 caption。
- **图件观察**：Fig.3 主图显示高/低迁移性，四张小图单独显示各组分不确定性，另配洲际统计。
- **拟写入技能的改进**：估计值与不确定性用不同图层或独立面板，并明确区间定义、覆盖率和样本依据。
- **复刻映射**：M05；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M05 的点纹只为设计演示，不是该文置信区间、显著性或风险。

<a id="a08"></a>
## A08 · A global dataset of river network geometry

Scientific Data (2018) · [DOI](https://doi.org/10.1038/sdata.2018.127) · [目标图](https://www.nature.com/articles/sdata2018127#Fig1)

- **软件证据（B）**：ArcGIS-compatible SHP/LYR; exact export version unstated。作者提供与 Fig.1 对应的 ArcGIS LYR 符号化及 SHP，也提供 SLD；这证明 ArcGIS 可复用样式，不独立证明最终排版软件。 定位：Usage Notes: Dataset Organization; Fig.1。
- **图件观察**：Fig.1 用两幅全球河网比较两个几何指标，低到高色标一致组织，但采用彩虹与黑底。
- **拟写入技能的改进**：保留河网对象和可复用 LYR；按线宽/色阶突出支流层次，避免彩虹制造假边界。
- **复刻映射**：M07；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：属于 B 级软件证据；M07 复刻河网层次，不声称计算或复现 chi 指标。

<a id="a09"></a>
## A09 · Soil surface temperatures reveal moderation of the urban heat island effect by trees and shrubs

Scientific Reports (2016) · [DOI](https://doi.org/10.1038/srep33708) · [目标图](https://www.nature.com/articles/srep33708#Fig1)

- **软件证据（A）**：ArcGIS 10。图注明确 ArcGIS 10 及所用绿地和基础地图来源。 定位：Fig.1 caption。
- **图件观察**：Fig.1 以不同点形区分庭院、草本和乔灌木采样位置，绿地类别为背景。
- **拟写入技能的改进**：点用形状与颜色双重编码；压低背景饱和度，确保符号在灰度输出中仍可辨认。
- **复刻映射**：M01；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：不分发该文受许可约束的 Ordnance Survey/Infoterra 底图。

<a id="a10"></a>
## A10 · Topographic, soil, and climate drivers of drought sensitivity in forests and shrublands of the Pacific Northwest, USA

Scientific Reports (2020) · [DOI](https://doi.org/10.1038/s41598-020-75273-5) · [目标图](https://www.nature.com/articles/s41598-020-75273-5#Fig1)

- **软件证据（A）**：ArcGIS Desktop 10.4.1 + R。图注分别说明 R 处理和 ArcGIS 地图制作。 定位：Fig.1 caption。
- **图件观察**：Fig.1 上部为分布诊断，下部两张同范围干旱敏感性图；灰色与黑色明确表示两种未计算原因。
- **拟写入技能的改进**：对比图固定色标，并把观测不足、非目标地类与有效零值分开；需要时采用独立缺失掩膜。
- **复刻映射**：M02；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：示例只有域外 NoData，不模拟论文的两类缺失机制和分布统计。

<a id="a11"></a>
## A11 · Correlation analysis of land surface temperature and topographic elements in Hangzhou, China

Scientific Reports (2020) · [DOI](https://doi.org/10.1038/s41598-020-67423-6) · [目标图](https://www.nature.com/articles/s41598-020-67423-6#Fig5)

- **软件证据（A）**：ArcMap 10.0。图注明确 ESRI ARCMAP 10.0 绘制自然地表温度图。 定位：Fig.5 caption。
- **图件观察**：Fig.5 裁剪后的连续温度面配经纬网、摄氏度色标与局部比例尺，水体/剔除区留白。
- **拟写入技能的改进**：温度连续量使用有序亮度色标；负温不必自动变为异常量发散图；掩膜意义单列。
- **复刻映射**：M02；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M02 借鉴连续场组织，展示降水而非复现 LST 反演。

<a id="a12"></a>
## A12 · An integrated modeling approach for estimating monthly global rainfall erosivity

Scientific Reports (2024) · [DOI](https://doi.org/10.1038/s41598-024-59019-1) · [目标图](https://www.nature.com/articles/s41598-024-59019-1#Fig4)

- **软件证据（A）**：ArcGIS Pro 3.2。图注明确 ArcGIS Pro 3.2 制作最大月降雨侵蚀力月份图。 定位：Fig.4 caption。
- **图件观察**：Fig.4 将每个像元的峰值月份编码为12个类别，并以月份名称列出图例。
- **拟写入技能的改进**：月份视作循环相位，12月邻接1月；并列数字月份，缺测单列；不能对月份编码做线性均值。
- **复刻映射**：M09；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M09 是角相位合成场，没有估计真实降雨侵蚀力。

<a id="a13"></a>
## A13 · Deep learning-based landslide susceptibility mapping

Scientific Reports (2021) · [DOI](https://doi.org/10.1038/s41598-021-03585-1) · [目标图](https://www.nature.com/articles/s41598-021-03585-1#Fig9)

- **软件证据（A）**：ArcGIS 10.4.1 + Python。最终易发性图的图注明确使用 ArcGIS 10.4.1。 定位：Fig.9 caption。
- **图件观察**：Fig.9 五级易发性覆盖整区，边界、比例尺和等级图例清楚，但红绿为主要对比。
- **拟写入技能的改进**：改用有序亮度且非红绿依赖的五级色；图例写数值边界及闭开区间。
- **复刻映射**：M03；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：不复现 CNN-DNN；类别图本身不能证明分类准确性。

<a id="a14"></a>
## A14 · Evaluating scale effects of topographic variables in landslide susceptibility models using GIS-based machine learning techniques

Scientific Reports (2019) · [DOI](https://doi.org/10.1038/s41598-019-48773-2) · [目标图](https://www.nature.com/articles/s41598-019-48773-2#Fig7)

- **软件证据（B）**：ArcGIS 10.4 + SAGA 4.0.1 (mixed pipeline)。方法明确 ArcGIS 与 SAGA 共同用于因子/易发性图的整理及可视化，没有拆分各软件的最终绘图责任。 定位：Methods: Data; Fig.7 caption。
- **图件观察**：Fig.7 用3×3矩阵对照模型和 DEM 来源/分辨率，共用等级图例并减少重复图饰。
- **拟写入技能的改进**：模型与空间支持放在正交行列；保持范围、色标和验证样本一致，保留原生像元纹理。
- **复刻映射**：M10；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：属于 B 级混合软件证据；M10 演示聚合分辨率，未重跑三个学习器。

<a id="a15"></a>
## A15 · Protection status, human disturbance, snow cover and trapping drive density of a declining wolverine population in the Canadian Rocky Mountains

Scientific Reports (2022) · [DOI](https://doi.org/10.1038/s41598-022-21499-4) · [目标图](https://www.nature.com/articles/s41598-022-21499-4#Fig1)

- **软件证据（A）**：ArcMap 10.7.1。图注明确 ArcMap 10.7.1，并详细列出基础数据许可。 定位：Fig.1 caption。
- **图件观察**：Fig.1 在积雪持续度底图上，用点形表示三类采样方案、填充深浅表示检出状态，边界线粗细区分保护区。
- **拟写入技能的改进**：把采样类型与观测状态拆成独立视觉通道，地形纹理弱化；保留许可来源。
- **复刻映射**：M01；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M01 保留点形通道，未模拟检出概率、种群密度或雪盖年数。

<a id="a16"></a>
## A16 · Dynamic landslide susceptibility analysis that combines rainfall period, accumulated rainfall, and geospatial information

Scientific Reports (2022) · [DOI](https://doi.org/10.1038/s41598-022-21795-z) · [目标图](https://www.nature.com/articles/s41598-022-21795-z#Fig4)

- **软件证据（A）**：ArcGIS Pro 2.9.2。图注明确 ArcGIS Pro 2.9.2；正文说明用 Near 匹配雨量站。 定位：Fig.4 caption。
- **图件观察**：Fig.4 地图与数据筛选流程并列，黄色站点与红色滑坡点区分数据角色。
- **拟写入技能的改进**：站点/事件用不同形状；就近匹配需要投影距离、阈值和时间覆盖规则，不能仅凭视觉靠近。
- **复刻映射**：M01；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：只借鉴点位角色；M01 不执行 Near、不做事件归因。

<a id="a17"></a>
## A17 · Assessment of vegetation growth and drought conditions using satellite-based vegetation health indices in Jing-Jin-Ji region of China

Scientific Reports (2021) · [DOI](https://doi.org/10.1038/s41598-021-93328-z) · [目标图](https://www.nature.com/articles/s41598-021-93328-z#Fig1)

- **软件证据（A）**：ArcGIS 10.2。只有研究区/土地覆盖 Fig.1 明确声明 ArcGIS 10.2；其他统计图不据此推定。 定位：Fig.1 caption。
- **图件观察**：Fig.1 同时展示大尺度定位、三期城市概况和主体土地覆盖，分类色与背景一致。
- **拟写入技能的改进**：定位与专题图各自控制尺度；按阅读目标精简插图，分类与连续量采用不同图例。
- **复刻映射**：M01；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：示例没有复现植被健康指数和小波分析。

<a id="a18"></a>
## A18 · Variations in urban land surface temperature intensity over four cities in different ecological zones

Scientific Reports (2021) · [DOI](https://doi.org/10.1038/s41598-021-99693-z) · [目标图](https://www.nature.com/articles/s41598-021-99693-z#Fig7)

- **软件证据（A）**：ArcGIS 10.5 (Fig.7); QGIS for LST maps。Fig.7 的土地覆盖图明确 ArcGIS；同文温度图3—6注明 QGIS，不能统称 ArcGIS 出图。 定位：Fig.7 caption; compare Figs.3-6 captions。
- **图件观察**：Fig.7 按城市分行、年份分列对照土地利用，类别图例跨年份重复。
- **拟写入技能的改进**：每个城市固定范围、年份顺序与颜色；合并重复图例并保留每城市独立尺度。
- **复刻映射**：M04；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M04 复刻土地覆盖对照，未复刻 QGIS 温度图。

<a id="a19"></a>
## A19 · Deciphering of groundwater potential zones in hard rock terrain using GIS technology with AHP statistical methods: A case study of Nilgiri, Tamil Nadu, India

Scientific Reports (2025) · [DOI](https://doi.org/10.1038/s41598-025-10948-5) · [目标图](https://www.nature.com/articles/s41598-025-10948-5#Fig4)

- **软件证据（A）**：ArcGIS 10.7 (figure statement)。地下水潜力图注明 ArcGIS 10.7；正文还提到10.8，引用图件版本不强行统一。 定位：Fig.4 caption。
- **图件观察**：Fig.4 展示五级潜力区与带标签地点，蓝色为高潜力、红色为低潜力。
- **拟写入技能的改进**：先固定低→高语义再选色；避免照搬另一灾害图相反的颜色意义，标签用克制描边。
- **复刻映射**：M03；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M03 展示等级规则，不估计地下水产能；该文坐标描述需要另行核对。

<a id="a20"></a>
## A20 · AHP and Geospatial technology-based assessment of groundwater potential zones in Natham taluk, Tamil nadu, India

Scientific Reports (2025) · [DOI](https://doi.org/10.1038/s41598-025-13829-z) · [目标图](https://www.nature.com/articles/s41598-025-13829-z#Fig3)

- **软件证据（A）**：ArcGIS 10.7。方法说明 ArcGIS 中制作专题图，具体描述线密度、排水密度和降水 IDW。 定位：Methods and Fig.3 caption。
- **图件观察**：Fig.3 图注列出10项条件因子；已查看首幅图像中的岩性、地貌、密度和土壤面板，各自使用不同图例。
- **拟写入技能的改进**：原始类别用定性色、原始连续量标单位；若转为评分须另列评分规则，不能共享含糊的高低图例。
- **复刻映射**：M08；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：视觉核验限定于页面的首幅图像；M08 仅复刻混合因子板式，不执行 AHP。

<a id="a21"></a>
## A21 · Evaluation of multi-hazard map produced using MaxEnt machine learning technique

Scientific Reports (2021) · [DOI](https://doi.org/10.1038/s41598-021-85862-7) · [目标图](https://www.nature.com/articles/s41598-021-85862-7#Fig8)

- **软件证据（A）**：ArcGIS 10.5 + SAGA。正文说明在 ArcGIS 10.5 中合成三类灾害为八类多灾种图。 定位：Methods: Multi-hazard probability mapping; Fig.8。
- **图件观察**：Fig.8 以不同颜色表示灾种及组合，低/无灾用灰色，底部比例尺和边界保持一致。
- **拟写入技能的改进**：使用位编码枚举全部8种组合，图例说明组合关系；避免把组合类别颜色读成严重程度。
- **复刻映射**：M06；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M06 合成布尔掩膜，不估计真实联合发生概率。

<a id="a22"></a>
## A22 · Application of smart technologies for predicting soil erosion patterns

Scientific Reports (2025) · [DOI](https://doi.org/10.1038/s41598-025-12125-0) · [目标图](https://www.nature.com/articles/s41598-025-12125-0#Fig16)

- **软件证据（A）**：ArcGIS Pro (map caption); ArcGIS 10.3 (preprocessing)。最终图16明确 ArcGIS Pro；数据预处理段写 ArcGIS 10.3。 定位：Fig.16 caption。
- **图件观察**：Fig.16 将模型和训练/测试图成组，点覆盖在易发性面上；首幅图像比例尺出现极小公里值，值得核查。
- **拟写入技能的改进**：训练与测试符号/角色分开；必须计算投影单位与比例尺对应关系，不能复制可疑标尺数值。
- **复刻映射**：M03；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：只将该比例尺记为视觉疑点，不据此裁定研究错误；未重训侵蚀模型。

<a id="a23"></a>
## A23 · Mapping forest aboveground carbon stock of combined stratified sampling and RFRK model with mean annual temperature and precipitation

Scientific Reports (2025) · [DOI](https://doi.org/10.1038/s41598-025-02338-8) · [目标图](https://www.nature.com/articles/s41598-025-02338-8#Fig7)

- **软件证据（A）**：ArcGIS 10.8 + ENVI preprocessing。研究区多面板图注明由作者用 ArcGIS 10.8 创建。 定位：Fig.7 caption。
- **图件观察**：Fig.7 左侧两级定位，中部 DEM 与样点，右侧温度和降水细长面板，以布局表达环境背景。
- **拟写入技能的改进**：主采样地图占最大面积；辅助气候面板保留独立单位和范围，定位插图不挤占图例。
- **复刻映射**：M01；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M01 复刻主图/详情层次，M08 提供变量拆分；不估计森林碳。

<a id="a24"></a>
## A24 · Swamp-AI: a deep learning model for monitoring wetlands change across the globe

Scientific Reports (2026) · [DOI](https://doi.org/10.1038/s41598-026-39257-1) · [目标图](https://www.nature.com/articles/s41598-026-39257-1#Fig2)

- **软件证据（A）**：ArcGIS Pro 3.6.0。全球样区定位图注明 ArcGIS Pro 和 National Geographic Style 底图。 定位：Fig.2 caption。
- **图件观察**：Fig.2 用橙色菱形在全球底图上统一标识湿地地点，图例单一且点大小固定。
- **拟写入技能的改进**：点符号应压过底图文字；公开包采用自制底图或经许可素材，不把在线商业底图打包。
- **复刻映射**：M01；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M01 只迁移点位可见性规则，不复现 Swamp-AI 或全球地点数据。

<a id="a25"></a>
## A25 · A multi-temporal framework for assessing flood risk to cultural heritage: spatiotemporal evidence from Shandong Province (2000–2020)

Scientific Reports (2026) · [DOI](https://doi.org/10.1038/s41598-026-53019-z) · [目标图](https://www.nature.com/articles/s41598-026-53019-z#Fig3)

- **软件证据（A）**：ArcGIS Pro (version in cited software reference)。权重方案空间对照图注明 ArcGIS Pro，图注未单列版本。 定位：Fig.3 caption。
- **图件观察**：Fig.3 将风险等级占比柱图与五种权重方案地图配对，呈现权重变化引起的空间差异。
- **拟写入技能的改进**：所有方案用统一数值边界和同一验证基准；柱图与地图类别颜色一一对应。
- **复刻映射**：M03；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M03 提供固定分级基础，未计算遗产暴露或复现权重敏感性。

<a id="a26"></a>
## A26 · Driving mechanisms of drought triggers in response to vegetation loss across the Weihe River Basin

Scientific Reports (2026) · [DOI](https://doi.org/10.1038/s41598-026-65412-9) · [目标图](https://www.nature.com/articles/s41598-026-65412-9#Fig4)

- **软件证据（A）**：ArcGIS 10.8 + Python preprocessing。图注明确地图由作者用 ArcGIS 10.8 创建。 定位：Fig.4 caption。
- **图件观察**：Fig.4 行为月份、列为干旱等级，共用0—100%概率色标；每幅重复的地名挤占较多空间。
- **拟写入技能的改进**：固定矩阵维度和概率范围；减少重复标签，标注条件概率定义、样本量与不确定性。
- **复刻映射**：M02；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M02 借鉴矩阵比较原则；合成降水图不冒充条件概率。

<a id="a27"></a>
## A27 · Transfer learning for identifying rainwater harvesting sites in training data-scarce catchments

Scientific Reports (2026) · [DOI](https://doi.org/10.1038/s41598-026-51218-2) · [目标图](https://www.nature.com/articles/s41598-026-51218-2#Fig3)

- **软件证据（A）**：ArcGIS Pro 2.9。图注及方法均明确六类专题因子地图由 ArcGIS Pro 2.9 生成。 定位：Fig.3 caption; Methodology。
- **图件观察**：Fig.3 将坡度、土壤、土地覆盖、地质、地貌与河网流量六面板排列；河网采用分级线色。
- **拟写入技能的改进**：分开面状类别、连续表面和线状量的图例；流量/河级不能因共用色表而混同。
- **复刻映射**：M07；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M07 的线宽代表示意河级而非流量；M08 演示不同类型因子的并置。

<a id="a28"></a>
## A28 · Water content alters soil organic carbon metabolism via microbial traits in Tibetan alpine peatlands

Scientific Reports (2025) · [DOI](https://doi.org/10.1038/s41598-025-13788-5) · [目标图](https://www.nature.com/articles/s41598-025-13788-5#Fig1)

- **软件证据（A）**：ArcGIS 10.2。正文明确 Fig.1 使用 ArcGIS 10.2。 定位：Study area / map description; Fig.1。
- **图件观察**：Fig.1 研究区图叠加等高线、河流和编号样点，并配较大范围定位插图。
- **拟写入技能的改进**：保留编号与样点表联动，减少过密等高线；高程垂直基准和水平 CRS 分开记录。
- **复刻映射**：M01；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M01 使用虚构高程和样点，没有真实高程基准或土壤实验结果。

<a id="a29"></a>
## A29 · Prediction of spatiotemporal evolution and zoning of ecological sensitivity in the upper reaches of Minjiang river, sichuan, China

Scientific Reports (2025) · [DOI](https://doi.org/10.1038/s41598-025-16056-8) · [目标图](https://www.nature.com/articles/s41598-025-16056-8#Fig5)

- **软件证据（A）**：ArcMap 10.8。稳定性指标空间图明确注明 ArcMap 10.8。 定位：Fig.5 caption。
- **图件观察**：Fig.5 把高程、坡度、土壤、岩性、侵蚀、道路距离转成统一敏感性等级后共用图例。
- **拟写入技能的改进**：区分原始物理量与标准化评分；共享评分图例之前公开每个因子的转换阈值及方向。
- **复刻映射**：M08；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M08 展示原始异质量并分别标单位，不复制该文评分体系。

<a id="a30"></a>
## A30 · Identifying the coupling coordination relationship and driving forces between urbanization and the supply–demand of ecosystem service: a case study of the Gansu Province

Scientific Reports (2026) · [DOI](https://doi.org/10.1038/s41598-026-42914-0) · [目标图](https://www.nature.com/articles/s41598-026-42914-0#Fig7)

- **软件证据（A）**：ArcGIS 10.7。网格/县域耦合协调与变化趋势图注明 ArcGIS 10.7。 定位：Fig.7 caption。
- **图件观察**：Fig.7 按行对比格网和县域支持，按列区分水平与变化；水平和变化使用不同图例。
- **拟写入技能的改进**：连续水平与变化方向分开编码；县域统计写清加权/聚合方法，避免把行政均值解释成像元结果。
- **复刻映射**：M05；见 [期刊图件配方](journal-map-recipes.md)。
- **限制**：M05 只演示有符号变化；M10 覆盖尺度支持，不复现耦合指标。
