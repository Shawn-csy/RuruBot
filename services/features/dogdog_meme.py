import random

def dogdog_meme():
    meme_no = random.randint(1, 11)
    base_url = "https://storage.googleapis.com/linebot01/dogdog_meme/"

    
    match meme_no:
        case 7:
            filename = "07.webp"
        case 11:
            filename = "11.webp"
        case _:  # "_" 代表所有其他情況 (1-6, 8-10)
            # 使用 f-string 的 :02d 格式化
            # 不足兩位數時，前面自動補 0 (例如 5 -> "05")
            # 剛好兩位數時，保持不變 (例如 10 -> "10")
            filename = f"{meme_no:02d}.jpg"

    meme_url = base_url + filename
    return meme_url