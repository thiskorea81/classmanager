<template>
    <div class="summary-card">
      <h3>📝 상담 기록 요약</h3>
      <p v-if="summaryText">{{ summaryText }}</p>
      <p v-else class="loading-text">요약 중입니다...</p>
    </div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue';
  
  const props = defineProps({
    summaryText: {
      type: String,
      default: ''
    }
  });
  </script>