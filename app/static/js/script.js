document.addEventListener("DOMContentLoaded", () => {

    // =====================================================
    // DOM ELEMENTS
    // =====================================================

    const form = document.getElementById("smsForm");

    const messageInput = document.getElementById("message");

    const clearBtn = document.getElementById("clearBtn");

    const loading = document.getElementById("loading");

    const resultCard = document.getElementById("resultCard");

    const predictionBadge = document.getElementById("predictionBadge");

    const confidence = document.getElementById("confidence");

    const spamProbability = document.getElementById("spamProbability");

    const hamProbability = document.getElementById("hamProbability");

    const riskLevel = document.getElementById("riskLevel");

    const spamBar = document.getElementById("spamBar");

    const hamBar = document.getElementById("hamBar");

    const spamPercent = document.getElementById("spamPercent");

    const hamPercent = document.getElementById("hamPercent");

    const keywordsContainer = document.getElementById("keywordsContainer");

    const originalMessage = document.getElementById("originalMessage");


    // =====================================================
    // HELPER FUNCTIONS
    // =====================================================

    function showLoading() {

        loading.classList.remove("hidden");

        resultCard.classList.add("hidden");

    }


    function hideLoading() {

        loading.classList.add("hidden");

    }


    function resetResult() {

        predictionBadge.textContent = "Waiting...";

        predictionBadge.className = "prediction-badge";

        confidence.textContent = "0%";

        spamProbability.textContent = "0%";

        hamProbability.textContent = "0%";

        riskLevel.textContent = "Low";

        riskLevel.className = "";

        spamBar.style.width = "0%";

        hamBar.style.width = "0%";

        spamPercent.textContent = "0%";

        hamPercent.textContent = "0%";

        keywordsContainer.innerHTML =
            '<span class="keyword">None Detected</span>';

        originalMessage.textContent = "";

    }


    function updateRiskStyle(level) {

        riskLevel.classList.remove(

            "risk-low",

            "risk-medium",

            "risk-high",

            "risk-critical"

        );

        switch (level) {

            case "Critical":

                riskLevel.classList.add("risk-critical");

                break;

            case "High":

                riskLevel.classList.add("risk-high");

                break;

            case "Medium":

                riskLevel.classList.add("risk-medium");

                break;

            default:

                riskLevel.classList.add("risk-low");

        }

    }


    function updatePredictionBadge(label) {

        predictionBadge.classList.remove(

            "badge-safe",

            "badge-spam"

        );

        predictionBadge.textContent = label;

        if (label === "Spam") {

            predictionBadge.classList.add("badge-spam");

        } else {

            predictionBadge.classList.add("badge-safe");

        }

    }


    function updateKeywords(words) {

        keywordsContainer.innerHTML = "";

        if (!words || words.length === 0) {

            keywordsContainer.innerHTML =
                '<span class="keyword">None Detected</span>';

            return;

        }

        words.forEach(word => {

            const badge = document.createElement("span");

            badge.className = "keyword";

            badge.textContent = word;

            keywordsContainer.appendChild(badge);

        });

    }


    // =====================================================
    // FORM SUBMIT
    // =====================================================

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const message = messageInput.value.trim();

        if (message.length > 500) {

    alert("SMS message must not exceed 500 characters.");

    return;

}

        if (message.length === 0) {

            alert("Please enter an SMS message.");

            return;

        }

        showLoading();

        try {

            const response = await fetch("/predict", {

                method: "POST",

                headers: {

                    "Content-Type": "application/json"

                },

                body: JSON.stringify({

                    message: message

                })

            });

            const data = await response.json();

            hideLoading();

            /* Handle HTTP errors */
            if (!response.ok) {

            alert(data.error || "Prediction failed.");

            resultCard.classList.add("hidden");

            return;

            }

/* Handle application errors returned by Flask */
            if (data.error) {

            alert(data.error);

            resultCard.classList.add("hidden");

    return;

}

/* Display prediction */
        resultCard.classList.remove("hidden");

        updatePredictionBadge(data.prediction);
            confidence.textContent =
                `${Number(data.confidence).toFixed(2)}%`;

            spamProbability.textContent =
                `${Number(data.spam_probability).toFixed(2)}%`;

            hamProbability.textContent =
                `${Number(data.ham_probability).toFixed(2)}%`;

            spamPercent.textContent =
                `${Number(data.spam_probability).toFixed(2)}%`;

            hamPercent.textContent =
                `${Number(data.ham_probability).toFixed(2)}%`;

            spamBar.style.width =
                `${data.spam_probability}%`;

            hamBar.style.width =
                `${data.ham_probability}%`;

            riskLevel.textContent = data.risk;

            updateRiskStyle(data.risk);

            updateKeywords(data.keywords);

            originalMessage.textContent = message;
            
            
        }

        catch (error) {

            hideLoading();

            console.error("Prediction Error:", error);

            resultCard.classList.add("hidden");

            alert(
            "Unable to connect to the Fraud SMS Classifier server.\n\nPlease make sure the Flask application is running."
            );

            }
        loadStatistics();

        loadHistory();

    });


    // =====================================================
    // CLEAR BUTTON
    // =====================================================

    clearBtn.addEventListener("click", () => {

        resetResult();

        loadStatistics();

        loadHistory();



        resultCard.classList.add("hidden");

        hideLoading();

    });


    // =====================================================
    // INITIALIZE
    // =====================================================

    resetResult();// =====================================================
