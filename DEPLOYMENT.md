# 导购演示启动与部署

## 当前能力

同一个 FastAPI 服务返回网页与 JSON 接口。无需外部数据库、API Key 或模型费用。示例商品保存在随代码发布的只读 JSON 中，不存储访客个人资料或对话。

Planner 使用规则识别常见中文预算、品类与偏好；Product 严格过滤预算与品类；Compare 使用偏好对应的示例评分排序；Recommendation 输出推荐、备选与处理记录。角色按顺序执行，未使用 LLM、LangGraph 或 RAG。

`data/products.json` 中 12 个商品都是构造数据。明确填写的预算、品类和偏好优先于文字识别；未填写偏好时从文字识别，没有可识别偏好时按性价比评分。同分时按示例价格从低到高排序。

## 本地

Python 3.12。在仓库根目录：

```bash
python -m venv .venv
```

Windows 激活：`.venv\Scripts\Activate.ps1`；Linux 激活：`source .venv/bin/activate`。

```bash
python -m pip install -r requirements-deploy.txt
python -m backend.serve
```

浏览器打开 `http://127.0.0.1:8000/`。`backend.serve` 监听 `0.0.0.0`，供容器和服务器使用；仅本机预览可改用：

```bash
python -m uvicorn backend.main:app --host 127.0.0.1 --port 4180
```

## 容器

```bash
docker build -t lyd-shopping-demo .
docker run --rm -p 8000:8000 -e PORT=8000 lyd-shopping-demo
```

镜像使用非 root 用户，源码复制和构建上下文均限制为服务需要的文件。不要将原始简历、环境文件或其他仓库打包。

**本轮本地 Docker daemon 不可用，镜像构建尚未实测。** 已验证的是 Python 环境中的服务与接口。选定服务器后必须在实际 Linux / Docker 环境构建并运行，不能把 Dockerfile 已写好视为容器已验证。

## 可选平台模板

`render.yaml` 是待选方案，服务名 `lyd-shop` 是建议名称，不代表名称已占用或域名已经分配。可使用 Docker 部署，也可使用 Python Web Service：

- Build command: `python -m pip install -r requirements-deploy.txt`
- Start command: `python -m backend.serve`
- Python: 3.12；Health check: `/healthz`
- 平台提供 `PORT` 时自动使用；不要填入模型 Key、数据库密码或其他无用环境变量。

免费 Render 服务空闲 15 分钟后休眠，再次打开需要唤醒，官方说明约一分钟；不适合要求即时打开的求职展示。该服务的数据不需要写磁盘，避免依赖免费服务的临时文件系统。使用前检查最新条款与资源额度。[官方免费服务说明](https://render.com/docs/free)

如已有云服务器，优先在现有资源上部署，用 HTTPS 反向代理到本服务。此文档不代表已创建平台资源或同意付费方案。

## 验证与短链接

```bash
curl http://127.0.0.1:8000/healthz
curl -X POST http://127.0.0.1:8000/api/chat -H 'Content-Type: application/json' -d '{"query":"预算4000元，推荐拍照手机"}'
```

完整 HTTP 检查脚本在作品集工作目录 `D:\mywebsite\deployment\check_shopping.py`。将 `--url` 指向实际服务可重复检查。上线后还要实际在浏览器体验一次、检查匿名访问、手机布局与冷启动。

最终填写招聘系统的地址应直接进入可体验项目，不需要账户或仓库阅读。以实际分配域名为准，用 `len(url)` 校验包含 `https://` 的完整地址不超过 40 字符。当前未创建公网地址，本机 `127.0.0.1` 不能填给招聘方。
