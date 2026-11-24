# -*- coding: utf-8 -*-
"""cyber_code — auto-typing programmer terminal (PyQt6)."""

from __future__ import annotations

import json
import os
import random
import re
import sys
from datetime import datetime
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer, QEventLoop
from PyQt6.QtGui import (
    QAction,
    QActionGroup,
    QColor,
    QFont,
    QFontDatabase,
    QIcon,
    QPainter,
    QPixmap,
    QTextCharFormat,
    QTextCursor,
)
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

def _frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def resource_root() -> Path:
    if _frozen():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
    return Path(__file__).resolve().parent


def writable_root() -> Path:
    if _frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def user_settings_path() -> Path:
    base = os.environ.get("APPDATA") or os.environ.get("LOCALAPPDATA")
    if base:
        return Path(base) / "cyber_code" / "settings.json"
    return Path.home() / ".cyber_code" / "settings.json"


FONTS_DIR = resource_root() / "fonts"
SETTINGS_PATH = writable_root() / "settings.json"
USER = "cutec"
HOST = "g16"
MAX_LINES = 420

FONT_FILES = [
    ("JetBrainsMono-Regular.ttf", "JetBrains Mono"),
    ("AdwaitaMono-Regular.ttf", "Adwaita Mono"),
    ("DejaVuSansMono.ttf", "DejaVu Sans Mono"),
    ("UbuntuSansMono-Regular.ttf", "Ubuntu Sans Mono"),
]

SCHEMES = {
    "tokyo-night": {
        "name": "Tokyo Night",
        "bg": "#1a1b26",
        "bar": "#12121a",
        "border": "#2a2b3d",
        "fg": "#c0caf5",
        "dim": "#565f89",
        "green": "#9ece6a",
        "yellow": "#e0af68",
        "red": "#f7768e",
        "blue": "#7aa2f7",
        "cyan": "#7dcfff",
        "magenta": "#bb9af7",
        "black": "#414868",
        "title": "#9aa5ce",
    },
    "catppuccin-mocha": {
        "name": "Catppuccin Mocha",
        "bg": "#1e1e2e",
        "bar": "#181825",
        "border": "#313244",
        "fg": "#cdd6f4",
        "dim": "#6c7086",
        "green": "#a6e3a1",
        "yellow": "#f9e2af",
        "red": "#f38ba8",
        "blue": "#89b4fa",
        "cyan": "#89dceb",
        "magenta": "#cba6f7",
        "black": "#45475a",
        "title": "#bac2de",
    },
    "one-dark": {
        "name": "One Dark",
        "bg": "#282c34",
        "bar": "#21252b",
        "border": "#3e4451",
        "fg": "#abb2bf",
        "dim": "#5c6370",
        "green": "#98c379",
        "yellow": "#e5c07b",
        "red": "#e06c75",
        "blue": "#61afef",
        "cyan": "#56b6c2",
        "magenta": "#c678dd",
        "black": "#3e4451",
        "title": "#9da5b4",
    },
    "dracula": {
        "name": "Dracula",
        "bg": "#282a36",
        "bar": "#21222c",
        "border": "#44475a",
        "fg": "#f8f8f2",
        "dim": "#6272a4",
        "green": "#50fa7b",
        "yellow": "#f1fa8c",
        "red": "#ff5555",
        "blue": "#bd93f9",
        "cyan": "#8be9fd",
        "magenta": "#ff79c6",
        "black": "#44475a",
        "title": "#bd93f9",
    },
    "nord": {
        "name": "Nord",
        "bg": "#2e3440",
        "bar": "#3b4252",
        "border": "#4c566a",
        "fg": "#eceff4",
        "dim": "#7b88a1",
        "green": "#a3be8c",
        "yellow": "#ebcb8b",
        "red": "#bf616a",
        "blue": "#81a1c1",
        "cyan": "#88c0d0",
        "magenta": "#b48ead",
        "black": "#4c566a",
        "title": "#d8dee9",
    },
    "gruvbox-dark": {
        "name": "Gruvbox Dark",
        "bg": "#282828",
        "bar": "#1d2021",
        "border": "#3c3836",
        "fg": "#ebdbb2",
        "dim": "#928374",
        "green": "#b8bb26",
        "yellow": "#fabd2f",
        "red": "#fb4934",
        "blue": "#83a598",
        "cyan": "#8ec07c",
        "magenta": "#d3869b",
        "black": "#3c3836",
        "title": "#d5c4a1",
    },
    "github-dark": {
        "name": "GitHub Dark",
        "bg": "#0d1117",
        "bar": "#010409",
        "border": "#30363d",
        "fg": "#e6edf3",
        "dim": "#7d8590",
        "green": "#3fb950",
        "yellow": "#d29922",
        "red": "#f85149",
        "blue": "#58a6ff",
        "cyan": "#39d5c5",
        "magenta": "#bc8cff",
        "black": "#21262d",
        "title": "#8b949e",
    },
    "classic-green": {
        "name": "经典绿磷",
        "bg": "#0b120c",
        "bar": "#071008",
        "border": "#163018",
        "fg": "#33ff66",
        "dim": "#1f8a3a",
        "green": "#33ff66",
        "yellow": "#b6ff3b",
        "red": "#ff5a5a",
        "blue": "#7cff9a",
        "cyan": "#9affc2",
        "magenta": "#c8ff6a",
        "black": "#0d1a10",
        "title": "#2ad85a",
    },
    "amber": {
        "name": "琥珀",
        "bg": "#120c05",
        "bar": "#0c0804",
        "border": "#3a2a10",
        "fg": "#ffb000",
        "dim": "#8a6500",
        "green": "#ffb000",
        "yellow": "#ffd06a",
        "red": "#ff6a3b",
        "blue": "#e09a2a",
        "cyan": "#ffc14d",
        "magenta": "#ff8a3b",
        "black": "#2a1c08",
        "title": "#e0a020",
    },
}

THEME: dict = dict(SCHEMES["tokyo-night"])
THEME["id"] = "tokyo-night"


def ansi_map() -> dict[int, str]:
    t = THEME
    return {
        30: t["black"], 31: t["red"], 32: t["green"], 33: t["yellow"],
        34: t["blue"], 35: t["magenta"], 36: t["cyan"], 37: t["fg"],
        90: t["dim"], 91: t["red"], 92: t["green"], 93: t["yellow"],
        94: t["blue"], 95: t["magenta"], 96: t["cyan"], 97: t["fg"],
    }


def load_fonts() -> list[dict]:
    found = []
    for filename, label in FONT_FILES:
        path = FONTS_DIR / filename
        if not path.exists():
            continue
        fid = QFontDatabase.addApplicationFont(str(path))
        if fid < 0:
            continue
        families = QFontDatabase.applicationFontFamilies(fid)
        found.append({
            "id": label,
            "label": label,
            "family": families[0] if families else label,
        })
    if not found:
        found.append({"id": "Consolas", "label": "Consolas", "family": "Consolas"})
    return found


def load_settings(fonts: list[dict]) -> dict:
    default_font = fonts[0]["id"]
    for item in fonts:
        if item["id"] == "JetBrains Mono":
            default_font = item["id"]
            break
    data = {"font": default_font, "scheme": "tokyo-night"}
    seen = []
    for path in (SETTINGS_PATH, user_settings_path()):
        if path in seen:
            continue
        seen.append(path)
        try:
            saved = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError):
            continue
        if saved.get("font") in {f["id"] for f in fonts}:
            data["font"] = saved["font"]
        if saved.get("scheme") in SCHEMES:
            data["scheme"] = saved["scheme"]
        break
    return data


def save_settings(settings: dict) -> None:
    payload = json.dumps(settings, ensure_ascii=False, indent=2) + "\n"
    seen = []
    for path in (SETTINGS_PATH, user_settings_path()):
        if path in seen:
            continue
        seen.append(path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload, encoding="utf-8")
            return
        except OSError:
            continue


def set_scheme(scheme_id: str) -> None:
    THEME.clear()
    THEME.update(SCHEMES.get(scheme_id, SCHEMES["tokyo-night"]))
    THEME["id"] = scheme_id


def fmt(color: str | None = None, bold: bool = False, dim: bool = False) -> QTextCharFormat:
    f = QTextCharFormat()
    f.setForeground(QColor(THEME["dim"] if dim else (color or THEME["fg"])))
    f.setFontWeight(QFont.Weight.Bold if bold else QFont.Weight.Normal)
    return f


