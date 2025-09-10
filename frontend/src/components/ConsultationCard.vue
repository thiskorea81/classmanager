<template>
    <div class="consultation-card-container">
      <h3>상담 기록</h3>
      <div
        v-if="student.consultations && student.consultations.length > 0"
        class="consultation-list"
      >
        <div v-for="(consultation, index) in student.consultations" :key="index" class="consultation-item">
          <p class="consultation-date">
            <strong>상담 일자:</strong> {{ new Date(consultation.date).toLocaleString() }}
          </p>
          <p class="consultation-content">{{ consultation.content }}</p>
        </div>
      </div>
      <div v-else class="no-consultation-message">
        <p>기존 상담 기록이 없습니다.</p>
      </div>
  
      <div class="add-consultation-form">
        <h4>새로운 상담 추가</h4>
        <textarea
          v-model="newConsultationContent"
          placeholder="상담 내용을 입력하세요..."
          rows="5"
        ></textarea>
        <button @click="addConsultation">상담 기록 저장</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { defineProps, ref } from 'vue';
  import { useStudentStore } from '../stores/studentStore';
  
  const props = defineProps({
    student: {
      type: Object,
      required: true,
    },
  });
  
  const studentStore = useStudentStore();
  const newConsultationContent = ref('');
  
  const addConsultation = async () => {
    if (newConsultationContent.value.trim() !== '') {
      try {
        const consultationData = {
          date: new Date().toISOString(),
          content: newConsultationContent.value.trim(),
        };
        await studentStore.addConsultation(props.student.id, consultationData);
        alert('상담 기록이 저장되었습니다.');
        newConsultationContent.value = '';
      } catch (error) {
        alert('상담 기록 저장에 실패했습니다.');
      }
    } else {
      alert('상담 내용을 입력해주세요.');
    }
  };
  </script>