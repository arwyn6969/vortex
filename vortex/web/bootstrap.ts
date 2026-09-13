import { mount } from "./main.ts";

// The standalone Vite page owns its offline worker. Embedded hosts own theirs.
const unmount = mount(document.querySelector<HTMLDivElement>("#app")!, {
  offline: true,
});
import.meta.hot?.dispose(unmount);
