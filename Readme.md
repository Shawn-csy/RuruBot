# RuruBot - LINE 智能助手

RuruBot 是一個基於 LINE Messaging API 開發的 LineBot，使用 cursor 開發 。

## 功能特點

### 1. 氣象雷達 🌧

- 即時查看氣象雷達圖
- 支援關鍵字：雷達、radar、天氣雷達等

### 2. 星座運勢 ⭐

- 支援 12 星座日運、週運查詢
- 完整的運勢分析（整體運、愛情運、事業運、財運）
- 智能分析和建議

### 3. 淺草寺抽籤 🎋

- 電子淺草寺觀音籤
- AI 解籤服務
- 客製化問題分析

### 4. 六十甲子籤 🎯

- 傳統六十甲子籤詩
- AI 智能解籤
- 詳細解析和建議

### 5. 國師運勢 📻

- 每週星座運勢速報
- 分類整理（讚的、穩的、累的）
- 完整星座分析

## 技術特點

- 使用 FastAPI 建構 Web 服務
- 整合 LINE Messaging API
- 支援 Flex Message 客製化訊息
- AI 智能分析（使用 Google Gemini）
- Docker 容器化部署

## 開發環境設置

1. 安裝依賴：

```bash
pip install -r requirements.txt
```

2. 設置環境變數：

```bash
# .env 檔案
LINE_CHANNEL_ACCESS_TOKEN=your_access_token
LINE_CHANNEL_SECRET=your_channel_secret
GEMINI_API_KEY=your_gemini_api_key
```

## 專案結構

RuruBot/
├── services/
│ ├── features/ # 功能模組
│ ├── linebot_reply/ # LINE Bot 回覆處理
│ └── constants.py # 常數定義
├── layout/ # Flex Message 版面配置
├── tests/ # 測試目錄
│ ├── features/ # 功能測試
│ └── commands/ # 指令測試
├── main.py # 主程式
└── requirements.txt # 依賴套件

## 測試

執行所有測試：

```bash
python -m tests.run_tests
```

執行特定測試：

```bash
# 執行功能測試
pytest tests/features/

# 執行指令測試
pytest tests/commands/
```

## 部署

使用 Docker 部署：

```bash
docker build -t ruru-bot .
docker run -d -p 8000:8000 ruru-bot
```

## 授權

MIT License

## 作者

Shawn Chang

## 更新日誌

## [0.1.4] - 2025-04-25

### 更新

- 新增嚴格語意解析器

### 修正

- 星座指令過於敏感

## [0.1.3] - 2025-03-19

### 更新

- 新增星座運勢強調色(4 星以上)

### 修正

## [0.1.2] - 2025-03-19

### 更新

- 新增使用說明功能
- 新增 Dockerfile

### 修正

- Gemini Reply 修正

## [0.1.1] - 2025-03-19

### 更新

- 新增骰子功能
- 新增 Gemini Reply
- 新增國師開示功能

### 修正

- 統一 Flex Message 格式

## [0.1.0] - 2025-03-18

### 開發

- 新增籤詩功能,增加 layout
- 新增星座功能
- 新增雷達功能
- 新增露露開示功能
- 重構整體套件格式
- 新增版控
