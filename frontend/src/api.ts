export interface HelpSection {
  title: string;
  commands: string[];
  description: string;
}

export interface HelpResponse {
  title: string;
  sections: HelpSection[];
}

export interface TicketResponse {
  title: string;
  ticket_type: string;
  poem: string;
  explain: string;
  result: string;
  img_url?: string;
  ai_reply?: string | null;
  error?: string | null;
}

export interface AnswersBookResponse {
  question: string;
  answer: string;
  error?: string | null;
}

export interface AstroFortune {
  label: string;
  stars: number;
  content: string;
}

export interface AstroResponse {
  sign: string;
  fortune_type: "daily" | "weekly";
  title: string;
  fortunes: AstroFortune[];
  error?: string | null;
}

export interface PodcastGroupItem {
  sign: string;
  fortune: string;
}

export interface PodcastResponse {
  title: string;
  groups: Record<string, PodcastGroupItem[]>;
  error?: string | null;
}

export interface RadarResponse {
  urls: string[];
  error?: string | null;
}

export interface ReadyzResponse {
  status: string;
  checks: Record<string, boolean>;
}

export interface RateLimitedResult<T> {
  data: T;
  remaining: number | null;
}

async function fetchJsonWithMeta<T>(
  url: string,
  init?: RequestInit
): Promise<RateLimitedResult<T>> {
  const res = await fetch(url, init);
  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const err = await res.json();
      if (err?.detail) detail = err.detail;
    } catch {
      // ignore non-json
    }
    throw new Error(detail);
  }
  const remHeader = res.headers.get("X-RateLimit-Remaining");
  const remaining = remHeader !== null ? Number(remHeader) : null;
  const data = (await res.json()) as T;
  return { data, remaining };
}

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const { data } = await fetchJsonWithMeta<T>(url, init);
  return data;
}

export const api = {
  readyz: () => fetchJson<ReadyzResponse>("/readyz"),
  help: () => fetchJson<HelpResponse>("/api/help"),
  ticket: (question: string) =>
    fetchJsonWithMeta<TicketResponse>("/api/ticket", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    }),
  answersBook: (question: string) =>
    fetchJsonWithMeta<AnswersBookResponse>("/api/answers-book", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    }),
  astro: (sign: string, type: "daily" | "weekly") =>
    fetchJson<AstroResponse>(
      `/api/astro?sign=${encodeURIComponent(sign)}&type=${type}`
    ),
  podcast: () => fetchJson<PodcastResponse>("/api/podcast"),
  radar: () => fetchJson<RadarResponse>("/api/radar"),
};
