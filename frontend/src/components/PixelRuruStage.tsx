import { useEffect, useRef, useState } from "react";

interface PixelRuruStageProps {
  isNight: boolean;
  ticketLoading: boolean;
  answersLoading: boolean;
  onDrawTicket: () => void;
  onAskAnswers: () => void;
  onOpenAstro: () => void;
}

const DAY_LINES = [
  "喵？點左邊抽籤筒試試！",
  "別戳我肚子啦…",
  "今天感覺會抽到大吉喵",
  "有煩惱就點那本解答之書",
  "呼嚕呼嚕…",
];

const NIGHT_LINES = [
  "唔…再睡五分鐘喵…",
  "zZz…明天再抽啦…",
  "好睏…（縮更緊）",
];

function SpriteFrame({
  src,
  frame,
  totalFrames,
  aspect,
  alt,
}: {
  src: string;
  frame: number;
  totalFrames: number;
  aspect: string;
  alt: string;
}) {
  const posX = totalFrames > 1 ? (frame / (totalFrames - 1)) * 100 : 0;
  return (
    <div
      role="img"
      aria-label={alt}
      className="w-full bg-no-repeat"
      style={{
        aspectRatio: aspect,
        backgroundImage: `url(${src})`,
        backgroundSize: `${totalFrames * 100}% 100%`,
        backgroundPosition: `${posX}% 0%`,
        imageRendering: "pixelated",
      }}
    />
  );
}

// 32-bit-matched curled-up sleeping black cat (same velvety charcoal-blue palette as cat-sheet.png)
function SleepingPixelCat({
  breatheFrame,
  peeking,
}: {
  breatheFrame: 0 | 1;
  peeking: boolean;
}) {
  const yOff = breatheFrame === 1 ? -0.5 : 0;
  return (
    <svg
      viewBox="0 0 36 26"
      shapeRendering="crispEdges"
      className="w-full"
      aria-label="縮成一團睡覺的黑貓露露"
    >
      {/* Grounded pixel shadow */}
      <rect x="4" y="22" width="28" height="3" fill="rgba(0,0,0,0.34)" />
      <rect x="6" y="21" width="24" height="1" fill="rgba(0,0,0,0.2)" />

      {/* Outer silhouette of curled sleeping cat ball */}
      <g transform={`translate(0, ${yOff})`}>
        {/* Ears tucked in on right-top */}
        <rect x="20" y="5" width="3" height="3" fill="#0d0c12" />
        <rect x="21" y="6" width="1" height="2" fill="#262b38" />
        <rect x="25" y="6" width="3" height="3" fill="#0d0c12" />
        <rect x="26" y="7" width="1" height="2" fill="#262b38" />

        {/* Main curled body outline */}
        <rect x="7" y="8" width="21" height="14" fill="#0d0c12" />
        <rect x="5" y="10" width="25" height="10" fill="#0d0c12" />
        <rect x="4" y="12" width="27" height="7" fill="#0d0c12" />

        {/* Deep velvety charcoal-blue fur */}
        <rect x="8" y="9" width="19" height="12" fill="#1b1e28" />
        <rect x="6" y="11" width="23" height="8" fill="#1b1e28" />
        <rect x="5" y="13" width="25" height="5" fill="#1b1e28" />

        {/* Soft top-back dithered highlight */}
        <rect x="9" y="10" width="10" height="2" fill="#2b3142" />
        <rect x="11" y="9" width="6" height="1" fill="#373f54" />
        <rect x="8" y="12" width="3" height="3" fill="#2b3142" />
        <rect x="12" y="12" width="2" height="1" fill="#2b3142" />
        <rect x="16" y="11" width="2" height="1" fill="#2b3142" />

        {/* Curled tail wrapped snugly around front */}
        <rect x="7" y="18" width="13" height="3" fill="#0d0c12" />
        <rect x="8" y="19" width="11" height="1" fill="#2b3142" />
        <rect x="19" y="17" width="3" height="3" fill="#0d0c12" />
        <rect x="19" y="18" width="2" height="1" fill="#373f54" />

        {/* Face tucked near paws */}
        <rect x="20" y="11" width="8" height="7" fill="#1b1e28" />
        <rect x="21" y="10" width="6" height="2" fill="#2b3142" />

        {/* Eyes: closed peaceful curve, or peeking yellow-green eye when poked */}
        {peeking ? (
          <>
            <rect x="22" y="13" width="2" height="2" fill="#bef264" />
            <rect x="23" y="13" width="1" height="2" fill="#0d0c12" />
            <rect x="26" y="14" width="2" height="1" fill="#0d0c12" />
          </>
        ) : (
          <>
            <rect x="22" y="14" width="2" height="1" fill="#0d0c12" />
            <rect x="26" y="14" width="2" height="1" fill="#0d0c12" />
          </>
        )}
        {/* Tiny nose */}
        <rect x="25" y="15" width="1" height="1" fill="#d97b8c" />
      </g>

      {/* Floating pixel Zzz (steps discreetly with breatheFrame) */}
      {!peeking && (
        <g fill="#fde68a" opacity={0.9}>
          {breatheFrame === 0 ? (
            <>
              <rect x="29" y="4" width="3" height="1" />
              <rect x="30" y="5" width="1" height="1" />
              <rect x="29" y="6" width="3" height="1" />
            </>
          ) : (
            <>
              <rect x="31" y="1" width="3" height="1" />
              <rect x="32" y="2" width="1" height="1" />
              <rect x="31" y="3" width="3" height="1" />
              <rect x="28" y="5" width="2" height="1" opacity="0.6" />
            </>
          )}
        </g>
      )}
    </svg>
  );
}

