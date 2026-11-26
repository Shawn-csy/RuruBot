import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { ArrowUpRight, Loader2, RefreshCw, X } from "lucide-react";
import {
  api,
  type AnswersBookResponse,
  type AstroResponse,
  type HelpSection,
  type PodcastResponse,
  type RadarResponse,
  type TicketResponse,
} from "./api";
import { CatRoomToggle } from "./components/ui-stage/CatRoomToggleDemo";
import { ClickSpark } from "./components/ui-stage/ClickSpark";
import { VanishInput } from "./components/ui-stage/VanishInput";
import { PixelRuruStage } from "./components/PixelRuruStage";
import { AboutPage } from "./pages/AboutPage";
import { GuidePage } from "./pages/GuidePage";

type RoutePath = "/" | "/guide" | "/about";

const NAV_ITEMS: { path: RoutePath; label: string }[] = [
  { path: "/", label: "試玩" },
  { path: "/guide", label: "文件" },
  { path: "/about", label: "關於" },
];

const ZODIAC_SIGNS = [
  "牡羊座",
  "金牛座",
  "雙子座",
  "巨蟹座",
  "獅子座",
  "處女座",
  "天秤座",
  "天蠍座",
  "射手座",
  "摩羯座",
  "水瓶座",
  "雙魚座",
];

const FALLBACK_SECTIONS: HelpSection[] = [
  {
    title: "淺草寺抽籤",
    commands: ["抽淺草寺", "抽淺草寺 工作運"],
    description: "抽淺草寺觀音籤，在 LINE 加上問題可獲得 AI 解籤",
  },
  {
    title: "解答之書",
    commands: ["解答之書 我會成功嗎"],
    description: "向解答之書提問，翻開一個指引",
  },
  {
    title: "星座運勢",
    commands: ["牡羊座", "-w 牡羊座"],
    description: "日運直接輸入星座名，週運加上 -w",
  },
  {
    title: "本週國師",
    commands: ["本週國師"],
    description: "查看本週唐綺陽星座運勢速報",
  },
  {
    title: "氣象雷達",
    commands: ["雷達", "radar"],
    description: "查看中央氣象署即時降雨雷達回波圖",
  },
  {
    title: "暈船迷因",
    commands: ["暈船仔", "暈船"],
    description: "隨機取得暈船迷因圖",
  },
];

function parseRoute(pathname: string): RoutePath {
  if (pathname === "/guide") return "/guide";
  if (pathname === "/about") return "/about";
  return "/";
}

function stampTone(type: string) {
  if (type.includes("大吉")) {
    return "border-red-700 bg-red-700 text-[#F7F6F2] dark:border-red-400 dark:bg-red-500/20 dark:text-red-300";
  }
  if (type.includes("凶")) {
    return "border-zinc-700 bg-zinc-800 text-zinc-100 dark:border-zinc-500 dark:bg-zinc-800 dark:text-zinc-200";
  }
  return "border-amber-700/70 text-amber-800 dark:border-amber-400/70 dark:text-amber-300";
}

