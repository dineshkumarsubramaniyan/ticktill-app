def get_js(event_str, audio_available):
    audio_enabled = "true" if audio_available else "false"

    return f"""
    <script>
    window.onload = function() {{
        const eventDate = new Date("{event_str}").getTime();
        const audioEnabled = {audio_enabled};
        const audio = document.getElementById("bg-music");
        const btn = document.getElementById("music-btn");
        const icon = document.getElementById("music-icon");

        if (audioEnabled) {{
          audio.volume = 1.0;
        }}

        function updateCountdown() {{
          const now = new Date().getTime();
          const diff = Math.max(eventDate - now, 0);

          const days = Math.floor(diff / (1000 * 60 * 60 * 24));
          const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
          const minutes = Math.floor((diff / (1000 * 60)) % 60);
          const seconds = Math.floor((diff / 1000) % 60);

          document.getElementById("days").innerHTML = String(days).padStart(2, "0");
          document.getElementById("hours").innerHTML = String(hours).padStart(2, "0");
          document.getElementById("minutes").innerHTML = String(minutes).padStart(2, "0");
          document.getElementById("seconds").innerHTML = String(seconds).padStart(2, "0");
        }}

        async function toggleMusic() {{
          if (!audioEnabled) {{
            return;
          }}

          if (audio.paused) {{
            try {{
              await audio.play();
              icon.innerHTML = "&#10074;&#10074;";
              btn.setAttribute("aria-label", "Pause background music");
              btn.setAttribute("title", "Pause background music");
            }} catch (err) {{
              console.error("Play failed:", err);
            }}
          }} else {{
            audio.pause();
            icon.innerHTML = "&#9654;";
            btn.setAttribute("aria-label", "Play background music");
            btn.setAttribute("title", "Play background music");
          }}
        }}

        btn.addEventListener("click", toggleMusic);
        audio.addEventListener("ended", function() {{
          icon.innerHTML = "&#9654;";
          btn.setAttribute("aria-label", "Play background music");
          btn.setAttribute("title", "Play background music");
        }});

        updateCountdown();
        setInterval(updateCountdown, 1000);
    }};
    </script>
    """
