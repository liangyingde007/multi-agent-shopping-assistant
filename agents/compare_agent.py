from agents.planner_agent import PRIORITIES

class CompareAgent:
    def compare(self, products, task):
        ranked = []
        for product in products:
            supported = [key for key in task["priorities"] if key in product["ratings"]]
            selected = supported or ["value"]
            score = round(sum(product["ratings"][key] for key in selected) / len(selected) * 20)
            reasons = [f"{PRIORITIES[key]}示例评分 {product['ratings'][key]}/5" for key in selected]
            if task["budget"] is not None:
                reasons.append(f"示例价格在预算内，剩余 {task['budget'] - product['price']} 元")
            ranked.append({**product, "score": score, "reasons": reasons})
        return sorted(ranked, key=lambda product: (-product["score"], product["price"], product["id"]))
