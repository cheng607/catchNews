import {
  Button,
  Card,
  CardBody,
  Divider,
  Grid,
  H2,
  LineChart,
  Link,
  Pill,
  Row,
  Spacer,
  Stack,
  Stat,
  Table,
  Text,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

const REPO = {
  name: "vercel/next.js",
  url: "https://github.com/vercel/next.js",
  language: "JavaScript",
  description: "The React Framework for the Web",
  stars: 134200,
  forks: 28400,
  openIssues: 3120,
  lifecycle: "上升",
};

const STAR_TREND_30D = {
  categories: [
    "5/15", "5/17", "5/19", "5/21", "5/23", "5/25", "5/27",
    "5/29", "5/31", "6/2", "6/4", "6/6", "6/8", "6/10", "6/12", "6/14",
  ],
  series: [{ name: "Star 总数", data: [
    132100, 132280, 132450, 132620, 132780, 132950, 133100,
    133260, 133420, 133580, 133720, 133860, 134020, 134120, 134180, 134200,
  ]}],
};

const COMPARE_REPOS = [
  { repo: "facebook/react", language: "JavaScript", stars: "234k", d1: 892, d7: 4521, url: "https://github.com/facebook/react" },
  { repo: "remix-run/remix", language: "JavaScript", stars: "31.2k", d1: 124, d7: 680, url: "https://github.com/remix-run/remix" },
  { repo: "nuxt/nuxt", language: "TypeScript", stars: "56.8k", d1: 156, d7: 820, url: "https://github.com/nuxt/nuxt" },
  { repo: "sveltejs/kit", language: "JavaScript", stars: "18.4k", d1: 98, d7: 540, url: "https://github.com/sveltejs/kit" },
  { repo: "angular/angular", language: "TypeScript", stars: "96.5k", d1: 210, d7: 1120, url: "https://github.com/angular/angular" },
];

const PERIOD_TABS = ["7d", "30d", "90d"] as const;

function formatStars(n: number) {
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`;
  return String(n);
}

export default function CatchNewsGitHubRepoDetail() {
  const theme = useHostTheme();
  const [period, setPeriod] = useCanvasState<(typeof PERIOD_TABS)[number]>("repoDetailPeriod", "30d");

  const d1 = 387;
  const d7 = 1620;
  const growthRate = ((d7 / REPO.stars) * 100).toFixed(2);

  return (
    <Stack gap={16} style={{ padding: "16px 20px", maxWidth: 960, margin: "0 auto" }}>
      <Row align="center" gap={8} wrap>
        <Text size="small" tone="tertiary">
          CatchNews Pro
        </Text>
        <Text size="small" tone="quaternary">
          /
        </Text>
        <Text size="small" tone="secondary">
          分析
        </Text>
        <Text size="small" tone="quaternary">
          /
        </Text>
        <Text size="small">GitHub</Text>
      </Row>

      <Row align="center" gap={16} wrap>
        <Stack gap={4} style={{ flex: 1, minWidth: 0 }}>
          <Row align="center" gap={12} wrap>
            <H2 style={{ margin: 0 }}>{REPO.name}</H2>
            <Pill size="sm">{REPO.language}</Pill>
            <Pill size="sm" active>
              {REPO.lifecycle}
            </Pill>
          </Row>
          <Link href={REPO.url}>{REPO.url}</Link>
          <Text size="small" tone="secondary">
            {REPO.description}
          </Text>
        </Stack>
        <Row align="center" gap={12} wrap>
          <Text weight="semibold">{formatStars(REPO.stars)} Stars</Text>
          <Text size="small" style={{ color: theme.category.green }}>
            +{formatStars(d7)} (7d)
          </Text>
          <Button variant="primary">监控</Button>
          <Button variant="secondary">导出</Button>
        </Row>
      </Row>

      <Divider />

      <Stack gap={8}>
        <Row align="center" gap={8}>
          <Text weight="semibold">Star 趋势</Text>
          <Row gap={4}>
            {PERIOD_TABS.map((p) => (
              <Pill key={p} size="sm" active={period === p} onClick={() => setPeriod(p)}>
                {p}
              </Pill>
            ))}
          </Row>
        </Row>
        <LineChart
          categories={STAR_TREND_30D.categories}
          series={STAR_TREND_30D.series}
          height={220}
          fill
          beginAtZero={false}
          yMin={131500}
        />
        <Text size="small" tone="quaternary">
          Y 轴：Star 总数 · 来源：GitHub API · 时间范围：{period} · 2026-05-15 ~ 2026-06-14
        </Text>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value={`+${d1}`} label="1d Star 增量" tone="success" />
        <Stat value={`+${d7.toLocaleString()}`} label="7d Star 增量" tone="success" />
        <Stat value={`${growthRate}%`} label="7d 增速" tone="info" />
        <Stat value={REPO.lifecycle} label="生命周期阶段" tone="success" />
      </Grid>

      <Row gap={16} wrap>
        <Stat value={formatStars(REPO.forks)} label="Forks" />
        <Stat value={REPO.openIssues.toLocaleString()} label="Open Issues" />
        <Stat value="Trending #4" label="当前 Trending 排名" tone="info" />
        <Stat value="6/14 10:00" label="最近快照" />
      </Row>

      <Divider />

      <Stack gap={10}>
        <Row align="center" justify="space-between">
          <H2 style={{ margin: 0, fontSize: 16 }}>同语言对比仓库</H2>
          <Text size="small" tone="tertiary">
            JavaScript / TypeScript 框架
          </Text>
        </Row>
        <Table
          headers={["仓库", "语言", "Star", "1d", "7d"]}
          columnAlign={["left", "left", "right", "right", "right"]}
          rows={COMPARE_REPOS.map((r) => [
            <Link key="repo" href={r.url}>
              {r.repo}
            </Link>,
            r.language,
            r.stars,
            <Text key="d1" size="small" style={{ color: theme.category.green }}>
              +{r.d1}
            </Text>,
            <Text key="d7" size="small" style={{ color: theme.category.green }}>
              +{r.d7}
            </Text>,
          ])}
          striped
          framed
        />
        <Text size="small" tone="quaternary">
          对比：react · remix · nuxt · sveltekit · angular · 数据来源 GitHub API
        </Text>
      </Stack>

      <Card variant="borderless">
        <CardBody style={{ padding: 0 }}>
          <Row gap={8}>
            <Button variant="ghost">添加对比仓库</Button>
            <Spacer />
            <Button variant="secondary">查看 API 数据</Button>
          </Row>
        </CardBody>
      </Card>
    </Stack>
  );
}
