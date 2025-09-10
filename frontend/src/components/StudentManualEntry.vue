<template>
  <div class="manual-input-container">
    <h3>학생 정보 수동 입력</h3>
    <form @submit.prevent="addStudent">
      <div class="form-group">
        <label for="grade">학년:</label>
        <input type="number" id="grade" v-model="newStudent.grade" required />
      </div>
      <div class="form-group">
        <label for="classNum">반:</label>
        <input type="number" id="classNum" v-model="newStudent.classNum" required />
      </div>
      <div class="form-group">
        <label for="studentNum">번호:</label>
        <input type="number" id="studentNum" v-model="newStudent.studentNum" required />
      </div>
      <div class="form-group">
        <label for="name">이름:</label>
        <input type="text" id="name" v-model="newStudent.name" required />
      </div>
      <div class="form-group">
        <label for="phone">전화번호:</label>
        <input type="text" id="phone" v-model="newStudent.phone" />
      </div>
      <div class="form-group">
        <label for="address">주소:</label>
        <input type="text" id="address" v-model="newStudent.address" />
      </div>
      <div class="form-group">
        <label for="guardianPhone1">보호자1 연락처:</label>
        <input type="text" id="guardianPhone1" v-model="newStudent.guardianPhone1" />
      </div>
      <div class="form-group">
        <label for="guardianPhone2">보호자2 연락처:</label>
        <input type="text" id="guardianPhone2" v-model="newStudent.guardianPhone2" />
      </div>
      <button type="submit">학생 추가</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useStudentStore } from '../stores/studentStore';
import { useRouter } from 'vue-router';

const studentStore = useStudentStore();
const router = useRouter();

const newStudent = ref({
  grade: null,
  classNum: null,
  studentNum: null,
  name: '',
  phone: '',
  address: '',
  guardianPhone1: '',
  guardianPhone2: '',
});

const addStudent = async () => {
  if (
    newStudent.value.name &&
    newStudent.value.grade &&
    newStudent.value.classNum &&
    newStudent.value.studentNum
  ) {
    const studentData = {
      grade: newStudent.value.grade,
      class_num: newStudent.value.classNum,
      student_num: newStudent.value.studentNum,
      name: newStudent.value.name,
      phone: newStudent.value.phone || null,
      address: newStudent.value.address || null,
      guardian_phone1: newStudent.value.guardianPhone1 || null,
      guardian_phone2: newStudent.value.guardianPhone2 || null,
    };
    try {
      await studentStore.addStudent(studentData);
      alert(`${studentData.name} 학생이 추가되었습니다.`);
      newStudent.value = {
        grade: null,
        classNum: null,
        studentNum: null,
        name: '',
        phone: '',
        address: '',
        guardianPhone1: '',
        guardianPhone2: '',
      };
      router.push('/students/list');
    } catch (error) {
      alert('학생 추가에 실패했습니다. 콘솔을 확인해주세요.');
    }
  } else {
    alert('필수 정보를 모두 입력해주세요 (학년, 반, 번호, 이름).');
  }
};
</script>