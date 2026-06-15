'use client';

import { useCallback, useLayoutEffect, useRef, useState, type ReactNode } from 'react';
import { createPortal } from 'react-dom';

import type { HotItem, RankChange } from '@/lib/api';

function HoverTooltip({
  tooltip,
  className,
  children,
}: {
  tooltip: ReactNode;
  className?: string;
  children: ReactNode;
}) {
  const anchorRef = useRef<HTMLDivElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });

  const updatePosition = useCallback(() => {
    const rect = anchorRef.current?.getBoundingClientRect();
    if (!rect) return;

    const gap = 6;
    const tooltipHeight = tooltipRef.current?.offsetHeight ?? 80;
    const spaceBelow = window.innerHeight - rect.bottom;
    const placeAbove = spaceBelow < tooltipHeight + gap;

    const top = placeAbove ? rect.top - tooltipHeight - gap : rect.bottom + gap;
    const maxLeft = window.innerWidth - 280;
    const left = Math.max(8, Math.min(rect.left, maxLeft));

    setPosition({ top, left });
  }, []);

  const show = useCallback(() => {
    setVisible(true);
    requestAnimationFrame(updatePosition);
  }, [updatePosition]);

  const hide = useCallback(() => setVisible(false), []);

  useLayoutEffect(() => {
    if (visible) {
      updatePosition();
    }
  }, [visible, updatePosition]);

  return (
    <>
      <div ref={anchorRef} className={className} onMouseEnter={show} onMouseLeave={hide}>
        {children}
      </div>
      {visible &&
        typeof document !== 'undefined' &&
        createPortal(
          <div
            ref={tooltipRef}
            role="tooltip"
            className="pointer-events-none fixed z-[100] w-max max-w-xs rounded-md border border-zinc-700 bg-zinc-900 px-2.5 py-1.5 text-xs leading-relaxed text-zinc-200 shadow-lg"
            style={{ top: position.top, left: position.left }}
          >
            {tooltip}
          </div>,
          document.body,
        )}
    </>
  );
}

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

function getDescription(item: HotItem): string | null {
  const raw = item.metrics.description;
  if (typeof raw === 'string' && raw.trim()) {
    return raw.trim();
  }
  return null;
}

function formatStarsTotal(item: HotItem): string {
  if (item.platform === 'github') {
    const stars = item.metrics.stars;
    if (typeof stars === 'number' || typeof stars === 'string') {
      return `⭐ ${stars}`;
    }
  }
  if (item.heat_score != null) {
    return String(item.heat_score);
  }
  return '—';
}

function formatStarsGained(item: HotItem): number | null {
  if (item.platform !== 'github') {
    return null;
  }
  const since = item.metrics.since;
  const key = since === 'weekly' ? 'stars_this_week' : 'stars_today';
  const gained = item.metrics[key];
  if (typeof gained === 'number' && gained > 0) {
    return gained;
  }
  return null;
}

function TitleCell({ title, url, sourceLabel }: { title: string; url: string; sourceLabel: string }) {
  return (
    <HoverTooltip
      className="max-w-[11rem]"
      tooltip={
        <>
          <p>{title}</p>
          <p className="mt-1 text-zinc-500">{sourceLabel}</p>
        </>
      }
    >
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="block truncate font-medium"
      >
        {title}
      </a>
      <div className="mt-0.5 truncate text-xs text-zinc-500">{sourceLabel}</div>
    </HoverTooltip>
  );
}

function DescriptionCell({ text }: { text: string | null }) {
  if (!text) {
    return <span className="text-zinc-600">—</span>;
  }

  return (
    <HoverTooltip className="max-w-[14rem]" tooltip={text}>
      <p className="truncate text-zinc-400">{text}</p>
    </HoverTooltip>
  );
}

export function HotItemTable({
  items,
  emptyLabel,
  gainColumnLabel = '增速',
}: {
  items: HotItem[];
  emptyLabel: string;
  gainColumnLabel?: string;
}) {
  if (items.length === 0) {
    return <p className="py-8 text-center text-sm text-zinc-500">{emptyLabel}</p>;
  }

  return (
    <div className="mb-2 overflow-x-auto rounded-lg border border-zinc-800 pb-12">
      <table className="min-w-full table-fixed text-sm">
        <thead className="bg-zinc-900 text-left text-zinc-400">
          <tr>
            <th className="w-12 px-3 py-2">榜位</th>
            <th className="w-44 px-3 py-2">标题</th>
            <th className="w-56 px-3 py-2">简介</th>
            <th className="w-32 whitespace-nowrap px-3 py-2">总 Star</th>
            <th className="w-24 whitespace-nowrap px-3 py-2 text-right">{gainColumnLabel}</th>
            <th className="w-24 whitespace-nowrap px-3 py-2 text-right">榜位变化</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => {
            const starsGained = formatStarsGained(item);
            return (
              <tr key={item.id} className="border-t border-zinc-800 hover:bg-zinc-900/60">
                <td className="px-3 py-2 text-zinc-400">{item.rank ?? '—'}</td>
                <td className="px-3 py-2">
                  <TitleCell title={item.title} url={item.url} sourceLabel={item.source_label} />
                </td>
                <td className="px-3 py-2">
                  <DescriptionCell text={getDescription(item)} />
                </td>
                <td className="whitespace-nowrap px-3 py-2 text-zinc-300">
                  {formatStarsTotal(item)}
                </td>
                <td className="whitespace-nowrap px-3 py-2 text-right">
                  {starsGained != null ? (
                    <span className="text-emerald-400" title={`GitHub Trending ${gainColumnLabel}新增 Star`}>
                      +{starsGained.toLocaleString()}
                    </span>
                  ) : (
                    <span className="text-zinc-500">—</span>
                  )}
                </td>
                <td className="whitespace-nowrap px-3 py-2 text-right">
                  <RankBadge change={item.rank_change} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
