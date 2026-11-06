async function askThyroidAssistant(message) {
  const query = message.toLowerCase();

  if (query.includes("symptom")) {
    return "Common thyroid symptoms include fatigue, unexplained weight changes, feeling too cold or too hot, and changes in heart rate.";
  } else if (query.includes("hypothyroid")) {
    return "Hypothyroidism is an underactive thyroid gland where it doesn't produce enough thyroid hormones.";
  } else if (query.includes("hyperthyroid")) {
    return "Hyperthyroidism occurs when the thyroid gland produces too much thyroid hormone, speeding up body metabolism.";
  } else {
    return "Thank you for your question about " + message + ". For medical safety, please consult a healthcare professional.";
  }
}

module.exports = askThyroidAssistant;