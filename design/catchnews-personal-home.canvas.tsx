import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Divider,
  H2,
  H3,
  Link,
  Pill,
  Row,
  Spacer,
  Stack,
  Table,
  Text,
  TextInput,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type RankChange = { type: "up" | "down" | "new" | "flat"; value?: number };

type HotItem = {
  rank: number;
  title: string;
  heat: string;
  change: RankChange;
  url: string;
};

type GitHubItem = {
  rank: number;
  repo: string;
  language: string;
  stars: string;
  today: number;
  week: number;
  change: RankChange;
  url: string;
};

type WeeklyItem = {
  title: string;
  source: string;
  detail: string;
  url: string;
};

const TRACK_TABS = ["全部", "娱乐", "技术", "新闻"] as const;
const TIME_TABS = ["实时", "今日", "本周"] as const;
const ENT_SOURCES = ["微博", "百度"] as const;

const WEIBO_HOT: HotItem[] = [
  { rank: 1, title: "某顶流演唱会开票秒空", heat: "1.24M", change: { type: "up", value: 2 }, url: "https://s.weibo.com/weibo?q=%23%E6%BC%94%E5%94%B1%E4%BC%9A%23" },
  { rank: 2, title: "春季档电影票房破30亿", heat: "986K", change: { type: "down", value: 1 }, url: "https://s.weibo.com/weibo?q=%23%E7%94%B5%E5%BD%B1%23" },
  { rank: 3, title: "多地发布高温橙色预警", heat: "872K", change: { type: "new" }, url: "https://s.weibo.com/weibo?q=%23%E9%AB%98%E6%B8%A9%23" },
  { rank: 4, title: "AI换脸监管新规征求意见", heat: "756K", change: { type: "up", value: 5 }, url: "https://s.weibo.com/weibo?q=%23AI%23" },
  { rank: 5, title: "某综艺嘉宾退赛引热议", heat: "698K", change: { type: "flat" }, url: "https://s.weibo.com/weibo?q=%23%E7%BB%BC%E8%89%BA%23" },
  { rank: 6, title: "高考志愿填报攻略", heat: "621K", change: { type: "down", value: 3 }, url: "https://s.weibo.com/weibo?q=%23%E9%AB%98%E8%80%83%23" },
  { rank: 7, title: "国产游戏Steam特别好评", heat: "589K", change: { type: "up", value: 4 }, url: "https://s.weibo.com/weibo?q=%23Steam%23" },
  { rank: 8, title: "某城市地铁新线开通", heat: "512K", change: { type: "down", value: 2 }, url: "https://s.weibo.com/weibo?q=%23%E5%9C%B0%E9%93%81%23" },
  { rank: 9, title: "网红餐厅排队8小时", heat: "478K", change: { type: "new" }, url: "https://s.weibo.com/weibo?q=%23%E7%BE%8E%E9%A3%9F%23" },
  { rank: 10, title: "端午假期出行预测", heat: "445K", change: { type: "up", value: 1 }, url: "https://s.weibo.com/weibo?q=%23%E7%AB%AF%E5%8D%88%23" },
];

const BAIDU_HOT: HotItem[] = [
  { rank: 1, title: "DeepSeek 发布新模型版本", heat: "892万", change: { type: "up", value: 3 }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 2, title: "全国多地迎来强降雨", heat: "756万", change: { type: "down", value: 1 }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 3, title: "新能源汽车销量数据公布", heat: "698万", change: { type: "new" }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 4, title: "某省高考分数线公布", heat: "621万", change: { type: "up", value: 2 }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 5, title: "苹果WWDC开发者大会", heat: "589万", change: { type: "flat" }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 6, title: "某明星官宣恋情", heat: "534万", change: { type: "down", value: 4 }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 7, title: "租房市场最新报告", heat: "498万", change: { type: "up", value: 1 }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 8, title: "医保新政解读", heat: "467万", change: { type: "down", value: 2 }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 9, title: "某球队夺冠庆祝", heat: "421万", change: { type: "new" }, url: "https://top.baidu.com/board?tab=realtime" },
  { rank: 10, title: "夏季防晒产品测评", heat: "389万", change: { type: "up", value: 6 }, url: "https://top.baidu.com/board?tab=realtime" },
];

