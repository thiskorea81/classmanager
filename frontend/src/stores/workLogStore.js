// src/stores/workLogStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../api/axios';

export const useWorkLogStore = defineStore('workLog', () => {
  const workLogs = ref([]);
  const currentLog = ref(null);

  // 모든 업무일지를 가져오는 API
  const fetchWorkLogs = async () => {
    try {
      const response = await apiClient.get('/work-logs/');
      workLogs.value = response.data;
    } catch (error) {
      console.error('업무일지를 가져오는 데 실패했습니다:', error);
    }
  };

  // 특정 날짜의 업무일지를 가져오는 API
  const fetchWorkLogByDate = async (logDate) => {
    try {
      const response = await apiClient.get(`/work-logs/${logDate}`);
      currentLog.value = response.data;
    } catch (error) {
      if (error.response && error.response.status === 404) {
        currentLog.value = null; // 해당 날짜에 일지가 없으면 null로 설정
      } else {
        console.error('해당 날짜의 업무일지를 가져오는 데 실패했습니다:', error);
      }
    }
  };

  // 업무일지를 저장하거나 업데이트하는 API
  const saveWorkLog = async (logData) => {
    try {
      const response = await apiClient.post('/work-logs/', logData);
      currentLog.value = response.data;
      await fetchWorkLogs(); // 목록 새로고침
    } catch (error) {
      console.error('업무일지 저장에 실패했습니다:', error);
      throw error;
    }
  };

  // 업무일지를 삭제하는 API
  const deleteWorkLog = async (logDate) => {
    try {
      await apiClient.delete(`/work-logs/${logDate}`);
      await fetchWorkLogs(); // 목록 새로고침
    } catch (error) {
      console.error('업무일지 삭제에 실패했습니다:', error);
      throw error;
    }
  };

  return {
    workLogs,
    currentLog,
    fetchWorkLogs,
    fetchWorkLogByDate,
    saveWorkLog,
    deleteWorkLog,
  };
});