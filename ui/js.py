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

        let sourceLoaded = false;
        let isLoading = false;

        function setPlayState() {{
          isLoading = false;
          btn.classList.remove("loading");
          icon.innerHTML = "&#9654;";
          btn.setAttribute("aria-label", "Play background music");
          btn.setAttribute("title", "Play background music");
        }}

        function setPauseState() {{
          isLoading = false;
          btn.classList.remove("loading");
          icon.innerHTML = "&#10074;&#10074;";
          btn.setAttribute("aria-label", "Pause background music");
          btn.setAttribute("title", "Pause background music");
        }}

        function setLoadingState() {{
          isLoading = true;
          btn.classList.add("loading");
          icon.innerHTML = "";
          btn.setAttribute("aria-label", "Loading background music");
          btn.setAttribute("title", "Loading background music");
        }}

        function ensureAudioSource() {{
          if (!audioEnabled || sourceLoaded) {{
            return;
          }}

          const src = audio.dataset.src;
          if (src) {{
            audio.src = src;
            sourceLoaded = true;
          }}
        }}

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
          if (!audioEnabled || isLoading) {{
            return;
          }}

          if (audio.paused) {{
            try {{
              ensureAudioSource();
              setLoadingState();
              await audio.play();
              setPauseState();
            }} catch (err) {{
              console.error("Play failed:", err);
              setPlayState();
            }}
          }} else {{
            audio.pause();
            setPlayState();
          }}
        }}

        btn.addEventListener("click", toggleMusic);
        audio.addEventListener("playing", setPauseState);
        audio.addEventListener("canplay", function() {{
          if (!audio.paused) {{
            setPauseState();
          }}
        }});
        audio.addEventListener("waiting", function() {{
          if (!audio.paused) {{
            setLoadingState();
          }}
        }});
        audio.addEventListener("pause", setPlayState);
        audio.addEventListener("ended", setPlayState);
        audio.addEventListener("error", function(err) {{
          console.error("Audio error:", err);
          setPlayState();
        }});

        setPlayState();
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }};
    </script>
    """