const GITHUB_TRENDING: GitHubItem[] = [
  { rank: 1, repo: "anthropics/claude-code", language: "TypeScript", stars: "12.4k", today: 892, week: 3200, change: { type: "up", value: 1 }, url: "https://github.com/anthropics/claude-code" },
  { rank: 2, repo: "google-gemini/gemini-cli", language: "Go", stars: "8.7k", today: 654, week: 2100, change: { type: "new" }, url: "https://github.com/google-gemini/gemini-cli" },
  { rank: 3, repo: "fastapi/fastapi", language: "Python", stars: "82.1k", today: 421, week: 1850, change: { type: "down", value: 1 }, url: "https://github.com/fastapi/fastapi" },
  { rank: 4, repo: "vercel/next.js", language: "JavaScript", stars: "134k", today: 387, week: 1620, change: { type: "flat" }, url: "https://github.com/vercel/next.js" },
  { rank: 5, repo: "openai/codex", language: "Rust", stars: "5.2k", today: 356, week: 1480, change: { type: "up", value: 3 }, url: "https://github.com/openai/codex" },
  { rank: 6, repo: "langchain-ai/langgraph", language: "Python", stars: "9.8k", today: 298, week: 1120, change: { type: "up", value: 2 }, url: "https://github.com/langchain-ai/langgraph" },
  { rank: 7, repo: "tailwindlabs/tailwindcss", language: "TypeScript", stars: "86.3k", today: 245, week: 980, change: { type: "down", value: 2 }, url: "https://github.com/tailwindlabs/tailwindcss" },
  { rank: 8, repo: "oven-sh/bun", language: "Zig", stars: "78.5k", today: 198, week: 870, change: { type: "flat" }, url: "https://github.com/oven-sh/bun" },
  { rank: 9, repo: "microsoft/playwright", language: "TypeScript", stars: "71.2k", today: 176, week: 720, change: { type: "down", value: 1 }, url: "https://github.com/microsoft/playwright" },
  { rank: 10, repo: "hashicorp/terraform", language: "Go", stars: "44.6k", today: 142, week: 610, change: { type: "up", value: 1 }, url: "https://github.com/hashicorp/terraform" },
];

const WEEKLY_PERSISTENT: WeeklyItem[] = [
  { title: "某顶流演唱会开票秒空", source: "微博", detail: "在榜 5 天 · 最高 #2", url: "https://s.weibo.com/weibo" },
  { title: "DeepSeek 发布新模型版本", source: "百度", detail: "在榜 4 天 · 最高 #1", url: "https://top.baidu.com/board" },
  { title: "anthropics/claude-code", source: "GitHub", detail: "7 日 Star +3,200", url: "https://github.com/anthropics/claude-code" },
  { title: "AI换脸监管新规征求意见", source: "微博", detail: "在榜 3 天 · 最高 #4", url: "https://s.weibo.com/weibo" },
  { title: "google-gemini/gemini-cli", source: "GitHub", detail: "7 日 Star +2,100 · 本周新上榜", url: "https://github.com/google-gemini/gemini-cli" },
  { title: "苹果WWDC开发者大会", source: "百度", detail: "在榜 6 天 · 最高 #3", url: "https://top.baidu.com/board" },
];

function RankBadge({ change, theme }: { change: RankChange; theme: ReturnType<typeof useHostTheme> }) {
  if (change.type === "new") {
    return (
      <Text size="small" weight="semibold" style={{ color: theme.accent.primary, minWidth: 36, textAlign: "right" }}>
        NEW
      </Text>
    );
  }
  if (change.type === "flat") {
    return (
      <Text size="small" tone="quaternary" style={{ minWidth: 36, textAlign: "right" }}>
        —
      </Text>
    );
  }
  const isUp = change.type === "up";
  return (
    <Text
      size="small"
      weight="semibold"
      style={{
        color: isUp ? theme.category.green : theme.diff.stripRemoved,
        minWidth: 36,
        textAlign: "right",
      }}
    >
      {isUp ? "↑" : "↓"}
      {change.value}
    </Text>
  );
}

