'use client';

import type { HotItem, RankChange } from '@/lib/api';

function RankBadge({ change }: { change?: RankChange | null }) {
  if (!change || change.type === 'flat') {
    return <span className="text-zinc-500">—</span>;
  }
  if (change.type === 'new') {
    return <span className="font-medium text-sky-400">NEW</span>;
  }
  const up = change.type === 'up';
  return (
    <span className={up ? 'text-emerald-400' : 'text-rose-400'}>
      {up ? '↑' : '↓'}
      {change.value ?? ''}
    </span>
  );
}

function formatMetric(item: HotItem): string {
  if (item.platform === 'github') {
    const stars = item.metrics.stars;
    const today = item.metrics.stars_today;
    if (typeof stars === 'number' || typeof stars === 'string') {
      const todayPart = typeof today === 'number' && today > 0 ? ` +${today}` : '';
      return `⭐ ${stars}${todayPart}`;
    }
  }
  if (item.heat_score != null) {
    return String(item.heat_score);
  }
  return '—';
}

export function HotItemTable({ items, emptyLabel }: { items: HotItem[]; emptyLabel: string }) {
  if (items.length === 0) {
    return <p className="py-8 text-center text-sm text-zinc-500">{emptyLabel}</p>;
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-zinc-800">
      <table className="min-w-full text-sm">
        <thead className="bg-zinc-900 text-left text-zinc-400">
          <tr>
            <th className="w-12 px-3 py-2">#</th>
            <th className="px-3 py-2">标题</th>
            <th className="w-44 whitespace-nowrap px-3 py-2">指标</th>
            <th className="w-24 whitespace-nowrap px-3 py-2 text-right">变化</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id} className="border-t border-zinc-800 hover:bg-zinc-900/60">
              <td className="px-3 py-2 text-zinc-400">{item.rank ?? '—'}</td>
              <td className="px-3 py-2">
                <a href={item.url} target="_blank" rel="noopener noreferrer" className="font-medium">
                  {item.title}
                </a>
                <div className="mt-0.5 text-xs text-zinc-500">{item.source_label}</div>
              </td>
              <td className="whitespace-nowrap px-3 py-2 text-zinc-300">{formatMetric(item)}</td>
              <td className="whitespace-nowrap px-3 py-2 text-right">
                <RankBadge change={item.rank_change} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
