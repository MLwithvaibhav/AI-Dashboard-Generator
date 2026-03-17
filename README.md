# 🚀 AI Dashboard Generator

An AI-powered data visualization tool that converts natural language queries into interactive charts.

## ✨ Features

* 📊 Generate charts using plain English queries
* 🤖 Powered by Gemini AI
* 📈 Interactive visualizations using Plotly
* ⚡ Fast UI built with Streamlit
* 🎯 Automatic data understanding and chart generation

## 🧠 How it works

1. User enters a query (e.g., "Show average income by gender")
2. Gemini AI interprets the query
3. Pandas processes the dataset
4. Plotly generates the chart
5. Results are displayed instantly

## 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* Plotly
* Google Gemini API

## 📂 Project Structure

* `app.py` – Main application file
* `data.csv` – Dataset
* `.env` – API keys (not included in repo)

## ⚙️ Setup Instructions

```bash
git clone <your-repo-url>
cd ai-dashboard-generator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 🔐 Environment Variables

Create a `.env` file and add:

```
YOUR_API_KEY=your_gemini_api_key
```

## 🎯 Use Case

This project demonstrates how AI can simplify data analysis by allowing users to interact with data using natural language instead of writing code.

## 🚀 Future Improvements

* Multi-page dashboards
* Export charts
* User authentication
* Advanced analytics

## 🏆 Hackathon Project

Built during a hackathon using AI-assisted development.

---

⭐ If you like this project, consider giving it a star!
