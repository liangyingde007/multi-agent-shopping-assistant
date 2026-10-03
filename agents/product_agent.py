import json
from pathlib import Path

CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"

def load_catalog():
    with CATALOG_PATH.open(encoding="utf-8") as file:
        return json.load(file)

class ProductAgent:

    def search(self, task):
        if task["needs_clarification"]:
            return []
        budget = task["budget"]
        return [product for product in load_catalog() if product["category"] == task["category"] and (budget is None or product["price"] <= budget)]
