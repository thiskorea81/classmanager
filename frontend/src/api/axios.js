import axios from 'axios';

// 백엔드 서버의 기본 URL을 설정
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;