 const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");

    canvas.height = window.innerHeight;
    canvas.width = window.innerWidth;

    const letras = "アァイィウヴエエェカガキギクグケゲコゴサザシジスズセゼソゾタダチッヂツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヲンABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@$%&";
    const chars = letras.split("");
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function draw() {
      ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      ctx.fillStyle = "#0F0";
      ctx.font = fontSize + "px monospace";

      for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }

    setInterval(draw, 35);

    const texto = "{{ respuesta | default('') | escapejs }}";
    const nivelStr = "{{ nivel | default(0) }}";
    const nivel = parseInt(nivelStr) || 0;

    function hablarConDeterioro(texto, deterioro) {
      const synth = window.speechSynthesis;
      const utterance = new SpeechSynthesisUtterance(texto);
      utterance.lang = "es-ES";

      let baseRate = 1 - (deterioro / 200);
      let basePitch = 1 - (deterioro / 200);

      if (deterioro >= 80) {
        baseRate += (Math.random() - 0.5) * 0.3;
        basePitch += (Math.random() - 0.5) * 0.3;

        baseRate = Math.max(0.2, Math.min(1.2, baseRate));
        basePitch = Math.max(0.2, Math.min(2.0, basePitch));

        document.body.style.animation = "glitchFlash 0.1s alternate infinite";
        setTimeout(() => {
          document.body.style.animation = "none";
        }, 1000);
      }

      utterance.rate = baseRate;
      utterance.pitch = basePitch;
      synth.speak(utterance);
    }

    if (texto) {
      hablarConDeterioro(texto, nivel);
    }

    
    function escribirTextoGradualmente(texto, elementoId, velocidad = 30) {
  const destino = document.getElementById(elementoId);
  if (!destino) return;

  let i = 0;
  const escribir = () => {
    if (i < texto.length) {
      destino.textContent += texto.charAt(i);
      i++;
      setTimeout(escribir, velocidad);
    }
  };
  escribir();
}