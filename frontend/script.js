// Thyroid disease information
const diseases = {

    hypo: {
        title: "Hypothyroidism",
        description: "Hypothyroidism occurs when the thyroid gland does not produce enough thyroid hormones.",

        sections: [
            {
                title: "Causes",
                items: [
                    "Hashimoto's disease (an autoimmune condition).",
                    "Thyroid surgery or certain medical treatments.",
                    "Some medications or iodine-related problems."
                ]
            },
            {
                title: "Common Symptoms",
                items: [
                    "Fatigue and low energy.",
                    "Feeling unusually cold.",
                    "Dry skin.",
                    "Constipation.",
                    "Difficulty concentrating."
                ]
            },
            {
                title: "Diagnosis",
                items: [
                    "TSH blood test.",
                    "Free T4 (FT4) blood test.",
                    "Additional tests when recommended by a doctor."
                ]
            },
            {
                title: "Treatment Overview",
                items: [
                    "Treatment depends on the underlying cause.",
                    "Doctors may prescribe thyroid hormone replacement.",
                    "Regular medical follow-up and blood tests may be needed."
                ]
            }
        ]
    },

    hyper: {
        title: "Hyperthyroidism",
        description: "Hyperthyroidism occurs when the thyroid gland produces more hormones than the body needs.",

        sections: [
            {
                title: "Causes",
                items: [
                    "Graves' disease (an autoimmune condition).",
                    "Overactive thyroid nodules.",
                    "Thyroid inflammation in some cases."
                ]
            },
            {
                title: "Common Symptoms",
                items: [
                    "Rapid heartbeat.",
                    "Feeling unusually hot.",
                    "Nervousness or anxiety.",
                    "Difficulty sleeping.",
                    "Unintentional weight loss."
                ]
            },
            {
                title: "Diagnosis",
                items: [
                    "TSH blood test.",
                    "Free T4 (FT4) and sometimes T3 tests.",
                    "Additional tests when recommended by a doctor."
                ]
            },
            {
                title: "Treatment Overview",
                items: [
                    "Treatment depends on the cause and severity.",
                    "Medical options may include medication or other treatments.",
                    "Regular follow-up with a healthcare professional is important."
                ]
            }
        ]
    }
};

// Get modal elements
const modal = document.getElementById("diseaseModal");
const title = document.getElementById("diseaseTitle");
const info = document.getElementById("diseaseInfo");
const closeBtn = document.getElementById("closeModal");

// Open disease information
document.querySelectorAll(".details-btn[data-disease]")
.forEach(button => {

    button.addEventListener("click", () => {

        const disease = diseases[button.dataset.disease];

        title.textContent = disease.title;

       info.innerHTML = `
                  <p>${disease.description}</p>

                 ${disease.sections.map(section => `
                   <h3>${section.title}</h3>
        <ul>
            ${section.items.map(item => `<li>${item}</li>`).join("")}
        </ul>
            `).join("")}
          `;

        modal.hidden = false;
    });

});

// Close modal
closeBtn.addEventListener("click", () => {
    modal.hidden = true;
});

// Close when clicking outside
modal.addEventListener("click", (event) => {
    if (event.target === modal) {
        modal.hidden = true;
    }
});
// Close with Escape key
document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        modal.hidden = true;
    }
});

console.log("Thyroid Care JavaScript Loaded!");
// Open Thyroid Tests Modal
const exploreTestsBtn = document.getElementById("exploreTests");
const testsModal = document.getElementById("testsModal");
const closeTestsBtn = document.getElementById("closeTestsModal");

exploreTestsBtn.addEventListener("click", () => {
    testsModal.hidden = false;
});

// Close Tests Modal
closeTestsBtn.addEventListener("click", () => {
    testsModal.hidden = true;
});

// Close when clicking outside
testsModal.addEventListener("click", (event) => {
    if (event.target === testsModal) {
        testsModal.hidden = true;
    }
});
// AI Assistant Chat
const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

async function sendMessage() {
    const message = userInput.value.trim();

    if (message === "") return;

    // Display user's message
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message;
    chatBox.appendChild(userMessage);

    userInput.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    // Show loading message
    const loading = document.createElement("div");
    loading.className = "bot-message";
    loading.textContent = "Thinking...";
    chatBox.appendChild(loading);

    try {
        const response = await fetch("http://localhost:3000/api/thyroid/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error("Server error");
        }

        const data = await response.json();

        loading.textContent = data.reply;

    } catch (error) {
        loading.textContent =
            "Sorry, I couldn't connect to the assistant. Please try again.";
        console.error(error);
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send button
sendBtn.addEventListener("click", sendMessage);

// Send with Enter key
userInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        sendMessage();
    }
});