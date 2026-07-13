# RuruBot 架構重構步驟

## 目標

把 RuruBot 從「LINE webhook 主導的 bot」逐步整理成「可被多種 client 呼叫的後端服務」。

重構完成後應該達成：

- LINE Bot 仍可正常使用。
- 核心功能可以被 REST API 呼叫。
- 未來 Web 前端可以直接向後端拿 JSON 資料。
- handler 不再直接產生 LINE SDK 物件。
- 外部 API client 更容易 mock 與測試。

## 原則

- 每一步都要保持 LINE Bot 可運作。
- 不一次大改所有功能，先挑一個功能作為範本。
- 每完成一個 phase，都補對應測試。
- 核心功能層不 import LINE SDK。
- API route 和 LINE adapter 共用同一個 use case。
- Use case result 只保留新的 JSON-native 結構；舊 layout 格式只在 presenter 內部轉換。

## Phase 0: 整理測試環境

### 目的

先讓測試可以穩定執行，避免後續重構沒有安全網。

### 修改內容

1. 在 `requirements.txt` 加入測試依賴：

```text
pytest
httpx
```

2. 確認以下指令可執行：

```bash
python3 -m pytest -q
```

3. 修正 mock 位置。

目前 handler 內是這樣 import：

```python
from services.features.astro import get_astro_info
```

測試要 patch 實際被呼叫的 reference：

```python
patch("services.commands.handlers.get_astro_info")
```

而不是：

```python
patch("services.features.astro.get_astro_info")
```

### 驗收標準

- `python3 -m pytest -q` 可以執行。
- 不需要真實呼叫 LINE、Gemini、Spotify、星座網站就能跑主要測試。

## Phase 1: 定義標準回傳格式

### 目的

先統一 handler 和 message builder 之間的資料契約。

### 建議新增檔案

```text
services/results.py
```

### 建議內容

先用簡單 dict 或 dataclass 都可以。初期建議用 dataclass，讓格式更清楚。

```python
from dataclasses import dataclass
from typing import Any, Literal

ResultType = Literal["text", "image", "flex", "mixed", "error"]

@dataclass
class CommandResult:
    type: ResultType
    data: Any
```

如果想先保持改動小，也可以暫時維持 dict，但文件化格式：

```python
{
    "type": "text",
    "data": "message"
}
```

### 修改內容

1. 明確規定 `services/commands/handlers.py` 回傳 `CommandResult` 或標準 dict。
2. `services/message_builder.py` 只接受這種標準格式。
3. 先不要急著改所有功能，只先補型別與測試。

### 驗收標準

- 每個 handler 的回傳格式一致。
- `message_builder` 不需要猜太多格式。
- 測試能檢查 handler 回傳的 `type` 與 `data`。

## Phase 2: 選一個功能做範本

### 建議先選星座功能

原因：

- 功能常用。
- 有 daily / weekly 參數。
- 現在已經有 parser 測試。
- 適合示範「LINE 和 API 共用同一份資料」。

### 目標資料流

```text
LINE 文字
  -> command parser
  -> astro use case
  -> AstroResult
  -> LINE presenter
  -> FlexMessage

Web API
  -> /api/astro
  -> astro use case
  -> AstroResult
  -> JSON
```

### 建議新增檔案

```text
services/use_cases/
  __init__.py
  astro.py

services/presenters/
  __init__.py
  line_astro.py
```

### 修改內容

1. 新增 `services/use_cases/astro.py`。
2. 把 `handle_astro()` 裡的業務流程搬到 use case。
3. use case 回傳乾淨資料，不回傳 FlexMessage。
4. use case result 使用 JSON-native 新結構，不保留 `star_counts`、`fortune_labels` 這類舊 layout 欄位。
5. LINE FlexMessage 轉換移到 presenter。

### AstroResult 公開資料結構

use case/API 應只回傳這種新結構：

```python
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
    "error": None
}
```

不要在 use case result 同時保留舊格式：

```python
{
    "star_counts": [(4, "今天適合推進重要事項"), (3, "保持自然互動即可")],
    "fortune_labels": ["整體運勢", "愛情運勢"]
}
```

如果既有 `create_astro_bubble()` 仍需要 `star_counts`，由 LINE presenter 內部轉換：

```python
star_counts = [
    (fortune["stars"], fortune["content"])
    for fortune in result["fortunes"]
]
```

### 範例結構

```python
def get_astro_result(sign: str, fortune_type: str) -> dict:
    raw_data = get_astro_info(sign, fortune_type)
    return normalize_astro_data(sign, fortune_type, raw_data)
```

handler 變成：

```python
def handle_astro(params):
    result = get_astro_result(params["astro_name"], params["type"])
    reply = build_astro_flex(result)
    return {"type": "flex", "data": reply}
```

LINE presenter 負責：

```python
def build_astro_flex(result):
    star_counts = [
        (fortune["stars"], fortune["content"])
        for fortune in result["fortunes"]
    ]
    ...
```

### 驗收標準

- 星座 use case 不 import LINE SDK。
- 星座 use case result 只包含 `fortunes` 新結構，不包含 `star_counts` 或 `fortune_labels`。
- 舊 layout 需要的格式只在 LINE presenter 內部轉換。
- 星座 API 可以直接回 JSON。
- LINE 星座指令仍能回 FlexMessage。
- 星座測試不用打真實外部網站。

## Phase 3: 新增第一個 REST API

### 目的

驗證後端核心可以被 LINE 以外的 client 使用。

### 建議新增檔案

```text
api/
  __init__.py
  routes.py
```

或：

```text
services/api/
  __init__.py
  astro.py
```

目前專案較小，建議先用：

```text
api/routes.py
```

