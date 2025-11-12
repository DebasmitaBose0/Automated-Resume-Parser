# Automated Resume Parser

A sophisticated web application that extracts and categorizes information from resumes using AI and Natural Language Processing (NLP). Built with Python, Flask, spaCy, and PostgreSQL.

## Features

 # ✨ Automated Resume Parser — Beautiful, Fast, Intelligent

Welcome to the shiny new README! This page is a compact, emoji-friendly guide to get you up and running, explore features, and contribute. The project extracts structured candidate data from resumes using NLP and streamlined document parsing.

🚀 Quick highlights

- 🧠 AI-powered extraction (spaCy + heuristics)
- 📄 PDF / DOC / DOCX processing
- 🔎 Advanced search + REST API
- 🗄️ PostgreSQL-backed storage
- 💻 Web UI (responsive, Bootstrap)

---

## 🎯 What makes this special

- Human-readable structured output for resumes (names, contacts, skills, experience, education).
- Extensible skill dictionaries and pattern-based extractors.
- Lightweight, easy to run locally or in a container.

---

## 🔧 Quick Start (Windows PowerShell)

1. Clone and enter the repo:

```powershell
git clone <repository-url>
cd Resumeparser
```

2. Create & activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install deps and run setup (automated):

```powershell
pip install -r requirements.txt
python setup.py
```

4. Start the app:

```powershell
python run.py
# Open http://localhost:5000
```

Tip: if PowerShell blocks activation, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

---

## 🗂️ Project structure (quick view)

app/ — core app, models, routes, services
templates/ — HTML templates
static/ — CSS, JS, images
uploads/ — temp upload storage
setup.py, run.py, requirements.txt, README.md, LICENSE

---

## 🔍 Example API endpoints

- POST /api/upload — upload a resume (form-data file)
- GET /api/candidates — list candidates (pagination + filtering)
- GET /api/candidates/{id} — candidate detail
- GET /api/search?q=python — search across fields

---

## 🎛️ Configuration

Create a `.env` with:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/resume_parser_db
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
ALLOWED_EXTENSIONS=pdf,doc,docx
```

Run migrations or start the app — it will create tables automatically on first run.

---

## ✨ Tips & Customization

- Add new technical/soft skills in `app/services/resume_extractor.py`.
- Improve NER by training or adding spaCy patterns.
- Add dockerfile / CI for automated builds.

---

## 🛠️ Troubleshooting (common)

- spaCy model missing: `python -m spacy download en_core_web_sm`
- NLTK data: run the small downloader in `setup.py` or use `nltk.download(...)`
- DB errors: check `.env` and ensure PostgreSQL is running

---

## 🧾 License

This project is licensed under the MIT License — see the `LICENSE` file.

---

## ❤️ Contributing

1. Fork → branch → PR
2. Add tests where applicable
3. Keep changes small and documented

---

If you'd like a more playful visual README (badges, screenshots, animated GIFs, or a landing image), I can add them — tell me which style you prefer (clean/professional, playful/startup, or developer-first). ✨
