# 🔍 Circle-to-Search Desktop AI Tool

A minimalist, keyboard-driven, dark-themed desktop utility inspired by Android's "Circle to Search" and macOS Spotlight. Select any portion of your screen, type your question, and get AI anwers instantly—all without leaving your current workspace.

---

> ### 💬 *Why build this?*
> *"I know we can just copy text or screenshot, open an AI tab, and ask. I just made this because I wanted to."* 

---

## ✨ Features

- **Instant Screen Capture:** Drag a box over any screen area.

---

## 🚀 Setup & Installation

### 1. Prerequisites
Ensure you have Python 3.10+ installed and added to your system PATH.

Install the required Python libraries:
```bash
pip install PyQt6 pillow google-genai
2. Configure Your API KeySet up your Gemini API key as a system environment variable:Windows:Press Win + R, type sysdm.cpl, and press Enter.Go to Advanced -> Environment Variables.Under User variables, click New:Variable name: GEMINI_API_KEYVariable value: your_actual_gemini_api_key⌨️ Setting Up Your Custom HotkeyYou can use AutoHotkey (v2) to trigger the script seamlessly with any key combination you want.Download and install AutoHotkey v2.Save your Python script to a fixed location (e.g., C:\Scripts\circle_search.py).Create a new file named circle_search.ahk and paste the following:AutoHotkey#Requires AutoHotkey v2.0

; Default Hotkey: Win + Shift + C
#+c::
{
    ; Silent background execution using pythonw.exe
    Run('pythonw.exe "C:\Scripts\circle_search.py"', , "Hide")
}
💡 Customizing Your HotkeyYou can change #+c:: to whatever key combination suits your workflow best:AutoHotkey SymbolKey#Windows Key+Shift!Alt^CtrlExamples:^!a:: -> Ctrl + Alt + A#F1:: -> Win + F1!Space:: -> Alt + Space (Spotlight style)Double-click circle_search.ahk to run it.(Optional: Move the .ahk file into your Windows Startup folder shell:startup so it runs automatically when your PC boots up!)🛠️ UsagePress your configured hotkey (e.g., Win + Shift + C).Drag & select any area on your screen.Type your prompt immediately (input field is auto-focused).Press Enter to submit.Press Esc anytime to close.
