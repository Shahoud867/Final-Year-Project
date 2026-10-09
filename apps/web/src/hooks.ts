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
