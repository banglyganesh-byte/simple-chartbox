# 📊 Simple Chartbox

**Simple Chartbox makes data visualization simple, fast, and accessible.**

A beginner-friendly web application that allows users to upload CSV data, analyze it, and create meaningful visualizations without requiring advanced data visualization knowledge.

![Simple Chartbox](simple%20chartbox.png)
## 🚀 Live Demo

Try Simple Chartbox by running the project locally.

```text
CSV → Preview → Analyze → Choose Chart → Customize → Download PNG
## 🚀 Features

### 📁 CSV Upload

* Upload CSV files directly through the web interface.
* Automatically reads and processes the uploaded data.

### 👀 Data Preview

* View uploaded data in a clean table.
* Easily inspect rows and columns before creating charts.

### 📈 Data Insights

Automatically calculates:

* Number of rows
* Number of columns
* Numeric columns
* Average value
* Maximum value
* Minimum value

### 📊 Performance Analysis

Automatically analyzes numerical data and categorizes values into:

* Excellent
* Good
* Average
* Needs Improvement

### 🏫 Class-wise Analysis

When class/group information is available, the application can calculate:

* Number of students
* Average marks
* Highest marks
* Lowest marks

### 🤖 AI Data Insights

Uses a local AI model through Ollama to generate meaningful observations from the uploaded dataset.

### 🤖 Smart Chart Recommendation

AI analyzes the dataset and recommends a suitable chart type based on the data.

### 📊 Multiple Chart Types

Currently supports:

* Bar Chart
* Line Chart
* Pie Chart
* Scatter Plot

### 🎨 Chart Customization

Users can customize:

* Chart title
* X-axis label
* Y-axis label
* Chart color
* Chart type

### 👥 Group By

Users can group data using a column such as Class and generate separate charts for each group.

### 🖼️ Download Charts

Generated charts can be downloaded as PNG images.

### 📱 Responsive Design

The interface is designed to work across:

* Desktop
* Tablet
* Mobile

### ⚠️ Error Handling

The application handles common problems such as:

* Missing X/Y-axis selections
* Invalid CSV files
* Unsupported data for certain chart types

---

## 🔄 How It Works

```text
Upload CSV
     ↓
Preview Data
     ↓
Analyze Dataset
     ↓
View Data Insights
     ↓
AI Insights & Recommendation
     ↓
Select X-Axis / Y-Axis
     ↓
Choose Chart Type
     ↓
Generate Chart
     ↓
Customize Chart
     ↓
Download PNG
```

---

## 🛠️ Technologies Used

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### Backend

* Python
* Flask
* Pandas
* Flask-CORS

### AI

* Ollama
* GPT-OSS 20B

### Development Tools

* Visual Studio Code
* Git
* GitHub

---

## 📂 Project Structure

```text
simple-chartbox/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── backend/
│   ├── app.py
│   └── requirements.txt
│
├── data/
│
└── README.md
```

---

## ⚙️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/banglyganesh-byte/simple-chartbox.git
```

### 2. Open the Project

```bash
cd simple-chartbox
```

### 3. Install Backend Dependencies

Activate your Python virtual environment and install the requirements:

```bash
pip install -r backend/requirements.txt
```

### 4. Start the Flask Backend

```bash
cd backend
python app.py
```

The backend will run on:

```text
http://127.0.0.1:5000
```

### 5. Start the Frontend

Open:

```text
frontend/index.html
```

in your browser.

---

## 🤖 AI Integration

Simple Chartbox uses **Ollama** to run AI locally.

The application can use the local:

```text
gpt-oss:20b
```

model to generate:

* Dataset insights
* Chart recommendations
* Basic observations about the uploaded data

This allows AI-powered analysis without requiring a paid cloud AI API.

---

## 📊 Example

Example dataset:

```csv
Class,Student,Marks
10,Rahul,85
10,Priya,92
10,Arjun,78
10,Sneha,88
10,Kiran,95
11,Anjali,72
11,Vikram,81
11,Rohan,68
11,Pooja,87
11,Neha,90
```

Simple Chartbox can analyze this dataset and create visualizations such as:

* Student marks bar chart
* Class-wise charts
* Performance distribution
* Scatter plots for suitable numerical datasets

---

## 🎯 Project Goal

The goal of Simple Chartbox is to make data visualization easier for beginners.

Instead of manually writing visualization code, users can upload their data, understand the dataset, select a chart, and generate a visualization through a simple interface.

---

## 🔮 Future Improvements

Possible future features include:

* Excel file support
* JSON file support
* Natural-language chart creation
* Advanced AI insights
* Automatic anomaly detection
* Multiple datasets
* Dashboard creation
* Save and share charts
* User accounts
* Cloud deployment
* More chart types
* Advanced analytics

---

## 👨‍💻 Author

**Ganesh B**

Built as a learning project to explore:

* Web Development
* Python
* Data Analysis
* Data Visualization
* AI Integration
* Full-Stack Application Development

---

## 📄 License

This project is created for educational and learning purposes.
![Simple Chartbox](../simple%20chartbox.png)
