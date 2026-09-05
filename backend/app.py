from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import requests
import os

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Simple Chartbox Backend is Running!"


@app.route("/api/test")
def test():
    return jsonify({
        "status": "success",
        "message": "Backend API is working!"
    })


@app.route("/api/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "status": "error",
            "message": "No file selected."
        }), 400

    try:
        df = pd.read_csv(file)

        return jsonify({
            "status": "success",
            "message": "File uploaded successfully.",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=["number"]
        ).columns.tolist()

        statistics = {}

        for column in numeric_columns:
            statistics[column] = {
                "mean": float(df[column].mean()),
                "max": float(df[column].max()),
                "min": float(df[column].min())
            }

        primary_numeric_column = (
            numeric_columns[0]
            if numeric_columns
            else None
        )

        primary_statistics = (
            statistics[primary_numeric_column]
            if primary_numeric_column
            else {}
        )

        return jsonify({
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "missing_values": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "statistics": statistics,
            "primary_numeric_column": primary_numeric_column,
            "primary_statistics": primary_statistics
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/class-analysis", methods=["POST"])
def class_analysis():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        class_column = None

        possible_class_columns = [
            "Class",
            "class",
            "Grade",
            "grade",
            "Section",
            "section"
        ]

        for column in possible_class_columns:
            if column in df.columns:
                class_column = column
                break

        if class_column is None:
            return jsonify({
                "status": "success",
                "classes": []
            })

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        score_column = None

        possible_score_columns = [
            "Marks",
            "marks",
            "Score",
            "score",
            "Percentage",
            "percentage"
        ]

        for column in possible_score_columns:
            if column in df.columns:
                score_column = column
                break

        if score_column is None and numeric_columns:
            for column in numeric_columns:
                if column != class_column:
                    score_column = column
                    break

        if score_column is None:
            return jsonify({
                "status": "success",
                "classes": []
            })

        results = []

        for class_name, group in df.groupby(class_column):
            scores = pd.to_numeric(
                group[score_column],
                errors="coerce"
            ).dropna()

            if len(scores) == 0:
                continue

            results.append({
                "class": str(class_name),
                "students": int(len(scores)),
                "average": float(scores.mean()),
                "highest": float(scores.max()),
                "lowest": float(scores.min())
            })

        return jsonify({
            "status": "success",
            "classes": results
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/performance-analysis", methods=["POST"])
def performance_analysis():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        score_column = None

        possible_score_columns = [
            "Marks",
            "marks",
            "Score",
            "score",
            "Percentage",
            "percentage"
        ]

        for column in possible_score_columns:
            if column in df.columns:
                score_column = column
                break

        if score_column is None and numeric_columns:
            score_column = numeric_columns[-1]

        if score_column is None:
            return jsonify({
                "status": "success",
                "distribution": {}
            })

        scores = pd.to_numeric(
            df[score_column],
            errors="coerce"
        ).dropna()

        distribution = {
            "Excellent": int((scores >= 90).sum()),
            "Good": int(((scores >= 75) & (scores < 90)).sum()),
            "Average": int(((scores >= 60) & (scores < 75)).sum()),
            "Needs Improvement": int((scores < 60).sum())
        }

        largest_group = max(
            distribution,
            key=distribution.get
        )

        return jsonify({
            "status": "success",
            "distribution": distribution,
            "largest_group": largest_group
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


def generate_ollama_response(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gpt-oss:20b",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        if response.status_code != 200:
            raise Exception(
                "Ollama API error: " + response.text
            )

        data = response.json()

        return data.get("response", "")

    except Exception as e:
        raise Exception(str(e))


@app.route("/api/ai-insights", methods=["POST"])
def ai_insights():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=["number"]
        ).columns.tolist()

        statistics = {}

        for column in numeric_columns:
            statistics[column] = {
                "average": round(
                    float(df[column].mean()), 2
                ),
                "maximum": float(df[column].max()),
                "minimum": float(df[column].min())
            }

        prompt = (
            "Analyze this CSV dataset briefly.\n\n"
            "Rows: "
            + str(len(df))
            + "\nColumns: "
            + str(df.columns.tolist())
            + "\nNumeric columns: "
            + str(numeric_columns)
            + "\nCategorical columns: "
            + str(categorical_columns)
            + "\nStatistics: "
            + str(statistics)
            + "\n\nGive 3 short useful insights."
        )

        result = generate_ollama_response(prompt)

        return jsonify({
            "status": "success",
            "insights": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/ai-recommendation", methods=["POST"])
def ai_recommendation():
    if "file" not in request.files:
        return jsonify({
            "status": "error",
            "message": "No file uploaded."
        }), 400

    file = request.files["file"]

    try:
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=["number"]
        ).columns.tolist()

        prompt = (
            "Recommend the best chart for this CSV dataset.\n\n"
    "Columns: "
    + str(df.columns.tolist())
    + "\nNumeric columns: "
    + str(numeric_columns)
    + "\nCategorical columns: "
    + str(categorical_columns)
    + "\n\n"
    "Important rules:\n"
    "1. Do not use a column as a comparison variable if it has the same value in every row.\n"
    "2. For a categorical column such as Student and a numeric column such as Marks, recommend Bar.\n"
    "3. For two numeric columns showing a relationship, recommend Scatter.\n"
    "4. For values changing over an ordered sequence, recommend Line.\n"
    "5. For parts of a meaningful total, recommend Pie.\n\n"
    "Choose only one from: Bar, Line, Pie, Scatter.\n"
    "Respond exactly in this format:\n"
    "Chart: <chart name>\n"
    "Reason: <short reason>"

        )

        result = generate_ollama_response(prompt)

        chart_name = "Bar"
        reason = result

        lines = result.splitlines()

        for line in lines:
            if line.lower().startswith("chart:"):
                chart_name = line.split(
                    ":", 1
                )[1].strip()

            if line.lower().startswith("reason:"):
                reason = line.split(
                    ":", 1
                )[1].strip()

        return jsonify({
            "status": "success",
            "chart": chart_name,
            "reason": reason
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )