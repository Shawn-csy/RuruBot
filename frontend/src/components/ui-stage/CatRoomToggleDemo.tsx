import { useEffect, useRef, useState } from "react";

interface CatRoomToggleProps {
  isNight?: boolean;
  onToggle?: (nextNight: boolean) => void;
  scale?: number;
}

const W = 224;
const H = 104;
const FLOOR_Y = 97;
const CUSHION_X = 168;
const CUSHION_Y = 82;
const CUSHION_EDGE_X = 145;

// Hue-shifted 16-bit black cat palettes (velvety charcoal-violet + glowing golden-amber eyes)
const CAT_PAL_DAY: Record<string, string> = {
  o: "#12101c",
  d: "#1d1a2b",
  g: "#2a273d",
  L: "#474266",
  w: "#36324d",
  p: "#d97b8c",
  e: "#fbbf24",
  k: "#12101c",
};

const CAT_PAL_NIGHT: Record<string, string> = {
  o: "#0b0914",
  d: "#141224",
  g: "#1e1c33",
  L: "#353157",
  w: "#262340",
  p: "#a85c6f",
  e: "#fde047",
  k: "#0b0914",
};

// 1. Plump sitting cat (22x19)
const CAT_SIT_BASE: string[] = [
  "....oo.....oo.........",
  "...oLpo...opLo........",
  "...oLgLoooLgLo........",
  "..oLLgdLLdgLLo........",
  "..oLggggggggLo........",
  "..oLgegggggeLo........",
  "..oLgwwpwwgLo.........",
  "...oLgwwwgLo..........",
  "....ooowwoo...........",
  "...oLggwwwggo.........",
  "..oLLgwwwwwggo........",
  "..oLggwwwwwgdgo.......",
  "..oLggwwwwwgggo.......",
  "..oLggwwwwwgdggo......",
  "..oLggwwwwwggggo......",
  "..oLgggwwwgggggo......",
  "...oLggwwwggggo.......",
  "...oowwoowwggoo.......",
  "....oooooooooo........",
];

// 2. Smooth 4-frame quadruped walk cycle (facing RIGHT, 24x14)
const CAT_WALK_0: string[] = [
  "..oo....................",
  ".oLgo..........oo..oo...",
  "..oLgo........oLpoopLo..",
  "...oLgo.......oLLggLLo..",
  "....oLgooooo..oLgggggLo.",
  "....oLLgggggooLgggeggLo.",
  "...oLLggggggggLgggggpLo.",
  "...oLggggggggggLggwwwgo.",
  "...oLgggggggggggLggggo..",
  "....oLgggggggggggoooo...",
  "...oLgdgggggggddgo......",
  "..oLgo..oLgo.oLgo.oLgo..",
  ".oLgo...oLgo..oLgo.oLgo.",
  ".ooo....ooo....ooo..ooo.",
];

const CAT_WALK_1: string[] = [
  "...oo...................",
  "..oLgo.........oo..oo...",
  "..oLgo........oLpoopLo..",
  "...oLgo.......oLLggLLo..",
  "....oLgooooo..oLgggggLo.",
  "....oLLgggggooLgggeggLo.",
  "...oLLggggggggLgggggpLo.",
  "...oLggggggggggLggwwwgo.",
  "...oLgggggggggggLggggo..",
  "....oLgggggggggggoooo...",
  "....oLgdggggggddgo......",
  "...oLgo.oLgo..oLgo.oLgo.",
  "...oLgo..oLgo.oLgo..ooo.",
  "...ooo...ooo..ooo.......",
];

const CAT_WALK_2: string[] = [
  "....oo..................",
  "...oLgo........oo..oo...",
  "...oLgo.......oLpoopLo..",
  "...oLgo.......oLLggLLo..",
  "....oLgooooo..oLgggggLo.",
  "....oLLgggggooLgggeggLo.",
  "...oLLggggggggLgggggpLo.",
  "...oLggggggggggLggwwwgo.",
  "...oLgggggggggggLggggo..",
  "....oLgggggggggggoooo...",
  "....oLgdggggggddgo......",
  "....oLgo.oLgo.oLgo......",
  "....oLgo.oLgo..oLgo.....",
  "....ooo..ooo....ooo.....",
];

