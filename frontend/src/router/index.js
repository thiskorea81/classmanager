import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/HomePage.vue';
import StudentDetail from '../views/StudentDetail.vue';
import StudentEntry from '../views/StudentEntry.vue';
import StudentListAndSearch from '../views/StudentListAndSearch.vue';
import WorkLogPage from '../views/WorkLogPage.vue';
import ToDoListPage from '../views/ToDoListPage.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomePage,
    },
    {
      path: '/students/list',
      name: 'StudentListAndSearch',
      component: StudentListAndSearch,
    },
    {
      path: '/students/entry',
      name: 'StudentEntry',
      component: StudentEntry,
    },
    {
      path: '/students/:id',
      name: 'StudentDetail',
      component: StudentDetail,
      props: true,
    },
    {
      path: '/work-log',
      name: 'WorkLog',
      component: WorkLogPage,
    },
    {
      path: '/todos',
      name: 'ToDos',
      component: ToDoListPage,
    },
  ],
});

export default router;