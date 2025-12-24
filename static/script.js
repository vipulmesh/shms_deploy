// ===========================
// DATA SUBMISSION
// ===========================
async function submitData() {
    const village = document.getElementById("village").value.trim();
    const diarrhea = document.getElementById("diarrhea").value;
    const fever = document.getElementById("fever").value;
    const rainfall = document.getElementById("rainfall").value;

    if (!village || !diarrhea || !fever) {
        showNotification("Please fill all required fields", "error");
        return;
    }

    const payload = {
        village,
        diarrhea: parseInt(diarrhea),
        fever: parseInt(fever),
        rainfall
    };

    try {
        const response = await fetch("/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            showNotification(`Submitted! Risk: ${result.risk}`, "success");
            document.getElementById("village").value = "";
            document.getElementById("diarrhea").value = "";
            document.getElementById("fever").value = "";
            document.getElementById("rainfall").value = "Low";
        } else {
            showNotification("Submission failed", "error");
        }
    } catch {
        showNotification("Server not reachable", "error");
    }
}

// ===========================
// LOAD DATA
// ===========================
async function loadData() {
    try {
        const response = await fetch("/data");
        const data = await response.json();

        updateStatistics(data);
        populateTable(data);
        showHighRiskAlert(data);
    } catch {
        showEmptyState("Unable to load data");
    }
}

// ===========================
// STATISTICS
// ===========================
function updateStatistics(data) {
    document.getElementById("total-records").textContent = data.length;
    document.getElementById("safe-areas").textContent =
        data.filter(d => d.risk === "Safe").length;
    document.getElementById("medium-risk").textContent =
        data.filter(d => d.risk === "Medium Risk").length;
    document.getElementById("high-risk").textContent =
        data.filter(d => d.risk === "High Risk").length;
}

// ===========================
// TABLE
// ===========================
function populateTable(data) {
    const container = document.getElementById("table-container");

    if (data.length === 0) {
        showEmptyState();
        return;
    }

    let html = `
        <table class="data-table">
            <thead>
                <tr>
                    <th>Village</th>
                    <th>Diarrhea</th>
                    <th>Fever</th>
                    <th>Rainfall</th>
                    <th>Risk</th>
                    <th>Date</th>
                </tr>
            </thead>
            <tbody>
    `;

    data.forEach(r => {
        html += `
            <tr>
                <td>${r.village}</td>
                <td>${r.diarrhea}</td>
                <td>${r.fever}</td>
                <td>${r.rainfall}</td>
                <td class="${getRiskClass(r.risk)}">${r.risk}</td>
                <td>${r.date}</td>
            </tr>
        `;
    });

    html += "</tbody></table>";
    container.innerHTML = html;
}

// ===========================
// HELPERS
// ===========================
function getRiskClass(risk) {
    if (risk === "High Risk") return "high";
    if (risk === "Medium Risk") return "medium";
    return "safe";
}

function showEmptyState(msg = "No data available") {
    document.getElementById("table-container").innerHTML =
        `<p>${msg}</p>`;
}

function showHighRiskAlert(data) {
    const high = data.filter(d => d.risk === "High Risk");
    const box = document.getElementById("high-risk-alert");
    if (!box) return;

    box.style.display = high.length > 0 ? "block" : "none";
}

function showNotification(msg, type) {
    const n = document.getElementById("notification");
    if (!n) return;

    n.textContent = msg;
    n.className = `notification ${type}`;
    n.style.display = "block";

    setTimeout(() => n.style.display = "none", 3000);
}
