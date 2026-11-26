import { useCallback, useEffect, useState } from "react";
import { ApiError } from "./api";

export interface Loadable<T> { data: T | null; error: string; loading: boolean; reload: () => void }

interface State<T> { data: T | null; error: string; loading: boolean }

/**
 * Load data when the component mounts and whenever reload() is called. Pages that depend on an id are
 * mounted with key={id}, so a new id starts fresh. Old data stays visible while a reload is in flight.
 */
export function useLoad<T>(fn: () => Promise<T>, deps: unknown[]): Loadable<T> {
  const [state, setState] = useState<State<T>>({ data: null, error: "", loading: true });
  const [tick, setTick] = useState(0);
  useEffect(() => {
    let live = true;
    fn()
      .then((data) => { if (live) setState({ data, error: "", loading: false }); })
      .catch((e: unknown) => {
        const error = e instanceof ApiError ? e.message : "Something went wrong.";
        if (live) setState((s) => ({ ...s, error, loading: false }));
      });
    return () => { live = false; };
    // fn is a fresh closure every render; the caller's deps say when to load again
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, tick]);
  const reload = useCallback(() => {
    setState((s) => ({ ...s, loading: true }));
    setTick((t) => t + 1);
  }, []);
  return { ...state, reload };
}

/** Hash-based route: "#/runs/run_1" becomes ["runs", "run_1"]. */
export function useRoute(): string[] {
  const read = () => window.location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  const [route, setRoute] = useState(read);
  useEffect(() => {
    const on = () => setRoute(read());
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return route;
}

/** True while the media query matches. False where matchMedia does not exist (tests, old browsers). */
export function useMediaQuery(query: string): boolean {
  const get = () => typeof window !== "undefined" && typeof window.matchMedia === "function" && window.matchMedia(query).matches;
  const [matches, setMatches] = useState(get);
  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const mq = window.matchMedia(query);
    const on = () => setMatches(mq.matches);
    on();
    mq.addEventListener("change", on);
    return () => mq.removeEventListener("change", on);
  }, [query]);
  return matches;
}

export type Theme = "dark" | "light";
const THEME_KEY = "granite.theme";

function storedTheme(): Theme {
  try { return localStorage.getItem(THEME_KEY) === "dark" ? "dark" : "light"; } catch { return "light"; }
}

/** Light by default; the choice is kept in this browser. The dark theme is optional. */
export function useTheme(): [Theme, () => void] {
  const [theme, setTheme] = useState<Theme>(storedTheme);
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try { localStorage.setItem(THEME_KEY, theme); } catch { /* private mode */ }
  }, [theme]);
  const toggle = useCallback(() => setTheme((t) => (t === "dark" ? "light" : "dark")), []);
  return [theme, toggle];
}

/** Copy text to the clipboard; `copied` is true for a moment afterwards. Fails quietly where the API is missing. */
export function useCopy(resetMs = 1500): [boolean, (text: string) => void] {
  const [copied, setCopied] = useState(false);
  useEffect(() => {
    if (!copied) return;
    const t = setTimeout(() => setCopied(false), resetMs);
    return () => clearTimeout(t);
  }, [copied, resetMs]);
  const copy = useCallback((text: string) => {
    const done = () => setCopied(true);
    if (navigator.clipboard?.writeText) void navigator.clipboard.writeText(text).then(done, () => undefined);
  }, []);
  return [copied, copy];
}
