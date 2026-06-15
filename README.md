# CatchNews — 多源热点聚合（个人版 + 产品版）

多维度热点速览台：聚合娱乐、技术、新闻多源榜单，点击跳转官方原文。

## 仓库结构

```
catchNews/
├── backend/
│   ├── core/              # 共享采集器、模型、校验器
│   ├── personal/          # 个人版 API（M0 开发中）
│   └── pro/               # 产品版 API（占位）
├── frontend/
│   ├── personal/          # 个人版 Next.js
│   └── pro/               # 产品版（后续）
├── docker/
│   ├── personal/          # 个人版 Docker Compose
│   └── pro/               # 产品版（占位）
├── design/                # Cursor Canvas 原型
├── docs/                  # 文档（规范见 docs/dev/CONTRIBUTING.md）
├── 个人版.md              # 个人版产品方案
└── 产品版.md              # 产品版产品方案
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.11 + FastAPI + APScheduler + SQLite |
| 前端 | Next.js 14 + Tailwind CSS |
| 部署 | Docker Compose |

## 快速启动

### Docker（推荐）

```bash
cd docker/personal
docker compose up --build
```

- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

首次启动会自动采集 GitHub Trending；也可 `POST /api/v1/refresh` 手动触发。

### 本地开发

**Backend**

```bash
cd backend/personal
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install -r ../../requirements-dev.txt   # 可选：测试与 lint
copy .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend**

```bash
cd frontend/personal
copy .env.example .env.local
npm install
npm run dev
```

## 环境变量

| 文件 | 说明 |
|------|------|
| `backend/personal/.env` | 数据库、GitHub Token、刷新间隔、CORS |
| `frontend/personal/.env.local` | `NEXT_PUBLIC_API_URL` |

根目录 `.env.example` 仅为索引说明。

## 测试与 Lint

```bash
pip install -r backend/personal/requirements.txt -r requirements-dev.txt
ruff format backend/
ruff check backend/
pytest backend/tests -q
```

## 文档

| 文档 | 路径 |
|------|------|
| 个人版产品方案 | [个人版.md](./个人版.md) |
| 个人版需求文档 | [docs/personal/需求文档.md](./docs/personal/需求文档.md) |
| 产品版方案 | [产品版.md](./产品版.md) |
| 开发规范 | [docs/dev/CONTRIBUTING.md](./docs/dev/CONTRIBUTING.md) |

## 里程碑

- **M0**：GitHub Trending + Star 指标（当前）
- **M1**：微博 + 百度热搜，赛道 Tab
- **M2**：链接校验、本周汇总
- **M3**：收藏、导出

## License

[MIT](./LICENSE)
