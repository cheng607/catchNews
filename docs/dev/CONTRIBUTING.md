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

> 详细工作流参见 [开发指南](./开发指南.md) 第 3 章。

### 6.1 分支策略

| 分支 | 命名示例 | 来源 → 目标 | 说明 |
|------|----------|-------------|------|
| `main` | — | — | 稳定可发布版本，仅通过 `dev` 合入 |
| `dev` | — | `main` → `main` | 日常开发集成，所有功能先合到这里 |
| `feature/xxx` | `feature/M0-github-collector` | `dev` → `dev` | 功能开发，建议用里程碑编号前缀 |
| `fix/xxx` | `fix/weibo-parse-error` | `dev` → `dev` | Bug 修复 |
| `hotfix/xxx` | `hotfix/link-crash` | `main` → `main` + `dev` | 线上紧急修复 |

### 6.2 Commit 消息（中文）

格式：`<类型>: <中文简要描述>`

- **类型**：英文，见下表
- **中文简要描述**：必填，用中文概括本次变更（一行，50 字以内为宜）

**类型**：

| 类型 | 含义 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复缺陷 |
| `refactor` | 重构（不改变外部行为） |
| `docs` | 文档变更 |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖/CI |
| `style` | 代码格式（不影响逻辑） |
| `perf` | 性能优化 |

**示例**：

```
feat: 实现百度热搜采集
fix: 修复 hot-items 分页参数缺失
test: 添加 GitHub Trending mock 测试
chore: 优化后端镜像体积
docs: 补充本地启动说明
```

**多行 commit（复杂变更时）**：

```
feat: 实现 GitHub Trending 页面解析

- 支持 daily / weekly 两个维度
- 使用 selectolax 解析 HTML，提取 repo 名、语言、Star 数
- 异常时返回空列表，不阻塞其他采集器

关联: M0 里程碑
```

### 6.3 Tag 版本号

格式：`v<主版本>.<里程碑>.<补丁>`

| Tag | 时机 |
|-----|------|
| `v0.1.0` | M0 完成 |
| `v0.2.0` | M1 完成 |
| `v0.3.0` | M2 完成 |
| `v0.4.0` | M3 完成 |
| `v1.0.0` | 个人版正式发布 |

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
