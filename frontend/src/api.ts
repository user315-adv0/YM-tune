import axios from 'axios';

export interface Track {
  title: string;
  artist: string;
  url: string;
  duration: number;
  bpm?: number;
  onsets?: number[];
}

const API_BASE = 'http://localhost:8000';

export async function fetchPlaylist(id: string): Promise<Track[]> {
  try {
    const { data } = await axios.get<Track[]>(`${API_BASE}/playlist/${id}`);
    return data;
  } catch (error) {
    console.error('Ошибка при получении плейлиста:', error);
    throw new Error('Не удалось загрузить плейлист');
  }
}

export async function checkHealth(): Promise<boolean> {
  try {
    const { data } = await axios.get(`${API_BASE}/health`);
    return data.yandex_connected;
  } catch {
    return false;
  }
} 