async function generate() {
  const text = document.getElementById("text").value.trim();
  const voice = document.getElementById("voice").value;

  if (!text) {
    alert("Введите текст");
    return;
  }

  const res = await fetch("/api/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice })
  });

  if (!res.ok) {
    alert("Ошибка API");
    return;
  }

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);

  document.getElementById("player").src = url;
  const d = document.getElementById("download");
  d.href = url;
  d.style.display = "inline-block";
}
