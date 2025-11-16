
# 📄 Playwright Research Data Extractor

Automated web data extraction using Python & Playwright  
**Assignment Project – Automation Module**

---

## 🚀 Introduction

[`site_scraper_playwright.py`](site_scraper_playwright.py) is a fully automated Python script designed to extract structured research data from a curated list of popular tech websites. Leveraging Playwright (Chromium), it visits each site, collects key metadata, cleans and formats the content, and exports everything into a single, well-organized text file.  
Perfect for research, documentation, or content analysis tasks!

---

## ✨ Features

- **Automated Browsing:** Visits a predefined list of tech and developer sites
- **Metadata Extraction:** Captures page title, all H1/H2/H3 headings, and full visible text
- **Content Cleaning:** Removes unnecessary whitespace and HTML tags for clarity
- **Structured Output:** Saves results in a formatted text file (`playwright_research_output.txt`)
- **Error Handling:** Logs failures and continues processing remaining sites
- **Headless Operation:** Runs Chromium browser in headless mode for speed and reliability

---

## 🛠️ Prerequisites

- **Python 3.7+**
- **Playwright Python package**

---

## ⚡ Installation

1. **Clone the repository:**
	```bash
	git clone https://github.com/yourusername/genai-challenge.git
	cd genai-challenge/playwright-for-begineers
	```

2. **Create a virtual environment (recommended):**
	```bash
	python3 -m venv venv
	source venv/bin/activate
	```

3. **Install dependencies:**
	```bash
	pip install playwright
	```

4. **Install Playwright browsers:**
	```bash
	playwright install
	```

---

## ▶️ How to Run

Simply execute the script from your terminal:

```bash
python site_scraper_playwright.py
```

The script will visit each site, extract and clean the content, and save everything to `playwright_research_output.txt`.

---

## 📁 Project Structure

```
playwright-for-begineers/
│
├── site_scraper_playwright.py      # Main automation script
├── playwright_research_output.txt  # Output file (generated after run)
└── README.md                       # Project documentation
```

---

## 📝 Example Output Snippet

```
🌐 URL: https://www.python.org/downloads/release/python-3110/
📌 Title: Python 3.11.0 Release

🔹 HEADINGS:
	- Python 3.11.0 Release
	- Download
	- Documentation

🔹 FULL TEXT CONTENT:
Python 3.11.0 is now available. Python is a programming language that lets you work quickly...
--------------------------------------------------------------------------------
```

---

## 💡 Notes & Tips

- For best results, ensure a stable internet connection.
- The script runs Chromium in headless mode; no browser window will appear.
- You can customize the [`TARGET_URLS`](site_scraper_playwright.py) list in the script to add or remove sites.
- Output is limited to the first 5000 characters of each page’s body for brevity (adjustable in code).
- If you encounter errors, check that Playwright and its browsers are properly installed.

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 👤 Credit

**Author:** Mohamed Uvais  
Assignment for Playwright Automation Module

---

Happy scraping! 🚀