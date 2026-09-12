// A revision check alone cannot serialize asynchronous work across tabs.
// Browsers without Web Locks may read/export, but must not write concurrently.
export async function withJourneyLock<T>(task: () => Promise<T>): Promise<T> {
  if (!navigator.locks)
    throw new Error(
      "This browser cannot safely coordinate saves. You can export your journey here and continue in a current browser.",
    );
  return navigator.locks.request("vortex-world-v3", task);
}
