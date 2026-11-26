import { useState, type ReactNode } from "react";
import { AnimatePresence, motion } from "motion/react";

interface SparkBurst {
  id: number;
  x: number;
  y: number;
}

const ANGLES = [0, 45, 90, 135, 180, 225, 270, 315];

interface ClickSparkProps {
  children: ReactNode;
  className?: string;
  distance?: number;
  duration?: number;
}

// Adapted from ui.shawnup.com (fb-cs-01 / react-click-spark)
export function ClickSpark({
  children,
  className = "",
  distance = 32,
  duration = 0.45,
}: ClickSparkProps) {
  const [bursts, setBursts] = useState<SparkBurst[]>([]);

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const target = e.currentTarget;
    const rect = target.getBoundingClientRect();
    const id = Date.now() + Math.random();
    const x =
      ((e.clientX - rect.left) * target.offsetWidth) / rect.width -
      target.clientLeft;
    const y =
      ((e.clientY - rect.top) * target.offsetHeight) / rect.height -
      target.clientTop;

    setBursts((prev) => [...prev, { id, x, y }]);
    setTimeout(() => {
      setBursts((prev) => prev.filter((b) => b.id !== id));
    }, duration * 1000 + 70);
  };

  return (
    <div onClick={handleClick} className={`relative ${className}`}>
      {children}
      <AnimatePresence>
        {bursts.map((burst) => (
          <div
            key={burst.id}
            style={{ left: burst.x, top: burst.y }}
            className="pointer-events-none absolute z-50"
          >
            {ANGLES.map((deg) => {
              const rad = (deg * Math.PI) / 180;
              return (
                <motion.span
                  key={deg}
                  initial={{ x: 0, y: 0, scale: 1, opacity: 1 }}
                  animate={{
                    x: Math.cos(rad) * distance,
                    y: Math.sin(rad) * distance,
                    scale: 0.2,
                    opacity: 0,
                  }}
                  transition={{ duration, ease: "easeOut" }}
                  style={{ rotate: deg }}
                  className="absolute -left-1.5 -top-0.5 h-1 w-3 rounded-full bg-gradient-to-r from-amber-400 to-indigo-400"
                />
              );
            })}
          </div>
        ))}
      </AnimatePresence>
    </div>
  );
}
