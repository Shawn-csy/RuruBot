# RuruBot - LINEBOT

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

RuruBot 是一個基於 LINE Messaging API 開發的 LineBot，使用 FastAPI 進行開發。

## 功能特點

1.  **氣象雷達** 🌧️
    - 即時查看氣象雷達圖。
2.  **星座運勢** ⭐
    - 查詢 12 星座的日運、週運，並提供完整的運勢分析。
3.  **淺草寺抽籤** 🎋
    - 提供電子淺草寺觀音籤，並附有 AI 解籤服務。
4.  **國師運勢** 📻
    - 提供每週星座運勢速報，由 AI 分類整理。
5.  **暈船迷因** 🐶
    - 隨機取得暈船迷因圖。
6.  **解答之書** 📖
    - 向解答之書提問，隨機得到一個答案。
7.  **使用說明** ℹ️
    - 顯示目前支援的所有指令。

目前保留服務：氣象雷達、星座運勢、淺草寺抽籤、本週國師、暈船迷因、解答之書、使用說明。
六十甲子、音樂推薦、露露聊天、塔羅、每日梗圖已暫停，底層檔案暫時保留待確認後清除。

## 如何使用

大部分功能支援透過關鍵字觸發：

- **天氣**：`雷達`、`radar`
- **星座**：`牡羊座`、`-w 牡羊座`（週運）
- **抽籤**：`抽淺草寺`
- **國師**：`本週國師`
- **迷因**：`暈船仔`、`暈船`
- **解答之書**：`解答之書 我會成功嗎`
- **幫助**：`--help`

## 技術特點

- FastAPI 後端，支援 LINE Webhook 與 REST API 雙入口
- 核心功能（use case）不依賴 LINE SDK，可被多種 client 共用
- 外部 API client（Gemini）lazy init，import 時不建立連線
- 指令解析、業務邏輯、LINE 呈現分層，各層職責明確
- Docker 容器化部署

## 架構方向

RuruBot 的長期方向是把核心功能整理成可被多種 client 呼叫的後端服務。LINE Bot 會是其中一個 adapter，未來也可以新增 Web 前端透過 API 取得同一份資料。

詳細說明請參考 [architecture.md](./docs/architecture.md)。
實作遷移步驟請參考 [refactor_plan.md](./docs/refactor_plan.md)。

## REST API

目前已上線：

```text
GET /api/astro?sign=牡羊座&type=daily
GET /api/astro?sign=牡羊座&type=weekly
GET /api/radar
POST /api/ticket
GET /api/podcast
POST /api/answers-book
GET /api/help
```

回傳 JSON-native 結構，可直接給 Web 前端使用。
`POST /api/ticket` 是純資料 API，固定不呼叫 Gemini；AI 解籤只保留在 LINE Bot 內部流程。

## Health Check

```text
GET /healthz  # 輕量 liveness，確認服務有回應
GET /readyz   # readiness，檢查必要環境變數與本地資料檔
```

Health endpoints 不呼叫 Gemini、Spotify、LINE 等外部服務，避免外部服務抖動時被誤判為 Cloud Run instance 不健康。

## 開發環境設置

1.  安裝依賴：

    ```bash
    pip install -r requirements.txt
    ```

2.  設置環境變數 (建立一個 `.env` 檔案):
    ```bash
    # .env 檔案
    LINE_CHANNEL_ACCESS_TOKEN=your_access_token
    LINE_CHANNEL_SECRET=your_channel_secret
    GEMINI_API_KEY=your_gemini_api_key
    CORS_ALLOW_ORIGINS=*  # 可改成正式前端網域，多個網域用逗號分隔
    ```

## 專案結構

```
RuruBot/
├── main.py               # FastAPI app 入口
├── api/
│   └── routes.py         # REST API endpoints
├── services/
│   ├── adapters/         # LINE webhook / sender adapter
│   ├── commands/         # 指令解析與路由（config / parsers / handlers / processor）
│   ├── use_cases/        # 核心功能邏輯（不依賴 LINE SDK）
│   ├── features/         # 外部資料來源（含部分暫停服務殘留）
│   └── linebot_reply/    # LINE presenter（domain result → FlexMessage）
├── layout/               # Flex Message bubble builder
├── statics/              # 靜態資源（籤詩 JSON 等）
├── docs/                 # 架構文件
└── tests/
    ├── use_cases/        # use case 單元測試（不打外部 API）
    ├── features/         # command parser / handler 測試
    ├── api/              # REST API 整合測試
    ├── adapters/         # LINE sender / webhook 測試
    ├── commands/         # LINE webhook callback 測試
    └── manual/           # 需要真實 API key 的手動測試（不自動執行）
        └── suspended/    # 暫停服務的手動/歷史測試
```

## 測試

```bash
.venv/bin/pytest -q
```

預設測試不需要真實 API key，全部 mock 外部服務。`tests/manual/` 下的手動測試不會被自動執行。
目前預設測試排除暫停服務的手動/歷史測試。

## 部署

使用 Docker 部署：

```bash
docker build -t ruru-bot .
docker run -d -p 8000:8000 --env-file .env ruru-bot
```

## 更新日誌

詳細的更新歷史請參考 [changelog.md](./docs/changelog.md)。

## 授權

MIT License

## 作者

Shawn Chang
