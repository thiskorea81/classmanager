<template>
  <main>
    <h1>교사업무도우미에 오신 것을 환영합니다!</h1>
    <p>
      이 프로그램은 담임 교사의 학생 관리 및 학급 업무를 효율적으로 지원하기 위해 만들어졌습니다.
      아래의 주요 기능을 통해 편리하게 업무를 처리해 보세요.
    </p>

    <div class="feature-card-container">
      <div class="feature-card">
        <h3>학생 관리</h3>
        <p>
          학급 학생들의 정보를 한눈에 확인하고, 이름으로 쉽게 검색할 수 있습니다.
          개별 학생의 상세 정보(수정, 삭제, 상담 기록)를 관리할 수 있습니다.
        </p>
        <router-link to="/students/list" class="go-btn">학생 목록으로 이동</router-link>
      </div>

      <div class="feature-card">
        <h3>학생 정보 입력</h3>
        <p>
          새로운 학생 정보를 수동으로 입력하거나, CSV, TSV, 엑셀 파일을 업로드하여
          한 번에 여러 학생의 정보를 추가할 수 있습니다.
        </p>
        <router-link to="/students/entry" class="go-btn">정보 입력 페이지로 이동</router-link>
      </div>

      <div class="feature-card">
        <h3>업무일지 기록</h3>
        <p>
          매일의 교사업무를 날짜별로 기록하고 관리하세요.
          '이전/다음 날' 버튼을 통해 편리하게 일지를 확인하고 수정할 수 있습니다.
        </p>
        <router-link to="/work-log" class="go-btn">업무일지 페이지로 이동</router-link>
      </div>
      
      <div class="feature-card">
        <h3>할 일 목록</h3>
        <p>
          업무일지에서 자동으로 할 일 목록을 추출하거나, 수동으로 입력하여
          오늘의 할 일을 체계적으로 관리하고 완료 여부를 체크할 수 있습니다.
        </p>
        <router-link to="/todos" class="go-btn">할 일 목록으로 이동</router-link>
      </div>
    </div>
  </main>
</template>

<script setup>
// 스크립트 코드는 비어 있습니다.
</script>