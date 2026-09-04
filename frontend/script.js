
let csvData = [];
let chartInstance = null;
let performanceChartInstance = null;


// ========================================
// CSV UPLOAD
// ========================================

document.getElementById("csvFile").addEventListener("change", function (event) {

    const file = event.target.files[0];

    if (!file) {
        return;
    }

    document.getElementById("fileName").textContent =
        "Selected file: " + file.name;

    document.getElementById("loadingMessage").textContent =
        "Loading CSV...";

    const reader = new FileReader();

    reader.onload = function (e) {

        try {

            csvData = parseCSV(e.target.result);

            if (csvData.length === 0) {
                alert("CSV file is empty.");
                return;
            }

            displayTable();
            populateSelectors();
            generateDataInsights();
            generatePerformanceAnalysis();
            generateClassAnalysis();
            generateDataQuality();

            sendToBackend(file);
            sendForAIInsights(file);
            sendForAIRecommendation(file);

            document.getElementById("loadingMessage").textContent =
                "CSV loaded successfully.";

        } catch (error) {

            console.error("CSV error:", error);

            document.getElementById("loadingMessage").textContent =
                "Error loading CSV.";

            alert("There was an error reading the CSV file.");

        }

    };

    reader.readAsText(file);

});


// ========================================
// CSV PARSER
// ========================================

function parseCSV(text) {

    const lines = text.trim().split(/\r?\n/);

    if (lines.length < 2) {
        return [];
    }

    const headers = lines[0].split(",").map(function (header) {
        return header.trim();
    });

    const data = [];

    for (let i = 1; i < lines.length; i++) {

        if (lines[i].trim() === "") {
            continue;
        }

        const values = lines[i].split(",");
        const row = {};

        headers.forEach(function (header, index) {

            row[header] =
                values[index] !== undefined
                    ? values[index].trim()
                    : "";

        });

        data.push(row);

    }

    return data;
}


// ========================================
// DISPLAY TABLE
// ========================================

function displayTable() {

    const container =
        document.getElementById("tableContainer");

    if (!csvData.length) {

        container.innerHTML =
            "<p>No data available.</p>";

        return;
    }

    const headers =
        Object.keys(csvData[0]);

    let html = "<table>";

    html += "<thead><tr>";

    headers.forEach(function (header) {

        html +=
            "<th>" +
            header +
            "</th>";

    });

    html += "</tr></thead>";

    html += "<tbody>";

    csvData.forEach(function (row) {

        html += "<tr>";

        headers.forEach(function (header) {

            html +=
                "<td>" +
                row[header] +
                "</td>";

        });

        html += "</tr>";

    });

    html += "</tbody>";
    html += "</table>";

    container.innerHTML = html;
}


// ========================================
// POPULATE SELECTORS
// ========================================

function populateSelectors() {

    const headers =
        Object.keys(csvData[0]);

    const xColumn =
        document.getElementById("xColumn");

    const yColumn =
        document.getElementById("yColumn");

    const groupColumn =
        document.getElementById("groupColumn");

    xColumn.innerHTML =
        '<option value="">Select X-Axis</option>';

    yColumn.innerHTML =
        '<option value="">Select Y-Axis</option>';

    groupColumn.innerHTML =
        '<option value="">No Grouping</option>';

    headers.forEach(function (header) {

        const xOption =
            document.createElement("option");

        xOption.value = header;
        xOption.textContent = header;

        xColumn.appendChild(xOption);


        const yOption =
            document.createElement("option");

        yOption.value = header;
        yOption.textContent = header;

        yColumn.appendChild(yOption);


        const groupOption =
            document.createElement("option");

        groupOption.value = header;
        groupOption.textContent = header;

        groupColumn.appendChild(groupOption);

    });

    const numericColumn =
        findNumericColumn();

    if (numericColumn) {

        yColumn.value =
            numericColumn;

    }

}


// ========================================
// FIND NUMERIC COLUMN
// ========================================

