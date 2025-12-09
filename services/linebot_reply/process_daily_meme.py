"""
處理每日梗圖的 LINE Bot 回覆格式
"""
from linebot.v3.messaging import (
    ImageCarouselTemplate,
    ImageCarouselColumn,
    TemplateMessage,
    URIAction
)
from typing import List


def process_daily_meme_carousel(image_urls: List[str], date_str: str = "今日") -> TemplateMessage:
    """
    將梗圖 URL 列表轉換為 Image Carousel 格式

    Args:
        image_urls: 圖片 URL 列表
        date_str: 日期字串 (用於顯示)

    Returns:
        TemplateMessage: LINE Image Carousel 訊息
    """
    # Image Carousel 最多支援 10 個 columns
    # 如果圖片超過 10 張,只取前 10 張
    max_images = 10
    display_urls = image_urls[:max_images]

    # 建立 Image Carousel Columns
    columns = []
    for i, url in enumerate(display_urls, 1):
        column = ImageCarouselColumn(
            image_url=url,
            action=URIAction(
                label=f"查看圖片 {i}",
                uri=url
            )
        )
        columns.append(column)

    # 建立 Image Carousel Template
    template = ImageCarouselTemplate(columns=columns)

    # 建立 Template Message
    total_count = len(image_urls)
    alt_text = f"{date_str}梗圖 (共 {total_count} 張)"
    if total_count > max_images:
        alt_text += f" - 顯示前 {max_images} 張"

    message = TemplateMessage(
        alt_text=alt_text,
        template=template
    )

    return message