const CAT_WALK_3: string[] = [
  "...oo...................",
  "..oLgo.........oo..oo...",
  "..oLgo........oLpoopLo..",
  "...oLgo.......oLLggLLo..",
  "....oLgooooo..oLgggggLo.",
  "....oLLgggggooLgggeggLo.",
  "...oLLggggggggLgggggpLo.",
  "...oLggggggggggLggwwwgo.",
  "...oLgggggggggggLggggo..",
  "....oLgggggggggggoooo...",
  "...oLgdgggggggddgo......",
  "...oLgo..oLgo.oLgo......",
  "..oLgo...oLgo..oLgo.....",
  "..ooo....ooo....ooo.....",
];

const WALK_FRAMES = [CAT_WALK_0, CAT_WALK_1, CAT_WALK_2, CAT_WALK_3];

// 3. Classic Cat Yoga Big Stretch (front paws extended low, butt high, curly tail! 24x15)
const CAT_STRETCH: string[] = [
  "..oo....................",
  ".oLgo...................",
  "..oLgo..................",
  "..oLgooo................",
  "..oLLgggoo..............",
  "..oLggggggoo....oo..oo..",
  "..oLggggggggoo.oLpoopLo.",
  "...oLgggggggggoLLggggLo.",
  "...oLggdggggggoLgggeggo.",
  "...oLgo..ooogggLggggpLo.",
  "...oLgo.....ooogggwwwgo.",
  "...oLgo........oogggggoo",
  "..oLgo...........ooooooo",
  "..ooo...................",
];

// 4. Playful Crouch / Wiggle Ready to Pounce (24x12)
const CAT_CROUCH: string[] = [
  "........................",
  "........................",
  ".oo............oo..oo...",
  "oLgo..........oLpoopLo..",
  ".oLgooooooooo.oLLggLLo..",
  "..oLLggggggggoLggggggLo.",
  "..oLggggggggggLgggeggLo.",
  "..oLgggdggggggLgggggpLo.",
  "..oLgggggggggggLggwwwgo.",
  "..oowwoooowwggggggggoo..",
  "...oooooooooooooooooo...",
  "........................",
];

// 5. Playful Paw Batting Yarn Ball (facing RIGHT, extended front paw! 24x14)
const CAT_BAT_PAW: string[] = [
  "..oo....................",
  ".oLgo.........oo..oo....",
  "..oLgo.......oLpoopLo...",
  "...oLgo......oLLggLLo...",
  "....oLgooooo.oLgggggLo..",
  "....oLLgggggoLgggeggLo..",
  "...oLLgggggggLgggggpLo..",
  "...oLgggggggggLggwwwgo..",
  "...oLggggggggggLgggggooo",
  "....oLgggggggggggooLggLo",
  "....oLgdggggdggo...oooo.",
  "...oLgo.oLgo............",
  "..oLgo..oLgo............",
  "..ooo...ooo.............",
];

// 6. Rearing up on hind legs swatting floating sunbeam mote! (20x21)
const CAT_REAR_A: string[] = [
  "......oo...oo.......",
  ".....oLpo.opLo......",
  ".....oLLgggLLo......",
  "....oLgggggggLo.....",
  "....oLgeggggeLo.....",
  "....oLgwwpwwgLo..oo.",
  ".....oLgwwwgLoo.oLgo",
  "..oo..ooowwoooLggLo.",
  ".oLgo.oLggwwwggooo..",
  "..oLgooLLgwwwwggo...",
  "...ooooLggwwwwggo...",
  "......oLggwwwwggo...",
  "......oLggwwwwggo...",
  "......oLggwwwwggo...",
  ".....oLgggwwwgggo...",
  ".....oLggwwwwgggo...",
  "....oLgo.oLgggo.....",
  "...oLgo..oLgo.oLgo..",
  "...ooo...oLgo.oLgo..",
  ".........ooo...ooo..",
];

const CAT_REAR_B: string[] = [
  "......oo...oo.......",
  ".....oLpo.opLo......",
  ".....oLLgggLLo......",
  "....oLgggggggLo.....",
  "....oLgeggggeLo.....",
  "..oooLgwwpwwgLo.....",
  ".oLgooLgwwwgLo......",
  "..oLggooowwoooo..oo.",
  "...ooooLggwwwggooLgo",
  "......oLLgwwwwggooo.",
  "......oLggwwwwggo...",
  "......oLggwwwwggo...",
  "......oLggwwwwggo...",
  "......oLggwwwwggo...",
  ".....oLgggwwwgggo...",
  ".....oLggwwwwgggo...",
  "....oLgo.oLgggo.....",
  "...oLgo..oLgo.oLgo..",
  "...ooo...oLgo.oLgo..",
  ".........ooo...ooo..",
];

