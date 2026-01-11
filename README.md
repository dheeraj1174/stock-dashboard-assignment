# 📈 Stock Data Intelligence Dashboard

A mini financial data platform built as part of the **Assignment – Stock Data Intelligence Dashboard**.  


This project demonstrates real-world skills in **data collection, data processing, REST API development, and visualization** using Python.

---

## 🧭 Project Overview

The goal of this project is to:
- Collect real stock market data
- Clean and process financial data
- Expose insights via REST APIs
- Visualize stock trends using a simple dashboard

The backend is built using **FastAPI**, while the frontend uses **HTML + Chart.js** to display interactive stock charts.

---

## 🧰 Tech Stack

### Backend
- **Language**: Python  
- **Framework**: FastAPI  
- **Data Source**: yfinance  
- **Data Processing**: Pandas, NumPy  

### Frontend
- **HTML**
- **JavaScript**
- **Chart.js**

---

## 📁 Project Structure

stock-dashboard/
│
├── app/
│ ├── main.py # FastAPI application & routes
│ └── services.py # Data fetching, cleaning & analytics logic
│
├── frontend/
│ └── index.html # Visualization dashboard
│
├── requirements.txt
├── README.md