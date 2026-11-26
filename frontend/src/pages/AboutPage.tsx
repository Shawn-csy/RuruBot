import { ArrowUpRight } from "lucide-react";

export function AboutPage() {
  return (
    <div className="divide-y divide-zinc-900/12 dark:divide-white/12">
      {/* Masthead */}
      <header className="border-b-2 border-zinc-900 pb-8 dark:border-[#F4F4F0]">
        <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
          關於機器露露
        </h2>
        <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
          一隻住在 LINE 裡、偶爾幫人解籤的黑貓。
        </p>
      </header>

      {/* Story */}
      <section className="py-10">
        <div className="mb-4 flex items-baseline gap-3">
          <span className="font-mono text-xs font-semibold text-zinc-400">
            01
          </span>
          <h3 className="text-xl font-bold tracking-tight">這是什麼</h3>
        </div>
        <div className="max-w-2xl space-y-4 text-sm leading-7 text-zinc-700 dark:text-zinc-300">
          <p>
            機器露露（<code className="font-mono">@330vvigh</code>
            ）原本是做給朋友在 LINE 群組裡抽淺草寺靈籤、查每日星座運勢、看本週唐綺陽國師速報與降雨雷達的小機器人。
          </p>
          <p>
            後來把原本綁在 LINE 裡的邏輯抽成獨立的 Use Case 與 REST
            API，順手做了這個網頁版——不用加好友也能直接在瀏覽器裡抽一支籤或翻解答之書；如果想聽露露用
            AI 解籤、或看暈船迷因，再點旁邊加 LINE 好友就行。
          </p>
        </div>
      </section>

      {/* Architecture */}
      <section className="py-10">
        <div className="mb-5 flex items-baseline gap-3">
          <span className="font-mono text-xs font-semibold text-zinc-400">
            02
          </span>
          <h3 className="text-xl font-bold tracking-tight">運作方式</h3>
        </div>

        <dl className="grid gap-6 sm:grid-cols-2">
          <div className="border-l-2 border-zinc-900/20 pl-4 dark:border-white/20">
            <dt className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
              後端與對話
            </dt>
            <dd className="mt-1 text-sm font-medium">
              FastAPI · LINE Messaging API · Gemini 3.1 Flash-Lite
            </dd>
          </div>

          <div className="border-l-2 border-zinc-900/20 pl-4 dark:border-white/20">
            <dt className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
              部署與備援
            </dt>
            <dd className="mt-1 text-sm font-medium">
              MacMini（Docker + Cloudflare Tunnel）主力，斷線自動切換至 GCP Cloud
              Run
            </dd>
          </div>

          <div className="border-l-2 border-zinc-900/20 pl-4 dark:border-white/20">
            <dt className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
              前端與元件
            </dt>
            <dd className="mt-1 text-sm font-medium">
              React · Tailwind CSS ·{" "}
              <a
                href="https://ui.shawnup.com"
                target="_blank"
                rel="noreferrer"
                className="underline underline-offset-4 hover:opacity-75"
              >
                ui.shawnup.com
              </a>
            </dd>
          </div>

          <div className="border-l-2 border-zinc-900/20 pl-4 dark:border-white/20">
            <dt className="text-xs font-semibold text-zinc-500 dark:text-zinc-400">
              原始碼
            </dt>
            <dd className="mt-1 text-sm font-medium">
              <a
                href="https://github.com/Shawn-csy/RuruBot"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-1 underline underline-offset-4 hover:opacity-75"
              >
                <span>Shawn-csy/RuruBot</span>
                <ArrowUpRight className="h-3.5 w-3.5" />
              </a>
            </dd>
          </div>
        </dl>
      </section>

      {/* Contact */}
      <section className="pt-10">
        <div className="mb-4 flex items-baseline gap-3">
          <span className="font-mono text-xs font-semibold text-zinc-400">
            03
          </span>
          <h3 className="text-xl font-bold tracking-tight">聯絡方式</h3>
        </div>
        <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
          功能建議、問題回報或合作交流，歡迎直接寄信到{" "}
          <a
            href="mailto:silence0603@gmail.com"
            className="font-mono font-medium text-zinc-900 underline underline-offset-4 hover:opacity-75 dark:text-[#F4F4F0]"
          >
            silence0603@gmail.com
          </a>
          。
        </p>
      </section>
    </div>
  );
}