### 修改內容

1. 在 `main.py` include API router。
2. 新增 endpoint：

```text
GET /api/astro?sign=牡羊座&type=daily
GET /api/astro?sign=牡羊座&type=weekly
```

3. endpoint 呼叫 Phase 2 建立的 `get_astro_result()`。

### 驗收標準

- `GET /api/astro?sign=牡羊座&type=daily` 回傳 JSON。
- API response 是 JSON-native 結構，例如 `fortunes: [{label, stars, content}]`。
- API response 不包含 presenter/layout 專用欄位，例如 `star_counts`、`fortune_labels`。
- LINE bot 和 REST API 共用同一個 use case。
- API 測試使用 FastAPI `TestClient` 可以通過。

## Phase 4: 拆出 LINE Adapter

### 目的

讓 `main.py` 更薄，LINE webhook 相關流程集中管理。

### 建議新增檔案

```text
services/adapters/
  __init__.py
  line_webhook.py
  line_sender.py
```

### 修改內容

1. 把 `handle_message(event)` 的流程搬到 `line_webhook.py`。
2. 把 reply/push 分批邏輯搬到 `line_sender.py`。
3. `main.py` 只保留 FastAPI app、router、LINE handler 註冊。

### 目前可搬出的邏輯

- 測試 reply token bypass。
- `process_message(event.message.text)`。
- `build_messages_from_result(result)`。
- LINE Reply API 最多 5 則訊息限制。
- 超過 5 則時使用 Push API 分批發送。

### 驗收標準

- `main.py` 明顯變薄。
- LINE 發送限制有單元測試。
- 不需要建立真實 LINE client 就能測 sender 分批邏輯。

## Phase 5: 逐步搬其他功能到 Use Case

### 建議順序

1. 星座：已在 Phase 2 當範本。
2. 每日梗圖：資料結構簡單，適合第二個。
3. 雷達：圖片 URL 類型簡單。
4. 塔羅：有 fallback 和較複雜資料，等 pattern 穩定後再搬。
5. Spotify：外部 API client 較複雜，適合後面處理。
6. 抽籤與六十甲子籤：牽涉 AI 解籤和 Flex 排版，最後整理。

### 每個功能的固定步驟

1. 建立 use case。
2. use case 回傳純資料。
3. handler 改成呼叫 use case。
4. LINE presenter 負責轉 FlexMessage。
5. 如果適合前端使用，新增 `/api/*` endpoint。
6. 補 use case test 和 API test。
7. 移除 use case result 裡的舊 presenter/layout 欄位。

### 驗收標準

- 搬完的 feature 不 import LINE SDK。
- LINE 和 API 使用同一個 use case。
- use case/API 只暴露新資料結構。
- 每個 feature 至少有 use case test。

## Phase 6: 整理外部 API Client

### 目的

降低 import 時副作用，讓測試與部署更穩。

### 問題點

目前有幾種 pattern 需要整理：

- import module 時建立 Gemini client。
- import module 時建立 Spotify singleton。
- 多個檔案各自呼叫 `load_dotenv()`。
- 部分檔案使用 `sys.path.append()`。

### 建議新增檔案

```text
services/settings.py
services/clients/
  __init__.py
  gemini_client.py
  spotify_client.py
```

### 修改內容

1. `load_dotenv()` 集中在 app 啟動或 settings。
2. 外部 client 改成 lazy initialization。
3. use case 接受 client 參數，或透過簡單 factory 取得。
4. 測試時用 fake client。

### 驗收標準

- import `services.features.*` 不會立刻初始化外部 API client。
- 測試可以不用真實 API key。
- `sys.path.append()` 可以逐步移除。

## Phase 7: 補文件與維護規則

### 修改內容

1. 更新 `Readme.md` 的專案結構。
2. 更新 `docs/architecture.md`，讓它反映實際完成後的架構。
3. 新增 API 使用範例。
4. 新增「新增功能 checklist」。

### 新增功能 checklist

```text
- [ ] 有 command parser 或 API route
- [ ] 有 use case
- [ ] use case 不 import LINE SDK
- [ ] use case result 是 JSON-native 結構
- [ ] 沒有在 use case result 保留舊 presenter/layout 欄位
- [ ] 有 LINE presenter
- [ ] 如需前端使用，有 REST API
- [ ] 有測試
- [ ] 不在 import 時初始化外部 client
```

## 完成紀錄（2026-07）

所有 Phase 已執行完畢。

```text
✅ Phase 0: pytest 穩定，mock 位置修正
✅ Phase 1: CommandResult / VALID_RESULT_TYPES 標準 dict 契約
✅ Phase 2: astro use case（JSON-native fortunes 結構，不含 star_counts）
✅ Phase 3: GET /api/astro REST API，與 LINE handler 共用同一 use case
✅ Phase 4: LINE adapter 拆出（line_webhook.py / line_sender.py），main.py 變薄
✅ Phase 5: 保留服務 use case 搬移（radar / ticket / podcast / answers_book）
            服務範圍收斂：停用 sixty_poem / music / lulu_chat / tarot / daily_meme
✅ Phase 6: 暫停服務 import 清除，gemini_reply lazy init，load_dotenv 集中在 main.py
✅ Phase 7: architecture.md 更新為現況，Readme.md 同步
```

## Backlog（未執行，不緊急）

- `/api/radar`、`/api/ticket`、`/api/podcast`、`/api/answers-book` REST API
- `plurk_image.py` import-time PlurkAPI 初始化改 lazy（每日梗圖服務暫停，不急）
- 暫停服務底層檔案（`spotify_service.py`、`tarot.py`、`daily_meme.py` 等）確認無引用後刪除
