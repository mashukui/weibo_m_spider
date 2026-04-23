# 🐍 M端微博爬虫 / Weibo Mobile Crawler

> 基于Python3的微博m端数据采集爬虫，含：关键词搜索、长微博展开后全文、IP属地等

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
</p>

## 📖 项目简介

本项目是一款面向中文开发者的微博数据采集工具，基于 `m.weibo.cn` 移动端接口开发。相比PC端，移动端具有：

- ✅ 网页结构简单，解析容易
- ✅ 反爬能力较弱，采集稳定
- ✅ 接口响应快，数据完整
- ✅ 支持长微博全文获取
- ✅ 支持IP属地解析

## 📊 采集字段（12个核心字段）

| 字段 | 说明 | 示例 |
|------|------|------|
| 页码 | 当前页序号 | 1 |
| 微博ID | 微博唯一标识 | 5284062722001784 |
| 微博作者 | 发布者昵称 | 厨艺教程 |
| 发布时间 | 标准时间格式 | 2026-04-04 19:29:49 |
| 微博内容 | 完整文本（含长微博全文） | 微博正文... |
| 转发数 | 转发数量 | 27 |
| 评论数 | 评论数量 | 9 |
| 点赞数 | 点赞数量 | 20 |
| 发布于 | 发布地区 | 发布于 四川 |
| ip属地_城市 | IP城市 | 内江 |
| ip属地_省份 | IP省份 | 四川 |
| ip属地_国家 | IP国家 | 中国 |

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Windows / macOS / Linux

### 安装依赖

```bash
pip install requests pandas
```

### 基本使用

```python
from weibo_m_spider import get_weibo_list

# 配置搜索参数
search_keyword = '小龙虾'  # 搜索关键字
max_search_page = 5        # 爬取前几页

# 调用爬取函数
get_weibo_list(
    v_keyword=search_keyword,
    v_max_page=max_search_page
)
```

> ⚠️ **仅需修改这三处**：搜索关键词 `search_keyword`、最大页数 `max_search_page`、`cookie`（在源码 headers 中）。修改其他位置可能导致运行失败。

## ⚙️ 核心原理

### 1. 请求地址

```
https://m.weibo.cn/api/container/getIndex
```

### 2. 请求参数

| 参数 | 说明 |
|------|------|
| containerid | `100103type=1&q={关键词}` |
| page_type | `searchall` |
| page | 页码 |

### 3. 请求头（需要携带Cookie）

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "cookie": "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWOfHYXLA4vqC926wr4IK895JpX5KMhUgL.FoM0SozcS0nR1KM2dJLoI7_0dcpaeKeEeo5p1Btt; ..."
}
```

### 4. 长微博全文获取

当微博内容被截断时（`isLongText=True`），自动调用扩展接口获取完整内容：

```python
def getLongText(v_id):
    url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
    r = requests.get(url, headers=headers)
    json_data = r.json()
    long_text = json_data['data']['longTextContent']
    return long_text
```

## 🔧 核心特性

### ⏱️ 请求间隔
内置随机延迟 `1-2秒`，避免频繁请求被封禁

### 🔄 自动去重
根据 `微博ID` 自动去除重复数据，保留第一条

### 📝 长微博支持
自动识别长微博并请求全文内容

### 🌐 IP属地解析
支持获取微博发布者的IP属地（城市/省份/国家）

### 📁 文件追加模式
分页爬取时自动追加到CSV，避免数据丢失

## ⚠️ 重要说明

### 🔑 关于Cookie

**必须携带有效Cookie才能爬取！** 请按照以下步骤获取：

1. 打开 Chrome 浏览器
2. 登录 [微博移动端](https://m.weibo.cn)
3. 按 F12 打开开发者工具
4. 切换到 Network 标签
5. 刷新页面，找到任意请求
6. 复制 Request Headers 中的 Cookie 值
7. 替换源码中的 `headers["cookie"]`

![](assets/17769184604187.jpg)


### 🛡️ 注意事项

1. **频率控制**：已内置1-2秒随机延迟
2. **Cookie有效期**：Cookie通常有时效，发现失效请重新获取
3. **数据清洗**：部分微博可能包含重复数据，已自动去重
4. **合规使用**：请遵守微博服务条款，本工具仅供学习研究

## 📁 项目结构

```
weibo-mobile-crawler/
├── weibo_m_spider.py      # 核心爬虫源码
├── 微博清单_小龙虾_前5页.csv   # 演示数据
├── requirements.txt       # 依赖列表
├── README.md              # 项目说明
└── LICENSE                # MIT协议
```

## 🎯 适用场景

- 📝 内容分析：舆情监控、热点追踪
- 📈 数据挖掘：社交网络分析、用户行为研究
- 🤖 机器学习：NLP训练数据集构建
- 📊 商业分析：品牌曝光、竞品监控
- 🌐 IP分析：地域分布、用户画像

## 📜 开源协议

本项目采用 [MIT License](LICENSE)，可免费使用于个人和商业项目。

---

## 🔗 更多采集工具

本工具基于微博移动端免费接口开发，**每日采集量有限**，适合小规模数据采集和学习研究使用。

如需**更大采集量**、更丰富功能（搜索帖子采集、博主主页采集、评论采集、图片下载等），推荐使用增强版：

👉 **[爬微博聚合软件 Weibo One Spider](https://github.com/mashukui/weibo_one_spider)**

功能对比：

| 功能 | 本工具 | 爬微博聚合软件 |
|------|--------|---------------|
| 关键词搜索 | ✅ | ✅ |
| 博主主页采集 | ❌ | ✅ |
| 评论采集 | ❌ | ✅ |
| 图片下载 | ❌ | ✅ |
| 数据量 | 受限 | 无限制 |

---
📌 **声明**：本工具仅供学习研究使用，请勿用于商业牟利或任何违规场景。使用本工具产生的任何问题由使用者自行承担。