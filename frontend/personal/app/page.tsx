'use client';

import { useCallback, useEffect, useMemo, useState } from 'react';

import { HotItemTable } from '@/components/HotItemTable';
import { fetchHotItems, triggerRefresh, type HotItem } from '@/lib/api';

const TRACK_TABS = ['全部', '娱乐', '技术', '新闻'] as const;
const TRACK_MAP: Record<(typeof TRACK_TABS)[number], string> = {
  全部: 'all',
  娱乐: 'entertainment',
  技术: 'tech',
  新闻: 'news',
};

export default function HomePage() {
  const [trackTab, setTrackTab] = useState<(typeof TRACK_TABS)[number]>('全部');
  const [query, setQuery] = useState('');
  const [items, setItems] = useState<HotItem[]>([]);
  const [updatedAt, setUpdatedAt] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchHotItems({
        track: TRACK_MAP[trackTab],
        q: query || undefined,
        top_n: 20,
      });
      setItems(data.items);
      setUpdatedAt(data.meta.updated_at);
    } catch (err) {
      setError(err instanceof Error ? err.message : '加载失败');
    } finally {
      setLoading(false);
    }
  }, [trackTab, query]);

  useEffect(() => {
    void load();
  }, [load]);

  const entertainmentItems = useMemo(
    () => items.filter((i) => i.track === 'entertainment'),
    [items],
  );
  const techItems = useMemo(() => items.filter((i) => i.track === 'tech'), [items]);

  const onRefresh = async () => {
    setLoading(true);
    try {
      await triggerRefresh();
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : '刷新失败');
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen max-w-5xl flex-col gap-6 px-4 py-6">
      <header className="flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-semibold tracking-tight">CatchNews</h1>
        <div className="flex flex-wrap gap-2">
          {TRACK_TABS.map((tab) => (
            <button
              key={tab}
              type="button"
              onClick={() => setTrackTab(tab)}
              className={`rounded-full px-3 py-1 text-sm ${
                trackTab === tab
                  ? 'bg-zinc-100 text-zinc-900'
                  : 'bg-zinc-800 text-zinc-300 hover:bg-zinc-700'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
        <div className="ml-auto flex gap-2">
          <button
            type="button"
            onClick={() => void onRefresh()}
            className="rounded-md border border-zinc-700 px-3 py-1.5 text-sm hover:bg-zinc-900"
          >
            刷新
          </button>
        </div>
      </header>

      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="搜索热点标题、仓库名…"
        className="w-full rounded-lg border border-zinc-800 bg-zinc-900 px-3 py-2 text-sm outline-none ring-sky-500 focus:ring-1"
      />

      <p className="text-xs text-zinc-500">
        实时视图
        {updatedAt ? ` · 更新于 ${new Date(updatedAt).toLocaleString('zh-CN')}` : ''}
      </p>

      {error && <p className="rounded-lg border border-rose-900 bg-rose-950/40 px-3 py-2 text-sm text-rose-300">{error}</p>}
      {loading && <p className="text-sm text-zinc-500">加载中…</p>}

      {!loading && trackTab !== '新闻' && (trackTab === '全部' || trackTab === '娱乐') && (
        <section className="space-y-3">
          <h2 className="text-base font-medium">娱乐热点</h2>
          <HotItemTable items={entertainmentItems} emptyLabel="暂无娱乐热点数据（M1 接入微博/百度）" />
        </section>
      )}

      {!loading && trackTab !== '新闻' && (trackTab === '全部' || trackTab === '技术') && (
        <section className="space-y-3">
          <h2 className="text-base font-medium">GitHub Trending</h2>
          <HotItemTable items={techItems} emptyLabel="暂无 GitHub 数据，请点击刷新或等待采集" />
        </section>
      )}

      {!loading && trackTab === '新闻' && (
        <section className="space-y-3">
          <h2 className="text-base font-medium">综合新闻</h2>
          <p className="py-8 text-center text-sm text-zinc-500">新闻 RSS 将在后续里程碑接入</p>
        </section>
      )}
    </main>
  );
}