// ANALYTICS DASHBOARD
// =====================================================

const totalSMS = document.getElementById("totalSMS");
const spamSMS = document.getElementById("spamSMS");
const safeSMS = document.getElementById("safeSMS");
const historyTable = document.getElementById("historyTable");


async function loadStatistics() {

    if (!totalSMS) return;

    try {

        const response = await fetch("/statistics");

        if (!response.ok) {

            throw new Error("Unable to load statistics.");

        }

        const data = await response.json();

        totalSMS.textContent = data.total_predictions;

        spamSMS.textContent = data.spam_messages;

        safeSMS.textContent = data.safe_messages;

    }

    catch (error) {

        console.error("Statistics Error:", error);

    }

}


async function loadHistory() {

    if (!historyTable) return;

    try {

        const response = await fetch("/history");

        if (!response.ok) {

            throw new Error("Unable to load history.");

        }

        const history = await response.json();

        historyTable.innerHTML = "";

        if (history.length === 0) {

            historyTable.innerHTML = `
                <tr>
                    <td colspan="4" class="empty-row">
                        No prediction history yet.
                    </td>
                </tr>
            `;

            return;

        }

        history.forEach(item => {

            const badgeClass =
                item.prediction === "Spam"
                ? "history-spam"
                : "history-safe";

            const riskClass =
                item.risk === "Critical"
                ? "risk-critical"
                : item.risk === "High"
                ? "risk-high"
                : item.risk === "Medium"
                ? "risk-medium"
                : "risk-low";

            const row = document.createElement("tr");

            row.innerHTML = `

                <td>${item.created_at}</td>

                <td>

                    <span class="${badgeClass}">

                        ${item.prediction}

                    </span>

                </td>

                <td>

                    <span class="${riskClass}">

                        ${item.risk}

                    </span>

                </td>

                <td>

                    ${Number(item.confidence).toFixed(2)}%

                </td>

            `;

            historyTable.appendChild(row);

        });

    }

    catch (error) {

        console.error("History Error:", error);

    }

}// =====================================================
// EXPORT BUTTONS
// =====================================================

const csvExportButton = document.querySelector(".csv-btn");

const pdfExportButton = document.querySelector(".pdf-btn");


function handleDownload(button, originalText) {

    button.innerHTML = `

        <i class="fa-solid fa-spinner fa-spin"></i>

        Preparing...

    `;

    button.style.pointerEvents = "none";

    setTimeout(() => {

        button.innerHTML = originalText;

        button.style.pointerEvents = "auto";

    }, 2500);

}


if (csvExportButton) {

    const originalCSV = csvExportButton.innerHTML;

    csvExportButton.addEventListener("click", () => {

        handleDownload(csvExportButton, originalCSV);

    });

}


if (pdfExportButton) {

    const originalPDF = pdfExportButton.innerHTML;

    pdfExportButton.addEventListener("click", () => {

        handleDownload(pdfExportButton, originalPDF);

    });

}
});