function findNumericColumn() {

    if (!csvData.length) {
        return null;
    }

    const headers =
        Object.keys(csvData[0]);

    const preferredNames = [
        "marks",
        "mark",
        "score",
        "scores",
        "percentage",
        "percent",
        "points",
        "value",
        "rating"
    ];

    const ignoredNames = [
        "class",
        "grade",
        "section",
        "id",
        "roll",
        "rollno",
        "roll number"
    ];


    for (let i = 0; i < preferredNames.length; i++) {

        for (let j = 0; j < headers.length; j++) {

            const header =
                headers[j].toLowerCase().trim();

            if (header === preferredNames[i]) {
                return headers[j];
            }

        }

    }


    for (let i = 0; i < headers.length; i++) {

        const header =
            headers[i];

        const lowerHeader =
            header.toLowerCase().trim();

        if (ignoredNames.includes(lowerHeader)) {
            continue;
        }

        let numericCount = 0;

        csvData.forEach(function (row) {

            if (
                row[header] !== "" &&
                !isNaN(Number(row[header]))
            ) {

                numericCount++;

            }

        });

        if (numericCount === csvData.length) {
            return header;
        }

    }

    return null;
}


// ========================================
// DATA INSIGHTS
// ========================================

function generateDataInsights() {

    const container =
        document.getElementById("dataInsights");

    const rows =
        csvData.length;

    const columns =
        Object.keys(csvData[0]).length;

    const numericColumn =
        findNumericColumn();

    let average = "N/A";
    let maximum = "N/A";
    let minimum = "N/A";


    if (numericColumn) {

        const values =
            csvData
                .map(function (row) {
                    return Number(row[numericColumn]);
                })
                .filter(function (value) {
                    return !isNaN(value);
                });


        if (values.length > 0) {

            let total = 0;

            values.forEach(function (value) {
                total += value;
            });

            average =
                (total / values.length).toFixed(2);

            maximum =
                Math.max.apply(null, values);

            minimum =
                Math.min.apply(null, values);

        }

    }


    container.innerHTML =

        '<div class="insight-grid">' +

        '<div class="insight-box">' +
        '<h3>Rows</h3>' +
        '<p>' + rows + '</p>' +
        '</div>' +

        '<div class="insight-box">' +
        '<h3>Columns</h3>' +
        '<p>' + columns + '</p>' +
        '</div>' +

        '<div class="insight-box">' +
        '<h3>Numeric Column</h3>' +
        '<p>' +
        (numericColumn || "N/A") +
        '</p>' +
        '</div>' +

        '<div class="insight-box">' +
        '<h3>Average</h3>' +
        '<p>' + average + '</p>' +
        '</div>' +

        '<div class="insight-box">' +
        '<h3>Maximum</h3>' +
        '<p>' + maximum + '</p>' +
        '</div>' +

        '<div class="insight-box">' +
        '<h3>Minimum</h3>' +
        '<p>' + minimum + '</p>' +
        '</div>' +

        '</div>';
}


// ========================================
// PERFORMANCE ANALYSIS
// ========================================

function generatePerformanceAnalysis() {

    const container =
        document.getElementById("performanceAnalysis");

    const scoreColumn =
        findNumericColumn();

    if (!scoreColumn) {

        container.innerHTML =
            "<p>No score column detected.</p>";

        return;
    }


    let excellent = 0;
    let good = 0;
    let average = 0;
    let needsImprovement = 0;


    csvData.forEach(function (row) {

        const score =
            Number(row[scoreColumn]);

        if (isNaN(score)) {
            return;
        }

        if (score >= 90) {

            excellent++;

        } else if (score >= 75) {

            good++;

        } else if (score >= 60) {

            average++;

        } else {

            needsImprovement++;

        }

    });


    let largestGroup = "Excellent";
    let largestValue = excellent;


    if (good > largestValue) {

        largestGroup = "Good";
        largestValue = good;

    }


    if (average > largestValue) {

        largestGroup = "Average";
        largestValue = average;

    }


    if (needsImprovement > largestValue) {

        largestGroup = "Needs Improvement";
        largestValue = needsImprovement;

    }


    container.innerHTML =

        '<div class="performance-grid">' +

        '<div class="performance-box">' +
        '<h3>Excellent</h3>' +
        '<p>' + excellent + '</p>' +
        '<small>90 and above</small>' +
        '</div>' +

        '<div class="performance-box">' +
        '<h3>Good</h3>' +
        '<p>' + good + '</p>' +
        '<small>75 - 89</small>' +
        '</div>' +

        '<div class="performance-box">' +
        '<h3>Average</h3>' +
        '<p>' + average + '</p>' +
        '<small>60 - 74</small>' +
        '</div>' +

        '<div class="performance-box">' +
        '<h3>Needs Improvement</h3>' +
        '<p>' + needsImprovement + '</p>' +
        '<small>Below 60</small>' +
        '</div>' +

        '</div>' +

        '<p><strong>Largest group:</strong> ' +
        largestGroup +
        '</p>';


    createPerformanceChart(
        excellent,
        good,
        average,
        needsImprovement
    );
}