// 7. Curled round donut sleeping cat (22x12)
const CAT_SLEEP_A: string[] = [
  "......................",
  "......................",
  "......................",
  "......................",
  "......................",
  ".......ooooooooo......",
  "....oooLLdLLdLLGoo....",
  "..ooLpoLLggggggdggo...",
  ".oLLgoLLgLgggggggggo..",
  ".oLkkwkkLggggddggggo..",
  "..oowpwggggggLLggggo..",
  "...oooooooooooooooo...",
];

const CAT_SLEEP_B: string[] = [
  "......................",
  "......................",
  "......................",
  "......................",
  ".......ooooooooo......",
  "....oooLLdLLdLLGoo....",
  "...oLpoLLggggggdggo...",
  "..oLgoLLgLgggggggggo..",
  ".oLLgggggggggddggggo..",
  ".oLkkwkkLggggLLggggo..",
  "..oowpwggggggggggggo..",
  "...oooooooooooooooo...",
];

type PlayAction =
  | "cushion_groom"
  | "stretch"
  | "chase_yarn"
  | "swat_mote"
  | "sniff_plant";

const ACTION_LABELS: Record<PlayAction, string> = {
  cushion_groom: "在紅絲絨坐墊上理毛搖尾",
  stretch: "在木地板上大伸懶腰～",
  chase_yarn: "撲抓拍打紅毛線球玩耍！",
  swat_mote: "站起來拍打陽光裡的小光塵！",
  sniff_plant: "跑去龜背芋盆栽旁好奇聞葉子",
};

function drawBitmap(
  ctx: CanvasRenderingContext2D,
  rows: string[],
  pal: Record<string, string>,
  x: number,
  y: number,
  flipX = false
) {
  const w = rows[0].length;
  for (let r = 0; r < rows.length; r++) {
    const row = rows[r];
    for (let c = 0; c < w; c++) {
      const ch = row[c];
      if (ch === ".") continue;
      const col = pal[ch] ?? (ch === "G" ? pal.g : undefined);
      if (!col) continue;
      ctx.fillStyle = col;
      const px = flipX ? x + (w - 1 - c) : x + c;
      ctx.fillRect(Math.round(px), Math.round(y + r), 1, 1);
    }
  }
}

function drawParlorCover(
  ctx: CanvasRenderingContext2D,
  img: HTMLImageElement,
  w: number,
  h: number
) {
  const ir = img.width / img.height;
  const cr = w / h;
  let sx = 0;
  let sy = 0;
  let sw = img.width;
  let sh = img.height;
  if (ir > cr) {
    sw = img.height * cr;
    sx = (img.width - sw) / 2;
  } else {
    sh = img.width / cr;
    sy = (img.height - sh) * 0.78;
  }
  ctx.drawImage(img, sx, sy, sw, sh, 0, 0, w, h);
}

// Live rolling red yarn ball with trailing wavy thread
function drawYarnBall(
  ctx: CanvasRenderingContext2D,
  x: number,
  y: number,
  spin: number
) {
  const rx = Math.round(x);
  const ry = Math.round(y);
  // Contact shadow
  ctx.fillStyle = "rgba(20, 8, 16, 0.4)";
  ctx.fillRect(rx - 3, ry, 7, 1);
  // Trailing red yarn thread
  ctx.fillStyle = "#b91c1c";
  ctx.fillRect(rx + 4, ry - 1, 3, 1);
  ctx.fillRect(rx + 7, ry, 3, 1);
  // Ball outline
  ctx.fillStyle = "#450a0a";
  ctx.fillRect(rx - 3, ry - 6, 7, 6);
  ctx.fillRect(rx - 2, ry - 7, 5, 1);
  // Ball body
  ctx.fillStyle = "#dc2626";
  ctx.fillRect(rx - 2, ry - 6, 5, 5);
  // Rotating yarn highlight stripe
  ctx.fillStyle = "#f87171";
  const s = Math.floor(spin) % 3;
  ctx.fillRect(rx - 2 + s, ry - 5, 2, 1);
  ctx.fillRect(rx - 1 + ((s + 1) % 3), ry - 3, 2, 1);
}

