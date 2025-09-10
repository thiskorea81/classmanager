<template>
    <main>
      <h1>학생 정보 입력</h1>
      <StudentFileEntry />
      <hr />
      <StudentManualEntry />
    </main>
  </template>
  
  <script setup>
  import StudentFileEntry from '../components/StudentFileEntry.vue';
  import StudentManualEntry from '../components/StudentManualEntry.vue';
  </script>