// ========================================
// PERFORMANCE CHART
// ========================================

function createPerformanceChart(
    excellent,
    good,
    average,
    needsImprovement
) {

    const canvas =
        document.getElementById("performanceChart");

    if (!canvas) {
        return;
    }

    if (performanceChartInstance) {

        performanceChartInstance.destroy();

    }


    performanceChartInstance =
        new Chart(
            canvas.getContext("2d"),
            {

                type: "bar",

                data: {

                    labels: [
                        "Excellent",
                        "Good",
                        "Average",
                        "Needs Improvement"
                    ],

                    datasets: [
                        {

                            label: "Students",

                            data: [
                                excellent,
                                good,
                                average,
                                needsImprovement
                            ]

                        }
                    ]

                },

                options: {

                    responsive: true,

                    scales: {

                        y: {

                            beginAtZero: true,

                            ticks: {
                                precision: 0
                            }

                        }

                    }

                }

            }
        );
}


// ========================================
// CLASS-WISE ANALYSIS
// ========================================

function generateClassAnalysis() {

    const container =
        document.getElementById("classAnalysis");

    const headers =
        Object.keys(csvData[0]);

    let classColumn = null;


    headers.forEach(function (header) {

        const name =
            header.toLowerCase().trim();

        if (
            name === "class" ||
            name === "grade" ||
            name === "section"
        ) {

            if (!classColumn) {
                classColumn = header;
            }

        }

    });


    const scoreColumn =
        findNumericColumn();


    if (!classColumn || !scoreColumn) {

        container.innerHTML =
            "<p>Class-wise analysis is not available.</p>";

        return;
    }


    const groups = {};


    csvData.forEach(function (row) {

        const group =
            row[classColumn];

        const score =
            Number(row[scoreColumn]);


        if (!groups[group]) {
            groups[group] = [];
        }


        if (!isNaN(score)) {
            groups[group].push(score);
        }

    });


    let html =
        '<div class="class-analysis-grid">';


    Object.keys(groups).forEach(
        function (group) {

            const values =
                groups[group];

            if (values.length === 0) {
                return;
            }


            let total = 0;

            values.forEach(function (value) {
                total += value;
            });


            const avg =
                (
                    total /
                    values.length
                ).toFixed(2);


            const highest =
                Math.max.apply(null, values);


            const lowest =
                Math.min.apply(null, values);


            html +=

                '<div class="class-box">' +

                '<h3>Class ' +
                group +
                '</h3>' +

                '<p><strong>Students:</strong> ' +
                values.length +
                '</p>' +

                '<p><strong>Average:</strong> ' +
                avg +
                '</p>' +

                '<p><strong>Highest:</strong> ' +
                highest +
                '</p>' +

                '<p><strong>Lowest:</strong> ' +
                lowest +
                '</p>' +

                '</div>';

        }
    );


    html += '</div>';

    container.innerHTML =
        html;
}


// ========================================
// DATA QUALITY
// ========================================

function generateDataQuality() {

    const container =
        document.getElementById("dataQuality");

    const headers =
        Object.keys(csvData[0]);

    let missingValues = 0;


    csvData.forEach(function (row) {

        headers.forEach(function (header) {

            const value =
                row[header];

            if (
                value === undefined ||
                value === null ||
                String(value).trim() === ""
            ) {

                missingValues++;

            }

        });

    });


    const uniqueRows =
        new Set(
            csvData.map(function (row) {
                return JSON.stringify(row);
            })
        ).size;


    const duplicateRows =
        csvData.length -
        uniqueRows;


    container.innerHTML =

        '<div class="quality-grid">' +

        '<div class="quality-box">' +
        '<h3>Missing Values</h3>' +
        '<p>' + missingValues + '</p>' +
        '</div>' +

        '<div class="quality-box">' +
        '<h3>Duplicate Rows</h3>' +
        '<p>' + duplicateRows + '</p>' +
        '</div>' +

        '</div>';
}


// ========================================
// BACKEND ANALYSIS
// ========================================

function sendToBackend(file) {

    const formData =
        new FormData();

    formData.append("file", file);


    fetch(
        "http://127.0.0.1:5000/api/analyze",
        {
            method: "POST",
            body: formData
        }
    )

        .then(function (response) {
            return response.json();
        })

        .then(function (result) {

            console.log(
                "Backend analysis:",
                result
            );

        })

        .catch(function (error) {

            console.error(
                "Backend error:",
                error
            );

        });

}


// ========================================
// AI INSIGHTS
// ========================================

