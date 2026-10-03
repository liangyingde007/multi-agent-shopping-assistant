FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-deploy.txt ./
RUN pip install --no-cache-dir -r requirements-deploy.txt \
    && useradd --create-home --uid 10001 appuser
COPY backend ./backend
COPY agents/planner_agent.py agents/product_agent.py agents/compare_agent.py agents/recommendation_agent.py ./agents/
COPY workflow/graph.py ./workflow/graph.py
COPY data/products.json ./data/products.json
COPY web ./web
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '8000') + '/healthz', timeout=2)"
CMD ["python", "-m", "backend.serve"]