export function CatRoomToggle({
  isNight: controlledNight,
  onToggle,
  scale = 1,
}: CatRoomToggleProps = {}) {
  const [internalNight, setInternalNight] = useState(true);
  const isNight = controlledNight ?? internalNight;
  const handleToggle = () => {
    const next = !isNight;
    if (controlledNight === undefined) {
      setInternalNight(next);
    }
    onToggle?.(next);
  };
  const [statusLabel, setStatusLabel] = useState(ACTION_LABELS.cushion_groom);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const stateRef = useRef({
    isNight: isNight,
    nightAlpha: isNight ? 1 : 0,
    catX: CUSHION_X,
    catY: CUSHION_Y,
    onCushion: true,
    hopping: false,
    hopT: 0,
    hopFrom: { x: CUSHION_X, y: CUSHION_Y },
    hopTo: { x: CUSHION_EDGE_X, y: FLOOR_Y },
    action: "cushion_groom" as PlayAction,
    actionStart: 0,
    nextActionAt: 2.6,
    facing: -1 as 1 | -1,
    // Interactive rolling yarn ball physics
    yarnX: 124,
    yarnVx: 0,
    yarnSpin: 0,
    batCooldown: 0,
  });

  useEffect(() => {
    stateRef.current.isNight = isNight;
    if (isNight) {
      stateRef.current.action = "cushion_groom";
      setStatusLabel("小跑回坐墊縮成圓球睡覺 zZz");
    } else {
      stateRef.current.nextActionAt = 0;
      setStatusLabel("伸懶腰醒來準備玩耍！");
    }
  }, [isNight]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const roomImg = new Image();
    roomImg.src = "/pixel-worlds/cat-room.jpg";

    let rafId = 0;
    const start = performance.now();
    const PLAY_SEQUENCE: PlayAction[] = [
      "cushion_groom",
      "stretch",
      "chase_yarn",
      "swat_mote",
      "sniff_plant",
      "chase_yarn",
    ];
    let seqIdx = 0;

    const render = (now: number) => {
      const t = (now - start) / 1000;
      const st = stateRef.current;
      const targetAlpha = st.isNight ? 1 : 0;
      st.nightAlpha += (targetAlpha - st.nightAlpha) * 0.08;

      // Update yarn ball rolling physics on oak floor
      if (Math.abs(st.yarnVx) > 0.04) {
        st.yarnX += st.yarnVx;
        st.yarnSpin += Math.abs(st.yarnVx) * 0.6;
        st.yarnVx *= 0.94;
        if (st.yarnX < 74) {
          st.yarnX = 74;
          st.yarnVx = Math.abs(st.yarnVx) * 0.65;
        }
        if (st.yarnX > 142) {
          st.yarnX = 142;
          st.yarnVx = -Math.abs(st.yarnVx) * 0.65;
        }
      } else {
        st.yarnVx = 0;
      }

      // Advance autonomous daytime playful routine
      if (!st.isNight && t >= st.nextActionAt) {
        seqIdx = (seqIdx + 1) % PLAY_SEQUENCE.length;
        const nextAct = PLAY_SEQUENCE[seqIdx];
        st.action = nextAct;
        st.actionStart = t;
        st.nextActionAt =
          t +
          (nextAct === "chase_yarn"
            ? 5.8
            : nextAct === "swat_mote"
              ? 4.4
              : nextAct === "stretch"
                ? 3.4
                : 4.2);
        setStatusLabel(ACTION_LABELS[nextAct]);
      }

      // Determine target X & whether target is on cushion or floor
      const wantsCushion = st.isNight || st.action === "cushion_groom";
      let targetX = CUSHION_X;
      if (!wantsCushion) {
        if (st.action === "stretch") targetX = 132;
        else if (st.action === "chase_yarn") {
          targetX = st.yarnX + (st.catX < st.yarnX ? -13 : 13);
        } else if (st.action === "swat_mote") targetX = 108;
        else if (st.action === "sniff_plant") targetX = 64;
      }

      // Grounded 2-phase locomotion (short hop at cushion edge + flat oak floor walk)
      let isMoving = false;
      let hopLift = 0;

      if (st.hopping) {
        isMoving = true;
        st.hopT += 0.06;
        if (st.hopT >= 1) {
          st.hopT = 1;
          st.hopping = false;
          st.catX = st.hopTo.x;
          st.catY = st.hopTo.y;
          st.onCushion = st.hopTo.y === CUSHION_Y;
        } else {
          const p = st.hopT;
          st.catX = st.hopFrom.x + (st.hopTo.x - st.hopFrom.x) * p;
          st.catY = st.hopFrom.y + (st.hopTo.y - st.hopFrom.y) * p;
          hopLift = Math.round(Math.sin(p * Math.PI) * 5);
        }
      } else if (!wantsCushion && st.onCushion) {
        st.hopping = true;
        st.hopT = 0;
        st.facing = -1;
        st.hopFrom = { x: st.catX, y: CUSHION_Y };
        st.hopTo = { x: CUSHION_EDGE_X, y: FLOOR_Y };
        isMoving = true;
      } else if (wantsCushion && !st.onCushion) {
        const dxEdge = CUSHION_EDGE_X - st.catX;
        if (Math.abs(dxEdge) > 1.5) {
          isMoving = true;
          const speed = st.isNight ? 1.0 : 0.72;
          st.facing = dxEdge > 0 ? 1 : -1;
          st.catX += Math.sign(dxEdge) * speed;
          st.catY = FLOOR_Y;
        } else {
          st.hopping = true;
          st.hopT = 0;
          st.facing = 1;
          st.hopFrom = { x: CUSHION_EDGE_X, y: FLOOR_Y };
          st.hopTo = { x: CUSHION_X, y: CUSHION_Y };
          isMoving = true;
        }
      } else {
        const dx = targetX - st.catX;
        if (Math.abs(dx) > 1.5) {
          isMoving = true;
          const speed = st.action === "chase_yarn" ? 1.05 : 0.72;
          st.facing = dx > 0 ? 1 : -1;
          st.catX += Math.sign(dx) * speed;
          st.catY = st.onCushion ? CUSHION_Y : FLOOR_Y;
        } else {
          st.catX = targetX;
          st.catY = wantsCushion ? CUSHION_Y : FLOOR_Y;
          if (st.action === "chase_yarn") {
            st.facing = st.yarnX >= st.catX ? 1 : -1;
            // Bat the yarn ball periodically!
            if (t > st.batCooldown) {
              st.batCooldown = t + 1.55;
              const pushDir = st.yarnX > 120 ? -1 : st.yarnX < 92 ? 1 : st.facing;
              st.yarnVx = pushDir * (2.1 + Math.random() * 0.7);
            }
          } else if (st.action === "sniff_plant") {
            st.facing = -1;
          }
        }
      }

      const tick = Math.floor(t * 3);
      ctx.imageSmoothingEnabled = false;
      ctx.clearRect(0, 0, W, H);

      // 1. PARLOR BACKDROP
      if (roomImg.complete && roomImg.naturalWidth > 0) {
        drawParlorCover(ctx, roomImg, W, H);
      } else {
        ctx.fillStyle = "#f0dfc4";
        ctx.fillRect(0, 0, W, H);
      }

      // 2. WINDOW SKY & LIGHTING
      if (st.nightAlpha > 0.02) {
        ctx.save();
        ctx.globalCompositeOperation = "multiply";
        ctx.fillStyle = `rgba(36, 44, 106, ${st.nightAlpha * 0.84})`;
        ctx.fillRect(0, 0, W, H);
        ctx.restore();

        ctx.fillStyle = `rgba(10, 15, 42, ${st.nightAlpha * 0.72})`;
        ctx.fillRect(92, 10, 40, 56);

        ctx.globalAlpha = st.nightAlpha;
        [
          [97, 20],
          [106, 29],
          [123, 36],
          [101, 41],
          [115, 24],
        ].forEach(([sx, sy], i) => {
          ctx.fillStyle = (tick + i) % 3 === 0 ? "#ffffff" : "#94a3b8";
          ctx.fillRect(sx, sy, 1, 1);
        });
        ctx.fillStyle = "#fef08a";
        ctx.fillRect(118, 17, 4, 5);
        ctx.fillRect(117, 18, 6, 3);
        ctx.fillStyle = "#0f173a";
        ctx.fillRect(119, 18, 3, 3);
        ctx.globalAlpha = 1;

        ctx.save();
        ctx.globalCompositeOperation = "screen";
        const pulse = 0.44 + Math.sin(t * 2.4) * 0.06;
        const grad = ctx.createRadialGradient(49, 34, 4, 49, 48, 56);
        grad.addColorStop(0, `rgba(255, 224, 130, ${pulse * st.nightAlpha})`);
        grad.addColorStop(0.55, `rgba(251, 178, 76, ${0.22 * st.nightAlpha})`);
        grad.addColorStop(1, "rgba(251, 178, 76, 0)");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 118, H);
        ctx.restore();
      } else {
        ctx.save();
        ctx.beginPath();
        ctx.rect(92, 12, 40, 24);
        ctx.clip();
        const cx = 86 + ((Math.floor(t * 5) + 10) % 52);
        ctx.fillStyle = "rgba(255,255,255,0.78)";
        ctx.fillRect(cx, 21, 11, 3);
        ctx.fillRect(cx + 2, 19, 7, 2);
        ctx.restore();

        ctx.fillStyle = "rgba(255, 250, 214, 0.85)";
        for (let i = 0; i < 6; i++) {
          const mx = 88 + ((i * 11 + Math.floor(t * 3)) % 48);
          const my = 42 + ((i * 8 + Math.floor(Math.sin(t * 1.4 + i) * 4)) % 40);
          ctx.fillRect(mx, my, 1, 1);
        }
      }

      // 3. LIVE ROLLING RED YARN BALL ON THE OAK FLOOR
      drawYarnBall(ctx, st.yarnX, FLOOR_Y, st.yarnSpin);

      // 4. PLAYFUL BLACK CAT WITH MULTI-ACTION BEHAVIORS
      const sleeping = st.isNight && !isMoving && st.onCushion;
      const pal = st.nightAlpha > 0.5 ? CAT_PAL_NIGHT : CAT_PAL_DAY;
      const drawX = Math.round(st.catX - 11);
      const footY = Math.round(st.catY);

      const shadowW = st.hopping ? 13 : 17;
      ctx.fillStyle = "rgba(20, 8, 16, 0.44)";
      ctx.fillRect(drawX + Math.round((22 - shadowW) / 2), footY - 1, shadowW, 2);

      if (isMoving) {
        const frameIdx = st.hopping ? 0 : Math.floor(t * 9.5) % WALK_FRAMES.length;
        const bob = frameIdx === 1 || frameIdx === 3 ? -1 : 0;
        drawBitmap(
          ctx,
          WALK_FRAMES[frameIdx],
          pal,
          drawX,
          footY - 14 - hopLift + bob,
          st.facing === -1
        );
      } else if (sleeping) {
        const breathe = Math.floor(t * 1.5) % 2;
        drawBitmap(
          ctx,
          breathe === 0 ? CAT_SLEEP_A : CAT_SLEEP_B,
          pal,
          drawX,
          footY - 11
        );
        const zy = footY - 17 - (Math.floor(t * 4) % 9);
        ctx.fillStyle = "#e0e7ff";
        ctx.fillRect(drawX + 2, zy, 4, 1);
        ctx.fillRect(drawX + 4, zy + 1, 1, 1);
        ctx.fillRect(drawX + 3, zy + 2, 1, 1);
        ctx.fillRect(drawX + 2, zy + 3, 4, 1);
      } else if (st.action === "stretch") {
        // Classic front-paws-out big cat stretch!
        drawBitmap(ctx, CAT_STRETCH, pal, drawX, footY - 14, st.facing === -1);
        // Cute sparkle above stretched back
        if (Math.floor(t * 4) % 2 === 0) {
          ctx.fillStyle = "#fde047";
          ctx.fillRect(drawX + 10, footY - 19, 1, 3);
          ctx.fillRect(drawX + 9, footY - 18, 3, 1);
        }
      } else if (st.action === "chase_yarn") {
        // Alternate between playful crouch-wiggle and paw-bat swipe!
        const justBatted = st.batCooldown - t > 1.15;
        if (justBatted) {
          drawBitmap(ctx, CAT_BAT_PAW, pal, drawX, footY - 14, st.facing === -1);
        } else {
          const wiggle = Math.floor(t * 10) % 2;
          drawBitmap(ctx, CAT_CROUCH, pal, drawX + wiggle, footY - 12, st.facing === -1);
        }
      } else if (st.action === "swat_mote") {
        // Rearing up on hind legs swatting a glowing golden sunbeam mote!
        const rearFrame = Math.floor(t * 6) % 2 === 0 ? CAT_REAR_A : CAT_REAR_B;
        drawBitmap(ctx, rearFrame, pal, drawX + 1, footY - 20);
        // Floating golden sunbeam butterfly/mote bobbing right above paws
        const mx = Math.round(st.catX + Math.sin(t * 5) * 6);
        const my = Math.round(footY - 24 + Math.cos(t * 6) * 2);
        ctx.fillStyle = "#fef08a";
        ctx.fillRect(mx, my, 2, 2);
        ctx.fillStyle = "#ffffff";
        ctx.fillRect(mx, my, 1, 1);
      } else if (st.action === "sniff_plant") {
        // Leaning forward sniffing the potted monstera leaf
        const sniffBob = Math.floor(t * 4) % 2;
        drawBitmap(ctx, CAT_CROUCH, pal, drawX - sniffBob, footY - 12, true);
        // Subtle green leaf rustle pixel near monstera
        if (sniffBob === 0) {
          ctx.fillStyle = "#86efac";
          ctx.fillRect(drawX - 5, footY - 14, 1, 1);
          ctx.fillRect(drawX - 8, footY - 16, 1, 1);
        }
      } else {
        // Sitting on velvet cushion (swaying S-tail, blinking, grooming paw)
        const sitY = footY - 18;
        const sway = Math.round(Math.sin(t * 3.4) * 1.6);
        const tailPts = [
          [drawX + 15, sitY + 16],
          [drawX + 17, sitY + 15],
          [drawX + 18, sitY + 13],
          [drawX + 18 + sway, sitY + 11],
          [drawX + 17 + sway, sitY + 9],
          [drawX + 18 + sway, sitY + 7],
        ];
        tailPts.forEach(([tx, ty], i) => {
          ctx.fillStyle = pal.o;
          ctx.fillRect(tx - 1, ty, 3, 2);
          ctx.fillStyle = i % 2 === 0 ? pal.g : pal.L;
          ctx.fillRect(tx, ty, 1, 1);
        });

        drawBitmap(ctx, CAT_SIT_BASE, pal, drawX, sitY);

        const blink = Math.floor(t * 2.4) % 9 === 0;
        if (blink) {
          ctx.fillStyle = pal.g;
          ctx.fillRect(drawX + 5, sitY + 5, 1, 1);
          ctx.fillRect(drawX + 10, sitY + 5, 1, 1);
          ctx.fillStyle = pal.k;
          ctx.fillRect(drawX + 4, sitY + 5, 2, 1);
          ctx.fillRect(drawX + 9, sitY + 5, 2, 1);
        }

        const cycleSec = t % 9;
        if (cycleSec > 5.5 && cycleSec < 7.5) {
          const lift = Math.floor(t * 5) % 2;
          ctx.fillStyle = pal.o;
          ctx.fillRect(drawX + 1, sitY + 7 - lift, 4, 3);
          ctx.fillStyle = pal.L;
          ctx.fillRect(drawX + 2, sitY + 8 - lift, 2, 1);
        }
      }

      rafId = requestAnimationFrame(render);
    };

    rafId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(rafId);
  }, []);

  return (
    <div
      className="flex w-full flex-col items-center gap-2.5"
      style={{ transform: scale === 1 ? undefined : `scale(${scale})` }}
    >
      <button
        type="button"
        role="switch"
        aria-checked={isNight}
        aria-label={isNight ? "切換成白天黑貓書房" : "切換成夜晚黑貓臥室"}
        onClick={handleToggle}
        className="group relative aspect-[312/144] w-full max-w-[260px] cursor-pointer overflow-hidden rounded-full border-2 border-zinc-900/35 bg-zinc-950 transition-transform active:scale-[0.985] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-amber-400 dark:border-white/25"
        style={{
          boxShadow:
            "inset 0 6px 18px rgba(0,0,0,0.55), 0 8px 20px rgba(0,0,0,0.18)",
        }}
      >
        <canvas
          ref={canvasRef}
          width={W}
          height={H}
          className="h-full w-full"
          style={{ imageRendering: "pixelated" }}
        />
        <span
          aria-hidden
          className="pointer-events-none absolute inset-0 rounded-full ring-1 ring-inset ring-white/20"
        />
      </button>
    </div>
  );
}