function sendForAIInsights(file) {

    const container =
        document.getElementById("aiInsights");

    container.innerHTML =
        "<p>AI is analyzing your data...</p>";


    const formData =
        new FormData();

    formData.append("file", file);


    fetch(
        "http://127.0.0.1:5000/api/ai-insights",
        {
            method: "POST",
            body: formData
        }
    )

        .then(function (response) {
            return response.json();
        })

        .then(function (result) {

            if (
                result.status === "success" &&
                result.insights
            ) {

                container.innerHTML =
                    formatAIText(
                        result.insights
                    );

            } else {

                container.innerHTML =
                    "<p>AI insights could not be generated.</p>";

            }

        })

        .catch(function (error) {

            console.error(
                "AI insights error:",
                error
            );

            container.innerHTML =
                "<p>AI service is unavailable.</p>";

        });

}


// ========================================
// FORMAT AI TEXT
// ========================================

function formatAIText(text) {

    if (!text) {
        return "";
    }

    let formatted =
        String(text);

    formatted =
        formatted.split("**").join("");

    formatted =
        formatted.split("\\*\\*").join("");

    formatted =
        formatted.split("\\n").join("<br>");

    formatted =
        formatted.split("\n").join("<br>");

    return formatted;
}


// ========================================
// AI CHART RECOMMENDATION
// ========================================

function sendForAIRecommendation(file) {

    const container =
        document.getElementById("aiRecommendation");

    container.innerHTML =
        "<p>AI is choosing the best chart...</p>";


    const formData =
        new FormData();

    formData.append("file", file);


    fetch(
        "http://127.0.0.1:5000/api/ai-recommendation",
        {
            method: "POST",
            body: formData
        }
    )

        .then(function (response) {
            return response.json();
        })

        .then(function (result) {

            if (result.status === "success") {

                let html = "";

                if (result.chart_type) {

                    html +=
                        "<h3>Recommended Chart: " +
                        result.chart_type +
                        "</h3>";

                }

                if (result.reason) {

                    html +=
                        "<p>" +
                        result.reason +
                        "</p>";

                }

                container.innerHTML =
                    html;

            } else {

                container.innerHTML =
                    "<p>AI recommendation unavailable.</p>";

            }

        })

        .catch(function (error) {

            console.error(
                "AI recommendation error:",
                error
            );

            container.innerHTML =
                "<p>AI recommendation service is unavailable.</p>";

        });

}


// ========================================
// GENERATE CHART
// ========================================

document
    .getElementById("generateBtn")
    .addEventListener(
        "click",
        function () {

            if (!csvData.length) {

                alert(
                    "Please upload a CSV file first."
                );

                return;

            }


            const xColumn =
                document.getElementById(
                    "xColumn"
                ).value;


            const yColumn =
                document.getElementById(
                    "yColumn"
                ).value;


            const groupColumn =
                document.getElementById(
                    "groupColumn"
                ).value;


            const chartType =
                document.getElementById(
                    "chartType"
                ).value;


            const title =
                document.getElementById(
                    "chartTitle"
                ).value ||
                "Simple Chartbox";


            const xAxisLabel =
                document.getElementById(
                    "xAxisLabel"
                ).value ||
                xColumn;


            const yAxisLabel =
                document.getElementById(
                    "yAxisLabel"
                ).value ||
                yColumn;


            const color =
                document.getElementById(
                    "chartColor"
                ).value;


            if (!xColumn || !yColumn) {

                alert(
                    "Please select X-Axis and Y-Axis."
                );

                return;

            }


            if (groupColumn) {

                generateGroupedCharts(
                    xColumn,
                    yColumn,
                    groupColumn,
                    chartType,
                    title,
                    xAxisLabel,
                    yAxisLabel,
                    color
                );

                return;

            }


            const labels =
                csvData.map(function (row) {

                    return row[xColumn];

                });


            const values =
                csvData.map(function (row) {

                    const value =
                        Number(row[yColumn]);

                    return isNaN(value)
                        ? 0
                        : value;

                });


            const placeholder =
                document.getElementById(
                    "chartPlaceholder"
                );


            const container =
                document.getElementById(
                    "chartContainer"
                );


            if (chartInstance) {

                chartInstance.destroy();

                chartInstance = null;

            }


            container.innerHTML =
                '<canvas id="chart"></canvas>';


            placeholder.style.display =
                "none";


            const canvas =
                document.getElementById(
                    "chart"
                );


            chartInstance =
                new Chart(
                    canvas.getContext("2d"),
                    {

                        type: chartType,

                        data: {

                            labels: labels,

                            datasets: [

                                {

                                    label:
                                        yAxisLabel,

                                    data:
                                        values,

                                    backgroundColor:
                                        color,

                                    borderColor:
                                        color,

                                    borderWidth: 2

                                }

                            ]

                        },

                        options: {

                            responsive: true,

                            maintainAspectRatio: false,

                            plugins: {

                                title: {

                                    display: true,

                                    text: title

                                },

                                legend: {

                                    display:
                                        chartType === "pie"

                                }

                            },

                            scales:
                                chartType === "pie"
                                    ? {}
                                    : {

                                        x: {

                                            title: {

                                                display: true,

                                                text:
                                                    xAxisLabel

                                            }

                                        },

                                        y: {

                                            beginAtZero: true,

                                            title: {

                                                display: true,

                                                text:
                                                    yAxisLabel

                                            }

                                        }

                                    }

                        }

                    }
                );

        }
    );