def parse_ansi(text: str) -> list[tuple[str, QTextCharFormat]]:
    bold = False
    dim = False
    color = None
    out: list[tuple[str, QTextCharFormat]] = []
    colors = ansi_map()
    parts = re.split(r"(\x1b\[[0-9;]*m)", text)
    for part in parts:
        m = re.match(r"^\x1b\[([0-9;]*)m$", part)
        if m:
            codes = [0] if m.group(1) == "" else [int(n) for n in m.group(1).split(";")]
            for code in codes:
                if code == 0:
                    bold = dim = False
                    color = None
                elif code == 1:
                    bold = True
                elif code == 2:
                    dim = True
                elif code == 22:
                    bold = dim = False
                elif code == 39:
                    color = None
                elif code in colors:
                    color = colors[code]
            continue
        if part:
            out.append((part, fmt(color, bold=bold, dim=dim)))
    return out


def make_tray_icon() -> QIcon:
    pix = QPixmap(64, 64)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(THEME["bg"]))
    p.setPen(QColor(THEME["border"]))
    p.drawRoundedRect(2, 2, 60, 60, 14, 14)
    p.setPen(QColor(THEME["green"]))
    font = QFont("Segoe UI")
    font.setPixelSize(28)
    font.setBold(True)
    p.setFont(font)
    p.drawText(pix.rect().adjusted(0, -2, 0, 0), int(Qt.AlignmentFlag.AlignCenter), ">_")
    p.end()
    return QIcon(pix)


def app_icon_file() -> Path:
    return resource_root() / "assets" / "cyber_code.ico"


def load_app_icon() -> QIcon:
    path = app_icon_file()
    if path.is_file():
        icon = QIcon(str(path))
        if not icon.isNull():
            return icon
    return make_tray_icon()


def set_windows_app_id(app_id: str = "cutec.cyber_code") -> None:
    if sys.platform != "win32":
        return
    try:
        import ctypes

        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass


def c_dim(s: str) -> str:
    return f"\x1b[90m{s}\x1b[0m"


def c_green(s: str) -> str:
    return f"\x1b[32m{s}\x1b[0m"


def c_yellow(s: str) -> str:
    return f"\x1b[33m{s}\x1b[0m"


def c_red(s: str) -> str:
    return f"\x1b[31m{s}\x1b[0m"


def c_blue(s: str) -> str:
    return f"\x1b[34m{s}\x1b[0m"


def c_cyan(s: str) -> str:
    return f"\x1b[36m{s}\x1b[0m"


def c_magenta(s: str) -> str:
    return f"\x1b[35m{s}\x1b[0m"


def c_bold(s: str) -> str:
    return f"\x1b[1m{s}\x1b[0m"


def c_dir(s: str) -> str:
    return f"\x1b[1;34m{s}\x1b[0m"


def c_exe(s: str) -> str:
    return f"\x1b[1;32m{s}\x1b[0m"


def nearby_key(ch: str) -> str:
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
    lower = ch.lower()
    for row in rows:
        i = row.find(lower)
        if i >= 0:
            if i == 0:
                j = 1
            elif i == len(row) - 1:
                j = i - 1
            else:
                j = i + (-1 if random.random() < 0.5 else 1)
            repl = row[j]
            return repl.upper() if ch.isupper() else repl
    return ch


def ls_long() -> str:
    return "\n".join(
        [
            "total 144",
            f"drwxr-xr-x  14 {USER} {USER}    4096 Nov 24 09:02 {c_dir('.')}",
            f"drwxr-xr-x   8 {USER} {USER}    4096 Nov 20 09:11 {c_dir('..')}",
            f"drwxr-xr-x   8 {USER} {USER}    4096 Nov 23 17:41 {c_dir('.git')}",
            f"-rw-r--r--   1 {USER} {USER}     312 Nov 12 11:08 .gitignore",
            f"-rw-r--r--   1 {USER} {USER}    4281 Nov 22 16:20 README.md",
            f"drwxr-xr-x   3 {USER} {USER}    4096 Nov 23 18:20 {c_dir('deploy')}",
            f"drwxr-xr-x   3 {USER} {USER}    4096 Nov 23 10:02 {c_dir('dist')}",
            f"-rw-r--r--   1 {USER} {USER}    1840 Nov 23 14:11 {c_yellow('docker-compose.yml')}",
            f"-rw-r--r--   1 {USER} {USER}     986 Nov 21 19:33 Dockerfile",
            f"drwxr-xr-x   4 {USER} {USER}    4096 Nov 23 15:08 {c_dir('java-worker')}",
            f"drwxr-xr-x   2 {USER} {USER}    4096 Nov 24 09:02 {c_dir('k8s')}",
            f"drwxr-xr-x 214 {USER} {USER}    8192 Nov 23 16:02 {c_dir('node_modules')}",
            f"-rw-r--r--   1 {USER} {USER}    1892 Nov 23 13:55 package.json",
            f"-rw-r--r--   1 {USER} {USER}  142011 Nov 23 13:55 package-lock.json",
            f"drwxr-xr-x   8 {USER} {USER}    4096 Nov 23 16:40 {c_dir('src')}",
            f"drwxr-xr-x   3 {USER} {USER}    4096 Nov 23 11:20 {c_dir('tests')}",
        ]
    )


