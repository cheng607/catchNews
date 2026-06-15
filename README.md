# CatchNews 个人版

多维度热点速览台 — 聚合娱乐、技术、新闻多源榜单，点击跳转官方原文。

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11 + FastAPI + APScheduler + SQLite |
| 前端 | Next.js 14 + Tailwind CSS + shadcn/ui |
| 部署 | Docker Compose |

## 目录结构

```
catchNews/
├── backend/          # FastAPI 采集与 API
├── frontend/         # Next.js Web UI
├── design/           # UI 设计稿（Canvas）
├── 个人版.md         # 产品方案
└── 需求文档-个人版.md # 开发需求文档
```

## 快速启动

### Docker（推荐）

```bash
docker compose up --build
```

- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 本地开发

**Backend**

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**

```bash
cd frontend
copy .env.example .env.local
npm install
npm run dev
```

## 里程碑

- **M0**：GitHub Trending + Star 指标
- **M1**：微博 + 百度热搜，赛道 Tab
- **M2**：链接校验、本周汇总、自动刷新
- **M3**：收藏、导出、Docker 打包完善

详见 [需求文档-个人版.md](./需求文档-个人版.md)。
