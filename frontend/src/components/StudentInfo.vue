<template>
    <div>
      <div class="student-actions">
        <button @click="isEditing = !isEditing">{{ isEditing ? '취소' : '수정하기' }}</button>
        <button @click="deleteStudent" class="delete-btn">삭제하기</button>
      </div>
  
      <div v-if="!isEditing" class="detail-info">
        <p><strong>학년:</strong> {{ student.grade }}학년</p>
        <p><strong>반:</strong> {{ student.class_num }}반</p>
        <p><strong>번호:</strong> {{ student.student_num }}번</p>
        <p><strong>이름:</strong> {{ student.name }}</p>
        <p><strong>전화번호:</strong> {{ student.phone }}</p>
        <p><strong>주소:</strong> {{ student.address }}</p>
        <p><strong>보호자1 연락처:</strong> {{ student.guardian_phone1 }}</p>
        <p><strong>보호자2 연락처:</strong> {{ student.guardian_phone2 }}</p>
      </div>
  
      <form v-else @submit.prevent="updateStudent" class="edit-form">
        <div class="form-group">
          <label>학년:</label>
          <input type="number" v-model="editableStudent.grade" required />
        </div>
        <div class="form-group">
          <label>반:</label>
          <input type="number" v-model="editableStudent.class_num" required />
        </div>
        <div class="form-group">
          <label>번호:</label>
          <input type="number" v-model="editableStudent.student_num" required />
        </div>
        <div class="form-group">
          <label>이름:</label>
          <input type="text" v-model="editableStudent.name" required />
        </div>
        <div class="form-group">
          <label>전화번호:</label>
          <input type="text" v-model="editableStudent.phone" />
        </div>
        <div class="form-group">
          <label>주소:</label>
          <input type="text" v-model="editableStudent.address" />
        </div>
        <div class="form-group">
          <label>보호자1 연락처:</label>
          <input type="text" v-model="editableStudent.guardian_phone1" />
        </div>
        <div class="form-group">
          <label>보호자2 연락처:</label>
          <input type="text" v-model="editableStudent.guardian_phone2" />
        </div>
        <button type="submit">저장</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { defineProps, ref, watch } from 'vue';
  import { useStudentStore } from '../stores/studentStore';
  import { useRouter } from 'vue-router';
  
  const props = defineProps({
    student: {
      type: Object,
      required: true,
    },
  });
  
  const studentStore = useStudentStore();
  const router = useRouter();
  
  const isEditing = ref(false);
  const editableStudent = ref({});
  
  watch(
    () => props.student,
    (newVal) => {
      if (newVal) {
        // API 필드명과 일치하도록 속성 복사
        editableStudent.value = { 
          ...newVal,
          class_num: newVal.class_num,
          student_num: newVal.student_num,
          guardian_phone1: newVal.guardian_phone1,
          guardian_phone2: newVal.guardian_phone2
        };
      }
    },
    { immediate: true }
  );
  
  const updateStudent = async () => {
    if (editableStudent.value) {
      try {
        await studentStore.updateStudent(editableStudent.value);
        isEditing.value = false;
        alert('학생 정보가 수정되었습니다.');
      } catch (error) {
        alert('학생 정보 수정에 실패했습니다.');
      }
    }
  };
  
  const deleteStudent = async () => {
    if (confirm(`${props.student.name} 학생 정보를 정말로 삭제하시겠습니까?`)) {
      try {
        await studentStore.deleteStudent(props.student.id);
        alert('학생 정보가 삭제되었습니다.');
        router.push('/students/list');
      } catch (error) {
        alert('학생 정보 삭제에 실패했습니다.');
      }
    }
  };
  </script>