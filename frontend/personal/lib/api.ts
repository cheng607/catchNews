export type RankChange = {
  type: 'up' | 'down' | 'new' | 'flat';
  value?: number;
};

export type HotItem = {
  id: string;
  platform: string;
  track: string;
  title: string;
  url: string;
  rank: number | null;
  heat_score: number | null;
  metrics: Record<string, unknown>;
  rank_change?: RankChange | null;
  captured_at: string;
  first_seen_at: string;
  link_status: string;
  source_label: string;
};

export type HotItemsResponse = {
  items: HotItem[];
  meta: {
    updated_at: string;
    platforms: Record<string, { status: string; updated_at?: string | null }>;
  };
};

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1';

export async function fetchHotItems(params: {
  track?: string;
  q?: string;
  top_n?: number;
  time_range?: 'realtime' | 'week' | 'all';
}): Promise<HotItemsResponse> {
  const search = new URLSearchParams();
  if (params.track) search.set('track', params.track);
  if (params.q) search.set('q', params.q);
  if (params.top_n) search.set('top_n', String(params.top_n));
  if (params.time_range) search.set('time_range', params.time_range);

  const res = await fetch(`${API_BASE}/hot-items?${search.toString()}`, {
    next: { revalidate: 60 },
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}

export async function triggerRefresh(): Promise<void> {
  const res = await fetch(`${API_BASE}/refresh`, { method: 'POST' });
  if (!res.ok) {
    throw new Error(`Refresh failed: ${res.status}`);
  }
}
