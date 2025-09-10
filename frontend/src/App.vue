<template>
  <header>
    <h1>교사업무도우미</h1>
    <nav>
      <router-link to="/">홈</router-link>
      <router-link to="/students/list">학생 목록</router-link>
      <router-link to="/students/entry">학생 정보 입력</router-link>
      <router-link to="/work-log">업무일지</router-link>
      <router-link to="/todos">할 일 목록</router-link>
    </nav>
  </header>
  <main>
    <router-view></router-view>
  </main>
</template>

<script setup>
// 스크립트 코드는 비어 있습니다.
</script>