from dataclasses import dataclass
from typing import Any, Literal

# "astro" 等 domain-specific type 等 Phase 2 presenter 設計好再新增
ResultType = Literal["text", "image", "flex", "mixed", "error"]

# handler 合法回傳：標準 dict 或 None（表示不回覆）
# None 由 message_builder.build_messages_from_result 轉為空列表
VALID_RESULT_TYPES = ("text", "image", "flex", "mixed", "error")


@dataclass
class CommandResult:
    type: ResultType
    data: Any

    def to_dict(self) -> dict:
        return {"type": self.type, "data": self.data}
