import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../api/axios';

export const useToDoStore = defineStore('todo', () => {
  const todos = ref([]);

  // 할 일 목록을 백엔드에서 불러오기
  const fetchToDos = async () => {
    try {
      const response = await apiClient.get('/todos/');
      todos.value = response.data;
    } catch (error) {
      console.error('할 일 목록을 불러오는 데 실패했습니다:', error);
    }
  };

  // 새로운 할 일 추가
  const createToDo = async (content) => {
    try {
      const response = await apiClient.post('/todos/', { content });
      todos.value.push(response.data);
    } catch (error) {
      console.error('할 일 추가에 실패했습니다:', error);
      throw error;
    }
  };

  // 할 일 상태 업데이트
  const updateToDo = async (todoId, isCompleted) => {
    try {
      const response = await apiClient.put(`/todos/${todoId}`, { is_completed: isCompleted });
      const index = todos.value.findIndex(todo => todo.id === todoId);
      if (index !== -1) {
        todos.value[index] = response.data;
      }
    } catch (error) {
      console.error('할 일 업데이트에 실패했습니다:', error);
    }
  };

  // 할 일 삭제
  const deleteToDo = async (todoId) => {
    try {
      await apiClient.delete(`/todos/${todoId}`);
      todos.value = todos.value.filter(todo => todo.id !== todoId);
    } catch (error) {
      console.error('할 일 삭제에 실패했습니다:', error);
    }
  };

  // 업무일지에서 할 일 추출 (Gemini API 사용)
  const extractToDosFromLog = async (logContent) => {
    try {
      const response = await apiClient.post('/todos/from-log/', { 
        date: new Date().toISOString().split('T')[0],
        content: logContent 
      });
      todos.value.push(...response.data);
      alert(`${response.data.length}개의 새로운 할 일이 업무일지에서 추출되었습니다!`);
    } catch (error) {
      console.error('업무일지에서 할 일을 추출하는 데 실패했습니다:', error);
      alert('할 일 추출에 실패했습니다. 업무일지 내용이 너무 짧거나 오류가 발생했을 수 있습니다.');
    }
  };

  return { todos, fetchToDos, createToDo, updateToDo, deleteToDo, extractToDosFromLog };
});