def sessions() -> list[dict]:
    return [
        {
            "name": "explore",
            "steps": [
                {"cmd": "pwd", "output": "/home/cutec/projects/nexus"},
                {"cmd": "ls -la", "output": ls_long},
                {
                    "cmd": "git status",
                    "output": "\n".join(
                        [
                            f"On branch {c_green('main')}",
                            "Your branch is up to date with 'origin/main'.",
                            "",
                            "Changes not staged for commit:",
                            '  (use "git add <file>..." to update what will be committed)',
                            '  (use "git restore <file>..." to discard changes in working directory)',
                            f"\t{c_red('modified:   src/auth/token.ts')}",
                            f"\t{c_red('modified:   tests/auth.spec.ts')}",
                            "",
                            "no changes added to commit",
                        ]
                    ),
                },
                {
                    "cmd": "git log --oneline -8",
                    "output": "\n".join(
                        [
                            f"{c_yellow('e89b67b')} fix token expiry check on auth middleware",
                            f"{c_yellow('44cbbcc')} add region import endpoint and settings reset",
                            f"{c_yellow('844c24f')} tighten docker healthcheck for api",
                            f"{c_yellow('c3a10e2')} bump worker to Java 21 runtime",
                            f"{c_yellow('9f21ab0')} extract batch job queue from settings service",
                            f"{c_yellow('12d88c4')} npm scripts: test:watch and build:prod",
                            f"{c_yellow('a71e0b9')} initial compose stack for api + postgres + redis + worker",
                            f"{c_yellow('04bb2d1')} scaffold nexus monorepo",
                        ]
                    ),
                },
                {
                    "cmd": "cat package.json",
                    "output": "\n".join(
                        [
                            "{",
                            '  "name": "nexus-api",',
                            '  "version": "1.4.2",',
                            '  "private": true,',
                            '  "scripts": {',
                            '    "dev": "tsx watch src/server.ts",',
                            '    "build": "tsc -p tsconfig.json",',
                            '    "test": "vitest run",',
                            '    "start": "node dist/server.js"',
                            "  },",
                            '  "dependencies": {',
                            '    "express": "^4.21.2",',
                            '    "ioredis": "^5.4.2",',
                            '    "pg": "^8.13.1",',
                            '    "zod": "^3.23.8"',
                            "  }",
                            "}",
                        ]
                    ),
                },
            ],
        },
        {
            "name": "npm",
            "steps": [
                {
                    "cmd": "npm test",
                    "think": 720,
                    "ms_per_line": 92,
                    "output": "\n".join(
                        [
                            c_dim(" RUN  v2.1.9  /home/cutec/projects/nexus"),
                            "",
                            f" ✓ tests/health.spec.ts {c_dim('(3)')} {c_green('23ms')}",
                            f" ✓ tests/regions.spec.ts {c_dim('(8)')} {c_green('81ms')}",
                            f" ✓ tests/settings.spec.ts {c_dim('(6)')} {c_green('54ms')}",
                            f" {c_red('×')} tests/auth.spec.ts {c_dim('(7)')} {c_red('41ms')}",
                            "",
                            f"{c_red(c_bold(' FAIL  tests/auth.spec.ts'))}",
                            f"{c_red('  ● Auth › rejects expired tokens')}",
                            f"{c_red('    expected 401, received 500')}",
                            "",
                            c_dim("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"),
                            f" {c_red('Tests  ')} 1 failed {c_dim('|')} 23 passed {c_dim('|')} 24 total",
                            f" {c_dim('Time   ')} 1.12s",
                        ]
                    ),
                },
                {
                    "cmd": "git diff src/auth/token.ts",
                    "think": 1260,
                    "output": "\n".join(
                        [
                            c_dim("diff --git a/src/auth/token.ts b/src/auth/token.ts"),
                            c_dim("index 4c8a21d..b91e0f3 100644"),
                            c_cyan("--- a/src/auth/token.ts"),
                            c_cyan("+++ b/src/auth/token.ts"),
                            f"{c_magenta('@@ -41,8 +41,11 @@')} export function assertFresh(token: Token) {{",
                            "   const now = Date.now();",
                            c_red("-  if (token.exp > now) {"),
                            c_red('-    throw new HttpError(500, "expired");'),
                            c_green("+  if (token.exp <= now) {"),
                            c_green('+    throw new HttpError(401, "expired");'),
                            "   }",
                            "   return token;",
                            " }",
                        ]
                    ),
                },
                {
                    "cmd": "npm test",
                    "think": 630,
                    "ms_per_line": 79,
                    "output": "\n".join(
                        [
                            c_dim(" RUN  v2.1.9  /home/cutec/projects/nexus"),
                            "",
                            f" ✓ tests/health.spec.ts {c_dim('(3)')} {c_green('19ms')}",
                            f" ✓ tests/regions.spec.ts {c_dim('(8)')} {c_green('74ms')}",
                            f" ✓ tests/settings.spec.ts {c_dim('(6)')} {c_green('49ms')}",
                            f" ✓ tests/auth.spec.ts {c_dim('(7)')} {c_green('38ms')}",
                            "",
                            f" {c_green('Tests  ')} 24 passed {c_dim('(24)')}",
                            f" {c_dim('Time   ')} 0.96s",
                        ]
                    ),
                },
                {
                    "cmd": "npm run build",
                    "think": 504,
                    "ms_per_line": 88,
                    "output": "\n".join(
                        [
                            "> nexus-api@1.4.2 build",
                            "> tsc -p tsconfig.json",
                            "",
                            c_green("compiled 42 files successfully"),
                        ]
                    ),
                },
                {
                    "cmd": "npm ls --depth=0",
                    "output": "\n".join(
                        [
                            f"{c_bold('nexus-api@1.4.2')} {c_dim('/home/cutec/projects/nexus')}",
                            "├── express@4.21.2",
                            "├── ioredis@5.4.2",
                            "├── pg@8.13.1",
                            "├── tsx@4.19.2",
                            "├── typescript@5.6.3",
                            "├── vitest@2.1.9",
                            "└── zod@3.23.8",
                        ]
                    ),
                },
            ],
        },
        {
            "name": "docker",
            "steps": [
                {
                    "cmd": "docker ps",
                    "output": "\n".join(
                        [
                            "CONTAINER ID   IMAGE              COMMAND                  CREATED        STATUS                  PORTS                    NAMES",
                            f"a3f81c2e9b10   nexus-api:dev      \"node dist/server.js\"    2 hours ago    {c_green('Up 2 hours')}              0.0.0.0:8080->8080/tcp   nexus-api",
                            f"9c11d0aa4412   postgres:16        \"docker-entrypoint.s…\"   2 days ago     {c_green('Up 2 days (healthy)')}     0.0.0.0:5432->5432/tcp   nexus-db",
                            f"d14b77e0c8a9   nexus-worker:dev   \"java -jar app.jar\"      2 hours ago    {c_green('Up 2 hours')}              0.0.0.0:8081->8081/tcp   nexus-worker",
                            f"f4e90b12aa31   redis:7.4          \"redis-server /usr/…\"    2 days ago     {c_green('Up 2 days (healthy)')}     0.0.0.0:6379->6379/tcp   nexus-redis",
                        ]
                    ),
                },
                {
                    "cmd": "docker logs --tail 16 nexus-api",
                    "think": 432,
                    "ms_per_line": 61,
                    "output": "\n".join(
                        [
                            f"{c_dim('2026-11-23T09:41:02.118Z')} {c_green('INFO')}  listening on :8080",
                            f"{c_dim('2026-11-23T09:41:02.201Z')} {c_green('INFO')}  db pool ready  min=2 max=10",
                            f"{c_dim('2026-11-23T10:12:44.033Z')} {c_cyan('HTTP')}  GET /api/health 200 2ms",
                            f"{c_dim('2026-11-23T11:03:18.540Z')} {c_cyan('HTTP')}  POST /api/v1/regions/import 201 184ms",
                            f"{c_dim('2026-11-23T13:19:07.226Z')} {c_cyan('HTTP')}  GET /api/v1/settings 200 11ms",
                            f"{c_dim('2026-11-23T14:08:51.990Z')} {c_yellow('WARN')}  token exp skew=2s sid=8f2a",
                            f"{c_dim('2026-11-23T14:51:12.447Z')} {c_cyan('HTTP')}  PUT /api/v1/settings 200 37ms",
                            f"{c_dim('2026-11-23T17:22:03.015Z')} {c_cyan('HTTP')}  GET /api/health 200 1ms",
                        ]
                    ),
                },
                {
                    "cmd": "docker build -t nexus-api:dev .",
                    "think": 900,
                    "ms_per_line": 121,
                    "output": "\n".join(
                        [
                            f"[+] Building 18.4s (12/12) {c_green('FINISHED')}",
                            f" {c_dim('=>')} [internal] load build definition from Dockerfile                    0.1s",
                            f" {c_dim('=>')} [internal] load .dockerignore                                       0.0s",
                            f" {c_dim('=>')} [internal] load metadata for docker.io/library/node:22-alpine       1.2s",
                            f" {c_dim('=>')} [deps 1/4] FROM node:22-alpine@sha256:7c1e1c…                       0.0s",
                            f" {c_dim('=>')} [deps 2/4] WORKDIR /app                                             0.0s",
                            f" {c_dim('=>')} [deps 3/4] COPY package.json package-lock.json ./                   0.1s",
                            f" {c_dim('=>')} [deps 4/4] RUN npm ci --omit=dev                                    9.8s",
                            f" {c_dim('=>')} [build 5/6] COPY . .                                                0.3s",
                            f" {c_dim('=>')} [build 6/6] RUN npm run build                                       4.6s",
                            f" {c_dim('=>')} [runtime] COPY --from=build /app/dist ./dist                        0.2s",
                            f" {c_dim('=>')} exporting to image                                                  1.7s",
                            f" {c_dim('=>')} => naming to docker.io/library/nexus-api:dev                         0.0s",
                            "",
                            c_green("Successfully tagged nexus-api:dev"),
                        ]
                    ),
                },
                {
                    "cmd": "docker compose ps",
                    "output": "\n".join(
                        [
                            "NAME           IMAGE              COMMAND                  SERVICE   CREATED        STATUS                  PORTS",
                            f"nexus-api      nexus-api:dev      \"node dist/server.js\"    api       2 hours ago    {c_green('running (healthy)')}     0.0.0.0:8080->8080/tcp",
                            f"nexus-db       postgres:16        \"docker-entrypoint.s…\"   db        2 days ago     {c_green('running (healthy)')}     0.0.0.0:5432->5432/tcp",
                            f"nexus-worker   nexus-worker:dev   \"java -jar app.jar\"      worker    2 hours ago    {c_green('running')}                0.0.0.0:8081->8081/tcp",
                            f"nexus-redis    redis:7.4          \"redis-server /usr/…\"    redis     2 days ago     {c_green('running (healthy)')}     0.0.0.0:6379->6379/tcp",
                        ]
                    ),
                },
                {
                    "cmd": "docker compose logs --tail 12 redis",
                    "think": 480,
                    "ms_per_line": 64,
                    "output": "\n".join(
                        [
                            f"{c_cyan('nexus-redis')}  | 1:C 22 Nov 2026 09:41:08.112 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo",
                            f"{c_cyan('nexus-redis')}  | 1:C 22 Nov 2026 09:41:08.112 * Running mode=standalone, port=6379.",
                            f"{c_cyan('nexus-redis')}  | 1:M 22 Nov 2026 09:41:08.118 * Server initialized",
                            f"{c_cyan('nexus-redis')}  | 1:M 22 Nov 2026 09:41:08.119 * Ready to accept connections tcp",
                            f"{c_cyan('nexus-redis')}  | 1:M 24 Nov 2026 08:12:44.201 * 100 changes in 300 seconds. Saving...",
                            f"{c_cyan('nexus-redis')}  | 1:M 24 Nov 2026 08:12:44.402 * Background saving started by pid 21",
                            f"{c_cyan('nexus-redis')}  | 1:M 24 Nov 2026 08:12:44.618 * Background saving terminated with success",
                        ]
                    ),
                },
            ],
        },
        {
            "name": "java",
            "steps": [
                {
                    "cmd": "java -version",
                    "output": "\n".join(
                        [
                            c_yellow('openjdk version "21.0.12" 2025-07-15 LTS'),
                            "OpenJDK Runtime Environment (build 21.0.12+8-LTS)",
                            "OpenJDK 64-Bit Server VM (build 21.0.12+8-LTS, mixed mode, sharing)",
                        ]
                    ),
                },
                {"cmd": "cd java-worker", "output": "", "cwd": "~/projects/nexus/java-worker"},
                {
                    "cmd": "ls",
                    "output": f"{c_dir('src')}  {c_dir('target')}  pom.xml  {c_yellow('Dockerfile')}",
                },
                {
                    "cmd": "mvn -DskipTests package",
                    "think": 1080,
                    "ms_per_line": 83,
                    "output": "\n".join(
                        [
                            f"[{c_cyan('INFO')}] Scanning for projects...",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('----------------< com.nexus:java-worker >----------------')}",
                            f"[{c_cyan('INFO')}] {c_bold('Building nexus java-worker 1.4.2')}",
                            f"[{c_cyan('INFO')}]   from pom.xml",
                            f"[{c_cyan('INFO')}] {c_bold('--------------------------------[ jar ]---------------------------------')}",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('--- maven-resources-plugin:3.3.1:resources ---')}",
                            f"[{c_cyan('INFO')}] Copying 3 resources from src/main/resources to target/classes",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('--- maven-compiler-plugin:3.13.0:compile (default-compile) ---')}",
                            f"[{c_cyan('INFO')}] Recompiling the module because of {c_yellow('changed source code')}",
                            f"[{c_cyan('INFO')}] Compiling 18 source files with javac [debug parameters release 21]",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('--- maven-resources-plugin:3.3.1:testResources ---')}",
                            f"[{c_cyan('INFO')}] skip non existing resourceDirectory",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('--- maven-compiler-plugin:3.13.0:testCompile ---')}",
                            f"[{c_cyan('INFO')}] Not compiling test sources",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('--- maven-surefire-plugin:3.5.2:test ---')}",
                            f"[{c_cyan('INFO')}] Tests are skipped.",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('--- maven-jar-plugin:3.4.2:jar ---')}",
                            f"[{c_cyan('INFO')}] Building jar: /home/cutec/projects/nexus/java-worker/target/java-worker-1.4.2.jar",
                            f"[{c_cyan('INFO')}]",
                            f"[{c_cyan('INFO')}] {c_bold('--- spring-boot-maven-plugin:3.5.6:repackage ---')}",
                            f"[{c_cyan('INFO')}] Replacing main artifact with repackaged archive",
                            f"[{c_cyan('INFO')}] {c_bold('------------------------------------------------------------------------')}",
                            f"[{c_cyan('INFO')}] {c_bold(c_green('BUILD SUCCESS'))}",
                            f"[{c_cyan('INFO')}] {c_bold('------------------------------------------------------------------------')}",
                            f"[{c_cyan('INFO')}] Total time:  5.312 s",
                            f"[{c_cyan('INFO')}] Finished at: 2026-11-23T18:04:12+08:00",
                            f"[{c_cyan('INFO')}] {c_bold('------------------------------------------------------------------------')}",
                        ]
                    ),
                },
                {
                    "cmd": "ls -lh target",
                    "output": "\n".join(
                        [
                            "total 68M",
                            f"-rw-r--r-- 1 {USER} {USER}  68M Nov 23 18:04 {c_exe('java-worker-1.4.2.jar')}",
                            f"drwxr-xr-x 3 {USER} {USER} 4.0K Nov 23 18:04 {c_dir('classes')}",
                            f"drwxr-xr-x 2 {USER} {USER} 4.0K Nov 23 18:04 {c_dir('generated-sources')}",
                            f"drwxr-xr-x 2 {USER} {USER} 4.0K Nov 23 18:04 {c_dir('maven-archiver')}",
                            f"drwxr-xr-x 2 {USER} {USER} 4.0K Nov 23 18:04 {c_dir('maven-status')}",
                        ]
                    ),
                },
                {"cmd": "cd ..", "output": "", "cwd": "~/projects/nexus"},
            ],
        },
        {
            "name": "pack-and-ps",
            "steps": [
                {
                    "cmd": "curl -s http://localhost:8080/api/health",
                    "think": 360,
                    "output": '{"status":"ok","uptime":7482,"version":"1.4.2"}',
                },
                {
                    "cmd": "tar -czvf dist/nexus-1.4.2.tar.gz README.md package.json dist/server.js java-worker/target/java-worker-1.4.2.jar",
                    "think": 720,
                    "ms_per_line": 99,
                    "output": "\n".join(
                        [
                            "README.md",
                            "package.json",
                            "dist/server.js",
                            "java-worker/target/java-worker-1.4.2.jar",
                        ]
                    ),
                },
                {
                    "cmd": "ls -lh dist",
                    "output": "\n".join(
                        [
                            "total 69M",
                            f"-rw-r--r-- 1 {USER} {USER}  128K Nov 23 18:04 server.js",
                            f"-rw-r--r-- 1 {USER} {USER}   68M Nov 23 18:04 {c_exe('nexus-1.4.2.tar.gz')}",
                            f"drwxr-xr-x 2 {USER} {USER} 4.0K Nov 23 16:40 {c_dir('maps')}",
                        ]
                    ),
                },
                {
                    "cmd": "ps aux | grep -E 'node|java|docker|nginx' | grep -v grep",
                    "output": "\n".join(
                        [
                            "USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND",
                            f"{USER}    1042  0.1  0.4 615200 38240 ?        Ssl  09:41   0:12 {c_green('node')} dist/server.js",
                            f"{USER}    1188  0.3  1.8 4120880 214336 ?      Ssl  09:41   1:04 {c_green('java')} -jar /app/java-worker-1.4.2.jar",
                            "root      2210  0.0  0.2 1918840 22116 ?       Ssl  Nov21   0:31 dockerd --containerd",
                            f"{USER}    3341  0.0  0.1  32544  8940 ?        S    17:02   0:00 nginx: worker process",
                            f"{USER}    8910  0.2  0.6 987112  61208 pts/2    Sl+  17:58   0:03 {c_green('node')} /usr/bin/npm test",
                        ]
                    ),
                },
                {
                    "cmd": 'git add src/auth/token.ts tests/auth.spec.ts && git commit -m "fix: expired tokens should return 401"',
                    "think": 900,
                    "output": "\n".join(
                        [
                            f"[main {c_yellow('b7c41d2')}] fix: expired tokens should return 401",
                            " 2 files changed, 8 insertions(+), 5 deletions(-)",
                        ]
                    ),
                },
            ],
        },
        {
            "name": "redis",
            "steps": [
                {
                    "cmd": "docker exec nexus-redis redis-cli PING",
                    "think": 540,
                    "output": c_green("PONG"),
                },
                {
                    "cmd": "docker exec nexus-redis redis-cli INFO server",
                    "think": 480,
                    "ms_per_line": 58,
                    "output": "\n".join(
                        [
                            c_dim("# Server"),
                            "redis_version:7.4.2",
                            "redis_mode:standalone",
                            "os:Linux 6.8.0-51-generic x86_64",
                            "arch_bits:64",
                            "multiplexing_api:epoll",
                            "process_id:1",
                            "tcp_port:6379",
                            "uptime_in_seconds:176412",
                            "uptime_in_days:2",
                            "executable:/usr/local/bin/redis-server",
                            "config_file:/usr/local/etc/redis/redis.conf",
                            "listener0:name=tcp,bind=*,port=6379",
                        ]
                    ),
                },
                {
                    "cmd": "docker exec nexus-redis redis-cli CONFIG GET maxmemory*",
                    "output": "\n".join(
                        [
                            '1) "maxmemory"',
                            '2) "268435456"',
                            '3) "maxmemory-clients"',
                            '4) "0"',
                            '5) "maxmemory-policy"',
                            '6) "allkeys-lru"',
                            '7) "maxmemory-samples"',
                            '8) "5"',
                        ]
                    ),
                },
                {
                    "cmd": "docker exec nexus-redis redis-cli SCAN 0 MATCH nexus:* COUNT 20",
                    "output": "\n".join(
                        [
                            '1) "0"',
                            "2) 1) \"nexus:session:8f2a\"",
                            '   2) "nexus:settings:org:42"',
                            '   3) "nexus:region:lock:ap-east-1"',
                            '   4) "nexus:job:queue:default"',
                            '   5) "nexus:job:active:1842"',
                        ]
                    ),
                },
                {
                    "cmd": "docker exec nexus-redis redis-cli GET nexus:settings:org:42",
                    "think": 630,
                    "output": '{"theme":"dark","retentionDays":30,"region":"ap-east-1"}',
                },
                {
                    "cmd": "sed -n '1,22p' deploy/redis/redis.conf",
                    "think": 820,
                    "output": "\n".join(
                        [
                            c_dim("# nexus redis — cache + short-lived session store"),
                            "bind 0.0.0.0",
                            "port 6379",
                            "protected-mode yes",
                            "daemonize no",
                            "tcp-backlog 511",
                            "timeout 0",
                            "tcp-keepalive 300",
                            "",
                            "maxmemory 256mb",
                            "maxmemory-policy allkeys-lru",
                            "maxmemory-samples 5",
                            "",
                            "appendonly yes",
                            "appendfsync everysec",
                            "dir /data",
                            "dbfilename dump.rdb",
                            "save 900 1",
                            "save 300 10",
                            "save 60 10000",
                        ]
                    ),
                },
            ],
        },
        {
            "name": "postgres",
            "steps": [
                {
                    "cmd": "docker exec nexus-db psql -U nexus -d nexus -c '\\l'",
                    "think": 720,
                    "output": "\n".join(
                        [
                            "                                                 List of databases",
                            "   Name    |  Owner   | Encoding |   Collate   |    Ctype    | Access privileges",
                            "-----------+----------+----------+-------------+-------------+-----------------------",
                            " nexus     | nexus    | UTF8     | en_US.utf8  | en_US.utf8  |",
                            " postgres  | postgres | UTF8     | en_US.utf8  | en_US.utf8  |",
                            " template0 | postgres | UTF8     | en_US.utf8  | en_US.utf8  | =c/postgres          +",
                            "           |          |          |             |             | postgres=CTc/postgres",
                            " template1 | postgres | UTF8     | en_US.utf8  | en_US.utf8  | =c/postgres          +",
                            "           |          |          |             |             | postgres=CTc/postgres",
                            "(4 rows)",
                        ]
                    ),
                },
                {
                    "cmd": "docker exec nexus-db psql -U nexus -d nexus -c '\\dt'",
                    "output": "\n".join(
                        [
                            "             List of relations",
                            " Schema |   Name   | Type  | Owner",
                            "--------+----------+-------+-------",
                            " public | jobs     | table | nexus",
                            " public | regions  | table | nexus",
                            " public | settings | table | nexus",
                            " public | users    | table | nexus",
                            "(4 rows)",
                        ]
                    ),
                },
                {
                    "cmd": "docker exec nexus-db psql -U nexus -d nexus -c '\\d regions'",
                    "think": 680,
                    "output": "\n".join(
                        [
                            "                        Table \"public.regions\"",
                            "   Column    |           Type           | Collation | Nullable |      Default",
                            "-------------+--------------------------+-----------+----------+-------------------",
                            " id          | bigint                   |           | not null | nextval('regions_id_seq'::regclass)",
                            " org_id      | integer                  |           | not null |",
                            " code        | text                     |           | not null |",
                            " name        | text                     |           | not null |",
                            " status      | text                     |           | not null | 'active'::text",
                            " updated_at  | timestamp with time zone |           | not null | now()",
                            "Indexes:",
                            '    "regions_pkey" PRIMARY KEY, btree (id)',
                            '    "regions_org_id_status_idx" btree (org_id, status)',
                            '    "regions_code_key" UNIQUE CONSTRAINT, btree (code)',
                        ]
                    ),
                },
                {
                    "cmd": 'docker exec nexus-db psql -U nexus -d nexus -c "SELECT id, code, name, status FROM regions ORDER BY updated_at DESC LIMIT 5;"',
                    "output": "\n".join(
                        [
                            " id |     code      |         name          |  status",
                            "----+---------------+-----------------------+----------",
                            " 18 | ap-east-1     | Asia Pacific East     | active",
                            "  7 | us-west-2     | US West (Oregon)      | active",
                            " 11 | eu-central-1  | Europe (Frankfurt)    | active",
                            "  4 | ap-south-1    | Asia Pacific South    | draining",
                            "  9 | us-east-1     | US East (N. Virginia) | active",
                            "(5 rows)",
                        ]
                    ),
                },
                {
                    "cmd": "docker exec nexus-db psql -U nexus -d nexus -c \"EXPLAIN ANALYZE SELECT * FROM regions WHERE org_id = 42 AND status = 'active';\"",
                    "think": 900,
                    "ms_per_line": 72,
                    "output": "\n".join(
                        [
                            "                                                   QUERY PLAN",
                            "-------------------------------------------------------------------------------------------------------------",
                            " Index Scan using regions_org_id_status_idx on regions  (cost=0.29..12.41 rows=18 width=96) (actual time=0.042..0.118 rows=18 loops=1)",
                            "   Index Cond: ((org_id = 42) AND (status = 'active'::text))",
                            " Planning Time: 0.214 ms",
                            " Execution Time: 0.147 ms",
                            "(4 rows)",
                        ]
                    ),
                },
                {
                    "cmd": 'docker exec nexus-db psql -U nexus -d nexus -c "SHOW max_connections; SHOW shared_buffers; SELECT state, count(*) FROM pg_stat_activity GROUP BY state ORDER BY 2 DESC;"',
                    "think": 760,
                    "output": "\n".join(
                        [
                            " max_connections",
                            "-----------------",
                            " 100",
                            "(1 row)",
                            "",
                            " shared_buffers",
                            "----------------",
                            " 256MB",
                            "(1 row)",
                            "",
                            " state  | count",
                            "--------+-------",
                            " idle   |     6",
                            " active |     2",
                            "        |     1",
                            "(3 rows)",
                        ]
                    ),
                },
            ],
        },
        {
            "name": "nginx",
            "steps": [
                {
                    "cmd": "sudo nginx -t",
                    "think": 540,
                    "output": "\n".join(
                        [
                            f"nginx: the configuration file /etc/nginx/nginx.conf syntax is {c_green('ok')}",
                            f"nginx: configuration file /etc/nginx/nginx.conf test is {c_green('successful')}",
                        ]
                    ),
                },
                {
                    "cmd": "cat /etc/nginx/sites-available/nexus",
                    "think": 860,
                    "output": "\n".join(
                        [
                            "upstream nexus_api {",
                            "    server 127.0.0.1:8080;",
                            "    keepalive 16;",
                            "}",
                            "",
                            "upstream nexus_worker {",
                            "    server 127.0.0.1:8081;",
                            "}",
                            "",
                            "server {",
                            "    listen 80;",
                            "    listen 443 ssl;",
                            "    server_name nexus.internal;",
                            "",
                            "    ssl_certificate     /etc/nginx/ssl/nexus.internal.crt;",
                            "    ssl_certificate_key /etc/nginx/ssl/nexus.internal.key;",
                            "",
                            "    access_log /var/log/nginx/nexus.access.log;",
                            "    error_log  /var/log/nginx/nexus.error.log warn;",
                            "",
                            "    location /api/ {",
                            "        proxy_pass http://nexus_api;",
                            "        proxy_http_version 1.1;",
                            "        proxy_set_header Host $host;",
                            "        proxy_set_header X-Real-IP $remote_addr;",
                            "        proxy_set_header Connection \"\";",
                            "    }",
                            "}",
                        ]
                    ),
                },
                {
                    "cmd": "systemctl status nginx --no-pager",
                    "output": "\n".join(
                        [
                            f"{c_green('●')} nginx.service - A high performance web server and a reverse proxy server",
                            "     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: enabled)",
                            f"     Active: {c_green('active (running)')} since Mon 2026-11-23 17:02:11 CST; 16h ago",
                            "       Docs: man:nginx(8)",
                            "    Process: 3328 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)",
                            "    Process: 3332 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)",
                            "   Main PID: 3333 (nginx)",
                            "      Tasks: 5 (limit: 154027)",
                            "     Memory: 12.4M (peak: 14.1M)",
                            "        CPU: 1.882s",
                            "     CGroup: /system.slice/nginx.service",
                            '             ├─3333 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"',
                            '             └─3341 "nginx: worker process"',
                        ]
                    ),
                },
                {
                    "cmd": "curl -sI http://localhost/api/health",
                    "think": 400,
                    "output": "\n".join(
                        [
                            "HTTP/1.1 200 OK",
                            "Server: nginx/1.26.3",
                            "Date: Tue, 24 Nov 2026 01:24:18 GMT",
                            "Content-Type: application/json; charset=utf-8",
                            "Content-Length: 48",
                            "Connection: keep-alive",
                            "X-Request-Id: 7c1a9e2b4d08",
                        ]
                    ),
                },
                {
                    "cmd": "sudo tail -n 10 /var/log/nginx/nexus.access.log",
                    "ms_per_line": 62,
                    "output": "\n".join(
                        [
                            f'127.0.0.1 - - [24/Nov/2026:09:18:02 +0800] "GET /api/health HTTP/1.1" 200 48 "-" "curl/8.5.0"',
                            f'10.8.0.21 - - [24/Nov/2026:09:18:44 +0800] "GET /api/v1/settings HTTP/1.1" 200 812 "-" "nexus-web/1.4.2"',
                            f'10.8.0.21 - - [24/Nov/2026:09:19:11 +0800] "GET /api/v1/regions HTTP/1.1" 200 2410 "-" "nexus-web/1.4.2"',
                            f'10.8.0.37 - - [24/Nov/2026:09:20:06 +0800] "POST /api/v1/regions/import HTTP/1.1" 201 96 "-" "java-worker/1.4.2"',
                            f'10.8.0.21 - - [24/Nov/2026:09:21:33 +0800] "PUT /api/v1/settings HTTP/1.1" 200 812 "-" "nexus-web/1.4.2"',
                        ]
                    ),
                },
                {
                    "cmd": "sudo nginx -s reload",
                    "think": 880,
                    "output": "",
                },
            ],
        },
        {
            "name": "git-conflict",
            "steps": [
                {
                    "cmd": "git merge origin/feature/cache-ttl",
                    "think": 960,
                    "output": "\n".join(
                        [
                            "Auto-merging src/cache/ttl.ts",
                            f"{c_red('CONFLICT (content): Merge conflict in src/cache/ttl.ts')}",
                            "Automatic merge failed; fix conflicts and then commit the result.",
                        ]
                    ),
                },
                {
                    "cmd": "git status",
                    "output": "\n".join(
                        [
                            f"On branch {c_green('main')}",
                            "Your branch is up to date with 'origin/main'.",
                            "",
                            "You have unmerged paths.",
                            '  (fix conflicts and run "git commit")',
                            '  (use "git merge --abort" to abort the merge)',
                            "",
                            "Unmerged paths:",
                            '  (use "git add <file>..." to mark resolution)',
                            f"\t{c_red('both modified:   src/cache/ttl.ts')}",
                            "",
                            "no changes added to commit",
                        ]
                    ),
                },
                {
                    "cmd": "sed -n '1,24p' src/cache/ttl.ts",
                    "think": 1100,
                    "output": "\n".join(
                        [
                            "export const sessionTtlSec = 30 * 60;",
                            "",
                            c_red("<<<<<<< HEAD"),
                            "export const settingsTtlSec = 60;",
                            "export const regionLockTtlSec = 15;",
                            c_red("======="),
                            "export const settingsTtlSec = 120;",
                            "export const regionLockTtlSec = 30;",
                            c_red(">>>>>>> origin/feature/cache-ttl"),
                            "",
                            "export function ttlFor(kind: CacheKind): number {",
                            "  switch (kind) {",
                            "    case \"session\": return sessionTtlSec;",
                            "    case \"settings\": return settingsTtlSec;",
                            "    case \"region-lock\": return regionLockTtlSec;",
                            "  }",
                            "}",
                        ]
                    ),
                },
                {
                    "cmd": "sed -n '1,16p' src/cache/ttl.ts",
                    "think": 1500,
                    "output": "\n".join(
                        [
                            "export const sessionTtlSec = 30 * 60;",
                            "export const settingsTtlSec = 120;",
                            "export const regionLockTtlSec = 15;",
                            "",
                            "export function ttlFor(kind: CacheKind): number {",
                            "  switch (kind) {",
                            "    case \"session\": return sessionTtlSec;",
                            "    case \"settings\": return settingsTtlSec;",
                            "    case \"region-lock\": return regionLockTtlSec;",
                            "  }",
                            "}",
                        ]
                    ),
                },
                {
                    "cmd": 'git add src/cache/ttl.ts && git commit -m "merge: keep longer settings ttl, retain short region lock"',
                    "think": 920,
                    "output": "\n".join(
                        [
                            f"[main {c_yellow('c91e4a8')}] merge: keep longer settings ttl, retain short region lock",
                        ]
                    ),
                },
            ],
        },
        {
            "name": "ops",
            "steps": [
                {
                    "cmd": "ss -lptn",
                    "think": 500,
                    "output": "\n".join(
                        [
                            "State  Recv-Q Send-Q Local Address:Port  Peer Address:Port Process",
                            'LISTEN 0      4096         0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=1021,fd=3))',
                            'LISTEN 0      511          0.0.0.0:80         0.0.0.0:*    users:(("nginx",pid=3341,fd=8))',
                            'LISTEN 0      511          0.0.0.0:443        0.0.0.0:*    users:(("nginx",pid=3341,fd=9))',
                            'LISTEN 0      4096         0.0.0.0:5432       0.0.0.0:*    users:(("docker-proxy",pid=2401,fd=4))',
                            'LISTEN 0      4096         0.0.0.0:6379       0.0.0.0:*    users:(("docker-proxy",pid=2418,fd=4))',
                            'LISTEN 0      4096         0.0.0.0:8080       0.0.0.0:*    users:(("docker-proxy",pid=2440,fd=4))',
                            'LISTEN 0      4096         0.0.0.0:8081       0.0.0.0:*    users:(("docker-proxy",pid=2452,fd=4))',
                        ]
                    ),
                },
                {
                    "cmd": "journalctl -u nginx --no-pager -n 10",
                    "ms_per_line": 60,
                    "output": "\n".join(
                        [
                            f"{c_dim('Nov 23 17:02:11')} g16 systemd[1]: Starting nginx.service - A high performance web server and a reverse proxy server...",
                            f"{c_dim('Nov 23 17:02:11')} g16 nginx[3328]: Configuration complete; {c_green('ready')} for start up",
                            f"{c_dim('Nov 23 17:02:11')} g16 systemd[1]: Started nginx.service - A high performance web server and a reverse proxy server.",
                            f"{c_dim('Nov 24 09:21:48')} g16 nginx[3333]: {c_green('reloaded')} configuration (signal 1)",
                        ]
                    ),
                },
                {
                    "cmd": "top -bn1 | head -n 16 && echo && df -h / /var/lib/docker && echo && free -h",
                    "think": 640,
                    "ms_per_line": 55,
                    "output": "\n".join(
                        [
                            "top - 09:22:14 up 2 days, 14:41,  3 users,  load average: 0.42, 0.38, 0.35",
                            "Tasks: 312 total,   1 running, 311 sleeping,   0 stopped,   0 zombie",
                            "%Cpu(s):  4.8 us,  1.2 sy,  0.0 ni, 93.6 id,  0.3 wa,  0.0 hi,  0.1 si,  0.0 st",
                            "MiB Mem :  32018.4 total,   8124.1 free,  10402.6 used,  13491.7 buff/cache",
                            "MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.  20416.2 avail Mem",
                            "",
                            "    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND",
                            f"   1188 {USER}    20   0 4120880 214336  18944 S   3.3   0.7   1:04.11 {c_green('java')}",
                            f"   1042 {USER}    20   0  615200  38240  14816 S   1.3   0.1   0:12.40 {c_green('node')}",
                            "    891 systemd   20   0 1918840  22116   8320 S   0.7   0.1   0:31.02 dockerd",
                            "   2408 999       20   0  288144  42116  16320 S   0.7   0.1   0:22.18 postgres",
                            "   2459 999       20   0   12844   8120   3264 S   0.3   0.0   0:18.66 redis-server",
                            "   3341 www-data  20   0   32544   8940   4100 S   0.0   0.0   0:00.81 nginx",
                            "",
                            "Filesystem      Size  Used Avail Use% Mounted on",
                            "/dev/nvme0n1p2  916G  412G  458G  48% /",
                            "/dev/nvme0n1p3  200G   67G  123G  36% /var/lib/docker",
                            "",
                            "               total        used        free      shared  buff/cache   available",
                            "Mem:            31Gi        10Gi       7.9Gi       412Mi        13Gi        19Gi",
                            "Swap:          2.0Gi          0B       2.0Gi",
                        ]
                    ),
                },
                {
                    "cmd": "kubectl -n nexus get pods",
                    "think": 720,
                    "output": "\n".join(
                        [
                            "NAME                            READY   STATUS    RESTARTS        AGE",
                            f"nexus-api-7f9c4d8b6-xk2m1       1/1     {c_green('Running')}   0               2h",
                            f"nexus-api-7f9c4d8b6-4q8vz       1/1     {c_green('Running')}   0               2h",
                            f"nexus-worker-5c6d7b9f4-n2p1w    1/1     {c_green('Running')}   1 (26m ago)     2h",
                            f"nexus-redis-0                   1/1     {c_green('Running')}   0               2d",
                            f"nexus-db-0                      1/1     {c_green('Running')}   0               2d",
                        ]
                    ),
                },
                {
                    "cmd": "kubectl -n nexus logs deploy/nexus-api --tail=8",
                    "think": 680,
                    "ms_per_line": 62,
                    "output": "\n".join(
                        [
                            f"{c_dim('2026-11-24T01:12:08.441Z')} {c_green('INFO')}  db pool ready  min=2 max=10",
                            f"{c_dim('2026-11-24T01:14:22.018Z')} {c_cyan('HTTP')}  GET /api/health 200 2ms",
                            f"{c_dim('2026-11-24T01:16:03.774Z')} {c_cyan('HTTP')}  GET /api/v1/regions 200 18ms",
                            f"{c_dim('2026-11-24T01:18:44.190Z')} {c_cyan('HTTP')}  GET /api/v1/settings 200 9ms",
                            f"{c_dim('2026-11-24T01:20:06.552Z')} {c_cyan('HTTP')}  POST /api/v1/regions/import 201 163ms",
                            f"{c_dim('2026-11-24T01:21:33.901Z')} {c_cyan('HTTP')}  PUT /api/v1/settings 200 41ms",
                        ]
                    ),
                },
                {
                    "cmd": "gh pr status && echo && aws s3 ls s3://nexus-artifacts/releases/",
                    "think": 980,
                    "ms_per_line": 70,
                    "output": "\n".join(
                        [
                            f"Relevant pull requests in {c_cyan('cutec/nexus')}",
                            "",
                            "Current branch",
                            "  #128  fix: expired tokens should return 401",
                            f"       {c_green('✓ Checks passing')}",
                            "",
                            "Created by you",
                            "  #126  add redis cache for org settings",
                            f"       {c_green('✓ Checks passing')}",
                            "  #119  java worker backoff on region import",
                            f"       {c_yellow('• Review required')}",
                            "",
                            "Requesting a code review from you",
                            "  #131  k8s: add redis sidecar probes",
                            f"       {c_green('✓ Checks passing')}",
                            "",
                            "2026-11-22 11:14:02    70222410 nexus-1.4.1.tar.gz",
                            "2026-11-23 18:06:11    71303168 nexus-1.4.2.tar.gz",
                        ]
                    ),
                },
            ],
        },
    ]