// ========================================
// GROUPED CHARTS
// ========================================
function generateGroupedCharts(
    xColumn,
    yColumn,
    groupColumn,
    chartType,
    title,
    xAxisLabel,
    yAxisLabel,
    color
) {

    const placeholder =
        document.getElementById("chartPlaceholder");

    const container =
        document.getElementById("chartContainer");

    placeholder.style.display = "none";

    container.innerHTML = "";

    const groups = {};

    csvData.forEach(function (row) {

        const group = row[groupColumn];

        if (!groups[group]) {
            groups[group] = [];
        }

        groups[group].push(row);

    });

    Object.keys(groups).forEach(function (group) {

        const wrapper =
            document.createElement("div");

        wrapper.className =
            "group-chart-card";

        const heading =
            document.createElement("h3");

        heading.textContent =
            title + " - " + group;

        const canvas =
            document.createElement("canvas");

        canvas.style.width = "100%";
        canvas.style.height = "400px";

        const downloadButton =
            document.createElement("button");

        downloadButton.textContent =
            "Download " + group + " PNG";

        downloadButton.style.marginTop = "15px";

        wrapper.appendChild(heading);
        wrapper.appendChild(canvas);
        wrapper.appendChild(downloadButton);

        container.appendChild(wrapper);

        const labels =
            groups[group].map(function (row) {
                return row[xColumn];
            });

        const values =
            groups[group].map(function (row) {

                const value =
                    Number(row[yColumn]);

                return isNaN(value)
                    ? 0
                    : value;

            });

        const groupedChart =
            new Chart(
                canvas.getContext("2d"),
                {

                    type: chartType,

                    data: {

                        labels: labels,

                        datasets: [
                            {

                                label: yAxisLabel,

                                data: values,

                                backgroundColor: color,

                                borderColor: color,

                                borderWidth: 2

                            }
                        ]

                    },

                    options: {

                        responsive: true,

                        maintainAspectRatio: false,

                        plugins: {

                            title: {

                                display: true,

                                text:
                                    title +
                                    " - " +
                                    group

                            }

                        },

                        scales:
                            chartType === "pie"
                                ? {}
                                : {

                                    x: {

                                        title: {

                                            display: true,

                                            text:
                                                xAxisLabel

                                        }

                                    },

                                    y: {

                                        beginAtZero: true,

                                        title: {

                                            display: true,

                                            text:
                                                yAxisLabel

                                        }

                                    }

                                }

                    }

                }
            );

        downloadButton.addEventListener(
            "click",
            function () {

                const image =
                    groupedChart.toBase64Image();

                const link =
                    document.createElement("a");

                link.href = image;

                link.download =
                    "simple-chartbox-" +
                    String(group) +
                    ".png";

                link.click();

            }
        );

    });

}
// ========================================
// DOWNLOAD PNG
// ========================================

document
    .getElementById("downloadBtn")
    .addEventListener(
        "click",
        function () {

            const canvas =
                document.getElementById(
                    "chart"
                );


            if (!canvas) {

                alert(
                    "Please generate a chart first."
                );

                return;

            }


            try {

                const image =
                    canvas.toDataURL(
                        "image/png"
                    );


                const link =
                    document.createElement(
                        "a"
                    );


                link.href =
                    image;


                link.download =
                    "simple-chartbox-chart.png";


                document.body.appendChild(
                    link
                );


                link.click();


                document.body.removeChild(
                    link
                );


            } catch (error) {

                console.error(
                    "Download error:",
                    error
                );

                alert(
                    "Unable to download the chart."
                );

            }

        }
    );

