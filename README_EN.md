# 🐍 Weibo Mobile Crawler

> A Python-based Sina Weibo data collection tool for mobile (`m.weibo.cn`), featuring keyword search, long post fetching, and IP geolocation

<p align="center">
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT"></a>
</p>

## 📖 Introduction

This project is a Weibo data collection tool for Chinese developers, built on the `m.weibo.cn` mobile API. Compared to the PC version, the mobile version offers:

- ✅ Simpler page structure, easier parsing
- ✅ Weaker anti-scraping measures, more stable collection
- ✅ Faster API response, complete data
- ✅ Support for long post full-text fetching
- ✅ Support for IP geolocation

## 📊 Data Fields (12 Core Fields)

| Field | Description | Example |
|-------|-------------|---------|
| Page | Current page number | 1 |
| Weibo ID | Unique identifier | 5284062722001784 |
| Author | Poster's nickname | chef_tutorial |
| Post Time | Standard datetime | 2026-04-04 19:29:49 |
| Content | Full text (including long posts) | Post content... |
| Reposts | Repost count | 27 |
| Comments | Comment count | 9 |
| Likes | Like count | 20 |
| Region | Posting region | Sichuan |
| IP City | IP-based city | Neijiang |
| IP Province | IP-based province | Sichuan |
| IP Country | IP-based country | China |

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Windows / macOS / Linux

### Install Dependencies

```bash
pip3 install requests pandas
```

### Basic Usage

```bash
python3 weibo_m_spider.py
```

> ⚠️ **Only modify these 3 spots**: search keyword `search_keyword`, max pages `max_search_page`, and `cookie` (in the headers). Changing anything else may cause the code to fail.

## ⚙️ Core Principle

### 1. API Endpoint

```
https://m.weibo.cn/api/container/getIndex
```

### 2. Request Parameters

| Parameter | Description |
|-----------|-------------|
| containerid | `100103type=1&q={keyword}` |
| page_type | `searchall` |
| page | Page number |

### 3. Request Headers (Cookie Required)

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "cookie": "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWOfHYXLA4vqC926wr4IK895JpX5KMhUgL.FoM0SozcS0nR1KM2dJLoI7_0dcpaeKeEeo5p1Btt; ..."
}
```

### 4. Long Post Full-Text Fetching

When a post is truncated (`isLongText=True`), the tool automatically fetches the full content via the extended API:

```python
def getLongText(v_id):
    url = 'https://m.weibo.cn/statuses/extend?id=' + str(v_id)
    r = requests.get(url, headers=headers)
    json_data = r.json()
    long_text = json_data['data']['longTextContent']
    return long_text
```

## 🔧 Key Features

### ⏱️ Request Interval
Built-in random delay of `1-2 seconds` to avoid being blocked

### 🔄 Auto Deduplication
Automatically removes duplicate data based on `Weibo ID`, keeping the first occurrence

### 📝 Long Post Support
Automatically detects long posts and fetches full content

### 🌐 IP Geolocation
Retrieves the poster's IP-based location (city/province/country)

### 📁 Append Mode
Appends data page by page to CSV, preventing data loss

## ⚠️ Important Notes

### 🔑 About Cookie

**A valid Cookie is required for scraping!** Follow these steps to obtain it:

1. Open Chrome browser
2. Log in to [Weibo Mobile](https://m.weibo.cn)
3. Press F12 to open Developer Tools
4. Switch to the Network tab
5. Refresh the page and find any request
6. Copy the Cookie value from Request Headers
7. Replace the `headers["cookie"]` in the source code
<img width="2512" height="1612" alt="image" src="https://github.com/user-attachments/assets/ee7af8bc-f11c-4646-b296-b044db7f1592" />


### 🛡️ Precautions

1. **Rate Control**: Built-in 1-2 second random delay
2. **Cookie Expiry**: Cookies have limited validity; obtain a new one if it expires
3. **Data Cleaning**: Duplicate data is automatically removed
4. **Compliance**: Please follow Weibo's Terms of Service; this tool is for educational purposes only

## 📁 Project Structure

```
weibo-mobile-crawler/
├── weibo_m_spider.py         # Core crawler source
├── weibo_crawfish_5pages.csv  # Demo data
├── requirements.txt          # Dependencies
├── README.md                  # Documentation
└── LICENSE                    # MIT License
```

## 🎯 Use Cases

- 📝 Content Analysis: sentiment monitoring, trending tracking
- 📈 Data Mining: social network analysis, user behavior research
- 🤖 Machine Learning: NLP training dataset building
- 📊 Business Analysis: brand exposure, competitor monitoring
- 🌐 IP Analysis: geographic distribution, user profiling

## 📜 License

This project is licensed under the [MIT License](LICENSE), free for personal and commercial use.

---

## 🔗 More Collection Tools

This tool is built on Weibo's free mobile API with **limited daily collection** (a few hundred posts), suitable for small-scale data collection and research.

For **larger data volume** and **more features** (search, user posts, comments, image downloads), try the enhanced version:

👉 **[Weibo One Spider](https://github.com/mashukui/weibo_one_spider)**

Feature Comparison:

| Feature | This Tool | Weibo One Spider |
|---------|----------|------------------|
| Keyword Search | ✅ | ✅ |
| User Posts Collection | ❌ | ✅ |
| Comments Collection | ❌ | ✅ |
| Image Downloads | ❌ | ✅ |
| Data Volume | Limited | Unlimited |

---
📌 **Disclaimer**: This tool is for educational purposes only. Any commercial use or violation of Weibo's Terms of Service is at your own risk.