function TabBar<T extends string>({
  tabs,
  active,
  onChange,
}: {
  tabs: readonly T[];
  active: T;
  onChange: (tab: T) => void;
}) {
  return (
    <Row gap={6} wrap>
      {tabs.map((tab) => (
        <Pill key={tab} active={tab === active} onClick={() => onChange(tab)} size="sm">
          {tab}
        </Pill>
      ))}
    </Row>
  );
}

function EntertainmentPanel({
  source,
  onSourceChange,
  items,
  updatedAt,
  theme,
}: {
  source: (typeof ENT_SOURCES)[number];
  onSourceChange: (s: (typeof ENT_SOURCES)[number]) => void;
  items: HotItem[];
  updatedAt: string;
  theme: ReturnType<typeof useHostTheme>;
}) {
  return (
    <Stack gap={10}>
      <Row align="center" justify="space-between">
        <H3 style={{ margin: 0 }}>娱乐热点</H3>
        <TabBar tabs={ENT_SOURCES} active={source} onChange={onSourceChange} />
      </Row>
      <Table
        headers={["#", "标题", "热度", "变化"]}
        columnAlign={["right", "left", "right", "right"]}
        rows={items.map((item) => [
          <Text key="r" weight="semibold" tone="secondary" size="small">
            {item.rank}
          </Text>,
          <Link key="t" href={item.url}>
            <Text truncate style={{ maxWidth: 280 }}>
              {item.title}
            </Text>
          </Link>,
          <Text key="h" size="small" tone="tertiary">
            {item.heat}
          </Text>,
          <RankBadge key="c" change={item.change} theme={theme} />,
        ])}
        striped
        framed
      />
      <Text size="small" tone="tertiary">
        来源：{source}热搜 · 更新于 {updatedAt}
      </Text>
    </Stack>
  );
}

function GitHubPanel({ items, updatedAt, theme }: { items: GitHubItem[]; updatedAt: string; theme: ReturnType<typeof useHostTheme> }) {
  return (
    <Stack gap={10}>
      <Row align="center" justify="space-between">
        <H3 style={{ margin: 0 }}>GitHub Trending</H3>
        <Pill size="sm" active>
          Daily
        </Pill>
      </Row>
      <Table
        headers={["#", "仓库", "Star", "今日", "7日", "变化"]}
        columnAlign={["right", "left", "right", "right", "right", "right"]}
        rows={items.map((item) => [
          <Text key="r" weight="semibold" tone="secondary" size="small">
            {item.rank}
          </Text>,
          <Stack key="repo" gap={2}>
            <Link href={item.url}>
              <Text weight="medium" truncate style={{ maxWidth: 240 }}>
                {item.repo}
              </Text>
            </Link>
            <Text size="small" tone="quaternary">
              {item.language}
            </Text>
          </Stack>,
          <Text key="s" size="small">
            {item.stars}
          </Text>,
          <Text key="t" size="small" style={{ color: theme.accent.primary }}>
            +{item.today}
          </Text>,
          <Text key="w" size="small" tone="secondary">
            +{item.week}
          </Text>,
          <RankBadge key="c" change={item.change} theme={theme} />,
        ])}
        striped
        framed
      />
      <Text size="small" tone="tertiary">
        来源：GitHub Trending · 更新于 {updatedAt}
      </Text>
    </Stack>
  );
}