export function PixelRuruStage({
  isNight,
  ticketLoading,
  answersLoading,
  onDrawTicket,
  onAskAnswers,
  onOpenAstro,
}: PixelRuruStageProps) {
  // Day cat frames: 0=open, 1=blink, 2=belly-up happy
  const [catFrame, setCatFrame] = useState(0);
  // Subtle pixel-stepped day idle pose offset (in px) so cat feels alive & playful
  const [catHopY, setCatHopY] = useState(0);
  const [catFlipX, setCatFlipX] = useState(false);
  // Night sleeping breathe frame & sleepy peek
  const [sleepBreathe, setSleepBreathe] = useState<0 | 1>(0);
  const [sleepPeek, setSleepPeek] = useState(false);
  const [catLine, setCatLine] = useState<string | null>(null);
  const lineIdxRef = useRef(0);

  const [omikujiFrame, setOmikujiFrame] = useState(0);
  const [bookFrame, setBookFrame] = useState(0);
  const [orbFrame, setOrbFrame] = useState(0);

  const catBusyRef = useRef(false);
  const omikujiBusyRef = useRef(false);
  const bookBusyRef = useRef(false);
  const orbBusyRef = useRef(false);
  const timersRef = useRef<number[]>([]);

  const schedule = (fn: () => void, ms: number) => {
    const id = window.setTimeout(fn, ms);
    timersRef.current.push(id);
    return id;
  };

  useEffect(() => {
    return () => {
      timersRef.current.forEach((id) => clearTimeout(id));
    };
  }, []);

  // Reset speech bubble when switching Day/Night
  useEffect(() => {
    setCatLine(null);
    setSleepPeek(false);
    setCatHopY(0);
    setCatFrame(0);
    catBusyRef.current = false;
  }, [isNight]);

  // Day mode: lively, cohesive idle routine (blink, playful roll-over, subtle hop)
  useEffect(() => {
    if (isNight) return;
    let step = 0;
    const id = window.setInterval(() => {
      if (catBusyRef.current) return;
      step = (step + 1) % 4;
      if (step === 1) {
        // Gentle blink
        setCatFrame(1);
        schedule(() => {
          if (!catBusyRef.current) setCatFrame(0);
        }, 220);
      } else if (step === 2) {
        // Playful little pixel wiggle + flip direction
        setCatHopY(-3);
        schedule(() => setCatHopY(0), 140);
        schedule(() => setCatFlipX((f) => !f), 140);
      } else if (step === 3) {
        // Quick stretch sequence: 0 -> 1 -> 2 -> 1 -> 0
        setCatFrame(1);
        schedule(() => {
          if (!catBusyRef.current) setCatFrame(2);
        }, 120);
        schedule(() => {
          if (!catBusyRef.current) setCatFrame(1);
        }, 720);
        schedule(() => {
          if (!catBusyRef.current) setCatFrame(0);
        }, 840);
      }
    }, 2800);
    return () => clearInterval(id);
  }, [isNight]);

  // Night mode: slow rhythmic sleeping breath + Zzz toggle
  useEffect(() => {
    if (!isNight) return;
    const id = window.setInterval(() => {
      setSleepBreathe((b) => (b === 0 ? 1 : 0));
    }, 1100);
    return () => clearInterval(id);
  }, [isNight]);

  // Ambient twinkle for the crystal orb
  useEffect(() => {
    const id = window.setInterval(() => {
      if (orbBusyRef.current) return;
      setOrbFrame((f) => (f === 0 ? 1 : 0));
    }, 1800);
    return () => clearInterval(id);
  }, []);

  const handlePetCat = () => {
    if (isNight) {
      setSleepPeek(true);
      const line = NIGHT_LINES[lineIdxRef.current % NIGHT_LINES.length];
      lineIdxRef.current += 1;
      setCatLine(line);
      schedule(() => setSleepPeek(false), 1200);
      schedule(() => setCatLine(null), 2200);
      return;
    }

    catBusyRef.current = true;
    const line = DAY_LINES[lineIdxRef.current % DAY_LINES.length];
    lineIdxRef.current += 1;
    setCatLine(line);
    // Smooth transition frames: 1 (squint) -> 2 (happy belly-up) -> 1 -> 0
    setCatFrame(1);
    schedule(() => setCatFrame(2), 110);
    schedule(() => setCatFrame(1), 1150);
    schedule(() => {
      setCatFrame(0);
      catBusyRef.current = false;
    }, 1280);
    schedule(() => setCatLine(null), 2400);
  };

  const handleClickOmikuji = () => {
    if (omikujiBusyRef.current || ticketLoading) return;
    omikujiBusyRef.current = true;
    const seq = [1, 2, 1, 2, 1, 2, 3];
    seq.forEach((f, idx) => {
      schedule(() => setOmikujiFrame(f), idx * 105);
    });
    schedule(() => {
      onDrawTicket();
    }, seq.length * 105 + 180);
    schedule(() => {
      setOmikujiFrame(0);
      omikujiBusyRef.current = false;
    }, seq.length * 105 + 650);
  };

  const handleClickBook = () => {
    if (bookBusyRef.current || answersLoading) return;
    bookBusyRef.current = true;
    const seq = [1, 2, 3, 2, 3];
    seq.forEach((f, idx) => {
      schedule(() => setBookFrame(f), idx * 125);
    });
    schedule(() => {
      onAskAnswers();
    }, seq.length * 125 + 180);
    schedule(() => setBookFrame(2), seq.length * 125 + 550);
    schedule(() => setBookFrame(1), seq.length * 125 + 670);
    schedule(() => {
      setBookFrame(0);
      bookBusyRef.current = false;
    }, seq.length * 125 + 790);
  };

  const handleClickOrb = () => {
    if (orbBusyRef.current) return;
    orbBusyRef.current = true;
    const seq = [1, 2, 3, 2, 3];
    seq.forEach((f, idx) => {
      schedule(() => setOrbFrame(f), idx * 100);
    });
    schedule(() => {
      onOpenAstro();
    }, seq.length * 100 + 140);
    schedule(() => {
      setOrbFrame(0);
      orbBusyRef.current = false;
    }, seq.length * 100 + 500);
  };

  return (
    <div className="relative overflow-hidden rounded-2xl border border-zinc-900/15 bg-[#1e1b18] select-none dark:border-white/15">
      <div className="relative aspect-[16/9] w-full overflow-hidden">
        <img
          src="/images/ruru-pixel-room.jpg"
          alt="機器露露 16-bit 像素房間"
          className="h-full w-full object-cover"
          style={{ imageRendering: "pixelated" }}
        />

        {/* Day / Night Lighting Overlay */}
        <div
          aria-hidden="true"
          className={`pointer-events-none absolute inset-0 transition-opacity duration-500 ${
            isNight ? "opacity-100" : "opacity-0"
          }`}
          style={{
            background:
              "radial-gradient(circle at 92% 30%, rgba(251,191,36,0.24), rgba(14,17,38,0.5) 55%)",
            mixBlendMode: "multiply",
          }}
        />

        {/* 1. 淺草寺抽籤筒 (Left) */}
        <button
          type="button"
          onClick={handleClickOmikuji}
          className="group absolute bottom-[16%] left-[11%] flex w-[12.5%] min-w-[54px] max-w-[92px] cursor-pointer flex-col items-center focus:outline-none"
          title="點我抽淺草寺靈籤"
        >
          <div className="relative w-full">
            <div className="pointer-events-none absolute -bottom-1 left-1/2 h-2.5 w-[72%] -translate-x-1/2 rounded-full bg-black/35" />
            <SpriteFrame
              src="/images/sprites/omikuji-sheet.png"
              frame={omikujiFrame}
              totalFrames={4}
              aspect="130 / 220"
              alt="淺草寺抽籤筒"
            />
          </div>
          <span className="mt-1.5 rounded bg-zinc-950/80 px-2 py-0.5 font-mono text-[10px] font-medium text-amber-100 opacity-90 group-hover:bg-zinc-950 group-hover:opacity-100">
            {ticketLoading ? "抽籤中..." : "抽淺草寺"}
          </span>
        </button>

        {/* 2. 露露本尊黑貓 (Center on Tatami — Day: active/playful, Night: curled up sleeping) */}
        <button
          type="button"
          onClick={handlePetCat}
          className={`group absolute left-1/2 flex -translate-x-1/2 cursor-pointer flex-col items-center focus:outline-none ${
            isNight
              ? "bottom-[22%] w-[21%] min-w-[92px] max-w-[155px]"
              : "bottom-[18%] w-[18%] min-w-[78px] max-w-[136px]"
          }`}
          title={isNight ? "露露睡著了，點一下吵醒牠" : "點一下摸摸露露"}
        >
          {catLine && (
            <div className="pointer-events-none absolute -top-9 z-20 whitespace-nowrap rounded border-2 border-zinc-900 bg-[#FAF8F2] px-2.5 py-1 text-[11px] font-bold text-zinc-900 shadow-sm">
              {catLine}
            </div>
          )}

          {isNight ? (
            <SleepingPixelCat breatheFrame={sleepBreathe} peeking={sleepPeek} />
          ) : (
            <div
              className="relative w-full"
              style={{
                transform: `translateY(${catHopY}px) scaleX(${catFlipX ? -1 : 1})`,
              }}
            >
              <div className="pointer-events-none absolute -bottom-0.5 left-1/2 h-3 w-[82%] -translate-x-1/2 rounded-full bg-black/30" />
              <SpriteFrame
                src="/images/sprites/cat-sheet.png"
                frame={catFrame}
                totalFrames={3}
                aspect="132 / 240"
                alt="黑貓露露"
              />
            </div>
          )}
        </button>

        {/* 3. 解答之書 (Right) */}
        <button
          type="button"
          onClick={handleClickBook}
          className="group absolute bottom-[16%] right-[11%] flex w-[17%] min-w-[72px] max-w-[126px] cursor-pointer flex-col items-center focus:outline-none"
          title="點我翻開解答之書"
        >
          <div className="relative w-full">
            <div className="pointer-events-none absolute -bottom-1 left-1/2 h-2.5 w-[78%] -translate-x-1/2 rounded-full bg-black/35" />
            <SpriteFrame
              src="/images/sprites/book-sheet.png"
              frame={bookFrame}
              totalFrames={4}
              aspect="220 / 217"
              alt="解答之書"
            />
          </div>
          <span className="mt-1.5 rounded bg-zinc-950/80 px-2 py-0.5 font-mono text-[10px] font-medium text-amber-100 opacity-90 group-hover:bg-zinc-950 group-hover:opacity-100">
            {answersLoading ? "翻頁中..." : "解答之書"}
          </span>
        </button>

        {/* 4. 星象水晶球 (Upper Right) */}
        <button
          type="button"
          onClick={handleClickOrb}
          className="group absolute top-[28%] right-[24%] flex w-[11.5%] min-w-[50px] max-w-[86px] cursor-pointer flex-col items-center focus:outline-none"
          title="點我看星座運勢"
        >
          <div className="relative w-full">
            <div className="pointer-events-none absolute -bottom-0.5 left-1/2 h-2 w-[68%] -translate-x-1/2 rounded-full bg-black/35" />
            <SpriteFrame
              src="/images/sprites/orb-sheet.png"
              frame={orbFrame}
              totalFrames={4}
              aspect="183 / 220"
              alt="星象水晶球"
            />
          </div>
          <span className="mt-1 rounded bg-zinc-950/80 px-1.5 py-0.5 font-mono text-[10px] text-indigo-200 opacity-90 group-hover:bg-zinc-950 group-hover:opacity-100">
            星座運勢
          </span>
        </button>
      </div>
    </div>
  );
}
