<template>
    <main>
      <h1>업무일지</h1>
      <div class="work-log-container">
        <div class="date-picker-section">
          <button @click="goToPreviousDay">이전 날</button>
          <button @click="goToToday">오늘</button>
          <button @click="goToNextDay">다음 날</button>
          <input type="date" id="log-date" v-model="selectedDate" />
        </div>
        
        <div v-if="selectedDate" class="log-editor">
          <h3>{{ selectedDate }} 업무일지</h3>
          <textarea
            v-model="logContent"
            placeholder="오늘의 업무를 기록하세요..."
            rows="15"
          ></textarea>
          <div class="log-actions">
            <button @click="saveLog">저장</button>
            <button @click="extractToDos" class="extract-btn">할 일 추출</button>
            <button v-if="currentLog" @click="deleteLog" class="delete-btn">삭제</button>
          </div>
        </div>
        <p v-else class="info-message">날짜를 선택하여 업무일지를 작성하거나 확인하세요.</p>
      </div>
    </main>
  </template>
  
  <script setup>
  import { ref, watch, computed } from 'vue';
  import { useWorkLogStore } from '../stores/workLogStore';
  import { useToDoStore } from '../stores/toDoStore';
  
  const workLogStore = useWorkLogStore();
  const todoStore = useToDoStore();
  
  const getFormattedDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  };
  
  const today = getFormattedDate(new Date());
  const selectedDate = ref(today);
  const logContent = ref('');
  
  const currentLog = computed(() => workLogStore.currentLog);
  
  watch(selectedDate, async (newDate) => {
    if (newDate) {
      await workLogStore.fetchWorkLogByDate(newDate);
      if (workLogStore.currentLog) {
        logContent.value = workLogStore.currentLog.content;
      } else {
        logContent.value = '';
      }
    }
  }, { immediate: true });
  
  const goToPreviousDay = () => {
    const date = new Date(selectedDate.value);
    date.setDate(date.getDate() - 1);
    selectedDate.value = getFormattedDate(date);
  };
  
  const goToNextDay = () => {
    const date = new Date(selectedDate.value);
    date.setDate(date.getDate() + 1);
    selectedDate.value = getFormattedDate(date);
  };
  
  const goToToday = () => {
    selectedDate.value = getFormattedDate(new Date());
  };
  
  const saveLog = async () => {
    if (logContent.value.trim() === '') {
      alert('내용을 입력해주세요.');
      return;
    }
    const logData = {
      date: selectedDate.value,
      content: logContent.value,
    };
    try {
      await workLogStore.saveWorkLog(logData);
      alert('업무일지가 저장되었습니다.');
    } catch (error) {
      alert('업무일지 저장에 실패했습니다.');
    }
  };
  
  const deleteLog = async () => {
    if (confirm(`${selectedDate.value}의 업무일지를 삭제하시겠습니까?`)) {
      try {
        await workLogStore.deleteWorkLog(selectedDate.value);
        alert('업무일지가 삭제되었습니다.');
        logContent.value = '';
        workLogStore.currentLog = null;
      } catch (error) {
        alert('업무일지 삭제에 실패했습니다.');
      }
    }
  };
  
  const extractToDos = async () => {
    if (logContent.value.trim() !== '') {
      if (confirm('업무일지에서 할 일을 추출하여 할 일 목록에 추가하시겠습니까?')) {
        await todoStore.extractToDosFromLog(logContent.value);
      }
    } else {
      alert('업무일지 내용이 비어있습니다.');
    }
  };
  </script>