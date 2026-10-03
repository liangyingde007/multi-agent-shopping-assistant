class RecommendationAgent:

    def generate(self, data, task):
        if task["needs_clarification"]:
            message = "想选手机、笔记本还是耳机？请选择品类，或在需求中告诉我。"
        elif not data:
            message = "示例商品库中没有符合该预算的商品。可以调整预算或品类，再试一次。"
        else:
            message = "已按预算筛选，再根据偏好对示例商品评分。以下结果供体验流程使用。"
        if task["ignored_priority_labels"]:
            message += f" 当前品类未设置{'、'.join(task['ignored_priority_labels'])}评分，已按可比较的偏好处理。"
        return {
            "recommendation": data[0] if data else None, "alternatives": data[1:3],
            "matched_count": len(data), "message": message, "task": task, "data_mode": "sample",
        }
