from agents.planner_agent import PlannerAgent
from agents.product_agent import ProductAgent
from agents.compare_agent import CompareAgent
from agents.recommendation_agent import RecommendationAgent

def run_workflow(query, budget=None, category=None, priorities=None):

    planner = PlannerAgent()
    product = ProductAgent()
    compare = CompareAgent()
    recommend = RecommendationAgent()

    task = planner.plan(query, budget, category, priorities)
    products = product.search(task)
    result = compare.compare(products, task)

    answer = recommend.generate(result, task)
    answer["trace"] = [
        {"role": "Planner", "label": "理解需求", "detail": f"品类：{task['category_label'] or '待确认'}；预算：{str(task['budget']) + ' 元' if task['budget'] is not None else '未限定'}；偏好：{'、'.join(task['priority_labels'])}"},
        {"role": "Product", "label": "筛选商品", "detail": f"在本地示例商品库中找到 {len(products)} 个符合品类与预算的候选。"},
        {"role": "Compare", "label": "比较偏好", "detail": "根据所选偏好的示例评分排序；同分时优先选择示例价格更低的商品。"},
        {"role": "Recommendation", "label": "生成推荐", "detail": f"提供 {min(len(result), 3)} 个候选及匹配理由。" if result else answer["message"]},
    ]
    return answer
