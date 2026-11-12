# HTML 彩色速记讲义支线规范

本 reference 是 final-review-slides 的第三种产物形态：在 PDF（LaTeX）与 Word（.docx）之外，额外生成**单文件、自包含的彩色 HTML 速记讲义**，面向手机端扫读复习。五色语义与 PDF/docx 支线完全一致，只是载体换成 HTML。

模板：`assets/review-template.html`。生成新讲义时复制模板，按章节填充；不要从零另写一套样式。

## 1. 产物定位

- **用途**：把已核验的考点整理成可扫读、可强记忆的网页讲义，应试复习场景。
- **读者**：备考学生，注意力容易分散（ADHD 倾向），手机端优先；要求一眼看到重点，排斥严肃刻板排版。
- **形态约束**：单文件 `.html`，CSS/JS 全部内联；不拆外部 `.js`/`.css`，不用 React/Vue 等框架，原生 JS；静态资源如需图片先下载并随产物打包。
- **内容顺序与保真**：沿用主工作流的来源盘点、授课顺序、来源引用与覆盖台账；HTML 只是呈现层，不改变内容取舍与顺序。数字、剂量、阈值必须可追溯源材料，不目测、不凑整、不编造。

## 2. 五色编码（与 PDF/docx 共用同一套 kind）

| kind | 语义 | HTML 行内类 | HTML 框体/组件 | PDF 宏 | docx 函数 |
|---|---|---|---|---|---|
| `concept` 蓝 | 基础概念、定义、首选药、核心检查/术语 | `.tag.blue`、`.t-blue` | 卡片色条 `.k-blue` | `\tagConcept{…}` | `add_tag(doc,"concept",…)` |
| `number` 绿 | 必背数字、剂量、阈值、公式取值 | `.num-pill`、`.t-green`、`.tag.green` | 公式块 `.formula` | `\tagNumber{…}`/`\numBadge{…}` | `add_tag(doc,"number",…)`/`badge(p,…)` |
| `mechanism` 橙 | 机制、因果链、分型、部位、顺序 | `.tag.orange`、`.t-orange` | 流程链 `.flow`、色条 `.k-orange` | `\tagMechanism{…}`/`mechbox` | `add_tag(doc,"mechanism",…)`/`add_box(doc,"mechanism",…)` |
| `trap` 红 | 禁忌、坑点、易混、重度/危险表现 | `.tag.red`、`.t-red` | 坑点框 `.warn`、色条 `.k-red` | `\tagTrap{…}`/`trapbox` | `add_box(doc,"trap",…)` |
| `conclusion` 黄 | 核心结论、口诀、一句话主线 | `.tag.yellow`、`.t-yellow` | 结论框 `.tip`、色条 `.k-yellow` | `\tagConclusion{…}`/`conclbox` | `add_box(doc,"conclusion",…)` |

HTML 柔和版 token（深色=字/边框，浅色=底纹）：

| kind | 深色 | 浅色底 |
|---|---|---|
| 蓝 | `#3A6EA5` | `#EAF2FA` |
| 绿 | `#2E9E6B` | `#E7F4EC` |
| 橙 | `#E08A3C` | `#FBEFE1` |
| 红 | `#CF5148` | `#FBECEA` |
| 黄 | `#A8842A` | `#FCF4DB` |

中性色：背景 `#F7F5F0`，卡片 `#FFFFFF`，正文墨色 `#26303A`，次要说明 `#5E6873`，分隔线 `#EAE5DB`，圆角 `16px`。

> PDF/docx 支线使用另一组相近 hex（见 `assets/color-style.tex` 与 `scripts/color_docx.py` 的 `COLORS`）；三条线**kind 与语义映射必须一致**，色值允许按载体微调，但不得新增第六种语义色。缺类别时复用最接近的现有色，并在 `coverage-report.md` 记录。

## 3. 内嵌着色规则（避免两个极端）

- **不要整片黑字**：长段落里的数字、药物、禁忌、核心名词必须内嵌上色，否则等于没分层。
- **不要满屏彩色**：普通描述性句子保留墨色；颜色只压在考点要素上。满屏高亮会让重点失焦。
- 判定顺序：先识别考点要素属于哪个 kind，再挂对应类；一段内同色要素不重复堆叠标签。
- 数字/剂量/阈值一律进 `.num-pill` 绿色徽章；概念名、首选药、检查项用蓝色加粗；机制/分型/部位用橙色；禁忌/坑点/重度表现用红色加粗；节末主线结论进黄色 `.tip`。

## 4. 宽松版式参数（ADHD 扫读，直接照模板）

- `body`：`line-height:1.95`，正文 `font-size:15.5px`，系统中文字体栈。
- 卡片：`margin-bottom:26px`，内边距 `4px 22px 24px`。
- 小节块 `.block`：`margin-top:20px`。
- 列表 `ul.pt li`：`margin:13px 0`，左侧留自定义项目符号。
- 双列卡 `.kv`：`gap:13px`，单项 `padding:15px 17px`；窄屏单列，≥600px 两列。
- 提示框 `.warn`/`.tip`：`padding:15px 17px`，`margin-top:18px`。
- 表格 `td`：`padding:12px 13px`，行距 1.8。
- 次要说明 13–13.5px，正文 14–15.5px；层级靠字号/字重，不靠堆字体。

## 5. 页面结构（自上而下）

