def get_js(event_str, audio_available, popup_message=""):
    audio_enabled = "true" if audio_available else "false"

    return f"""
    <script>
    window.onload = function() {{
        const eventDate = new Date("{event_str}").getTime();
        const audioEnabled = {audio_enabled};
        const audio = document.getElementById("bg-music");
        const btn = document.getElementById("music-btn");
        const icon = document.getElementById("music-icon");
        const numberIds = ["days", "hours", "minutes", "seconds"];
        const previousValues = new Map();

        let sourceLoaded = false;
        let isLoading = false;

        function setPlayState() {{
          isLoading = false;
          btn.classList.remove("loading");
          btn.classList.remove("playing");
          icon.innerHTML = "&#9654;";
          btn.setAttribute("aria-label", "Play background music");
        }}

        function setPauseState() {{
          isLoading = false;
          btn.classList.remove("loading");
          btn.classList.add("playing");
          icon.innerHTML = "&#10074;&#10074;";
          btn.setAttribute("aria-label", "Pause background music");
        }}

        function setLoadingState() {{
          isLoading = true;
          btn.classList.remove("playing");
          btn.classList.add("loading");
          icon.innerHTML = "";
          btn.setAttribute("aria-label", "Loading background music");
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

        function animateNumber(id, value) {{
          const el = document.getElementById(id);
          const nextValue = String(value).padStart(2, "0");
          const previousValue = previousValues.get(id);

          if (previousValue === nextValue) {{
            return;
          }}

          el.classList.remove("tick");
          void el.offsetWidth;
          el.textContent = nextValue;
          el.classList.add("tick");
          previousValues.set(id, nextValue);
        }}

        function updateCountdown() {{
          const now = new Date().getTime();
          const diff = Math.max(eventDate - now, 0);

          const days = Math.floor(diff / (1000 * 60 * 60 * 24));
          const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
          const minutes = Math.floor((diff / (1000 * 60)) % 60);
          const seconds = Math.floor((diff / 1000) % 60);

          animateNumber("days", days);
          animateNumber("hours", hours);
          animateNumber("minutes", minutes);
          animateNumber("seconds", seconds);
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
        btn.addEventListener("mouseup", function() {{ btn.blur(); }});
        btn.addEventListener("touchend", function() {{ btn.blur(); }});
        audio.addEventListener("playing", setPauseState);
        audio.addEventListener("canplay", function() {{ if (!audio.paused) {{ setPauseState(); }} }});
        audio.addEventListener("waiting", function() {{ if (!audio.paused) {{ setLoadingState(); }} }});
        audio.addEventListener("pause", setPlayState);
        audio.addEventListener("ended", setPlayState);
        audio.addEventListener("error", function(err) {{ console.error("Audio error:", err); setPlayState(); }});

        numberIds.forEach(function(id) {{ previousValues.set(id, null); }});

        setPlayState();
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }};
    </script>
    """