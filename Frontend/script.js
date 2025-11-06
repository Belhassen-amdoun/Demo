const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const chat = document.getElementById("chat");
const resultDiv = document.getElementById("result");
const BACKEND_URL = "http://127.0.0.1:8000";

function appendChat(message, className = "bot-message") {
  const div = document.createElement("div");
  div.className = className;
  div.textContent = message;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

uploadBtn.addEventListener("click", async () => {
  const file = fileInput.files[0];
  if (!file) {
    alert("Choisis une image d'abord.");
    return;
  }

  appendChat("📤 Envoi de l'image...", "user-message");
  uploadBtn.disabled = true;
  resultDiv.innerHTML = "";
  const formData = new FormData();
  formData.append("file", file);

  try {
    const resp = await fetch(`${BACKEND_URL}/upload`, { method: "POST", body: formData });
    const data = await resp.json();

    if (!data.ok) throw new Error(data.detail || "Erreur backend");

    appendChat("🧠 Résumé de la facture :", "bot-message");
    appendChat(data.paragraph || "(Aucun paragraphe généré)", "bot-message");

    if (data.pdf_url) {
      const a = document.createElement("a");
      a.href = `${BACKEND_URL}${data.pdf_url}`;
      a.target = "_blank";
      a.textContent = "📄 Télécharger la facture PDF";
      a.style.display = "block";
      a.style.marginTop = "10px";
      resultDiv.appendChild(a);
    }

  } catch (e) {
    appendChat("❌ Erreur : " + e.message, "bot-message");
  } finally {
    uploadBtn.disabled = false;
  }
});
