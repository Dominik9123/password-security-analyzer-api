const API_URL = "http://127.0.0.1:8000/api";

const passwordInput = document.getElementById("passwordInput");
const analyzeBtn = document.getElementById("analyzeBtn");
const analysisResult = document.getElementById("analysisResult");

const passwordLength = document.getElementById("passwordLength");
const generateBtn = document.getElementById("generateBtn");
const generatedPassword = document.getElementById("generatedPassword");

const firstPassword = document.getElementById("firstPassword");
const secondPassword = document.getElementById("secondPassword");
const compareBtn = document.getElementById("compareBtn");
const compareResult = document.getElementById("compareResult");


function showResult(element, content) {
    // PL: Kazdy wynik trafia do gotowego kontenera bez przeladowania strony.
    // EN: Each result is rendered into the existing container without reloading the page.
    element.classList.remove("hidden");
    element.innerHTML = content;
}


function getStrengthClass(strength) {
    if (strength === "strong") {
        return "strong";
    }

    if (strength === "medium") {
        return "medium";
    }

    return "weak";
}


function formatAnalysisResult(data) {
    const strengthClass = getStrengthClass(data.strength);

    // PL: Najwazniejsze metryki sa w jednym wierszu, zeby wynik byl bardziej kompaktowy.
    // EN: Main metrics stay in one row to keep the result panel compact.
    return `
        <div class="result-summary">
            <span><strong>Score:</strong> ${data.score}/100</span>
            <span><strong>Strength:</strong> <span class="${strengthClass}">${data.strength}</span></span>
            <span><strong>Entropy:</strong> ${data.entropy}</span>
        </div>
        <p><strong>Issues</strong></p>
        <ul>
            ${data.issues.map(issue => `<li>${issue}</li>`).join("") || "<li>No major issues found.</li>"}
        </ul>
        <p><strong>Suggestions</strong></p>
        <ul>
            ${data.suggestions.map(suggestion => `<li>${suggestion}</li>`).join("") || "<li>No suggestions needed.</li>"}
        </ul>
    `;
}


analyzeBtn.addEventListener("click", async (event) => {
    event.preventDefault();

    try {
        // PL: Haslo jest wysylane do lokalnego API tylko w celu analizy.
        // EN: The password is sent to the local API only for analysis.
        const response = await fetch(`${API_URL}/analyze`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                password: passwordInput.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            showResult(analysisResult, `<p><strong>Error:</strong> ${data.detail}</p>`);
            return;
        }

        showResult(analysisResult, formatAnalysisResult(data));
    } catch (error) {
        showResult(analysisResult, "<p><strong>Error:</strong> Could not connect to API.</p>");
    }
});


generateBtn.addEventListener("click", async (event) => {
    event.preventDefault();

    try {
        const response = await fetch(`${API_URL}/generate?length=${passwordLength.value}`);
        const data = await response.json();

        if (!response.ok) {
            showResult(generatedPassword, `<p><strong>Error:</strong> ${data.detail}</p>`);
            return;
        }

        showResult(generatedPassword, `<p><strong>Generated password:</strong> ${data.password}</p>`);
    } catch (error) {
        showResult(generatedPassword, "<p><strong>Error:</strong> Could not connect to API.</p>");
    }
});


compareBtn.addEventListener("click", async (event) => {
    event.preventDefault();

    try {
        const response = await fetch(`${API_URL}/compare`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                first_password: firstPassword.value,
                second_password: secondPassword.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            showResult(compareResult, `<p><strong>Error:</strong> ${JSON.stringify(data.detail)}</p>`);
            return;
        }

        showResult(compareResult, `
            <p><strong>Stronger password:</strong> ${data.stronger_password}</p>

            <h3>First password</h3>
            ${formatAnalysisResult(data.first_password)}

            <h3>Second password</h3>
            ${formatAnalysisResult(data.second_password)}
        `);
    } catch (error) {
        showResult(compareResult, "<p><strong>Error:</strong> Could not connect to API.</p>");
    }
});
