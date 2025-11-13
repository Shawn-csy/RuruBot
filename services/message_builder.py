"""
LINE 訊息構建器 - 將業務資料轉換為 LINE 訊息對象
"""
from linebot.v3.messaging import (
    TextMessage, ImageMessage, FlexMessage, FlexContainer
)
from typing import Dict, Any, List, Union


def build_text_message(text: str) -> TextMessage:
    """構建文字訊息"""
    if not isinstance(text, str):
        if isinstance(text, list):
            text = "\n\n".join(text)
        else:
            text = str(text)

    if not text.strip():
        text = "抱歉，沒有獲取到資訊"

    return TextMessage(text=text)


def build_image_message(url: str) -> ImageMessage:
    """構建圖片訊息"""
    return ImageMessage(
        originalContentUrl=url,
        previewImageUrl=url
    )


def build_flex_message(flex_data: Union[Dict[str, Any], FlexMessage], alt_text: str = "Flex Message") -> FlexMessage:
    """構建 Flex 訊息"""
    # 如果已經是 FlexMessage 對象，直接返回
    if isinstance(flex_data, FlexMessage):
        return flex_data

    # 如果 flex_data 包含 content 和 alt_text，解包
    if isinstance(flex_data, dict):
        if "content" in flex_data:
            flex_json = flex_data["content"]
            alt_text = flex_data.get("alt_text", alt_text)
        else:
            flex_json = flex_data

        flex_container = FlexContainer.from_dict(flex_json)
        return FlexMessage(alt_text=alt_text, contents=flex_container)

    # 其他情況返回錯誤訊息
    raise TypeError(f"flex_data 必須是 dict 或 FlexMessage，但得到 {type(flex_data)}")


def build_messages_from_result(result: Dict[str, Any]) -> List[Union[TextMessage, ImageMessage, FlexMessage]]:
    """
    從舊的 result 格式構建訊息列表（向後兼容）

    Args:
        result: {"type": "text/image/flex/mixed", "data": ...}

    Returns:
        LINE 訊息對象列表
    """
    if result is None:
        return []

    result_type = result.get("type", "text")
    data = result.get("data")

    if result_type == "text":
        return [build_text_message(data)]

    elif result_type == "image":
        # data 可能是單個 URL 或 URL 列表
        if isinstance(data, str):
            return [build_image_message(data)]
        elif isinstance(data, list):
            return [build_image_message(url) for url in data]

    elif result_type == "flex":
        return [build_flex_message(data)]

    elif result_type == "mixed":
        # data 是訊息列表
        messages = []
        for msg_data in data:
            msg_type = msg_data.get("type")

            if msg_type == "text":
                messages.append(build_text_message(msg_data.get("text", "")))
            elif msg_type == "image":
                messages.append(build_image_message(msg_data.get("url", "")))
            elif msg_type == "flex":
                messages.append(build_flex_message(
                    msg_data.get("content", {}),
                    msg_data.get("alt_text", "Flex Message")
                ))

        return messages

    return [build_text_message("抱歉，發生未知錯誤")]
