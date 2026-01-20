import { contextBridge, ipcRenderer, IpcRendererEvent } from "electron";

contextBridge.exposeInMainWorld("api", {
  onAnswer: (cb: (text: string) => void) => {
    ipcRenderer.on(
      "coach-answer",
      (_event: IpcRendererEvent, text: string) => cb(text)
    );
  },
});
