def get_js(event_str):
    return f"""
    <script>
    const eventDate = new Date("{event_str}").getTime();

    setInterval(function() {{
      const now = new Date().getTime();
      const diff = eventDate - now;

      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((diff / (1000 * 60)) % 60);
      const seconds = Math.floor((diff / 1000) % 60);

      document.getElementById("days").innerHTML = String(days).padStart(2,'0');
      document.getElementById("hours").innerHTML = String(hours).padStart(2,'0');
      document.getElementById("minutes").innerHTML = String(minutes).padStart(2,'0');
      document.getElementById("seconds").innerHTML = String(seconds).padStart(2,'0');

    }}, 1000);
    </script>
    """