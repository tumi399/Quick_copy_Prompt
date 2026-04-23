---

# 🧠 Prompt Manager

A simple desktop application to store, manage, and quickly reuse your prompts.

Built with **Python + CustomTkinter**, this tool is designed for people who frequently work with AI (ChatGPT, coding assistants, etc.) and need a clean way to organize prompts.

---

## 📥 Download & Installation

### 🔹 Option 1: Download Executable (Recommended)

👉 **Download latest version here:**
**[Download Prompt Manager (.exe)](https://github.com/tumi399/Quick_copy_Prompt/releases)**

> Just download, install and run.

---

### 🔹 Option 2: Run from Source

```bash
pip install customtkinter pillow cairosvg
python main.py
```

---

## ✨ Features

* 📌 **Pin important prompts**
  Keep frequently used prompts at the top.

* 🔍 **Instant search**
  Search by title or content in real-time.

* ✏️ **Create / Edit / Delete prompts**
  Easily manage your prompt library.

* 📋 **One-click copy**
  Copy prompt content directly to clipboard.

* 🌙 **Dark / Light mode**
  Toggle UI theme anytime.

* 💾 **Persistent storage**
  Data is saved locally (`AppData/PromptManager`).

---

## 🖥️ Tech Stack

* **Python**
* **CustomTkinter** (modern UI)
* **Tkinter**
* **Pillow (PIL)** – image processing
* **CairoSVG** – SVG icon rendering
* **JSON** – local storage

---

## 📁 Project Structure

```
PromptManager/
│
├── main.py
├── icons/
│   ├── copy.svg
│   ├── edit.svg
│   ├── trash-2.svg
│   ├── pin.svg
│   └── ...
└── app.ico
```

---

## ⚙️ How It Works

* Prompts are stored as a list of objects:

```json
{
  "title": "Example",
  "content": "Your prompt here",
  "pinned": false
}
```

* The app automatically:

  * Loads data on startup
  * Falls back to sample prompts if file is missing/corrupted
  * Saves instantly after every change

---

## 🚀 Run Locally

```bash
pip install customtkinter pillow cairosvg
python main.py
```

---


## 🎯 Use Cases

* Save Ai prompts
* Store coding templates
* Reuse writing / summarization formats
* Personal prompt library

---

## 👤 Author

**Ngo Van Tuan**
📧 [ngovantuan060606@gmail.com](mailto:ngovantuan060606@gmail.com)

---
