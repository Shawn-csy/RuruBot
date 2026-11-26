import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { ArrowUp, Loader2 } from "lucide-react";

interface VanishInputProps {
  placeholders: string[];
  onSubmit: (value: string) => void;
  loading?: boolean;
  allowEmpty?: boolean;
  submitLabel?: string;
}

// Adapted from ui.shawnup.com (in-va-01 / react-vanish-input)
export function VanishInput({
  placeholders,
  onSubmit,
  loading = false,
  allowEmpty = true,
  submitLabel = "送出",
}: VanishInputProps) {
  const [placeholderIndex, setPlaceholderIndex] = useState(0);
  const [value, setValue] = useState("");
  const [vanishingText, setVanishingText] = useState<string | null>(null);

  useEffect(() => {
    const id = setInterval(() => {
      setPlaceholderIndex((prev) => (prev + 1) % placeholders.length);
    }, 3200);
    return () => clearInterval(id);
  }, [placeholders.length]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    const trimmed = value.trim();
    if (!trimmed && !allowEmpty) return;

    if (trimmed) {
      setVanishingText(trimmed);
      setTimeout(() => setVanishingText(null), 420);
    }
    setValue("");
    onSubmit(trimmed);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="relative flex w-full items-center border-b border-zinc-900/20 bg-transparent pb-2.5 pt-1 transition-colors focus-within:border-zinc-900 dark:border-white/20 dark:focus-within:border-white"
    >
      <div className="relative flex-1 overflow-hidden">
        <input
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          disabled={loading}
          className="relative z-10 w-full bg-transparent text-sm text-zinc-900 outline-none placeholder:text-transparent dark:text-[#F4F4F0]"
          aria-label={placeholders[placeholderIndex]}
        />

        {!value && !vanishingText && (
          <div className="pointer-events-none absolute inset-0 flex items-center">
            <AnimatePresence mode="wait">
              <motion.span
                key={placeholderIndex}
                initial={{ y: 8, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                exit={{ y: -8, opacity: 0 }}
                transition={{ duration: 0.25 }}
                className="truncate text-sm text-zinc-400 dark:text-zinc-500"
              >
                {placeholders[placeholderIndex]}
              </motion.span>
            </AnimatePresence>
          </div>
        )}

        <AnimatePresence>
          {vanishingText && (
            <motion.span
              initial={{ opacity: 1, filter: "blur(0px)", y: 0 }}
              animate={{ opacity: 0, filter: "blur(6px)", y: -6 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
              className="pointer-events-none absolute inset-0 flex items-center truncate text-sm text-zinc-900 dark:text-[#F4F4F0]"
            >
              {vanishingText}
            </motion.span>
          )}
        </AnimatePresence>
      </div>

      <button
        type="submit"
        disabled={loading || (!allowEmpty && !value.trim())}
        className="ml-3 inline-flex shrink-0 cursor-pointer items-center gap-1.5 rounded-full bg-zinc-900 px-4 py-1.5 text-xs font-medium text-[#F7F6F2] transition-opacity hover:opacity-85 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-[#F4F4F0] dark:text-[#111110]"
      >
        {loading ? (
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
        ) : (
          <ArrowUp className="h-3.5 w-3.5" />
        )}
        <span>{submitLabel}</span>
      </button>
    </form>
  );
}
