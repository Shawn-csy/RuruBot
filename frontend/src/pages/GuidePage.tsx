import { Check, Copy } from "lucide-react";
import type { HelpSection } from "../api";

interface GuidePageProps {
  helpSections: HelpSection[];
  copiedCmd: string | null;
  onCopy: (text: string) => void;
}

const API_ENDPOINTS = [
  {
    method: "POST",
    path: "/api/ticket",
    desc: "抽淺草寺觀音籤",
    example: `curl -X POST https://rurubot.shawnup.com/api/ticket -H "Content-Type: application/json" -d '{"question":"工作運"}'`,
  },
  {
    method: "POST",
    path: "/api/answers-book",
    desc: "向解答之書提問",
    example: `curl -X POST https://rurubot.shawnup.com/api/answers-book -H "Content-Type: application/json" -d '{"question":"今天適合出門嗎"}'`,
  },
  {
    method: "GET",
    path: "/api/astro?sign=金牛座&type=daily",
    desc: "查詢 12 星座日運（daily）或週運（weekly）",
    example: `curl "https://rurubot.shawnup.com/api/astro?sign=%E9%87%91%E7%89%9B%E5%BA%A7&type=daily"`,
  },
  {
    method: "GET",
    path: "/api/podcast",
    desc: "取得本週唐綺陽星座運勢速報",
    example: `curl https://rurubot.shawnup.com/api/podcast`,
  },
  {
    method: "GET",
    path: "/api/radar",
    desc: "取得中央氣象署即時降雨雷達圖 URL",
    example: `curl https://rurubot.shawnup.com/api/radar`,
  },
  {
    method: "GET",
    path: "/api/help",
    desc: "取得 LINE 指令清單 JSON",
    example: `curl https://rurubot.shawnup.com/api/help`,
  },
];

export function GuidePage({ helpSections, copiedCmd, onCopy }: GuidePageProps) {
  return (
    <div className="divide-y divide-zinc-900/12 dark:divide-white/12">
      {/* Masthead */}
      <header className="border-b-2 border-zinc-900 pb-8 dark:border-[#F4F4F0]">
        <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
          文件
        </h2>
        <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
          LINE 指令速查、公開 REST API 與請求頻率限制。
        </p>
      </header>

      {/* 01 LINE 指令 */}
      <section className="py-10">
        <div className="mb-5 flex items-baseline gap-3">
          <span className="font-mono text-xs font-semibold text-zinc-400">
            01
          </span>
          <h3 className="text-xl font-bold tracking-tight">LINE 指令</h3>
        </div>

        <div className="divide-y divide-zinc-900/10 border-y border-zinc-900/10 dark:divide-white/10 dark:border-white/10">
          {helpSections.map((sec) => (
            <div
              key={sec.title}
              className="grid gap-3 py-4 sm:grid-cols-[150px_1fr_auto] sm:items-center"
            >
              <div className="text-sm font-semibold">
                {sec.title.replace(/^[^\u4e00-\u9fffA-Za-z]+/, "")}
              </div>
              <div className="text-xs leading-relaxed text-zinc-600 dark:text-zinc-400">
                {sec.description || "直接傳送關鍵字即可觸發"}
              </div>
              <div className="flex flex-wrap gap-1.5 sm:justify-end">
                {sec.commands.map((cmd) => (
                  <button
                    key={cmd}
                    type="button"
                    onClick={() => onCopy(cmd)}
                    className="inline-flex cursor-pointer items-center gap-1 rounded bg-zinc-900/[0.06] px-2 py-1 font-mono text-[11px] font-medium transition-colors hover:bg-zinc-900/[0.12] dark:bg-white/[0.08] dark:hover:bg-white/[0.16]"
                  >
                    <span>{cmd}</span>
                    {copiedCmd === cmd ? (
                      <Check className="h-3 w-3 text-emerald-600 dark:text-emerald-400" />
                    ) : (
                      <Copy className="h-3 w-3 opacity-40" />
                    )}
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 02 REST API */}
      <section className="py-10">
        <div className="mb-5 flex items-baseline gap-3">
          <span className="font-mono text-xs font-semibold text-zinc-400">
            02
          </span>
          <h3 className="text-xl font-bold tracking-tight">公開 API</h3>
        </div>

        <div className="space-y-6">
          {API_ENDPOINTS.map((ep) => (
            <div
              key={ep.path}
              className="border-l-2 border-zinc-900/20 pl-4 dark:border-white/20"
            >
              <div className="flex flex-wrap items-center gap-2">
                <span
                  className={`rounded px-1.5 py-0.5 font-mono text-[11px] font-bold ${
                    ep.method === "POST"
                      ? "bg-zinc-900 text-[#F7F6F2] dark:bg-[#F4F4F0] dark:text-[#111110]"
                      : "border border-zinc-900/25 text-zinc-700 dark:border-white/25 dark:text-zinc-200"
                  }`}
                >
                  {ep.method}
                </span>
                <code className="font-mono text-sm font-semibold">
                  {ep.path}
                </code>
              </div>
              <p className="mt-1.5 text-xs text-zinc-600 dark:text-zinc-400">
                {ep.desc}
              </p>
              <div className="mt-2.5 flex items-center justify-between gap-2 rounded-lg bg-zinc-900/[0.04] px-3 py-2 font-mono text-[11px] text-zinc-700 dark:bg-white/[0.04] dark:text-zinc-300">
                <code className="overflow-x-auto whitespace-nowrap">
                  {ep.example}
                </code>
                <button
                  type="button"
                  onClick={() => onCopy(ep.example)}
                  className="shrink-0 cursor-pointer text-zinc-500 hover:text-zinc-900 dark:hover:text-white"
                  title="複製 curl"
                >
                  {copiedCmd === ep.example ? (
                    <Check className="h-3.5 w-3.5 text-emerald-600 dark:text-emerald-400" />
                  ) : (
                    <Copy className="h-3.5 w-3.5" />
                  )}
                </button>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 03 Rate Limit */}
      <section className="pt-10">
        <div className="mb-5 flex items-baseline gap-3">
          <span className="font-mono text-xs font-semibold text-zinc-400">
            03
          </span>
          <h3 className="text-xl font-bold tracking-tight">請求頻率限制</h3>
        </div>

        <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          為防止 API 被惡意刷流量，所有 <code className="font-mono">/api/*</code>{" "}
          端點皆依來源 IP 套用滑動視窗限流，超額時回傳{" "}
          <code className="font-mono font-semibold">HTTP 429</code> 與{" "}
          <code className="font-mono">Retry-After</code> 標頭。
        </p>

        <div className="mt-5 divide-y divide-zinc-900/10 border-y border-zinc-900/10 text-sm dark:divide-white/10 dark:border-white/10">
          <div className="flex flex-wrap items-center justify-between gap-2 py-3">
            <span className="font-mono text-xs font-semibold">
              POST /api/ticket · POST /api/answers-book
            </span>
            <span className="text-xs text-zinc-600 dark:text-zinc-400">
              每分鐘 10 次 · 每小時 30 次
            </span>
          </div>
          <div className="flex flex-wrap items-center justify-between gap-2 py-3">
            <span className="font-mono text-xs font-semibold">GET /api/*</span>
            <span className="text-xs text-zinc-600 dark:text-zinc-400">
              每分鐘 30 次
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
