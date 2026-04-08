def get_html(audio_src, audio_available):
    disabled_attr = "" if audio_available else "disabled"
    audio_markup = (
        f'<audio id="bg-music" loop playsinline preload="none" data-src="{audio_src}"></audio>'
        if audio_available
        else '<audio id="bg-music" preload="none"></audio>'
    )

    return f"""
    <div class="shell">
      <div class="app">
        {audio_markup}

        <div class="hero">
          <div class="hero-overlay"></div>
        </div>

        <button id="music-btn" class="music-btn" type="button" aria-label="Play background music" {disabled_attr}>
          <span id="music-icon" class="music-icon">&#9654;</span>
        </button>

        <div id="telegram-popup" class="telegram-popup" hidden>
          <div class="telegram-popup-card">
            <button id="telegram-popup-close" class="telegram-popup-close" type="button" aria-label="Close message">&times;</button>
            <div class="telegram-popup-label">A message for you</div>
            <div id="telegram-popup-text" class="telegram-popup-text"></div>
          </div>
        </div>

        <div class="content">
          <div class="eyebrow">Save the date</div>
          <div class="names">WE'RE GETTING MARRIED</div>
          <div class="tagline">A little countdown to our forever</div>

          <div class="date-pill">September 13, 2026</div>

          <div class="divider"></div>

          <div class="countdown">
            <div class="box accent-box">
              <div id="days" class="number">00</div>
              <div class="label">DAYS</div>
            </div>
            <div class="box">
              <div id="hours" class="number">00</div>
              <div class="label">HOURS</div>
            </div>
            <div class="box">
              <div id="minutes" class="number">00</div>
              <div class="label">MINUTES</div>
            </div>
            <div class="box accent-box">
              <div id="seconds" class="number">00</div>
              <div class="label">SECONDS</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """