# 🔍 Circle-to-Search Desktop AI Tool

Inspired by Android's "Circle to Search" and macOS Spotlight. Select any portion of your screen, type your question, and get AI answers instantly—all without leaving your current workspace.

---

> ### 💬 Why build this?
> *"I know we can just copy text or screenshot, open an AI tab, and ask. I just made this because I wanted to."*

---

## ✨ Features

- **Instant Screen Capture:** Drag a box over any screen area.
- **Auto-Focused Input:** Cursor is ready immediately upon releasing mouse.
- **Press Esc to Exit:** Instantly close the overlay anytime.

---

## 🚀 Setup & Installation

### 1. Prerequisites

Ensure you have Python 3.10+ installed and added to your system PATH.

Install the required Python libraries:

```bash
pip install PyQt6 pillow google-genai
```

### 2. Configure Your API Key

Set up your Gemini API key as a system environment variable:
1. Press `Win + R`, type `sysdm.cpl`, and press `Enter`.
2. Go to **Advanced** -> **Environment Variables**.
3. Under **User variables**, click **New**:
   - **Variable name:** `GEMINI_API_KEY`
   - **Variable value:** `your_actual_gemini_api_key`

### 3. Setting Up Your Custom Hotkey

You can use AutoHotkey (v2) to trigger the script seamlessly with any key combination you want.

1. Download and install AutoHotkey v2.
2. Save your Python script to a fixed location (e.g., `C:\Scripts\circle_search.py`).
3. Create a new file named `circle_search.ahk` and paste the following:

```autohotkey
#Requires AutoHotkey v2.0

; Default Hotkey: Win + Shift + C
#+c::
{
    ; Silent background execution using pythonw.exe
    Run('pythonw.exe "C:\Scripts\circle_search.py"', , "Hide")
}
```

#### 💡 Customizing Your Hotkey

You can change `#+c::` to whatever key combination suits your workflow best:

| AutoHotkey Symbol | Key |
| :--- | :--- |
| `#` | Windows Key |
| `+` | Shift |
| `!` | Alt |
| `^` | Ctrl |

**Examples:**
- `^!a::` -> `Ctrl + Alt + A`
- `#F1::` -> `Win + F1`
- `!Space::` -> `Alt + Space`

Double-click `circle_search.ahk` to run it.

---

## 🛠️ Usage

1. Press your configured hotkey.
2. Drag & select any area on your screen.
3. Type your prompt immediately.
4. Press `Enter` to submit.
5. Press `Esc` anytime to close.
