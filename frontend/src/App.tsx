import React, { useState, useEffect, useRef } from 'react';
import { fetchPlaylist, checkHealth, Track } from './api';
import { DJPlayer } from './player';
import './App.css';

function App() {
  const [tracks, setTracks] = useState<Track[]>([]);
  const [currentTrack, setCurrentTrack] = useState<Track | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [playlistId, setPlaylistId] = useState('');
  const [fadeDuration, setFadeDuration] = useState(5);
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  
  const playerRef = useRef<DJPlayer | null>(null);

  useEffect(() => {
    // Проверяем статус API при загрузке
    checkHealth().then(connected => {
      setApiStatus(connected ? 'connected' : 'disconnected');
    });

    // Создаем плеер
    playerRef.current = new DJPlayer();
    playerRef.current.setFadeDuration(fadeDuration);
    playerRef.current.setOnTrackChange((track, index) => {
      setCurrentTrack(track);
      setCurrentIndex(index);
    });

    return () => {
      if (playerRef.current) {
        playerRef.current.stop();
      }
    };
  }, []);

  const handleStart = async () => {
    if (!playlistId.trim()) {
      alert('Введите ID плейлиста!');
      return;
    }

    setIsLoading(true);
    try {
      const playlistTracks = await fetchPlaylist(playlistId);
      setTracks(playlistTracks);
      
      if (playlistTracks.length > 0) {
        setIsPlaying(true);
        playerRef.current?.play(playlistTracks);
      }
    } catch (error) {
      alert('Ошибка при загрузке плейлиста: ' + error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStop = () => {
    setIsPlaying(false);
    setCurrentTrack(null);
    setCurrentIndex(0);
    playerRef.current?.stop();
    playerRef.current = new DJPlayer();
    playerRef.current.setFadeDuration(fadeDuration);
    playerRef.current.setOnTrackChange((track, index) => {
      setCurrentTrack(track);
      setCurrentIndex(index);
    });
  };

  const handleFadeChange = (value: number) => {
    setFadeDuration(value);
    playerRef.current?.setFadeDuration(value);
  };

  const getStatusColor = () => {
    switch (apiStatus) {
      case 'connected': return '#4CAF50';
      case 'disconnected': return '#f44336';
      default: return '#ff9800';
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case 'connected': return 'API подключен';
      case 'disconnected': return 'API отключен';
      default: return 'Проверка API...';
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🎵 Auto DJ</h1>
        <div className="status" style={{ color: getStatusColor() }}>
          {getStatusText()}
        </div>
      </header>

      <main className="main">
        <div className="controls">
          <div className="input-group">
            <label htmlFor="playlist-id">ID плейлиста Яндекс.Музыки:</label>
            <input
              id="playlist-id"
              type="text"
              value={playlistId}
              onChange={(e) => setPlaylistId(e.target.value)}
              placeholder="Например: 123456789"
              disabled={isPlaying}
            />
          </div>

          <div className="input-group">
            <label htmlFor="fade-duration">Длительность кроссфейда: {fadeDuration}с</label>
            <input
              id="fade-duration"
              type="range"
              min="1"
              max="15"
              value={fadeDuration}
              onChange={(e) => handleFadeChange(Number(e.target.value))}
              disabled={isPlaying}
            />
          </div>

          <div className="buttons">
            {!isPlaying ? (
              <button 
                onClick={handleStart} 
                disabled={isLoading || apiStatus !== 'connected'}
                className="btn btn-primary"
              >
                {isLoading ? 'Загрузка...' : '▶️ Запустить DJ'}
              </button>
            ) : (
              <button onClick={handleStop} className="btn btn-danger">
                ⏹️ Остановить
              </button>
            )}
          </div>
        </div>

        {currentTrack && (
          <div className="now-playing">
            <h3>🎧 Сейчас играет:</h3>
            <div className="track-info">
              <div className="track-title">{currentTrack.title}</div>
              <div className="track-artist">{currentTrack.artist}</div>
              <div className="track-progress">
                Трек {currentIndex + 1} из {tracks.length}
              </div>
            </div>
          </div>
        )}

        {tracks.length > 0 && (
          <div className="playlist">
            <h3>📋 Плейлист ({tracks.length} треков):</h3>
            <div className="tracks-list">
              {tracks.map((track, index) => (
                <div 
                  key={index} 
                  className={`track-item ${index === currentIndex ? 'current' : ''}`}
                >
                  <span className="track-number">{index + 1}.</span>
                  <span className="track-title">{track.title}</span>
                  <span className="track-artist">— {track.artist}</span>
                  <span className="track-duration">({Math.floor(track.duration / 60)}:{String(track.duration % 60).padStart(2, '0')})</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App; 