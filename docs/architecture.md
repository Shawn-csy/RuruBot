# RuruBot 架構文件

## 目標

RuruBot 的長期方向是把核心功能整理成一個可被多種 client 呼叫的後端服務。LINE Bot 只是其中一個入口；未來如果要另外架 Web 前端、手機 App、Discord Bot 或管理後台，都應該能共用同一套核心功能。

重構完成後，核心功能已拆出 use case 層，handler 只做 params 清理 + use case 呼叫 + presenter 轉換，LINE 細節集中在 adapter 與 presenter，不再混入業務邏輯。

## 現行架構

```text
FastAPI App (main.py)
  -> api/routes.py
      -> services/use_cases/*
      -> JSON response

  -> services/adapters/line_webhook.py
      -> services/commands/  (processor → config → parsers → handlers)
      -> services/use_cases/*
      -> services/linebot_reply/  (LINE presenter)
      -> services/adapters/line_sender.py
      -> LINE Messaging API

services/use_cases/
  astro.py      — 星座運勢
  ticket.py     — 淺草寺抽籤 + Gemini 解籤
  podcast.py    — 國師運勢解析
  radar.py      — 雷達圖 URL
  answers_book.py — 解答之書

services/features/
  astro.py      — 星座資料抓取
  get_tickets.py — 籤詩 JSON 讀取
  get_podcast.py — Spotify podcast 抓取與解析
  radar.py      — 雷達圖 URL 生成
  gemini_reply.py — Gemini API（lazy init）
  dogdog_meme.py — 迷因圖 URL
  answers_book.py — 解答之書 JSON 讀取
  help.py        — 說明訊息 dict

services/linebot_reply/
  process_reply_data.py — 5 個 presenter（astro / ticket / podcast / help / answers_book）

layout/                 — Flex Message bubble builder（專案根目錄）
```

現行架構達成：

- 核心功能（use case）不 import LINE SDK。
- LINE adapter 和 REST API 共用同一個 use case。
- 外部 API client（Gemini）lazy init，import 時不建立連線。
- `main.py` 只做 FastAPI 設定與路由掛載。
- command handler 只做 params 清理 + use case 呼叫 + presenter 轉換。

## 分層責任

### 1. API / Adapter 層

負責處理不同入口的協定。

範例：

- LINE webhook：接收 LINE event，解析文字，回覆 LINE message。
- REST API：接收 HTTP request，回傳 JSON。
- 未來 WebSocket 或其他 bot adapter：只處理該平台的輸入輸出。

這一層可以知道 LINE SDK、FastAPI request/response，但不應該放核心業務邏輯。

### 2. Command Router 層

負責把使用者輸入轉成明確的 intent。

範例：

```text
"牡羊座 -w"
  -> CommandIntent(name="astro", params={"sign": "牡羊座", "type": "weekly"})

"抽淺草寺 感情運"
  -> CommandIntent(name="ticket", params={"text": "感情運"})

"解答之書 我會成功嗎"
  -> CommandIntent(name="answers_book", params={"question": "我會成功嗎"})
```

這一層只處理文字解析，不負責呼叫外部 API，也不負責組 LINE 訊息。

### 3. Use Case 層

負責一個完整功能流程。

範例：

- `get_astro_result(sign, type)` — 星座運勢
- `get_ticket_result(question)` — 淺草寺抽籤 + Gemini 解籤
- `get_podcast_result()` — 國師週運解析
- `get_radar_result()` — 雷達圖 URL
- `get_answers_book_result(question)` — 解答之書

Use case 可以呼叫 feature service、組合資料、處理 fallback，但回傳應該是乾淨的 domain result。

Use case 的 result 也是未來 REST API 的基礎資料契約，因此必須使用 JSON-native 結構。不要為了相容既有 LINE layout，把 tuple、平行陣列或 presenter 專用欄位放進 use case result。

### 4. Feature Service 層

負責與外部資料來源或核心演算法互動。

範例：

- 星座資料抓取（`features/astro.py`）
- Gemini API 解籤（`features/gemini_reply.py`，lazy init）
- Spotify podcast 抓取（`features/get_podcast.py`）
- 雷達圖 URL 生成（`features/radar.py`）
- 籤詩 JSON 讀取（`features/get_tickets.py`）
- 解答之書 JSON 讀取（`features/answers_book.py`）

這一層不應該知道 LINE FlexMessage，也不應該回傳 LINE SDK 物件。

