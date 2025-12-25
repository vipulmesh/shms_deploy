async function submitData() {
    const village = document.getElementById("village").value;
    const diarrhea = document.getElementById("diarrhea").value;
    const fever = document.getElementById("fever").value;
    const rainfall = document.getElementById("rainfall").value;

    if (!village || !diarrhea) {
        alert("Please fill required fields");
        return;
    }

    const response = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ village, diarrhea, fever, rainfall })
    });

    const result = await response.json();
    if (response.ok) {
        alert("Data Submitted! Calculated Risk: " + result.risk);
        window.location.href = "/dashboard";
    }
}

async function loadData() {
    try {
        const response = await fetch("/api/data");
        const data = await response.json();
        
        document.getElementById("total-records").innerText = data.length;
        document.getElementById("safe-areas").innerText = data.filter(d => d.risk === "Safe").length;
        document.getElementById("medium-risk").innerText = data.filter(d => d.risk === "Medium Risk").length;
        document.getElementById("high-risk").innerText = data.filter(d => d.risk === "High Risk").length;

        let html = '<table class="data-table"><thead><tr><th>Village</th><th>Diarrhea</th><th>Rainfall</th><th>Risk</th></tr></thead><tbody>';
        data.forEach(r => {
            const badgeClass = r.risk.toLowerCase().replace(' ', '-');
            html += `<tr>
                <td>${r.village}</td>
                <td>${r.diarrhea}</td>
                <td>${r.rainfall}</td>
                <td><span class="risk-badge ${badgeClass}">${r.risk}</span></td>
            </tr>`;
        });
        document.getElementById("table-container").innerHTML = html + '</tbody></table>';
    } catch (err) {
        console.error("Dashboard load error", err);
    }
}