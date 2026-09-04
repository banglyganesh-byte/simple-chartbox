from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests

app = Flask(__name__)
CORS(app)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():
    return "Simple Chartbox Backend is Running!"


# --------------------------------------------------
# TEST API
# --------------------------------------------------

@app.route("/api/test")
def test():
    return jsonify({
        "status": "success",
        "message": "Backend API is working!"
    })


# --------------------------------------------------
# UPLOAD API
# --------------------------------------------------

@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No file selected"
        }), 400

    try:
        df = pd.read_csv(file)

        return jsonify({
            "status": "success",
            "message": "CSV uploaded successfully",
            "rows": len(df),
            "columns": list(df.columns)
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# --------------------------------------------------
# ANALYZE DATA
# --------------------------------------------------

@app.route("/api/analyze", methods=["POST"])
def analyze():

    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude="number"
        ).columns.tolist()

        missing_values = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        statistics = {}

        for column in numeric_columns:
            statistics[column] = {
                "average": float(df[column].mean()),
                "minimum": float(df[column].min()),
                "maximum": float(df[column].max())
            }

        score_column = None

        for column in numeric_columns:
            name = column.lower()

            if (
                "mark" in name
                or "score" in name
                or "percentage" in name
                or "point" in name
            ):
                score_column = column
                break

        if score_column is None and len(numeric_columns) > 0:
            score_column = numeric_columns[-1]

        primary_statistics = None

        if score_column:
            primary_statistics = statistics[score_column]

        return jsonify({
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "statistics": statistics,
            "primary_numeric_column": score_column,
            "primary_statistics": primary_statistics
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# --------------------------------------------------
# CLASS ANALYSIS
# --------------------------------------------------

@app.route("/api/class-analysis", methods=["POST"])
def class_analysis():

    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        class_column = None

        for column in df.columns:
            name = column.lower()

            if (
                "class" in name
                or "grade" in name
                or "section" in name
            ):
                class_column = column
                break

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        score_column = None

        for column in numeric_columns:
            name = column.lower()

            if (
                "mark" in name
                or "score" in name
                or "percentage" in name
            ):
                score_column = column
                break

        if score_column is None and numeric_columns:
            score_column = numeric_columns[-1]

        if class_column is None or score_column is None:
            return jsonify({
                "status": "success",
                "available": False,
                "message": "Class or score column not found"
            })

        result = []

        grouped = df.groupby(class_column)

        for class_name, group in grouped:

            scores = group[score_column].dropna()

            result.append({
                "class": str(class_name),
                "students": int(len(scores)),
                "average": round(float(scores.mean()), 2),
                "highest": float(scores.max()),
                "lowest": float(scores.min())
            })

        return jsonify({
            "status": "success",
            "available": True,
            "class_column": class_column,
            "score_column": score_column,
            "classes": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# --------------------------------------------------
# PERFORMANCE ANALYSIS
# --------------------------------------------------

@app.route("/api/performance-analysis", methods=["POST"])
def performance_analysis():

    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        score_column = None

        for column in numeric_columns:
            name = column.lower()

            if (
                "mark" in name
                or "score" in name
                or "percentage" in name
            ):
                score_column = column
                break

        if score_column is None and numeric_columns:
            score_column = numeric_columns[-1]

        if score_column is None:
            return jsonify({
                "status": "error",
                "message": "No numeric score column found"
            }), 400

        scores = df[score_column].dropna()

        excellent = int((scores >= 90).sum())

        good = int(
            ((scores >= 75) & (scores < 90)).sum()
        )

        average = int(
            ((scores >= 60) & (scores < 75)).sum()
        )

        needs_improvement = int(
            (scores < 60).sum()
        )

        distribution = {
            "Excellent": excellent,
            "Good": good,
            "Average": average,
            "Needs Improvement": needs_improvement
        }

        largest_group = max(
            distribution,
            key=distribution.get
        )

        return jsonify({
            "status": "success",
            "score_column": score_column,
            "total_students": int(len(scores)),
            "distribution": distribution,
            "largest_group": largest_group
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

@app.route("/api/ai-insights", methods=["POST"])
def ai_insights():

    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        numeric_statistics = {}

        for column in numeric_columns:
            numeric_statistics[column] = {
                "average": round(float(df[column].mean()), 2),
                "minimum": float(df[column].min()),
                "maximum": float(df[column].max())
            }

        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "missing_values": int(
                df.isnull().sum().sum()
            ),
            "duplicate_rows": int(
                df.duplicated().sum()
            ),
            "numeric_statistics": numeric_statistics
        }

        prompt = """
You are a data analysis assistant.

Analyze the following dataset summary.

Give exactly 4 short and useful insights.

Focus on:
1. Overall performance or important numerical patterns
2. Differences or relationships between columns
3. Data quality
4. Unusual or important observations

Use only the information provided.

Do not invent facts.

Keep the answer concise.

Dataset summary:
""" + str(summary)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gpt-oss:20b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        result = response.json()

        ai_response = result.get(
            "response",
            "AI could not generate insights."
        )

        return jsonify({
            "status": "success",
            "insights": ai_response
        })

    except requests.exceptions.ConnectionError:

        return jsonify({
            "status": "error",
            "message": "Ollama is not running."
        }), 500

    except requests.exceptions.Timeout:

        return jsonify({
            "status": "error",
            "message": "AI analysis took too long."
        }), 500

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# --------------------------------------------------
# AI CHART RECOMMENDATION
# --------------------------------------------------

@app.route("/api/ai-recommendation", methods=["POST"])
def ai_recommendation():

    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded"
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude="number"
        ).columns.tolist()

        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns
        }

        prompt = """
You are a data visualization expert.

Look at the dataset structure below.

Recommend the BEST chart type for this dataset.

Allowed chart types:
- Bar
- Line
- Pie
- Scatter

Return your answer in exactly this format:

CHART: Bar
REASON: Compare categories with numerical values.

Rules:
- Choose only ONE chart.
- Use Bar for category comparisons.
- Use Line for trends or ordered data.
- Use Pie for part-to-whole proportions.
- Use Scatter when two numerical variables should be compared.
- Do not invent columns.
- Keep the reason to one short sentence.

Dataset:
""" + str(summary)

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gpt-oss:20b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        result = response.json()

        ai_response = result.get(
            "response",
            ""
        ).strip()

        recommended_chart = "Bar"
        reason = "A bar chart is suitable for comparing categories and numerical values."

        lines = ai_response.splitlines()

        for line in lines:

            clean_line = line.strip()

            if clean_line.upper().startswith("CHART:"):

                chart_name = clean_line.split(
                    ":", 1
                )[1].strip()

                chart_name_lower = chart_name.lower()

                if chart_name_lower == "bar":
                    recommended_chart = "Bar"

                elif chart_name_lower == "line":
                    recommended_chart = "Line"

                elif chart_name_lower == "pie":
                    recommended_chart = "Pie"

                elif chart_name_lower == "scatter":
                    recommended_chart = "Scatter"

            elif clean_line.upper().startswith("REASON:"):

                reason = clean_line.split(
                    ":",
                    1
                )[1].strip()

        return jsonify({
            "status": "success",
            "chart": recommended_chart,
            "reason": reason,
            "raw_response": ai_response
        })

    except requests.exceptions.ConnectionError:

        return jsonify({
            "status": "error",
            "message": "Ollama is not running."
        }), 500

    except requests.exceptions.Timeout:

        return jsonify({
            "status": "error",
            "message": "AI recommendation took too long."
        }), 500

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))