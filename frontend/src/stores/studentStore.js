import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../api/axios';

export const useStudentStore = defineStore('student', () => {
  const students = ref([]);

  // API로부터 모든 학생 목록을 가져오는 비동기 함수
  const fetchStudents = async () => {
    try {
      const response = await apiClient.get('/students/');
      students.value = response.data;
    } catch (error) {
      console.error('학생 목록을 가져오는 데 실패했습니다:', error);
      throw error;
    }
  };

  // 새로운 학생을 백엔드에 추가하는 비동기 함수
  const addStudent = async (student) => {
    try {
      const response = await apiClient.post('/students/', student);
      students.value.push(response.data);
      return response.data;
    } catch (error) {
      console.error('학생 추가에 실패했습니다:', error);
      throw error;
    }
  };

  // 여러 명의 학생을 한 번에 추가하는 비동기 함수
  const addStudents = async (newStudents) => {
    try {
      const promises = newStudents.map((student) => apiClient.post('/students/', student));
      const responses = await Promise.all(promises);
      responses.forEach((response) => students.value.push(response.data));
    } catch (error) {
      console.error('학생들을 추가하는 데 실패했습니다:', error);
      throw error;
    }
  };

  // 기존 학생 정보를 업데이트하는 비동기 함수
  const updateStudent = async (updatedStudent) => {
    try {
      const response = await apiClient.put(`/students/${updatedStudent.id}`, updatedStudent);
      const index = students.value.findIndex((s) => s.id === updatedStudent.id);
      if (index !== -1) {
        students.value[index] = response.data;
      }
      return response.data;
    } catch (error) {
      console.error('학생 정보 수정에 실패했습니다:', error);
      throw error;
    }
  };

  // 특정 학생을 삭제하는 비동기 함수
  const deleteStudent = async (studentId) => {
    try {
      await apiClient.delete(`/students/${studentId}`);
      students.value = students.value.filter((s) => s.id !== studentId);
    } catch (error) {
      console.error('학생 삭제에 실패했습니다:', error);
      throw error;
    }
  };

  // 모든 학생을 삭제하는 비동기 함수
  const deleteAllStudents = async () => {
    try {
      await apiClient.delete('/students/');
      students.value = [];
    } catch (error) {
      console.error('모든 학생 삭제에 실패했습니다:', error);
      throw error;
    }
  };

  // 특정 학생의 상담 기록을 추가하는 비동기 함수
  const addConsultation = async (studentId, consultation) => {
    try {
      const response = await apiClient.post(`/students/${studentId}/consultations`, consultation);
      const studentIndex = students.value.findIndex((s) => s.id === studentId);
      if (studentIndex !== -1) {
        // 서버에서 업데이트된 학생 정보로 스토어 업데이트
        students.value[studentIndex] = response.data;
      }
      return response.data;
    } catch (error) {
      console.error('상담 기록 추가에 실패했습니다:', error);
      throw error;
    }
  };

  // ID로 학생 정보를 찾는 함수 (로컬 데이터)
  const getStudentById = (id) => {
    return students.value.find((student) => student.id === parseInt(id));
  };

  return {
    students,
    fetchStudents,
    addStudent,
    addStudents,
    updateStudent,
    deleteStudent,
    deleteAllStudents,
    addConsultation,
    getStudentById,
  };
});