export default function CatchNewsPersonalHome() {
  const theme = useHostTheme();
  const [trackTab, setTrackTab] = useCanvasState<(typeof TRACK_TABS)[number]>("trackTab", "全部");
  const [timeTab, setTimeTab] = useCanvasState<(typeof TIME_TABS)[number]>("timeTab", "实时");
  const [entSource, setEntSource] = useCanvasState<(typeof ENT_SOURCES)[number]>("entSource", "微博");
  const [lastRefresh, setLastRefresh] = useCanvasState("lastRefresh", "刚刚");
  const [searchQuery, setSearchQuery] = useCanvasState("searchQuery", "");

  const entItems = (entSource === "微博" ? WEIBO_HOT : BAIDU_HOT).filter(
    (item) => !searchQuery || item.title.toLowerCase().includes(searchQuery.toLowerCase()),
  );
  const githubItems = GITHUB_TRENDING.filter(
    (item) =>
      !searchQuery ||
      item.repo.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.language.toLowerCase().includes(searchQuery.toLowerCase()),
  );
  const showEntertainment = trackTab === "全部" || trackTab === "娱乐";
  const showGitHub = trackTab === "全部" || trackTab === "技术";
  const showNews = trackTab === "新闻";

  const handleRefresh = () => {
    const now = new Date();
    const label = `${now.getHours().toString().padStart(2, "0")}:${now.getMinutes().toString().padStart(2, "0")}`;
    setLastRefresh(label);
  };

  return (
    <Stack gap={16} style={{ padding: "16px 20px", maxWidth: 1200, margin: "0 auto" }}>
      {/* Header */}
      <Row align="center" gap={16} wrap>
        <Text weight="bold" style={{ fontSize: 18, letterSpacing: "-0.02em" }}>
          CatchNews
        </Text>
        <Divider style={{ width: 1, height: 20, background: theme.stroke.secondary }} />
        <TabBar tabs={TRACK_TABS} active={trackTab} onChange={setTrackTab} />
        <Spacer />
        <TabBar tabs={TIME_TABS} active={timeTab} onChange={setTimeTab} />
        <Button variant="secondary" onClick={handleRefresh}>
          刷新
        </Button>
      </Row>

      <TextInput
        type="search"
        value={searchQuery}
        onChange={setSearchQuery}
        placeholder="搜索热点标题、仓库名…"
        style={{ width: "100%" }}
      />

      <Text size="small" tone="tertiary">
        {timeTab}视图 · 上次刷新 {lastRefresh} · 数据为原型 mock，链接指向各平台官方域名
      </Text>

      {/* Main dual-column */}
      {showNews ? (
        <Card>
          <CardHeader trailing="36氪 · 虎嗅">综合新闻</CardHeader>
          <CardBody>
            <Table
              headers={["标题", "来源", "时间"]}
              rows={[
                [<Link href="https://36kr.com">OpenAI 宣布新一代推理模型</Link>, "36氪", "2h"],
                [<Link href="https://www.huxiu.com">新能源车出海东南亚加速</Link>, "虎嗅", "4h"],
                [<Link href="https://36kr.com">SaaS 行业 Q2 融资报告发布</Link>, "36氪", "6h"],
                [<Link href="https://www.huxiu.com">大模型 Agent 框架对比评测</Link>, "虎嗅", "8h"],
                [<Link href="https://36kr.com">某独角兽宣布 IPO 计划</Link>, "36氪", "10h"],
              ]}
              striped
              framed={false}
            />
          </CardBody>
        </Card>
      ) : (
        <Stack gap={20}>
          {showEntertainment && (
            <EntertainmentPanel
              source={entSource}
              onSourceChange={setEntSource}
              items={entItems}
              updatedAt={entSource === "微博" ? "3 分钟前" : "5 分钟前"}
              theme={theme}
            />
          )}
          {showGitHub && (
            <GitHubPanel items={githubItems} updatedAt="10 分钟前" theme={theme} />
          )}
        </Stack>
      )}

      <Divider />

      {/* Weekly persistent */}
      <Stack gap={10}>
        <H2>本周持续在榜</H2>
        <Table
          headers={["话题", "来源", "本周表现"]}
          columnAlign={["left", "left", "left"]}
          rows={WEEKLY_PERSISTENT.map((item) => [
            <Link key="t" href={item.url}>
              {item.title}
            </Link>,
            <Pill key="s" size="sm">
              {item.source}
            </Pill>,
            <Text key="d" size="small" tone="secondary">
              {item.detail}
            </Text>,
          ])}
          striped
          framed
        />
        <Text size="small" tone="quaternary">
          汇总规则：过去 7 天内至少 2 次进入 Top 20 · 来源：CatchNews 本地快照
        </Text>
      </Stack>
    </Stack>
  );
}
