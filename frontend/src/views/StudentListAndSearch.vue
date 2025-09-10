<template>
  <main>
    <h1>학생 목록</h1>
    <div class="list-search-layout">
      <div class="search-section">
        <h3>학생 검색</h3>
        <div class="search-container">
          <input type="text" v-model="searchQuery" placeholder="이름으로 검색..." />
          <button @click="clearSearch">초기화</button>
        </div>
        <div class="student-list-actions">
          <button @click="clearAllStudents" class="delete-all-btn">학생 목록 전체 삭제</button>
        </div>
      </div>
      <div class="list-section">
        <h3>전체 학생 목록</h3>
        <StudentList :students="filteredStudents" />
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStudentStore } from '../stores/studentStore';
import StudentList from '../components/StudentList.vue';

const studentStore = useStudentStore();
const searchQuery = ref('');

onMounted(() => {
  studentStore.fetchStudents();
});

const filteredStudents = computed(() => {
  if (!searchQuery.value) {
    return studentStore.students;
  }
  const query = searchQuery.value.toLowerCase();
  return studentStore.students.filter((student) =>
    student.name.toLowerCase().includes(query)
  );
});

const clearSearch = () => {
  searchQuery.value = '';
};

const clearAllStudents = async () => {
  if (confirm('모든 학생 정보를 정말로 삭제하시겠습니까?')) {
    try {
      await studentStore.deleteAllStudents();
      alert('모든 학생 정보가 삭제되었습니다.');
    } catch (error) {
      alert('모든 학생 삭제에 실패했습니다.');
    }
  }
};
</script>