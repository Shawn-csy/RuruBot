import json
import random
import os
from dotenv import load_dotenv
import requests
from services.features.gemini_reply import get_gemini_reply

load_dotenv()

api_url = os.getenv("TAROT_API_URL")


# ==================== 新版塔羅 API 功能 ====================
def tarot_api_function(method, question):
    """
    使用外部 API 進行塔羅占卜

    Args:
        method: 占卜方式 ("daily" 或 "question")
        question: 使用者的問題 (僅在 method="question" 時需要)

    Returns:
        dict: 包含 success 和 data 的字典
    """
    try:
        match method:
            case "daily":
                data = {
                    "question_type": "daily-tarot",
                    "response_type":"json"
                }
            case "question":
                data = {
                    "question_type": "question-tarot",
                    "message": question
                }
            case _:
                # 暫時默認用這個
                data = {
                    "question_type": "daily-tarot"
                }

        res = requests.post(url=api_url, json=data, timeout=40)
        res.raise_for_status()

        return {
            "success": True,
            "data": res.text
        }
    except Exception as e:
        print(f"Tarot API error: {e}")
        return {
            "success": False,
            "error": str(e)
        }


# ==================== 本地塔羅功能 (API fallback 備用) ====================

# 模組級快取：只在第一次載入時讀取檔案
_TAROT_CARDS_CACHE = None
_TAROT_SPREADS_CACHE = None


def load_tarot_data():
    """
    載入塔羅牌和牌陣的 JSON 資料(使用快取)

    第一次呼叫時從檔案讀取,之後直接從記憶體快取返回
    """
    global _TAROT_CARDS_CACHE, _TAROT_SPREADS_CACHE

    # 如果快取已存在,直接返回
    if _TAROT_CARDS_CACHE is not None and _TAROT_SPREADS_CACHE is not None:
        return _TAROT_CARDS_CACHE, _TAROT_SPREADS_CACHE

    # 第一次載入：從檔案讀取
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))

    tarot_card_path = os.path.join(project_root, 'statics', 'tarot_card.json')
    tarot_spread_path = os.path.join(project_root, 'statics', 'tarot_spread.json')

    with open(tarot_card_path, 'r', encoding='utf-8') as f:
        tarot_cards = json.load(f)

    with open(tarot_spread_path, 'r', encoding='utf-8') as f:
        tarot_spreads = json.load(f)

    # 儲存到快取
    _TAROT_CARDS_CACHE = tarot_cards['cards']
    _TAROT_SPREADS_CACHE = tarot_spreads['spreads']

    return _TAROT_CARDS_CACHE, _TAROT_SPREADS_CACHE


def random_tarot_picker(num_cards):
    """
    隨機抽取指定數量的塔羅牌

    Args:
        num_cards: 要抽取的牌數

    Returns:
        list: 抽取的牌陣資料,每張牌包含牌名、正逆位、關鍵字等資訊
    """
    cards, _ = load_tarot_data()

    # 隨機抽取不重複的牌
    selected_cards = random.sample(cards, num_cards)

    # 為每張牌決定正逆位
    drawn_cards = []
    for card in selected_cards:
        is_upright = random.choice([True, False])

        drawn_card = {
            'name': card['name'],
            'arcana': card['arcana'],
            'is_upright': is_upright,
            'position': is_upright,  # True=正位, False=逆位
            'keywords': card['upright_keywords'] if is_upright else card['reversed_keywords'],
            'love_meaning': card.get('love_meaning', {}).get('upright' if is_upright else 'reversed', ''),
            'career_meaning': card.get('career_meaning', {}).get('upright' if is_upright else 'reversed', ''),
            'fortune_meaning': card.get('fortune_meaning', {}).get('upright' if is_upright else 'reversed', '')
        }
        drawn_cards.append(drawn_card)

    return drawn_cards


