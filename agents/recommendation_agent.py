class RecommendationAgent:

    def generate(self,data):
        return {
            "recommendation": data[0] if data else None
        }
