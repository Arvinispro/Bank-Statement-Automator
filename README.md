# Bank-Statement-Organizer-Automation
A Python automation tool using Google Sheets API and OOP to generate monthly reconciliation and income–expenditure reports from chequeing and savings accounts. Runs fully in Google Colab with no local setup required, making financial reporting easy for non-coders.
# 💰 Automated Bank Transaction Reconciliation & Reporting

This project automates the process of generating **monthly financial reports** (reconciliation and income–expenditure sheets) using **Python**, **Google Sheets API**, and **Google Colab** — so even non-coders can create clean reports with one click.

---

## ✨ Features

- 🔹 **Google Sheets Integration** — Reads initial balances and transaction file name directly from cells, and writes final reports back to the sheet.  
- 🧮 **OOP-Powered Transformations** — Organized logic into modular classes:
  - `chequeing_recon_transform()` and `saving_recon_transform()` — generate reconciliation reports
  - `income_transform()` and `expenditure_transform()` — generate income & expenditure reports
- ⚡ **Automation Rules**
  - Excludes internal transfers and e-transfer fees from income/expenditure
  - Cleans and transforms data with `pandas`, `numpy`, string methods, and list comprehensions
- ☁️ **Zero Local Setup** — Runs entirely in Google Colab, which automatically installs dependencies in a virtual environment.
- 🔐 **Simple UI/UX** — Designed so that people with no coding background can generate reports easily.
- 📂 **Credential Handling** — Stores API credential file and scripts in Google Drive to avoid repetitive uploads.

---

## 🧭 Project Structure

├── report_auto.py # Handles Google Sheet API connection and update logic

├── roc.py # Core transformation logic with OOP classes

├── Financial_Report_Automation.ipynb # Google Colab notebook for end users

├── README.md

└── .gitignore

---

## 🧠 How It Works

1. **Read** — Pull data from Google Sheets (initial balance, transaction file name).  
2. **Transform** — Apply OOP-based classes to clean and structure transactions:
   - Remove internal transfers and fees from income/expenditure.
   - Organize reconciliation data for chequeing and savings accounts.
3. **Write** — Update the processed data back into the Google Sheet.

---


## 🧪 Tech Stack

- 🐍 Python  
- 🧾 Pandas, Numpy  
- ☁️ Google Sheets API  
- 🧰 Google Colab  
- 🪝 GitHub

---


## ⚠️ Disclaimer

This project is intended for **personal or internal organizational use**.  
Do not share sensitive or personal financial data in public repositories.