### 5. Presenter / Message Builder 層

負責把 domain result 轉成特定 client 的呈現格式。

範例：

- LINE presenter：把 `AstroResult` 轉成 FlexMessage。
- Web presenter：通常不需要額外轉換，直接讓 API 回 JSON。
- 未來 Discord presenter：把 result 轉成 Discord embed。

既有 layout function 如果還需要舊格式，轉換應該只發生在 presenter 內部。例如星座 use case 對外只回 `fortunes`，LINE presenter 可以在呼叫舊的 `create_astro_bubble()` 前，暫時把 `fortunes` 轉成 layout 需要的 `star_counts`。

## 資料契約原則

Use case 和 API 只保留新的公開資料結構。舊格式只允許留在 presenter 或 layout adapter 內部，不能繼續作為 use case result 的欄位。

以星座功能為例，use case/API 應回傳：

```json
{
  "sign": "牡羊座",
  "fortune_type": "daily",
  "title": "牡羊座每日運勢",
  "fortunes": [
    {
      "label": "整體運勢",
      "stars": 4,
      "content": "今天適合推進重要事項"
    },
    {
      "label": "愛情運勢",
      "stars": 3,
      "content": "保持自然互動即可"
    }
  ],
  "reminder": "今天適合慢慢來",
  "error": null
}
```

不應在 use case/API result 保留這類舊格式：

```python
{
    "star_counts": [(4, "今天適合推進重要事項"), (3, "保持自然互動即可")],
    "fortune_labels": ["整體運勢", "愛情運勢"]
}
```

原因：

- tuple 不是清楚的 JSON API 契約。
- 平行陣列容易不同步。
- 前端需要猜欄位位置意義。
- 同時保留新舊格式會造成兩套資料來源，後續容易不一致。

## 建議資料流

### LINE Bot

```text
LINE event
  -> line_webhook_adapter
  -> command_router
  -> use_case
  -> domain result
  -> line_presenter
  -> LINE message
```

### Web 前端

```text
Frontend fetch()
  -> /api/*
  -> use_case
  -> domain result
  -> JSON
```

## 已上線 API

```text
GET  /api/astro?sign=牡羊座&type=daily
GET  /api/astro?sign=牡羊座&type=weekly
GET  /api/radar
POST /api/ticket
GET  /api/podcast
POST /api/answers-book
GET  /api/help
```

`POST /api/ticket` 是公開前端使用的純資料 API，固定不呼叫 Gemini。AI 解籤只保留在 LINE Bot 內部流程，避免公開網站被刷 AI 成本。

回傳範例：

```json
{
  "sign": "牡羊座",
  "fortune_type": "daily",
  "title": "牡羊座每日運勢",
  "fortunes": [
    {"label": "整體運勢", "stars": 4, "content": "今天適合推進重要事項"},
    {"label": "愛情運勢", "stars": 3, "content": "保持自然互動即可"}
  ],
  "reminder": "今天適合慢慢來",
  "error": null
}
```

## 待辦

- `plurk_image.py` import-time `PlurkAPI` 初始化改 lazy（目前每日梗圖服務已暫停，不急）
- 暫停服務底層檔案（`spotify_service.py`、`tarot.py` 等）確認無引用後刪除

## Health Endpoints

```text
GET /healthz
GET /readyz
```

- `/healthz` 是輕量 liveness，只確認服務有回應。
- `/readyz` 檢查必要環境變數與本地資料檔。
- health endpoints 不呼叫外部 API，避免 Gemini、Spotify、LINE 短暫異常時讓 Cloud Run 誤判 instance 不健康。

## 判斷原則

新增或修改功能時，用以下問題檢查架構是否保持乾淨：

- 這段程式是否只有 LINE Bot 需要？如果是，放在 LINE adapter 或 presenter。
- 這段程式是否 Web 前端也會需要？如果是，放在 use case 或 feature service。
- 這個 function 是否回傳 LINE SDK 物件？如果是，它不應該在核心功能層。
- 這個 use case result 是否是 JSON-native？如果不是，先改成 API 友善結構。
- 是否同時保留新舊兩套資料欄位？如果是，只保留新結構，把舊格式轉換移到 presenter。
- 這個模組 import 時是否會初始化外部 client？如果是，測試與部署可能會變脆。
- 同一份資料是否能同時支援 LINE 和 Web？如果不能，資料格式可能太靠近某個 client。
