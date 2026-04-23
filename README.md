---

# 🧠 Prompt Manager

A simple desktop application to store, manage, and quickly reuse your prompts.

Built with **Python + CustomTkinter**, this tool is designed for people who frequently work with AI (ChatGPT, coding assistants, etc.) and need a clean way to organize prompts.

---
<img width="710" height="672" alt="image" src="https://github.com/user-attachments/assets/5aad1f20-87b9-494d-a85c-a5ad99b7a933" />


## 📥 Download & Installation

### 🔹 Option 1: Download Executable (Recommended)

👉 **Download latest version here:**
**[Download Prompt Manager (.exe)](https://github.com/tumi399/Quick_copy_Prompt/releases)**

> Just download, install and run.

---

### 🔹 Option 2: Run from Source

```bash
pip install customtkinter pillow cairosvg
python application.py
```

---

## 🖥️ Tech Stack

* **Python**
* **CustomTkinter** (modern UI)
* **Tkinter**
* **Pillow (PIL)** – image processing
* **CairoSVG** – SVG icon rendering
* **JSON** – local storage

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
