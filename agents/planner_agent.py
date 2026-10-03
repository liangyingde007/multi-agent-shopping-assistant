"""Parse supported shopping needs without calling an external model."""
import re

CATEGORIES = {"phone": "手机", "laptop": "笔记本", "headphones": "耳机"}
PRIORITIES = {"camera": "拍照", "performance": "性能", "battery": "续航", "portable": "便携", "value": "性价比", "office": "办公", "gaming": "游戏", "audio": "音质", "noise": "降噪"}
CATEGORY_WORDS = {"headphones": ("耳机", "降噪", "听歌"), "laptop": ("笔记本", "电脑", "编程", "办公本", "游戏本", "轻薄本"), "phone": ("手机", "拍照", "摄影")}
CATEGORY_PRIORITIES = {
    "phone": ("camera", "performance", "battery", "portable", "value", "gaming"),
    "laptop": ("performance", "battery", "portable", "value", "office", "gaming"),
    "headphones": ("audio", "noise", "battery", "portable", "value"),
}
PRIORITY_WORDS = {
    "camera": ("拍照", "摄影", "影像"), "performance": ("性能", "流畅", "编程", "开发"),
    "battery": ("续航", "电池"), "portable": ("轻薄", "便携", "通勤"),
    "value": ("性价比", "便宜", "实惠"), "office": ("办公", "文档"),
    "gaming": ("游戏", "电竞"), "audio": ("音质", "听歌", "音乐"), "noise": ("降噪", "安静"),
}

def parse_budget(query):
    patterns = (r"(?:预算|不超过|最多|上限)\s*(\d+(?:\.\d+)?)\s*([千万元kK]?)", r"(\d+(?:\.\d+)?)\s*([千万元kK]?)\s*(?:块|元|以内|以下)")
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            unit = match.group(2)
            multiplier = 1000 if unit in ("千", "k", "K") else 10000 if unit == "万" else 1
            return int(float(match.group(1)) * multiplier)
    return None

class PlannerAgent:
    def plan(self, query, budget=None, category=None, priorities=None):
        selected_category = category or next((key for key, words in CATEGORY_WORDS.items() if any(word in query for word in words)), None)
        parsed_budget = budget if budget is not None else parse_budget(query)
        detected = [key for key, words in PRIORITY_WORDS.items() if any(word in query for word in words)]
        selected_priorities = list(dict.fromkeys(priorities or detected or ["value"]))
        supported = CATEGORY_PRIORITIES.get(selected_category, tuple(PRIORITIES))
        ignored = [PRIORITIES[key] for key in selected_priorities if key not in supported]
        selected_priorities = [key for key in selected_priorities if key in supported] or ["value"]
        return {
            "query": query, "intent": "shopping", "category": selected_category,
            "category_label": CATEGORIES.get(selected_category), "budget": parsed_budget,
            "priorities": selected_priorities, "priority_labels": [PRIORITIES[key] for key in selected_priorities],
            "needs_clarification": selected_category is None,
            "ignored_priority_labels": ignored,
        }
