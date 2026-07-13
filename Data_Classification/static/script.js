async function predictHeartDisease() {

    const patient_name = document.getElementById("patient_name").value.trim();
    const age      = document.getElementById("age").value;
    const sex      = document.getElementById("sex").value;
    const cp       = document.getElementById("cp").value;
    const trestbps = document.getElementById("trestbps").value;
    const chol     = document.getElementById("chol").value;
    const fbs      = document.getElementById("fbs").value;
    const restecg  = document.getElementById("restecg").value;
    const thalach  = document.getElementById("thalach").value;
    const exang    = document.getElementById("exang").value;
    const oldpeak  = document.getElementById("oldpeak").value;
    const slope    = document.getElementById("slope").value;
    const ca       = document.getElementById("ca").value;
    const thal     = document.getElementById("thal").value;

    const resultDiv = document.getElementById("result");

    if (!patient_name || !age || !sex || !cp || !trestbps || !chol ||
        !fbs || !restecg || !thalach || !exang || !oldpeak ||
        !slope || !ca || !thal) {

        resultDiv.innerHTML = `
            <div class="error-box">
                <h2><i class="fas fa-circle-exclamation"></i> Incomplete form</h2>
                <p>Please fill in every field before running the prediction.</p>
            </div>`;

        resultDiv.scrollIntoView({ behavior: "smooth", block: "center" });
        return;
    }

    resultDiv.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Analysing patient data, please wait…</p>
        </div>`;

    const payload = {
        patient_name,
        age: Number(age), sex: Number(sex), cp: Number(cp),
        trestbps: Number(trestbps), chol: Number(chol), fbs: Number(fbs),
        restecg: Number(restecg), thalach: Number(thalach), exang: Number(exang),
        oldpeak: Number(oldpeak), slope: Number(slope), ca: Number(ca), thal: Number(thal)
    };

    try {
        const res  = await fetch("/predict", {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify(payload)
        });
        const data = await res.json();

        if (!data.success) {
            resultDiv.innerHTML = `
                <div class="error-box">
                    <h2><i class="fas fa-circle-exclamation"></i> Prediction failed</h2>
                    <p>${data.message}</p>
                </div>`;
            return;
        }

        const high       = data.prediction === 1;
        const cls        = high ? "danger" : "success";
        const icon       = high ? "🔴" : "🟢";
        const label      = data.prediction_text.replace(/^[🔴🟢]\s*/u, "");
        const confidence = data.confidence;
        const date       = new Date();
        const dateStr    = date.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
        const timeStr    = date.toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" });

        const dlBtn = data.download_url ? `
            <a href="${data.download_url}" class="dl-btn">
                <i class="fas fa-file-pdf"></i> Download PDF Report
            </a>` : "";

        resultDiv.innerHTML = `
            <div class="result-output">
                <div class="result-banner ${cls}">
                    <h2>${icon} ${label}</h2>
                    <div class="conf-wrap">
                        <div class="conf-labels">
                            <span>Confidence</span><span>${confidence}%</span>
                        </div>
                        <div class="conf-track">
                            <div class="conf-fill" id="confFill" style="width:0%"></div>
                        </div>
                    </div>
                    <div class="result-meta">
                        <p><strong>Patient:</strong> ${patient_name}</p>
                        <p><strong>Date:</strong> ${dateStr}</p>
                        <p><strong>Time:</strong> ${timeStr}</p>
                    </div>
                </div>

                <div class="rec-box">
                    <h4><i class="fas fa-notes-medical"></i> Recommendations</h4>
                    <p>${data.recommendation}</p>
                </div>

                ${dlBtn}
            </div>`;

        requestAnimationFrame(() => {
            setTimeout(() => {
                const fill = document.getElementById("confFill");
                if (fill) fill.style.width = confidence + "%";
            }, 80);
        });

    } catch (err) {
        console.error(err);
        resultDiv.innerHTML = `
            <div class="error-box">
                <h2><i class="fas fa-server"></i> Cannot reach server</h2>
                <p>Make sure the Flask application is running and try again.</p>
            </div>`;
    }
}
