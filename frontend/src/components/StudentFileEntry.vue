<template>
  <div class="file-upload-container">
    <h3>파일로 학생 정보 가져오기</h3>
    <input type="file" ref="fileInput" @change="handleFileUpload" accept=".csv, .tsv, .xlsx, .xls" />
    <button @click="processFileData">학생 목록 가져오기</button>
    <p class="guide-text">
      지원 파일: CSV, TSV, 엑셀 파일 (.csv, .tsv, .xlsx, .xls)<br />
      파일의 첫 번째 행은 "학년,반,번호,이름,전화번호,주소,보호자연락처1,보호자연락처2" 순서여야 합니다.
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useStudentStore } from '../stores/studentStore';
import { useRouter } from 'vue-router';
import * as Papa from 'papaparse';
import * as XLSX from 'xlsx';

const studentStore = useStudentStore();
const router = useRouter();

const fileInput = ref(null);
const fileData = ref(null);
const fileType = ref(null);

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const fileName = file.name;
  const extension = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
  fileType.value = extension;

  const reader = new FileReader();
  if (extension === 'xlsx' || extension === 'xls') {
    reader.onload = (e) => {
      fileData.value = e.target.result;
    };
    reader.readAsArrayBuffer(file);
  } else {
    reader.onload = (e) => {
      fileData.value = e.target.result;
    };
    reader.readAsText(file);
  }
};

const processFileData = () => {
  if (!fileData.value) {
    alert('먼저 파일을 선택해주세요.');
    return;
  }

  let parsedData = [];
  if (fileType.value === 'csv' || fileType.value === 'tsv') {
    Papa.parse(fileData.value, {
      delimiter: fileType.value === 'tsv' ? '\t' : ',',
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: (results) => {
        parsedData = results.data;
      },
    });
  } else if (fileType.value === 'xlsx' || fileType.value === 'xls') {
    const workbook = XLSX.read(fileData.value, { type: 'array' });
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    parsedData = XLSX.utils.sheet_to_json(worksheet);
  }

  const newStudents = parsedData.map((row) => ({
    grade: row['학년'],
    class_num: row['반'],
    student_num: row['번호'],
    name: row['이름'],
    phone: row['전화번호'] || null,
    address: row['주소'] || null,
    guardian_phone1: row['보호자연락처1'] || null,
    guardian_phone2: row['보호자연락처2'] || null,
  }));

  studentStore.addStudents(newStudents);
  alert(`${newStudents.length}명의 학생이 추가되었습니다.`);
  fileInput.value.value = '';
  fileData.value = null;
  router.push('/students/list');
};
</script>