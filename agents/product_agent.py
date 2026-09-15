import json

class ProductAgent:

    def search(self, task):
        with open("data/products.json",encoding="utf-8") as f:
            return json.load(f)
