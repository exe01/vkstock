import Vue from 'vue';
import VueRouter from 'vue-router';
import Dashboard from '@/views/Dashboard';
import NotFound from '@/views/errors/404';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    component: Dashboard,
  },
  {
    path: '/projects/:id',
    name: 'projects',
    component: () => import('@/views/project/Project'),
    // props: true
  },
  {
    path: '*',
    component: NotFound,
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
