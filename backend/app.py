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
def upload_file():
    try:
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

        df = pd.read_csv(file)

        return jsonify({
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist()
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/analyze", methods=["POST"])
def analyze_data():
    try:
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded."
            }), 400

        file = request.files["file"]
        df = pd.read_csv(file)

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            exclude=["number"]
        ).columns.tolist()

        missing_values = int(df.isnull().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        statistics = {}

        if numeric_columns:
            statistics = df[numeric_columns].describe().to_dict()

        primary_numeric_column = None
        primary_statistics = {}

        if numeric_columns:
            primary_numeric_column = numeric_columns[0]

            column = df[primary_numeric_column].dropna()

            if len(column) > 0:
                primary_statistics = {
                    "mean": float(column.mean()),
                    "max": float(column.max()),
                    "min": float(column.min())
                }

        return jsonify({
            "status": "success",
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "numeric_columns": numeric_columns,
            "categorical_columns": categorical_columns,
            "missing_values": missing_values,
            "duplicate_rows": duplicate_rows,
            "statistics": statistics,
            "primary_numeric_column": primary_numeric_column,
            "primary_statistics": primary_statistics
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/class-analysis", methods=["POST"])
def class_analysis():
    try:
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded."
            }), 400

        file = request.files["file"]
        df = pd.read_csv(file)

        class_column = None
        score_column = None

        for column in df.columns:
            name = column.lower()

            if name in ["class", "grade", "section"]:
                class_column = column

        for column in df.columns:
            name = column.lower()

            if name in [
                "marks",
                "mark",
                "score",
                "scores",
                "percentage",
                "attendance"
            ]:
                if pd.api.types.is_numeric_dtype(df[column]):
                    score_column = column
                    break

        if class_column is None or score_column is None:
            return jsonify({
                "status": "success",
                "classes": []
            })

        classes = []

        for class_name, group in df.groupby(class_column):
            scores = pd.to_numeric(
                group[score_column],
                errors="coerce"
            ).dropna()

            if len(scores) == 0:
                continue

            classes.append({
                "class": str(class_name),
                "students": int(len(scores)),
                "average": float(scores.mean()),
                "highest": float(scores.max()),
                "lowest": float(scores.min())
            })

        return jsonify({
            "status": "success",
            "classes": classes
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/performance-analysis", methods=["POST"])
def performance_analysis():
    try:
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded."
            }), 400

        file = request.files["file"]
        df = pd.read_csv(file)

        score_column = None

        for column in df.columns:
            name = column.lower()

            if name in [
                "marks",
                "mark",
                "score",
                "scores",
                "percentage"
            ]:
                if pd.api.types.is_numeric_dtype(df[column]):
                    score_column = column
                    break

        if score_column is None:
            return jsonify({
                "status": "success",
                "distribution": {},
                "largest_group": None
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

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


def generate_gemini_response(prompt):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise Exception("GEMINI_API_KEY is not configured.")

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key="
        + api_key,
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        },
        timeout=120
    )

    if not response.ok:
        print("Gemini API error:", response.status_code)
        print("Gemini API response:", response.text)

        raise Exception(
            "Gemini API error: "
            + str(response.status_code)
            + " "
            + response.text
        )

    result = response.json()

    candidates = result.get("candidates", [])

    if not candidates:
        raise Exception("Gemini returned no response.")

    content = candidates[0].get("content", {})
    parts = content.get("parts", [])

    if not parts:
        raise Exception("Gemini returned an empty response.")

    return parts[0].get(
        "text",
        "AI could not generate a response."
    ).strip()
@app.route("/api/ai-insights", methods=["POST"])
def ai_insights():
    try:
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded."
            }), 400

        file = request.files["file"]
        df = pd.read_csv(file)

        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "numeric_columns": df.select_dtypes(
                include=["number"]
            ).columns.tolist(),
            "categorical_columns": df.select_dtypes(
                exclude=["number"]
            ).columns.tolist(),
            "missing_values": int(
                df.isnull().sum().sum()
            ),
            "duplicate_rows": int(
                df.duplicated().sum()
            )
        }

        numeric_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        for column in numeric_columns:
            values = pd.to_numeric(
                df[column],
                errors="coerce"
            ).dropna()

            if len(values) > 0:
                summary[column] = {
                    "average": round(float(values.mean()), 2),
                    "minimum": float(values.min()),
                    "maximum": float(values.max())
                }

        prompt = (
            "Analyze this dataset and provide useful insights for a user "
            "using a chart creation application.\n\n"
            "Give a concise response with:\n"
            "1. Main patterns\n"
            "2. Important statistics\n"
            "3. Any unusual observations\n"
            "4. One useful recommendation\n\n"
            "Dataset summary:\n"
            + str(summary)
        )

        ai_response = generate_gemini_response(prompt)

        return jsonify({
            "status": "success",
            "insights": ai_response
        })

    except requests.exceptions.RequestException as error:
        return jsonify({
            "status": "error",
            "message": "Gemini API request failed: " + str(error)
        }), 500

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/api/ai-recommendation", methods=["POST"])
def ai_recommendation():
    try:
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded."
            }), 400

        file = request.files["file"]
        df = pd.read_csv(file)

        summary = {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "numeric_columns": df.select_dtypes(
                include=["number"]
            ).columns.tolist(),
            "categorical_columns": df.select_dtypes(
                exclude=["number"]
            ).columns.tolist()
        }

        prompt = (
            "Analyze this dataset and recommend the best chart type.\n\n"
            "Choose ONLY one of these chart types:\n"
            "Bar\n"
            "Line\n"
            "Pie\n"
            "Scatter\n\n"
            "Respond in this format:\n"
            "Chart: <chart type>\n"
            "Reason: <short reason>\n\n"
            "Dataset summary:\n"
            + str(summary)
        )

        ai_response = generate_gemini_response(prompt)

        recommended_chart = "Bar"
        reason = (
            "A bar chart is suitable for comparing categories "
            "and numerical values."
        )

        lines = ai_response.splitlines()

        for line in lines:
            clean_line = line.strip()

            lower_line = clean_line.lower()

            if lower_line.startswith("chart:"):
                chart_value = clean_line.split(
                    ":",
                    1
                )[1].strip().lower()

                if chart_value == "bar":
                    recommended_chart = "Bar"

                elif chart_value == "line":
                    recommended_chart = "Line"

                elif chart_value == "pie":
                    recommended_chart = "Pie"

                elif chart_value == "scatter":
                    recommended_chart = "Scatter"

            elif lower_line.startswith("reason:"):
                reason = clean_line.split(
                    ":",
                    1
                )[1].strip()

        return jsonify({
            "status": "success",
            "chart": recommended_chart,
            "reason": reason
        })

    except requests.exceptions.RequestException as error:
        return jsonify({
            "status": "error",
            "message": "Gemini API request failed: " + str(error)
        }), 500

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )