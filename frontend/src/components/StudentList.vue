<template>
  <div>
    <ul v-if="props.students.length > 0">
      <li v-for="student in props.students" :key="student.id">
        <router-link :to="{ name: 'StudentDetail', params: { id: student.id } }">
          {{ student.grade }}학년 {{ student.class_num }}반 {{ student.student_num }}번 {{ student.name }}
        </router-link>
      </li>
    </ul>
    <p v-else>학생 정보가 없습니다. 파일을 업로드하거나 수동으로 추가해 보세요.</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  students: {
    type: Array,
    required: true,
  },
});
</script>