class TerminalView(QTextEdit):
    def __init__(self, font_family: str, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setUndoRedoEnabled(False)
        self.setCursorWidth(0)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setAcceptRichText(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._line_start = 0
        self._cursor_on = True
        self._show_cursor = True
        self._blink = QTimer(self)
        self._blink.setInterval(550)
        self._blink.timeout.connect(self._toggle_cursor)
        self._blink.start()
        self.apply_style(font_family)

    def apply_style(self, font_family: str):
        font = QFont(font_family)
        font.setPixelSize(15)
        font.setStyleHint(QFont.StyleHint.Monospace)
        font.setFixedPitch(True)
        self.setFont(font)
        t = THEME
        self.setStyleSheet(
            f"""
            QTextEdit {{
                background: {t['bg']};
                color: {t['fg']};
                border: none;
                padding: 10px 14px 20px 14px;
                selection-background-color: {t['border']};
                selection-color: {t['fg']};
            }}
            QScrollBar:vertical {{
                background: transparent;
                width: 10px;
                margin: 2px;
            }}
            QScrollBar::handle:vertical {{
                background: {t['border']};
                border-radius: 4px;
                min-height: 32px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
            """
        )

    def _toggle_cursor(self):
        if not self._show_cursor:
            return
        self._cursor_on = not self._cursor_on
        self.viewport().update()

    def set_cursor_visible(self, visible: bool, solid: bool = False):
        self._show_cursor = visible
        if solid:
            self._cursor_on = True

    def _cursor_fmt(self) -> QTextCharFormat:
        f = QTextCharFormat()
        t = THEME
        if self._show_cursor and self._cursor_on:
            f.setForeground(QColor(t["bg"]))
            f.setBackground(QColor(t["fg"]))
        else:
            f.setForeground(QColor(t["bg"]))
            f.setBackground(QColor(t["bg"]))
        return f

    def trim_old_lines(self):
        doc = self.document()
        while doc.blockCount() > MAX_LINES:
            cur = QTextCursor(doc.firstBlock())
            cur.select(QTextCursor.SelectionType.BlockUnderCursor)
            cur.removeSelectedText()
            cur.deleteChar()

    def begin_line(self):
        cur = self.textCursor()
        cur.movePosition(QTextCursor.MoveOperation.End)
        if self.document().characterCount() > 1:
            cur.insertText("\n")
        self._line_start = cur.position()
        self.setTextCursor(cur)

    def set_current_line(self, parts: list[tuple[str, QTextCharFormat]], show_cursor: bool = True):
        cur = self.textCursor()
        cur.setPosition(self._line_start)
        cur.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
        cur.removeSelectedText()
        for text, fmt_ in parts:
            cur.setCharFormat(fmt_)
            cur.insertText(text)
        self._show_cursor = show_cursor
        if show_cursor:
            cur.setCharFormat(self._cursor_fmt())
            cur.insertText(" ")
        self.setTextCursor(cur)
        self.ensureCursorVisible()

    def add_ansi_line(self, text: str):
        cur = self.textCursor()
        cur.movePosition(QTextCursor.MoveOperation.End)
        if self.document().characterCount() > 1:
            cur.insertText("\n")
        for piece, fmt_ in parse_ansi(text):
            cur.setCharFormat(fmt_)
            cur.insertText(piece)
        self._line_start = cur.position()
        self.setTextCursor(cur)
        self.ensureCursorVisible()
        self.trim_old_lines()

    def add_comment(self, text: str):
        self.add_ansi_line(c_dim(text))

    def reset_document(self):
        self.clear()
        self._line_start = 0


class MainWindow(QMainWindow):
    def __init__(self, fonts: list[dict], settings: dict):
        super().__init__()
        self._closed = False
        self._force_quit = False
        self._told_tray = False
        self.cwd = "~/projects/nexus"
        self.fonts = fonts
        self.settings = settings
        self.font_family = self._family_for(settings["font"])
        self.history: list[dict] = []
        self._live: dict | None = None

        set_scheme(settings["scheme"])
        self.setWindowTitle(f"{USER}@{HOST} — cyber_code")
        self.setWindowIcon(load_app_icon())
        self.resize(1040, 700)
        self.setMinimumSize(720, 480)

        root = QWidget()
        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header = QWidget()
        self.header.setFixedHeight(36)
        h = QHBoxLayout(self.header)
        h.setContentsMargins(14, 0, 14, 0)
        self.title_label = QLabel()
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        h.addWidget(self.title_label, 1)
        h.addWidget(self.clock_label, 0)

        self.term = TerminalView(self.font_family)
        layout.addWidget(self.header)
        layout.addWidget(self.term, 1)
        self.setCentralWidget(root)

        self._apply_chrome()
        self._update_title()
        self._tick_clock()
        clock = QTimer(self)
        clock.setInterval(1000)
        clock.timeout.connect(self._tick_clock)
        clock.start()

        self._setup_tray()
        QTimer.singleShot(200, self._run_loop)

    def _family_for(self, font_id: str) -> str:
        for item in self.fonts:
            if item["id"] == font_id:
                return item["family"]
        return self.fonts[0]["family"]

    def _menu_style(self) -> str:
        t = THEME
        return f"""
            QMenu {{
                background: {t['bar']};
                color: {t['fg']};
                border: 1px solid {t['border']};
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 28px 6px 12px;
            }}
            QMenu::item:selected {{
                background: {t['border']};
            }}
            QMenu::separator {{
                height: 1px;
                background: {t['border']};
                margin: 4px 8px;
            }}
        """

    def _apply_chrome(self):
        t = THEME
        self.setStyleSheet(f"QMainWindow {{ background: {t['bg']}; }}")
        self.centralWidget().setStyleSheet(f"background: {t['bg']};")
        self.header.setStyleSheet(
            f"background: {t['bar']}; border-bottom: 1px solid {t['border']};"
        )
        self.title_label.setStyleSheet(
            f"color: {t['title']}; font-size: 12px; background: transparent; border: none;"
        )
        self.clock_label.setStyleSheet(
            f"color: {t['dim']}; font-size: 11px; background: transparent; border: none;"
        )
        title_font = QFont(self.font_family)
        title_font.setPixelSize(12)
        self.title_label.setFont(title_font)
        self.clock_label.setFont(title_font)
        self.term.apply_style(self.font_family)
        if hasattr(self, "tray"):
            self.tray.setIcon(load_app_icon())
        if hasattr(self, "_tray_menu"):
            self._tray_menu.setStyleSheet(self._menu_style())

    def _rebuild_history(self):
        typing = self._live
        self.term.reset_document()
        for item in self.history:
            kind = item["kind"]
            if kind == "cmd":
                self.term.begin_line()
                parts = self.prompt_parts(item["cwd"]) + [(item["cmd"], fmt())]
                self.term.set_current_line(parts, show_cursor=False)
            elif kind == "ansi":
                self.term.add_ansi_line(item["text"])
            elif kind == "comment":
                self.term.add_comment(item["text"])
        if typing is not None:
            self.term.begin_line()
            self.term.set_current_line(
                self.prompt_parts() + [(typing.get("typed", ""), fmt())],
                show_cursor=True,
            )
            self.term.set_cursor_visible(True, solid=True)

    def _remember(self, item: dict):
        self.history.append(item)
        overflow = len(self.history) - MAX_LINES
        if overflow > 0:
            self.history = self.history[overflow:]

    def set_font(self, font_id: str):
        if font_id == self.settings.get("font"):
            return
        self.settings["font"] = font_id
        self.font_family = self._family_for(font_id)
        save_settings(self.settings)
        self._apply_chrome()
        self._rebuild_history()

    def set_color_scheme(self, scheme_id: str):
        if scheme_id == self.settings.get("scheme"):
            return
        self.settings["scheme"] = scheme_id
        set_scheme(scheme_id)
        save_settings(self.settings)
        self._apply_chrome()
        self._rebuild_history()

    def _setup_tray(self):
        self.tray = QSystemTrayIcon(load_app_icon(), self)
        self.tray.setToolTip("cyber_code")
        menu = QMenu()
        menu.setStyleSheet(self._menu_style())
        self._tray_menu = menu

        show_act = QAction("显示窗口", self)
        show_act.triggered.connect(self.show_window)
        menu.addAction(show_act)
        menu.addSeparator()

        font_menu = menu.addMenu("字体")
        font_group = QActionGroup(self)
        font_group.setExclusive(True)
        for item in self.fonts:
            act = QAction(item["label"], self, checkable=True)
            act.setChecked(item["id"] == self.settings["font"])
            act.triggered.connect(lambda checked, fid=item["id"]: checked and self.set_font(fid))
            font_group.addAction(act)
            font_menu.addAction(act)

        scheme_menu = menu.addMenu("配色方案")
        scheme_group = QActionGroup(self)
        scheme_group.setExclusive(True)
        for scheme_id, scheme in SCHEMES.items():
            act = QAction(scheme["name"], self, checkable=True)
            act.setChecked(scheme_id == self.settings["scheme"])
            act.triggered.connect(
                lambda checked, sid=scheme_id: checked and self.set_color_scheme(sid)
            )
            scheme_group.addAction(act)
            scheme_menu.addAction(act)

        menu.addSeparator()
        quit_act = QAction("退出", self)
        quit_act.triggered.connect(self.quit_app)
        menu.addAction(quit_act)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self._on_tray_activated)
        self.tray.show()

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason):
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
            QSystemTrayIcon.ActivationReason.MiddleClick,
        ):
            if self.isVisible() and not self.isMinimized():
                self.hide()
            else:
                self.show_window()

    def show_window(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def quit_app(self):
        self._force_quit = True
        self._closed = True
        loop = getattr(self, "_loop", None)
        if loop is not None and loop.isRunning():
            loop.quit()
        self.tray.hide()
        QApplication.quit()

    def closeEvent(self, event):
        if self._force_quit or not self.tray.isVisible():
            self._closed = True
            loop = getattr(self, "_loop", None)
            if loop is not None and loop.isRunning():
                loop.quit()
            event.accept()
            return
        event.ignore()
        self.hide()
        if not self._told_tray:
            self._told_tray = True
            self.tray.showMessage(
                "cyber_code",
                "程序还在托盘里运行，右键图标可以改字体和配色。",
                QSystemTrayIcon.MessageIcon.Information,
                2500,
            )

    def _update_title(self):
        self.title_label.setText(f"{USER}@{HOST}: {self.cwd}")
        self.setWindowTitle(f"{USER}@{HOST}: {self.cwd}")

    def _tick_clock(self):
        self.clock_label.setText(datetime.now().strftime("%H:%M:%S"))

    def wait(self, ms: float) -> bool:
        if self._closed:
            return False
        loop = QEventLoop(self)
        self._loop = loop
        QTimer.singleShot(max(0, int(ms)), loop.quit)
        loop.exec()
        self._loop = None
        return not self._closed

    def prompt_parts(self, cwd: str | None = None) -> list[tuple[str, QTextCharFormat]]:
        path = self.cwd if cwd is None else cwd
        t = THEME
        return [
            (USER, fmt(t["green"], bold=True)),
            ("@", fmt(t["dim"], dim=True)),
            (HOST, fmt(t["cyan"])),
            (":", fmt(t["dim"], dim=True)),
            (path, fmt(t["blue"])),
            ("$ ", fmt(t["fg"], bold=True)),
        ]

    def type_command(self, cmd: str) -> bool:
        self.term.begin_line()
        typed = ""
        self._live = {"typed": typed}
        self.term.set_cursor_visible(True, solid=True)
        self.term.set_current_line(self.prompt_parts() + [(typed, fmt())], show_cursor=True)
        if not self.wait(420 + random.random() * 380):
            return False
        for ch in cmd:
            if self._closed:
                return False
            if random.random() < 0.045 and ch.isalpha():
                typed += nearby_key(ch)
                self._live = {"typed": typed}
                self.term.set_current_line(self.prompt_parts() + [(typed, fmt())], True)
                if not self.wait(160 + random.random() * 120):
                    return False
                typed = typed[:-1]
                self._live = {"typed": typed}
                self.term.set_current_line(self.prompt_parts() + [(typed, fmt())], True)
                if not self.wait(110 + random.random() * 80):
                    return False
            typed += ch
            self._live = {"typed": typed}
            self.term.set_current_line(self.prompt_parts() + [(typed, fmt())], True)
            delay = 70 + random.random() * 90
            if ch.isupper():
                delay += 40
            if ch in " /.-_":
                delay += 70 + random.random() * 80
            if ch == " ":
                delay += 50
            if not self.wait(delay):
                return False
        if not self.wait(380 + random.random() * 320):
            return False
        self.term.set_current_line(self.prompt_parts() + [(typed, fmt())], show_cursor=False)
        self.term.set_cursor_visible(False)
        self._live = None
        self._remember({"kind": "cmd", "cwd": self.cwd, "cmd": typed})
        return True

    def print_output(self, text: str, ms_per_line: int | None = None) -> bool:
        if not text:
            return True
        lines = text.split("\n")
        ms = ms_per_line if ms_per_line is not None else (55 if len(lines) > 12 else 90)
        for raw in lines:
            if self._closed:
                return False
            self.term.add_ansi_line(raw)
            self._remember({"kind": "ansi", "text": raw})
            if ms > 0 and not self.wait(ms + random.random() * 40):
                return False
        return True

    def _run_loop(self):
        if not self.wait(1800):
            return
        comment = "# nexus dev session — " + datetime.now().strftime("%Y-%m-%d")
        self.term.add_comment(comment)
        self._remember({"kind": "comment", "text": comment})
        if not self.wait(800):
            return

        order = sessions()
        first = True
        while not self._closed:
            if not first:
                if not self.wait(1800):
                    return
                if random.random() < 0.5:
                    order = sessions()
                    random.shuffle(order)
            first = False
            for session in order:
                for step in session["steps"]:
                    think = step.get("think", 700 + random.random() * 900)
                    if not self.wait(think):
                        return
                    if not self.type_command(step["cmd"]):
                        return
                    output = step["output"]
                    if callable(output):
                        output = output()
                    if not self.print_output(output, step.get("ms_per_line")):
                        return
                    if "cwd" in step:
                        self.cwd = step["cwd"]
                        self._update_title()
            self.term.begin_line()
            self.term.set_current_line(self.prompt_parts(), show_cursor=True)
            self.term.set_cursor_visible(True)
            self._live = {"typed": ""}


def main():
    if _frozen():
        os.chdir(writable_root())
    set_windows_app_id()
    app = QApplication(sys.argv)
    app.setApplicationName("cyber_code")
    app.setQuitOnLastWindowClosed(False)
    fonts = load_fonts()
    settings = load_settings(fonts)
    set_scheme(settings["scheme"])
    icon = load_app_icon()
    app.setWindowIcon(icon)
    win = MainWindow(fonts, settings)
    win.setWindowIcon(icon)
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
