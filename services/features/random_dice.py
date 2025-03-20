import random
import re

def random_dice(dice_type):
    """
    處理骰子擲骰請求
    支援格式：
    - 單一數字：返回 1-該數字 的隨機值
    - XdY：擲 X 個 Y 面骰子，返回總和和每個骰子的值
    - 1d20：特殊處理 D&D 風格的 d20 擲骰
    
    參數:
        dice_type (str): 骰子類型，如 "6"、"2d6"、"1d20" 等
        
    返回:
        dict: 包含結果總和、每個骰子的值和說明文字
    """
    # 處理 XdY 格式
    dice_pattern = re.compile(r'^(\d+)d(\d+)$', re.IGNORECASE)
    match = dice_pattern.match(str(dice_type).strip())
    
    if match:
        num_dice = int(match.group(1))
        dice_faces = int(match.group(2))
        
        # 限制骰子數量，避免過多計算
        if num_dice > 100:
            return {
                "total": 0,
                "rolls": [],
                "text": "骰子數量過多，請限制在 100 個以內"
            }
        
        # 限制骰子面數，避免不合理的值
        if dice_faces <= 0 or dice_faces > 1000:
            return {
                "total": 0,
                "rolls": [],
                "text": "骰子面數必須在 1-1000 之間"
            }
        
        # 擲骰
        rolls = [random.randint(1, dice_faces) for _ in range(num_dice)]
        total = sum(rolls)
        
        # 特殊處理 1d20
        if num_dice == 1 and dice_faces == 20:
            if rolls[0] == 20:
                text = f"🎲 擲出了 {rolls[0]} - 大成功！"
            elif rolls[0] == 1:
                text = f"🎲 擲出了 {rolls[0]} - 大失敗！"
            else:
                text = f"🎲 擲出了 {rolls[0]}"
        else:
            # 一般 XdY 格式
            if num_dice > 1:
                text = f"🎲 擲出了 {num_dice}d{dice_faces}: {total} ({' + '.join(map(str, rolls))})"
            else:
                text = f"🎲 擲出了 {dice_faces} 面骰: {total}"
        
        return {
            "total": total,
            "rolls": rolls,
            "text": text
        }
    
    # 處理單一數字（視為 1dX）
    try:
        faces = int(dice_type)
        if faces <= 0 or faces > 1000:
            return {
                "total": 0,
                "rolls": [],
                "text": "骰子面數必須在 1-1000 之間"
            }
        
        roll = random.randint(1, faces)
        return {
            "total": roll,
            "rolls": [roll],
            "text": f"🎲 擲出了 {faces} 面骰: {roll}"
        }
    except (ValueError, TypeError):
        # 不是有效的骰子格式
        return {
            "total": 0,
            "rolls": [],
            "text": "無效的骰子格式，請使用 XdY 或單一數字"
        }


def risk_dice():
    """
    風險骰子
    
    返回:
        str: 骰子圖片的 URL
    """
    dice_value = random.randint(1, 20)
    if dice_value == 20:
        # 大成功圖片
        res = "https://storage.googleapis.com/linebot01/dice/tw-11134201-7qul2-lhzv1nmfozwua7.jpeg"
    else:
        # 普通骰子圖片
        res = "https://storage.googleapis.com/linebot01/dice/22030923649549_637%20(1).jpg"
    
    return res


