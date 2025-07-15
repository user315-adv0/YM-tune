import { Track } from './api';

export class DJPlayer {
  private ctx: AudioContext;
  private gainA: GainNode;
  private gainB: GainNode;
  private currentIndex = 0;
  private fadeDuration = 5; // секунды
  private isPlaying = false;
  private tracks: Track[] = [];
  private onTrackChange?: (track: Track, index: number) => void;

  constructor() {
    this.ctx = new AudioContext();
    this.gainA = this.ctx.createGain();
    this.gainB = this.ctx.createGain();
    
    this.gainA.connect(this.ctx.destination);
    this.gainB.connect(this.ctx.destination);
  }

  setFadeDuration(seconds: number) {
    this.fadeDuration = seconds;
  }

  setOnTrackChange(callback: (track: Track, index: number) => void) {
    this.onTrackChange = callback;
  }

  async play(tracks: Track[]) {
    this.tracks = tracks;
    this.currentIndex = 0;
    this.isPlaying = true;
    
    if (tracks.length === 0) return;
    
    await this.playNext();
  }

  stop() {
    this.isPlaying = false;
    this.ctx.close();
  }

  private async playNext() {
    if (!this.isPlaying || this.currentIndex >= this.tracks.length) {
      this.isPlaying = false;
      return;
    }

    const currentTrack = this.tracks[this.currentIndex];
    const nextTrack = this.tracks[this.currentIndex + 1];

    try {
      // Загружаем текущий трек
      const bufferA = await this.loadAudio(currentTrack.url);
      const sourceA = this.ctx.createBufferSource();
      sourceA.buffer = bufferA;
      sourceA.connect(this.gainA);

      // Уведомляем о смене трека
      if (this.onTrackChange) {
        this.onTrackChange(currentTrack, this.currentIndex);
      }

      // Запускаем текущий трек
      sourceA.start();
      this.gainA.gain.setValueAtTime(1, this.ctx.currentTime);

      // Если есть следующий трек, готовим кроссфейд
      if (nextTrack && this.isPlaying) {
        const bufferB = await this.loadAudio(nextTrack.url);
        const sourceB = this.ctx.createBufferSource();
        sourceB.buffer = bufferB;
        sourceB.connect(this.gainB);

        // Время начала кроссфейда
        const fadeStartTime = this.ctx.currentTime + bufferA.duration - this.fadeDuration;
        
        // Запускаем следующий трек
        sourceB.start(fadeStartTime);
        this.gainB.gain.setValueAtTime(0, fadeStartTime);
        this.gainB.gain.linearRampToValueAtTime(1, fadeStartTime + this.fadeDuration);

        // Затухание текущего трека
        this.gainA.gain.linearRampToValueAtTime(0, fadeStartTime + this.fadeDuration);

        // Планируем следующий трек
        setTimeout(() => {
          this.currentIndex++;
          this.playNext();
        }, (bufferA.duration - this.fadeDuration) * 1000);
      } else {
        // Последний трек - просто ждем окончания
        setTimeout(() => {
          this.currentIndex++;
          this.playNext();
        }, bufferA.duration * 1000);
      }

    } catch (error) {
      console.error('Ошибка при воспроизведении трека:', error);
      // Пропускаем проблемный трек
      this.currentIndex++;
      setTimeout(() => this.playNext(), 1000);
    }
  }

  private async loadAudio(url: string): Promise<AudioBuffer> {
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    return await this.ctx.decodeAudioData(arrayBuffer);
  }

  getCurrentTrack(): Track | null {
    if (this.currentIndex < this.tracks.length) {
      return this.tracks[this.currentIndex];
    }
    return null;
  }

  getProgress(): number {
    return this.currentIndex / this.tracks.length;
  }

  isCurrentlyPlaying(): boolean {
    return this.isPlaying;
  }
} 