export default function App() {
  const [route, setRoute] = useState<RoutePath>(() =>
    parseRoute(window.location.pathname)
  );
  const [isNight, setIsNight] = useState(false);
  const [serviceOk, setServiceOk] = useState<boolean | null>(null);
  const [helpSections, setHelpSections] =
    useState<HelpSection[]>(FALLBACK_SECTIONS);
  const [copiedCmd, setCopiedCmd] = useState<string | null>(null);
  const [askRemaining, setAskRemaining] = useState<number | null>(null);
  const [activeModal, setActiveModal] = useState<
    "ticket" | "answers" | "astro" | null
  >(null);

  // 1. 淺草寺抽籤
  const [ticketData, setTicketData] = useState<TicketResponse | null>(null);
  const [ticketQuestion, setTicketQuestion] = useState("");
  const [ticketLoading, setTicketLoading] = useState(false);
  const [ticketError, setTicketError] = useState<string | null>(null);

  // 2. 解答之書
  const [answersData, setAnswersData] = useState<AnswersBookResponse | null>(
    null
  );
  const [answersLoading, setAnswersLoading] = useState(false);
  const [answersError, setAnswersError] = useState<string | null>(null);

  // 3. 氣象雷達
  const [radarData, setRadarData] = useState<RadarResponse | null>(null);
  const [radarLoading, setRadarLoading] = useState(false);

  // 4. 星座運勢
  const [selectedSign, setSelectedSign] = useState("金牛座");
  const [astroType, setAstroType] = useState<"daily" | "weekly">("daily");
  const [astroData, setAstroData] = useState<AstroResponse | null>(null);
  const [astroLoading, setAstroLoading] = useState(false);

  // 5. 本週國師
  const [podcastData, setPodcastData] = useState<PodcastResponse | null>(null);
  const [podcastLoading, setPodcastLoading] = useState(false);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isNight);
  }, [isNight]);

  useEffect(() => {
    const titles: Record<RoutePath, string> = {
      "/": "機器露露 RuruBot — 淺草寺抽籤、解答之書、星座運勢 LINE Bot",
      "/guide": "文件與 API — 機器露露 RuruBot",
      "/about": "關於機器露露 — RuruBot",
    };
    document.title = titles[route];
  }, [route]);

  useEffect(() => {
    const onPopState = () => setRoute(parseRoute(window.location.pathname));
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") setActiveModal(null);
    };
    window.addEventListener("popstate", onPopState);
    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener("popstate", onPopState);
      window.removeEventListener("keydown", onKeyDown);
    };
  }, []);

  useEffect(() => {
    api
      .readyz()
      .then((res) => setServiceOk(res.status === "ok"))
      .catch(() => setServiceOk(false));

    api
      .help()
      .then((res) => {
        if (res.sections?.length) setHelpSections(res.sections);
      })
      .catch(() => {});

    loadRadar();
    loadPodcast();
  }, []);

  useEffect(() => {
    loadAstro(selectedSign, astroType);
  }, [selectedSign, astroType]);

  function navigate(path: RoutePath) {
    if (path === route) return;
    window.history.pushState({}, "", path);
    setRoute(path);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function handleDrawTicket(question: string) {
    setTicketLoading(true);
    setTicketError(null);
    setTicketQuestion(question);
    try {
      const { data, remaining } = await api.ticket(question);
      setTicketData(data);
      if (remaining !== null) setAskRemaining(remaining);
    } catch (e) {
      setTicketError(e instanceof Error ? e.message : "抽籤失敗");
    } finally {
      setTicketLoading(false);
    }
  }

  async function handleAskAnswers(question: string) {
    setAnswersLoading(true);
    setAnswersError(null);
    try {
      const { data, remaining } = await api.answersBook(
        question || "今天會順利嗎"
      );
      setAnswersData(data);
      if (remaining !== null) setAskRemaining(remaining);
    } catch (err) {
      setAnswersError(err instanceof Error ? err.message : "查詢失敗");
    } finally {
      setAnswersLoading(false);
    }
  }

  async function loadAstro(sign: string, type: "daily" | "weekly") {
    setAstroLoading(true);
    try {
      const res = await api.astro(sign, type);
      setAstroData(res);
    } catch {
      // keep previous
    } finally {
      setAstroLoading(false);
    }
  }

  async function loadRadar() {
    setRadarLoading(true);
    try {
      const res = await api.radar();
      setRadarData(res);
    } catch {
      // ignore
    } finally {
      setRadarLoading(false);
    }
  }

  async function loadPodcast() {
    setPodcastLoading(true);
    try {
      const res = await api.podcast();
      setPodcastData(res);
    } catch {
      // ignore
    } finally {
      setPodcastLoading(false);
    }
  }

  function handleCopy(cmd: string) {
    navigator.clipboard?.writeText(cmd);
    setCopiedCmd(cmd);
    setTimeout(() => setCopiedCmd(null), 1400);
  }

  return (
    <div className="mx-auto max-w-[1100px] px-6 py-10 sm:px-10 sm:py-14">
      <div className="grid items-start gap-12 lg:grid-cols-[260px_1fr] lg:gap-16">
        {/* Left Sticky Rail */}
        <aside className="space-y-8 lg:sticky lg:top-12">
          <div className="space-y-4">
            <button
              type="button"
              onClick={() => navigate("/")}
              className="flex cursor-pointer items-center gap-3.5 text-left"
            >
              <img
                src="https://profile.line-scdn.net/0hcQKryUrPPH52CyL2VudDKUpOMhMBJTo2DjhzHlMON0ZcPn18QmonGQRYax0Oa3N9QjomEAELYx5a"
                alt="機器露露"
                className="h-14 w-14 rounded-full border-2 border-zinc-900/15 object-cover dark:border-white/20"
              />
              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-2xl font-extrabold tracking-tight">
                    機器露露
                  </h1>
                  <span
                    className={`inline-block h-2 w-2 rounded-full ${
                      serviceOk === false ? "bg-amber-500" : "bg-emerald-500"
                    }`}
                  />
                </div>
                <p className="font-mono text-xs text-zinc-500 dark:text-zinc-400">
                  @330vvigh
                </p>
              </div>
            </button>

            <p className="text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
              住在 LINE 裡的黑貓。抽籤、看運勢、翻解答之書、查降雨雷達。
            </p>
          </div>

          {/* Primary Page Navigation */}
          <nav
            aria-label="主導覽"
            className="flex gap-5 border-y border-zinc-900/12 py-3 lg:flex-col lg:gap-1.5 lg:py-4 dark:border-white/12"
          >
            {NAV_ITEMS.map((item) => {
              const active = route === item.path;
              return (
                <button
                  key={item.path}
                  type="button"
                  onClick={() => navigate(item.path)}
                  className={`cursor-pointer text-left text-sm transition-colors lg:border-l-2 lg:py-1 lg:pl-3 ${
                    active
                      ? "font-bold text-zinc-950 lg:border-zinc-900 dark:text-[#F4F4F0] dark:lg:border-[#F4F4F0]"
                      : "font-medium text-zinc-500 hover:text-zinc-900 lg:border-transparent dark:text-zinc-400 dark:hover:text-white"
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* 16-bit Black Cat Study Room Toggle (mw-cr-02) */}
          <div className="w-full">
            <CatRoomToggle isNight={isNight} onToggle={setIsNight} />
          </div>

          <a
            href="https://line.me/R/ti/p/@330vvigh"
            target="_blank"
            rel="noreferrer"
            className="inline-flex w-full items-center justify-between rounded-full bg-[#06C755] px-5 py-2.5 text-xs font-bold text-white transition-opacity hover:opacity-90"
          >
            <span>加 LINE 好友</span>
            <ArrowUpRight className="h-4 w-4" />
          </a>

          <div className="border-t border-zinc-900/10 pt-4 text-xs text-zinc-500 dark:border-white/10 dark:text-zinc-400">
            <a
              href="mailto:silence0603@gmail.com"
              className="font-mono transition-colors hover:text-zinc-900 dark:hover:text-white"
            >
              silence0603@gmail.com
            </a>
          </div>
        </aside>

        {/* Right Main Content */}
        <main>
          {route === "/guide" ? (
            <GuidePage
              helpSections={helpSections}
              copiedCmd={copiedCmd}
              onCopy={handleCopy}
            />
          ) : route === "/about" ? (
            <AboutPage />
          ) : (
            <div className="divide-y divide-zinc-900/12 dark:divide-white/12">
              {/* Editorial Masthead + Interactive 16-bit Pixel Stage */}
              <header className="border-b-2 border-zinc-900 pb-10 dark:border-[#F4F4F0]">
                <div className="flex flex-wrap items-end justify-between gap-4">
                  <div>
                    <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl">
                      有事問黑貓
                    </h2>
                    <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
                      點點畫面裡的抽籤筒、解答之書、水晶球，或是直接摸摸露露。
                    </p>
                  </div>
                  <span className="font-mono text-xs text-zinc-400">
                    NO. 01 · RURUBOT
                  </span>
                </div>

                <div className="mt-6">
                  <PixelRuruStage
                    isNight={isNight}
                    ticketLoading={ticketLoading}
                    answersLoading={answersLoading}
                    onDrawTicket={() => {
                      setActiveModal("ticket");
                      handleDrawTicket("");
                    }}
                    onAskAnswers={() => {
                      setActiveModal("answers");
                      handleAskAnswers("");
                    }}
                    onOpenAstro={() => {
                      setActiveModal("astro");
                    }}
                  />
                </div>
              </header>

              {/* 01 淺草寺觀音籤 */}
              <ClickSpark>
                <section id="sec-ticket" className="scroll-mt-10 py-12">
                  <div className="mb-5 flex flex-wrap items-baseline justify-between gap-2">
                    <div className="flex items-baseline gap-3">
                      <span className="font-mono text-xs font-semibold text-zinc-400">
                        01
                      </span>
                      <h3 className="text-xl font-bold tracking-tight">
                        淺草寺觀音籤
                      </h3>
                    </div>

                    <div className="flex items-center gap-3">
                      {askRemaining !== null && askRemaining <= 5 && (
                        <span className="font-mono text-[11px] text-zinc-500">
                          本分鐘剩餘 {askRemaining} 次
                        </span>
                      )}
                      {ticketData && (
                        <span
                          className={`rounded border px-2.5 py-0.5 text-xs font-bold tracking-wider ${stampTone(
                            ticketData.ticket_type
                          )}`}
                        >
                          {ticketData.ticket_type}
                        </span>
                      )}
                    </div>
                  </div>

                  <VanishInput
                    placeholders={[
                      "心裡想件事，或直接按抽籤...",
                      "這份工作適不適合我？",
                      "最近感情運如何？",
                    ]}
                    onSubmit={handleDrawTicket}
                    loading={ticketLoading}
                    allowEmpty
                    submitLabel="抽一支籤"
                  />

                  {ticketError && (
                    <p className="mt-3 text-xs font-medium text-red-600 dark:text-red-400">
                      {ticketError}
                    </p>
                  )}

                  {ticketData && (
                    <motion.div
                      key={ticketData.title + ticketQuestion}
                      initial={{ opacity: 0, y: 8 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="mt-8 grid gap-6 sm:grid-cols-[1fr_170px]"
                    >
                      <div className="space-y-4">
                        <div className="flex items-baseline gap-3">
                          <span className="text-2xl font-extrabold tracking-tight">
                            {ticketData.title}
                          </span>
                          {ticketQuestion && (
                            <span className="text-xs text-zinc-500">
                              問：{ticketQuestion}
                            </span>
                          )}
                        </div>

                        <p className="border-l-2 border-zinc-900 pl-4 font-serif text-lg leading-relaxed font-medium dark:border-[#F4F4F0]">
                          {ticketData.poem}
                        </p>

                        <p className="text-sm leading-7 text-zinc-600 dark:text-zinc-300">
                          {ticketData.explain}
                        </p>

                        {ticketData.result && (
                          <div className="flex flex-wrap gap-x-4 gap-y-1.5 pt-1 text-xs text-zinc-500 dark:text-zinc-400">
                            {ticketData.result
                              .split("\n")
                              .filter(Boolean)
                              .map((line, i) => (
                                <span key={i}>{line}</span>
                              ))}
                          </div>
                        )}
                      </div>

                      {ticketData.img_url && (
                        <img
                          src={ticketData.img_url}
                          alt={ticketData.title}
                          className="max-h-64 rounded-lg border border-zinc-900/12 object-contain dark:border-white/12"
                        />
                      )}
                    </motion.div>
                  )}
                </section>
              </ClickSpark>

              {/* 02 解答之書 + 氣象雷達 */}
              <section id="sec-answers" className="grid scroll-mt-10 gap-12 py-12 md:grid-cols-2">
                <div className="flex flex-col justify-between">
                  <div>
                    <div className="mb-5 flex items-baseline gap-3">
                      <span className="font-mono text-xs font-semibold text-zinc-400">
                        02
                      </span>
                      <h3 className="text-xl font-bold tracking-tight">
                        解答之書
                      </h3>
                    </div>

                    <VanishInput
                      placeholders={[
                        "默念一個是非題...",
                        "今天適合買這件東西嗎？",
                        "該主動聯絡對方嗎？",
                      ]}
                      onSubmit={handleAskAnswers}
                      loading={answersLoading}
                      allowEmpty
                      submitLabel="翻開"
                    />
                    {answersError && (
                      <p className="mt-3 text-xs font-medium text-red-600 dark:text-red-400">
                        {answersError}
                      </p>
                    )}
                  </div>

                  <div className="mt-8 min-h-[92px] border-l-2 border-zinc-900 pl-4 dark:border-[#F4F4F0]">
                    {answersLoading ? (
                      <Loader2 className="h-4 w-4 animate-spin text-zinc-400" />
                    ) : answersData ? (
                      <motion.div
                        key={answersData.answer + answersData.question}
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                      >
                        {answersData.question && (
                          <p className="text-xs text-zinc-500 dark:text-zinc-400">
                            {answersData.question}
                          </p>
                        )}
                        <p className="mt-1.5 font-serif text-2xl font-bold tracking-wide">
                          {answersData.answer}
                        </p>
                      </motion.div>
                    ) : (
                      <p className="font-serif text-sm text-zinc-400 dark:text-zinc-500">
                        翻開這一頁，看看答案是什麼
                      </p>
                    )}
                  </div>
                </div>

                <div>
                  <div className="mb-5 flex items-center justify-between">
                    <div className="flex items-baseline gap-3">
                      <span className="font-mono text-xs font-semibold text-zinc-400">
                        03
                      </span>
                      <h3 className="text-xl font-bold tracking-tight">
                        氣象雷達
                      </h3>
                    </div>
                    <button
                      type="button"
                      onClick={loadRadar}
                      disabled={radarLoading}
                      className="inline-flex cursor-pointer items-center text-zinc-500 transition-colors hover:text-zinc-900 dark:hover:text-white"
                      title="更新雷達圖"
                    >
                      <RefreshCw
                        className={`h-3.5 w-3.5 ${
                          radarLoading ? "animate-spin" : ""
                        }`}
                      />
                    </button>
                  </div>

                  <div className="overflow-hidden rounded-xl border border-zinc-900/12 bg-zinc-900/[0.03] dark:border-white/12 dark:bg-white/[0.03]">
                    {radarData?.urls?.[0] ? (
                      <img
                        src={radarData.urls[0]}
                        alt="即時氣象雷達圖"
                        className="h-56 w-full object-contain"
                      />
                    ) : (
                      <div className="flex h-56 items-center justify-center">
                        <Loader2 className="h-4 w-4 animate-spin text-zinc-400" />
                      </div>
                    )}
                  </div>
                </div>
              </section>

              {/* 04 星座運勢 */}
              <section id="sec-astro" className="scroll-mt-10 py-12">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <div className="flex items-baseline gap-3">
                    <span className="font-mono text-xs font-semibold text-zinc-400">
                      04
                    </span>
                    <h3 className="text-xl font-bold tracking-tight">
                      {astroData?.title || "星座運勢"}
                    </h3>
                  </div>

                  <div className="flex items-center gap-4 text-xs">
                    {(["daily", "weekly"] as const).map((t) => (
                      <button
                        key={t}
                        type="button"
                        onClick={() => setAstroType(t)}
                        className={`cursor-pointer pb-0.5 font-semibold transition-colors ${
                          astroType === t
                            ? "border-b-2 border-zinc-900 text-zinc-900 dark:border-[#F4F4F0] dark:text-[#F4F4F0]"
                            : "text-zinc-400 hover:text-zinc-700 dark:text-zinc-500 dark:hover:text-zinc-300"
                        }`}
                      >
                        {t === "daily" ? "今日" : "本週"}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="mt-5 flex flex-wrap gap-1.5">
                  {ZODIAC_SIGNS.map((sign) => (
                    <button
                      key={sign}
                      type="button"
                      onClick={() => setSelectedSign(sign)}
                      className={`cursor-pointer rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                        selectedSign === sign
                          ? "bg-zinc-900 text-[#F7F6F2] dark:bg-[#F4F4F0] dark:text-[#111110]"
                          : "text-zinc-600 hover:bg-zinc-900/[0.06] dark:text-zinc-400 dark:hover:bg-white/[0.08]"
                      }`}
                    >
                      {sign}
                    </button>
                  ))}
                </div>

                {astroLoading && !astroData ? (
                  <div className="flex justify-center py-10">
                    <Loader2 className="h-4 w-4 animate-spin text-zinc-400" />
                  </div>
                ) : astroData ? (
                  <div
                    className={`mt-6 grid gap-x-10 gap-y-5 sm:grid-cols-2 ${
                      astroLoading ? "opacity-50" : ""
                    }`}
                  >
                    {astroData.fortunes.map((f) => (
                      <div key={f.label}>
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold">{f.label}</span>
                          <span className="text-xs tracking-wider text-amber-600 dark:text-amber-400">
                            {"★".repeat(Math.max(0, Math.min(5, f.stars)))}
                            <span className="text-zinc-300 dark:text-zinc-700">
                              {"★".repeat(
                                Math.max(0, 5 - Math.min(5, f.stars))
                              )}
                            </span>
                          </span>
                        </div>
                        <p className="mt-1.5 text-xs leading-relaxed text-zinc-600 dark:text-zinc-400">
                          {f.content}
                        </p>
                      </div>
                    ))}
                  </div>
                ) : null}
              </section>

              {/* 05 本週國師 */}
              <section className="pt-12">
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-baseline gap-3">
                    <span className="font-mono text-xs font-semibold text-zinc-400">
                      05
                    </span>
                    <h3 className="text-xl font-bold tracking-tight">
                      {podcastData?.title || "本週國師"}
                    </h3>
                  </div>
                  <button
                    type="button"
                    onClick={loadPodcast}
                    disabled={podcastLoading}
                    className="inline-flex cursor-pointer items-center text-zinc-500 transition-colors hover:text-zinc-900 dark:hover:text-white"
                    title="重整"
                  >
                    <RefreshCw
                      className={`h-3.5 w-3.5 ${
                        podcastLoading ? "animate-spin" : ""
                      }`}
                    />
                  </button>
                </div>

                {podcastData?.groups ? (
                  <div className="mt-6 grid gap-8 md:grid-cols-3">
                    {Object.entries(podcastData.groups).map(
                      ([groupName, items]) => (
                        <div key={groupName}>
                          <div className="mb-3 border-b border-zinc-900/15 pb-1.5 text-xs font-bold dark:border-white/15">
                            {groupName}
                          </div>
                          <ul className="space-y-2">
                            {items.map((item) => (
                              <li
                                key={item.sign}
                                className="text-xs leading-relaxed text-zinc-600 dark:text-zinc-400"
                              >
                                <span className="font-semibold text-zinc-900 dark:text-[#F4F4F0]">
                                  {item.sign}
                                </span>{" "}
                                {item.fortune}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )
                    )}
                  </div>
                ) : (
                  <div className="flex justify-center py-8">
                    <Loader2 className="h-4 w-4 animate-spin text-zinc-400" />
                  </div>
                )}
              </section>
            </div>
          )}
        </main>
      </div>

      {/* Interactive Modal Popup for Pixel Stage Icons */}
      <AnimatePresence>
        {activeModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setActiveModal(null)}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/55 p-4 backdrop-blur-xs"
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.94, y: 12 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.96, y: 8 }}
              transition={{ duration: 0.2 }}
              onClick={(e) => e.stopPropagation()}
              className="relative max-h-[85vh] w-full max-w-2xl overflow-y-auto rounded-2xl border border-zinc-900/15 bg-[#F7F6F2] p-6 shadow-2xl sm:p-8 dark:border-white/15 dark:bg-[#171716]"
            >
              <button
                type="button"
                onClick={() => setActiveModal(null)}
                aria-label="關閉視窗"
                className="absolute right-4 top-4 inline-flex h-8 w-8 cursor-pointer items-center justify-center rounded-full text-zinc-500 transition-colors hover:bg-zinc-900/10 hover:text-zinc-900 dark:hover:bg-white/10 dark:hover:text-white"
              >
                <X className="h-4 w-4" />
              </button>

              {/* Modal 1: 淺草寺抽籤 */}
              {activeModal === "ticket" && (
                <div className="space-y-5">
                  <div className="flex items-center gap-3 pr-8">
                    <img
                      src="/images/sprites/omikuji.png"
                      alt=""
                      className="h-8 w-8 object-contain"
                      style={{ imageRendering: "pixelated" }}
                    />
                    <h3 className="text-xl font-extrabold tracking-tight">
                      淺草寺觀音籤
                    </h3>
                    {ticketData && !ticketLoading && (
                      <span
                        className={`rounded border px-2 py-0.5 text-xs font-bold ${stampTone(
                          ticketData.ticket_type
                        )}`}
                      >
                        {ticketData.ticket_type}
                      </span>
                    )}
                  </div>

                  <VanishInput
                    placeholders={[
                      "想問特定問題再抽一次...",
                      "這份工作適不適合我？",
                      "最近感情運如何？",
                    ]}
                    onSubmit={handleDrawTicket}
                    loading={ticketLoading}
                    allowEmpty
                    submitLabel="再抽一支"
                  />

                  {ticketError && (
                    <p className="text-xs font-medium text-red-600 dark:text-red-400">
                      {ticketError}
                    </p>
                  )}

                  {ticketLoading ? (
                    <div className="flex items-center justify-center gap-2 py-12 text-sm text-zinc-500">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>求籤中...</span>
                    </div>
                  ) : ticketData ? (
                    <div className="grid gap-5 sm:grid-cols-[1fr_150px]">
                      <div className="space-y-3.5">
                        <div className="flex items-baseline gap-2.5">
                          <span className="text-2xl font-extrabold">
                            {ticketData.title}
                          </span>
                          {ticketQuestion && (
                            <span className="text-xs text-zinc-500">
                              問：{ticketQuestion}
                            </span>
                          )}
                        </div>
                        <p className="border-l-2 border-zinc-900 pl-3.5 font-serif text-base leading-relaxed font-medium dark:border-[#F4F4F0]">
                          {ticketData.poem}
                        </p>
                        <p className="text-sm leading-7 text-zinc-600 dark:text-zinc-300">
                          {ticketData.explain}
                        </p>
                        {ticketData.result && (
                          <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-zinc-500 dark:text-zinc-400">
                            {ticketData.result
                              .split("\n")
                              .filter(Boolean)
                              .map((line, i) => (
                                <span key={i}>{line}</span>
                              ))}
                          </div>
                        )}
                      </div>
                      {ticketData.img_url && (
                        <img
                          src={ticketData.img_url}
                          alt={ticketData.title}
                          className="mx-auto max-h-56 rounded-lg border border-zinc-900/12 object-contain dark:border-white/12"
                        />
                      )}
                    </div>
                  ) : null}
                </div>
              )}

              {/* Modal 2: 解答之書 */}
              {activeModal === "answers" && (
                <div className="space-y-6">
                  <div className="flex items-center gap-3 pr-8">
                    <img
                      src="/images/sprites/book.png"
                      alt=""
                      className="h-8 w-8 object-contain"
                      style={{ imageRendering: "pixelated" }}
                    />
                    <h3 className="text-xl font-extrabold tracking-tight">
                      解答之書
                    </h3>
                  </div>

                  <VanishInput
                    placeholders={[
                      "默念一個是非題再翻一次...",
                      "今天適合買這件東西嗎？",
                      "該主動聯絡對方嗎？",
                    ]}
                    onSubmit={handleAskAnswers}
                    loading={answersLoading}
                    allowEmpty
                    submitLabel="再翻一頁"
                  />

                  {answersError && (
                    <p className="text-xs font-medium text-red-600 dark:text-red-400">
                      {answersError}
                    </p>
                  )}

                  <div className="border-l-2 border-zinc-900 py-4 pl-5 dark:border-[#F4F4F0]">
                    {answersLoading ? (
                      <div className="flex items-center gap-2 text-sm text-zinc-500">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        <span>翻頁中...</span>
                      </div>
                    ) : answersData ? (
                      <div>
                        {answersData.question && (
                          <p className="text-xs text-zinc-500 dark:text-zinc-400">
                            {answersData.question}
                          </p>
                        )}
                        <p className="mt-2 font-serif text-3xl font-bold tracking-wide">
                          {answersData.answer}
                        </p>
                      </div>
                    ) : null}
                  </div>
                </div>
              )}

              {/* Modal 3: 星座運勢 */}
              {activeModal === "astro" && (
                <div className="space-y-5">
                  <div className="flex flex-wrap items-center justify-between gap-3 pr-10">
                    <div className="flex items-center gap-3">
                      <img
                        src="/images/sprites/orb.png"
                        alt=""
                        className="h-8 w-8 object-contain"
                        style={{ imageRendering: "pixelated" }}
                      />
                      <h3 className="text-xl font-extrabold tracking-tight">
                        {astroData?.title || "星座運勢"}
                      </h3>
                    </div>
                    <div className="flex items-center gap-4 text-xs">
                      {(["daily", "weekly"] as const).map((t) => (
                        <button
                          key={t}
                          type="button"
                          onClick={() => setAstroType(t)}
                          className={`cursor-pointer pb-0.5 font-semibold transition-colors ${
                            astroType === t
                              ? "border-b-2 border-zinc-900 text-zinc-900 dark:border-[#F4F4F0] dark:text-[#F4F4F0]"
                              : "text-zinc-400 hover:text-zinc-700 dark:text-zinc-500 dark:hover:text-zinc-300"
                          }`}
                        >
                          {t === "daily" ? "今日" : "本週"}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-1.5">
                    {ZODIAC_SIGNS.map((sign) => (
                      <button
                        key={sign}
                        type="button"
                        onClick={() => setSelectedSign(sign)}
                        className={`cursor-pointer rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                          selectedSign === sign
                            ? "bg-zinc-900 text-[#F7F6F2] dark:bg-[#F4F4F0] dark:text-[#111110]"
                            : "text-zinc-600 hover:bg-zinc-900/[0.06] dark:text-zinc-400 dark:hover:bg-white/[0.08]"
                        }`}
                      >
                        {sign}
                      </button>
                    ))}
                  </div>

                  {astroLoading && !astroData ? (
                    <div className="flex justify-center py-10">
                      <Loader2 className="h-4 w-4 animate-spin text-zinc-400" />
                    </div>
                  ) : astroData ? (
                    <div
                      className={`grid gap-x-8 gap-y-4 border-t border-zinc-900/10 pt-5 sm:grid-cols-2 dark:border-white/10 ${
                        astroLoading ? "opacity-50" : ""
                      }`}
                    >
                      {astroData.fortunes.map((f) => (
                        <div key={f.label}>
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-bold">{f.label}</span>
                            <span className="text-xs tracking-wider text-amber-600 dark:text-amber-400">
                              {"★".repeat(Math.max(0, Math.min(5, f.stars)))}
                              <span className="text-zinc-300 dark:text-zinc-700">
                                {"★".repeat(
                                  Math.max(0, 5 - Math.min(5, f.stars))
                                )}
                              </span>
                            </span>
                          </div>
                          <p className="mt-1.5 text-xs leading-relaxed text-zinc-600 dark:text-zinc-400">
                            {f.content}
                          </p>
                        </div>
                      ))}
                    </div>
                  ) : null}
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
