<template>
    <div v-if="student">
      <h2>학생 상세 정보</h2>
      <div class="student-details-layout">
        <div class="info-section">
          <StudentInfo :student="student" />
        </div>
        <div class="consultation-section">
          <ConsultationSummary :summary-text="consultationSummary" />
          <ConsultationCard :student="student" />
        </div>
      </div>
    </div>
    <div v-else>
      <p>학생 정보를 찾을 수 없습니다.</p>
    </div>
  </template>
  
  <script setup>
  import { defineProps, computed, ref, watch } from 'vue';
  import { useStudentStore } from '../stores/studentStore';
  import StudentInfo from '../components/StudentInfo.vue';
  import ConsultationCard from '../components/ConsultationCard.vue';
  import ConsultationSummary from '../components/ConsultationSummary.vue';
  import apiClient from '../api/axios';
  
  const props = defineProps({
    id: {
      type: [String, Number],
      required: true,
    },
  });
  
  const studentStore = useStudentStore();
  const consultationSummary = ref('');
  
  const student = computed(() => {
    return studentStore.getStudentById(parseInt(props.id));
  });
  
  const fetchSummary = async (studentId, consultations) => {
    if (!consultations || consultations.length === 0) {
      consultationSummary.value = '상담 기록이 없습니다.';
      return;
    }
    try {
      const response = await apiClient.post(`/students/${studentId}/summarize-consultations`, {
        consultations: consultations,
      });
      consultationSummary.value = response.data.summary;
    } catch (error) {
      console.error('상담 요약 불러오기 실패:', error);
      consultationSummary.value = '요약에 실패했습니다.';
    }
  };
  
  watch(
    student,
    (newStudent) => {
      if (newStudent) {
        fetchSummary(newStudent.id, newStudent.consultations);
      }
    },
    { immediate: true }
  );
  </script>