def _parse_ai_response(ai_response, drawn_cards, spread_info):
    """
    解析 AI 回應,分離綜合建議和各牌解析

    Args:
        ai_response: AI 的原始回應文本
        drawn_cards: 抽取的牌陣
        spread_info: 牌陣資訊

    Returns:
        dict: 包含 'overall' (綜合建議) 和 'cards' (各牌解析) 的字典
    """
    # 使用【位置】作為分隔符號
    sections = ai_response.split('【位置')

    # 第一段是綜合建議
    overall_advice = sections[0].strip()

    # 後續段落是各牌解析
    card_analyses = []
    for i, section in enumerate(sections[1:], 1):
        # 重新加上【位置】
        card_analysis = '【位置' + section.strip()
        card_analyses.append(card_analysis)

    # 如果 AI 沒有按格式輸出,則回傳原始內容
    if not card_analyses:
        # 嘗試用其他分隔符號
        if '【' in ai_response and '】' in ai_response:
            # 有標題但格式不同,保留原樣
            return {
                'overall': overall_advice,
                'cards': [ai_response]
            }
        else:
            # 完全沒有結構,將整段視為綜合建議
            return {
                'overall': ai_response,
                'cards': []
            }

    return {
        'overall': overall_advice,
        'cards': card_analyses
    }


def ai_process(drawn_cards, spread_info, question):
    """
    使用 AI 解讀塔羅牌

    Args:
        drawn_cards: 抽取的牌陣
        spread_info: 牌陣資訊
        question: 使用者的問題

    Returns:
        str: Markdown 格式的每日塔羅結果 (與 API 格式相同)
    """
    # 組建 prompt - 要求輸出 Markdown 格式
    system_prompt = """你是一位深具靈性與洞察力的塔羅占卜師。
你熟悉大阿爾克納與小阿爾克納的象徵意涵，能夠從每張牌的能量與圖像中，看出今日的情緒流動與生活狀態。

這次的占卜主題是：「今日運勢」。
請依序解讀三個面向：愛情運、事業運、財運。
每個面向各對應一張牌，最後再根據解讀結果評估整體運勢。

**重要：請嚴格按照以下 Markdown 格式輸出**

## 💞 **愛情運**
**牌名**: [塔羅牌名稱] ([正位/逆位])

[3-5 行文字描述愛情運勢的解讀，語氣溫柔、具有洞察力]

**建議**: [一句簡短的行動建議]

---

## 💼 **事業運**
**牌名**: [塔羅牌名稱] ([正位/逆位])

[3-5 行文字描述事業運勢的解讀，語氣溫柔、具有洞察力]

**建議**: [一句簡短的行動建議]

---

## 💰 **財運**
**牌名**: [塔羅牌名稱] ([正位/逆位])

[3-5 行文字描述財運的解讀，語氣溫柔、具有洞察力]

**建議**: [一句簡短的行動建議]

---

## 🌟 **整體運勢**

[2-3 行綜合前三張牌的能量，評估整體氛圍]

---

## ✨ **今日訊息**

[一句溫柔的祝福或鼓勵，例如：「相信今天的每一步，都在為明天鋪路。」]

占卜風格設定：
1. 專業 - 說明每張牌的象徵與能量
2. 溫柔引導 - 語氣安定、理解,不提問
3. 同理 - 理解情緒起伏,語氣柔和支持
4. 啟發 - 給出具體小建議

**請務必完全按照上述 Markdown 格式輸出，包含所有標題和分隔線。**
"""

    # 組裝牌陣資訊 - 簡化為 Markdown 格式
    cards_description = "**抽到的牌**:\n"

    # 根據牌陣位置對應到每日運勢面向
    position_labels = ["愛情運", "事業運", "財運"]

    for i, card in enumerate(drawn_cards[:3], 0):  # 只取前 3 張牌
        label = position_labels[i] if i < len(position_labels) else f"位置{i+1}"
        orientation = "正位" if card['is_upright'] else "逆位"
        cards_description += f"- {label}: {card['name']} ({orientation})\n"

    # 完整 prompt
    full_prompt = f"""{cards_description}

請根據以上抽到的牌，為今日運勢進行解讀。
記得完全按照 Markdown 格式輸出，包含所有 emoji 和標題。
"""

    # 呼叫 AI
    try:
        response = get_gemini_reply(full_prompt, system_prompt)
        # 直接返回 Markdown 格式的字串
        return response
    except Exception as e:
        return f"解讀過程發生錯誤：{str(e)}"


