import { createWebHistory, createRouter } from "vue-router";

import MainPage from "./apps/MainPage.vue";
import EventsPage from "./apps/EventsPage.vue";

const routes = [
    {
        path: '/',
        component: MainPage
    },
    {
        path: '/events',
        component: EventsPage
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes: routes,
});


export default router;