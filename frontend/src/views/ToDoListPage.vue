<template>
    <main>
      <h1>나의 할 일 목록</h1>
      <div class="todo-list-layout">
        <div class="todo-list-section">
          <h3>📝 할 일</h3>
          <ul class="todo-list">
            <li v-for="todo in incompleteTodos" :key="todo.id" class="todo-item">
              <input type="checkbox" :checked="todo.is_completed" @change="toggleCompletion(todo)" />
              <span class="todo-content">{{ todo.content }}</span>
              <button @click="deleteToDoItem(todo.id)" class="delete-btn">삭제</button>
            </li>
          </ul>
          <p v-if="incompleteTodos.length === 0" class="empty-message">남은 할 일이 없습니다.</p>
        </div>
  
        <div class="todo-list-section">
          <h3>✅ 완료된 할 일</h3>
          <ul class="todo-list">
            <li v-for="todo in completedTodos" :key="todo.id" class="todo-item completed">
              <input type="checkbox" :checked="todo.is_completed" @change="toggleCompletion(todo)" />
              <span class="todo-content">{{ todo.content }}</span>
              <button @click="deleteToDoItem(todo.id)" class="delete-btn">삭제</button>
            </li>
          </ul>
          <p v-if="completedTodos.length === 0" class="empty-message">아직 완료한 할 일이 없습니다.</p>
        </div>
  
        <div class="manual-todo-section">
          <h3>할 일 수동 추가</h3>
          <form @submit.prevent="addManualToDo" class="manual-form">
            <input type="text" v-model="newToDoContent" placeholder="새로운 할 일 입력" required />
            <button type="submit">추가</button>
          </form>
        </div>
      </div>
    </main>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useToDoStore } from '../stores/toDoStore';
  
  const todoStore = useToDoStore();
  const newToDoContent = ref('');
  
  onMounted(() => {
    todoStore.fetchToDos();
  });
  
  // 전체 할 일 목록을 가져오는 Computed Property
  const todos = computed(() => todoStore.todos);
  
  // 완료되지 않은 할 일만 필터링하는 Computed Property
  const incompleteTodos = computed(() => {
    return todos.value.filter(todo => !todo.is_completed);
  });
  
  // 완료된 할 일만 필터링하는 Computed Property
  const completedTodos = computed(() => {
    return todos.value.filter(todo => todo.is_completed);
  });
  
  const toggleCompletion = (todo) => {
    todoStore.updateToDo(todo.id, !todo.is_completed);
  };
  
  const deleteToDoItem = (todoId) => {
    if (confirm('정말로 이 할 일을 삭제하시겠습니까?')) {
      todoStore.deleteToDo(todoId);
    }
  };
  
  const addManualToDo = () => {
    if (newToDoContent.value.trim() !== '') {
      todoStore.createToDo(newToDoContent.value.trim());
      newToDoContent.value = '';
    }
  };
  </script>