def parse_reply(ai_response, drawn_cards, spread_info):
    """
    格式化 AI 回應為易讀的文本格式

    Args:
        ai_response: AI 的解析結果 (dict 或 str)
        drawn_cards: 抽取的牌陣
        spread_info: 牌陣資訊

    Returns:
        str: 格式化後的輸出文本
    """
    output = []

    # 處理錯誤情況
    if isinstance(ai_response, dict) and 'error' in ai_response:
        return ai_response['error']

    # 標題區塊
    output.append("━" * 30)
    output.append(f"✨ {spread_info['spread_name']}")
    output.append("━" * 30)
    output.append("")

    # 顯示抽到的牌 (簡潔版)
    output.append("🎴 抽到的牌")
    for i, card in enumerate(drawn_cards, 1):
        position_meaning = spread_info['positions'][i-1]['meaning']
        orientation = "正位⬆" if card['is_upright'] else "逆位⬇"
        output.append(f"{i}. {position_meaning}")
        output.append(f"   {card['name']} ({orientation})")

    output.append("")
    output.append("━" * 30)

    # 綜合建議
    output.append("💡 綜合建議")
    output.append("━" * 30)

    if isinstance(ai_response, dict):
        # 如果是結構化回應
        output.append(ai_response.get('overall', ''))
        output.append("")

        # 各牌解析
        if ai_response.get('cards'):
            output.append("━" * 30)
            output.append("📖 牌義解析")
            output.append("━" * 30)
            output.append("")

            for card_analysis in ai_response['cards']:
                output.append(card_analysis)
                output.append("")
    else:
        # 如果是純文字回應 (舊版相容)
        output.append(ai_response)
        output.append("")

    output.append("━" * 30)

    return "\n".join(output)


def tarot_function(question=None, spread_name="時間之流占卜法"):
    """
    塔羅牌占卜主函數 (本地版本,作為 API fallback)

    Args:
        question: 使用者的問題,如果為 None 則預設為「今天的運勢」
        spread_name: 使用的牌陣名稱,預設為「時間之流占卜法」

    Returns:
        str: Markdown 格式的每日塔羅結果 (與 API 格式相同)
    """
    # 處理預設問題
    if question is None or question.strip() == "":
        question = "今天的運勢如何？"

    # 載入牌陣資料
    _, spreads = load_tarot_data()

    # 尋找指定的牌陣 (每日運勢固定用 3 張牌)
    spread_info = None
    for spread in spreads:
        if spread['spread_name'] == spread_name:
            spread_info = spread
            break

    if spread_info is None:
        return f"找不到牌陣「{spread_name}」,請檢查牌陣名稱。"

    # 隨機抽 3 張牌 (愛情運、事業運、財運)
    drawn_cards = random_tarot_picker(3)

    # AI 解讀 - 直接返回 Markdown 格式
    markdown_output = ai_process(drawn_cards, spread_info, question)

    return markdown_output


# ==================== 整合函數 (優先使用 API, 失敗時 fallback 到本地) ====================

def tarot_with_fallback(method="daily", question=None, spread_name="時間之流占卜法"):
    """
    智能塔羅占卜函數：優先使用 API,失敗時自動切換到本地解法

    Args:
        method: API 占卜方式 ("daily" 或 "question")
        question: 使用者的問題
        spread_name: 牌陣名稱 (僅用於本地 fallback)

    Returns:
        dict: {
            "success": bool,
            "data": str,  # 占卜結果
            "source": str  # "api" 或 "local"
        }
    """
    # 先嘗試使用 API
    api_result = tarot_api_function(method, question)

    if api_result["success"]:
        return {
            "success": True,
            "data": api_result["data"],
            "source": "api"
        }

    # API 失敗,切換到本地解法
    print(f"API 失敗 ({api_result.get('error')}),切換到本地塔羅解法")

    try:
        local_result = tarot_function(question, spread_name)
        return {
            "success": True,
            "data": local_result,
            "source": "local"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"API 和本地解法都失敗: {str(e)}",
            "source": "none"
        }
