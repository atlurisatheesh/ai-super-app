import { app, BrowserWindow, globalShortcut, ipcMain } from "electron";
import path from "path";

let mainWindow: BrowserWindow | null = null;
let overlayWindow: BrowserWindow | null = null;

function createMain() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
    },
  });

  mainWindow.loadURL("http://localhost:3000/chat");
}

function createOverlay() {
  if (overlayWindow) return;

  overlayWindow = new BrowserWindow({
    width: 360,
    height: 180,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    focusable: false,
    skipTaskbar: true,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
    },
  });

  overlayWindow.setIgnoreMouseEvents(true);
  overlayWindow.loadFile(path.join(__dirname, "overlay.html"));
}

function destroyOverlay() {
  overlayWindow?.close();
  overlayWindow = null;
}

app.whenReady().then(() => {
  createMain();

  globalShortcut.register("CommandOrControl+Shift+O", () => {
    createOverlay();
  });

  globalShortcut.register("CommandOrControl+Shift+X", () => {
    destroyOverlay();
  });
});

ipcMain.on("coach-start", () => createOverlay());
ipcMain.on("coach-stop", () => destroyOverlay());
ipcMain.on("coach-answer", (_, text) => {
  overlayWindow?.webContents.send("coach-answer", text);
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
