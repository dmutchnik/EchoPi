<template>
  <div class="player-wrapper" :style="{ backgroundImage: track ? 'url(' + track.albumArt + ')' : 'none' }">
    <div class="overlay" />

    <div class="spotify-card">
      <img
        :src="track ? track.albumArt : placeholderImage"
        class="album-art"
        :class="{ 'is-placeholder': !track }"
      />

      <div class="track-details">
        <h2>{{ track?.name || 'Nothing is playing' }}</h2>
        <p class="artists">{{ track?.artists?.join(', ') || '–––' }}</p>
        <p class="album">{{ track?.album || '–––' }}</p>

        <a v-if="track" :href="track.url" target="_blank" class="open-link">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon" viewBox="0 0 24 24" fill="currentColor">
            <path d="M7 6v12l10-6z" />
          </svg>
          Play on Spotify
        </a>

        <div class="time-display">
          <span>{{ formatTime(track?.progress || 0) }}</span>
          <span>{{ formatTime(track?.duration || 0) }}</span>
        </div>

        <div class="progress-container">
          <div class="progress-bar" :style="{ width: progressPercent + '%' }"></div>
        </div>

        <div class="controls">
          <button @click="sendAction('previous')">⏮️</button>
          <button @click="sendAction('pause')">⏸️</button>
          <button @click="sendAction('play')">▶️</button>
          <button @click="sendAction('next')">⏭️</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      track: null,
      uiProgressInterval: null,
      backendPollInterval: null,
      placeholderImage: "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg",
    };
  },
  computed: {
    progressPercent() {
      if (!this.track || this.track.duration === 0) return 0;
      return (this.track.progress / this.track.duration) * 100;
    },
  },
  methods: {
    fetchTrack() {
      fetch("http://localhost:5000/api/spotify/current")
        .then((res) => res.json())
        .then((data) => {
          if (data.name) {
            this.track = {
              name: data.name,
              artists: data.artists,
              album: data.album,
              albumArt: data.album_art,
              url: data.url,
              duration: data.duration,
              progress: data.progress,
            };
          } else {
            this.track = null;
          }
        });
    },
    formatTime(seconds) {
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60).toString().padStart(2, "0");
      return `${m}:${s}`;
    },
    updateProgress() {
      if (this.track && this.track.progress < this.track.duration) {
        this.track.progress += 0.05;
      }
    },
    sendAction(action) {
      fetch("http://localhost:5000/api/spotify/control", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ action }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status === "success") {
            console.log("Action successful:", action);
            this.fetchTrack(); // refresh track info
          } else {
            console.warn("Action failed:", data.error);
          }
        })
        .catch((err) => {
          console.error("Error sending action:", err);
        });
    },
  },
  mounted() {
    this.fetchTrack();
    this.backendPollInterval = setInterval(this.fetchTrack, 3000);
    this.uiProgressInterval = setInterval(this.updateProgress, 50);
  },
  beforeUnmount() {
    clearInterval(this.backendPollInterval);
    clearInterval(this.uiProgressInterval);
  },
};
</script>

<style scoped>
.player-wrapper {
  position: relative;
  min-height: 100vh;
  padding: 40px;
  background-size: cover;
  background-position: center;
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  z-index: 0;
}

.spotify-card {
  position: relative;
  display: flex;
  gap: 32px;
  background: rgba(25, 25, 25, 0.95);
  border-radius: 20px;
  padding: 32px;
  color: white;
  max-width: 700px;
  width: 100%;
  z-index: 1;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
}

.album-art {
  width: 160px;
  height: 160px;
  border-radius: 12px;
  object-fit: cover;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.7);
  flex-shrink: 0;
  transition: filter 0.3s ease, opacity 0.3s ease;
}

.album-art.is-placeholder {
  opacity: 0.4;
  filter: grayscale(100%);
  background-color: #222;
}

.track-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.track-details h2 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: bold;
}

.artists {
  font-size: 1.1rem;
  color: #1db954;
  margin: 4px 0;
  opacity: 1;
}

.album {
  font-size: 0.95rem;
  color: #ccc;
  margin-bottom: 10px;
  opacity: 0.8;
}

.open-link {
  display: inline-flex;
  align-items: center;
  font-size: 0.9rem;
  text-decoration: none;
  color: white;
  background-color: #1db954;
  padding: 6px 12px;
  border-radius: 8px;
  font-weight: 500;
  width: fit-content;
  gap: 6px;
  transition: background 0.2s;
}
.open-link:hover {
  background-color: #1ed760;
}
.icon {
  width: 18px;
  height: 18px;
}

.time-display {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  margin: 8px 0;
  color: #bbb;
}

.progress-container {
  height: 8px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #1db954, #1ed760);
  transition: width 0.05s linear;
}

.controls {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}
.controls button {
  font-size: 1.4rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s ease;
}
.controls button:hover {
  background: rgba(255, 255, 255, 0.3);
}
</style>
