from agents.planner_agent import PlannerAgent
from agents.product_agent import ProductAgent
from agents.compare_agent import CompareAgent
from agents.recommendation_agent import RecommendationAgent

def run_workflow(query):

    planner = PlannerAgent()
    product = ProductAgent()
    compare = CompareAgent()
    recommend = RecommendationAgent()

    task = planner.plan(query)
    products = product.search(task)
    result = compare.compare(products)

    return recommend.generate(result)