1. **Hero**：大标题 + 副标题（章节线索引）+ 五色图例 chips（色点 + 语义名，先让读者看懂编码）。
2. **吸顶导航 `.nav`**：胶囊按钮横排锚点跳转；窄屏横向滑动、隐藏滚动条；平滑滚动。每个 `href="#sN"` 必须对应一个存在的 `<section id="sN">`，id 唯一。
3. **卡片列表**：每节一张 `.card`，头部序号色块 + 标题 + 折叠箭头，正文 `.card-body`；卡片左侧按主基调挂一色条 `.k-*`。
4. **页脚**：来源说明与折叠操作提示，小号次要色。

## 6. 组件清单

| 组件 | 作用 | 配色用法 |
|---|---|---|
| `.tag.{kind}` | 行内定性小标签 | 对应浅底 + 深色字 |
| `.num-pill` | 数字/剂量/阈值徽章 | 绿底绿字加粗 |
| `.t-{kind}` | 行内彩色加粗文字 | 对应深色字加粗 |
| `.kv > .item` | 并列要点双列卡 | 浅底圆角；名称可挂 `.t-*` |
| `.block` / `.block-title` | 节内分组与小标题 | 小标题次要色 + 左侧细线 |
| `.warn` | 红色坑点/危险框 | 红浅底 + 红左边框 |
| `.tip` | 黄色结论/主线框 | 黄浅底 + 黄左边框 |
| `.flow` | 流程/步骤链 | 步骤橙浅底橙字 + 箭头 |
| `.ctable` | 鉴别/分级对比表 | 细线表格，首列加粗 |
| `.formula` | 公式块 | 绿浅底，公式名绿字加粗 |
| `.k-{kind}` | 卡片左侧 4px 色条 | 按本节主基调挂一色 |

## 7. 交互与响应式

- **折叠卡片**：点击 `.card-head` 切换 `.collapsed`，隐藏 `.card-body`，箭头旋转；原生 JS `toggleCard(head)`。
- **锚点跳转**：`<a href="#sN">` 对应 `<section id="sN">`，`html{scroll-behavior:smooth}`。
- 导航横滑：`overflow-x:auto` 并隐藏 webkit 滚动条；所有可点入口必须有真实跳转或折叠行为，禁止僵尸按钮。
- `viewport` 必须 `width=device-width, initial-scale=1`；禁止 `maximum-scale=1` / `user-scalable=no`。
- 窄屏所有 grid/flex 显式单列；子项 `min-width:0`；全局 `overflow-wrap:break-word; word-break:break-word`。
- 多列表格 `table-layout:fixed`，列宽显式分配；外包 `.table-scroll` 横向滑动并设 `min-width`。

## 8. 验收清单（交付前逐条过）

- [ ] HTML 标签全部配对（div/section/ul/table/span/b 开闭一致）。
- [ ] 章节 `id` 唯一；导航每个 `href="#…"` 都能解析到存在的锚点。
- [ ] 五色 kind 使用一致：concept 蓝、number 绿、mechanism 橙、trap 红、conclusion 黄。
- [ ] 长段落考点已内嵌上色，无整片黑字段落；也无满屏彩色。
- [ ] 手机窄屏无横向溢出；表格可横滑；文字不重叠、不截断。
- [ ] **分段截图核验**：长页面隐藏其余板块后单独渲染本节，确认颜色、间距、层级正常。
- [ ] 颜色与背景对比度可读；浅底深字，不用浅字压浅底。
- [ ] 来源引用、覆盖结论与 PDF/docx 支线一致，不出现 HTML 独有而台账未记录的考点。

## 9. 发布为可转发在线链接

需要把 HTML 讲义转发给他人时，发布成正式在线网页链接；本地单文件也可直接发送或离线打开。

- 入口为单文件 `review.html`；路径只接受相对当前目录的相对路径，先 `cd` 到产物目录，且 `cd` 与发布命令写在同一条命令里。
- 首发：`lark-cli apps +deploy --file-path ./review.html`；更新已有应用时带上次 `--app-id app_xxx` 复发，覆盖同一链接。
- 成败看返回 JSON 的 `ok` 字段，不看命令退出码。
- 发布异步：受理后用 `lark-cli apps +release-get --app-id <id> --release-id <rid>` 轮询，间隔 ≥3 秒，到 `status=finished` 再取 `online_url`；整体超时未完成则报告当前状态与 release_id。
- 交付只用发布成功返回的 `online_url`（doubao.link 网页链接）；禁止把临时文件 CDN 链接当作分享入口。
- 发布成功后不再用浏览器或脚本回链复查（检查环境可能缺登录态，易把登录页误判为产物）。
- 体积限制：单个 `.html` ≤ 20 MiB；超限先收窄内容范围，不擅自放开参数。

## 10. 踩坑记录

- **超长整页截图不可信**：headless 浏览器截超长整页，后半段会行重叠/塌陷，属渲染缺陷；核验时隐藏前若干板块、只渲染待查节，正常即真实 CSS 无问题。
- **锚点在 headless 下不滚动定位**：截图核验靠隐藏板块，不靠 URL 锚点滚动。
- **单文件自包含**：CSS/JS 内联；不要把临时 CDN 链接写进产物；本地图片先下载并随打包。
- **改模板前先备份**到 `_backup/`，再动手改既有模板与规范。
