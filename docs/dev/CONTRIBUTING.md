# CatchNews 开发规范

> 所有参与开发（含 AI 辅助开发）的代码必须遵守本文档。
> 机器可执行的规则同步在 `.cursor/rules/project-conventions.mdc` 与 `pyproject.toml`。

---

## 1 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端语言 | Python | 3.11+ |
| Web 框架 | FastAPI | 0.110+ |
| ORM | SQLAlchemy 2.x | 2.0+ |
| 数据库 | SQLite（个人版）/ PostgreSQL（产品版） | — |
| 调度 | APScheduler（个人版）/ Celery（产品版） | — |
| HTTP | httpx | 0.27+ |
| 前端 | Next.js App Router | 14+ |
| UI | Tailwind CSS + shadcn/ui | — |
| 容器 | Docker Compose | — |

不得自行替换技术栈；如需引入新依赖，须在 PR 中说明理由。

---

## 2 目录结构

```
catchNews/
├── docs/                  # 文档（按版本分类）
│   ├── personal/          # 个人版文档
│   ├── pro/               # 产品版文档
│   └── dev/               # 开发规范
├── backend/
│   ├── core/              # 共享核心（采集器、模型、校验器）
│   ├── personal/          # 个人版后端（独立可运行）
│   ├── pro/               # 产品版后端（独立可运行）
│   └── tests/             # 测试（按 core/personal/pro 分目录）
├── frontend/
│   ├── shared/            # 共享 UI 组件
│   ├── personal/          # 个人版 Next.js 应用
│   └── pro/               # 产品版前端（后续开发）
├── docker/                # Docker 编排（按版本分离）
├── design/                # Canvas 设计稿
├── pyproject.toml         # Ruff / mypy / pytest 配置
└── .cursor/rules/         # AI 开发规范
```

---

## 3 Python 代码规范

### 3.1 工具链

| 工具 | 用途 | 配置位置 |
|------|------|----------|
| Ruff format | 代码格式化（行宽 100） | `pyproject.toml` |
| Ruff lint | 静态检查 | `pyproject.toml` |
| mypy | 类型检查（strict） | `pyproject.toml` |
| pytest | 单元 / 集成测试 | `pyproject.toml` |

提交前运行：

```bash
ruff format backend/
ruff check backend/ --fix
mypy backend/core/ backend/personal/
```

### 3.2 命名规则

| 对象 | 风格 | 示例 |
|------|------|------|
| 文件 / 模块 | `snake_case` | `github_trending.py` |
| 类 | `PascalCase` | `GitHubTrendingCollector` |
| 函数 / 方法 | `snake_case` | `async def fetch()` |
| 常量 | `UPPER_SNAKE` | `ALLOWED_HOSTS` |
| Pydantic Schema | `PascalCase` + `Schema` | `HotItemSchema` |
| SQLAlchemy 模型 | `PascalCase` 无后缀 | `HotItem` |
| 数据库表 | `snake_case` 复数 | `hot_items` |

### 3.3 类型标注

- 所有公开函数必须有完整类型标注
- 使用 `X | None` 而非 `Optional[X]`
- 集合用小写泛型：`list[str]`、`dict[str, Any]`

### 3.4 错误处理

- 采集器内部捕获异常，不向调用方抛未处理异常
- 单平台失败不阻塞其他平台
- 异常写入结构化日志（含 `platform`、`duration`、`error`）

---

## 4 前端代码规范

### 4.1 工具链

| 工具 | 用途 |
|------|------|
| ESLint | 静态检查（Next.js + @typescript-eslint） |
| Prettier | 格式化（行宽 100，单引号，尾逗号 all） |
| TypeScript | 严格模式 `strict: true` |

### 4.2 命名规则

| 对象 | 风格 | 示例 |
|------|------|------|
| 组件文件 | `PascalCase.tsx` | `HotItemRow.tsx` |
| 工具 / hooks | `camelCase.ts` | `useHotItems.ts` |
| 组件 | `PascalCase` | `HotItemRow` |
| hooks | `use` 前缀 | `useHotItems` |
| 常量 | `UPPER_SNAKE` | `API_BASE_URL` |

### 4.3 组件

- 函数组件 + Hooks，禁止 class 组件
- Props 使用 `interface XxxProps` 定义
- 页面 -> `app/`，复用组件 -> `components/`

---

## 5 API 设计规范

- 前缀 `/api/v1`
- RESTful，资源名复数 kebab-case：`/hot-items`
- 查询参数 snake_case：`time_range`
- 响应结构：`{ items: [...], meta: {...} }`

---

## 6 Git 规范

### 6.1 分支

| 分支 | 用途 |
|------|------|
| `main` | 稳定版本 |
| `dev` | 日常开发 |
| `feature/xxx` | 功能分支 |
| `fix/xxx` | 修复分支 |

### 6.2 Commit 消息

格式：`<type>(<scope>): <subject>`

**type**：`feat` / `fix` / `refactor` / `docs` / `test` / `chore` / `style`
**scope**：`collector` / `api` / `model` / `frontend` / `config` / `docker`

```
feat(collector): 实现百度热搜采集器
fix(api): 修复 hot-items 分页参数缺失
chore(docker): 优化镜像体积
```

---

## 7 测试

- 后端：`backend/tests/`，pytest + pytest-asyncio
- 文件命名：`test_<module>.py`
- 采集器测试必须 mock HTTP，禁止真实请求
- 前端：Jest + React Testing Library

---

## 8 安全与配置

- 敏感配置通过 `.env` 注入，不硬编码
- `.env` 文件不入 Git，提供 `.env.example` 模板
- URL 写入与跳转前必须通过 `link_validator` 白名单校验
