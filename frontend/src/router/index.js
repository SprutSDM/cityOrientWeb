import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/login/LoginVue.vue'
import Quests from '../views/quests/QuestsVue.vue'
import QuestEdit from "../views/questedit/QuestEditVue";
import Teams from "../views/teams/Teams";
import MainNavbar from "../layout/MainNavbar";
import LoginNavbar from "../layout/LoginNavbar";
import Statistic from "../views/statistic/StatisticVue";

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/quests'
    },
    {
        path: '/login',
        name: 'login',
        components: { default: Login, header: LoginNavbar }
    },
    {
        path: '/quests',
        name: 'quests',
        components: { default: Quests, header: MainNavbar }
    },
    {
        path: '/quests/:id',
        name: 'editQuest',
        components: { default: QuestEdit, header: MainNavbar }
    },
    {
        path: '/createQuest',
        name: 'createQuest',
        components: { default: QuestEdit, header: MainNavbar }
    },
    {
        path: '/teams',
        name: 'teams',
        components: { default: Teams, header: MainNavbar }
    },
    {
        path: '/quests/:id/statistic',
        name: 'statistic',
        components: { default: Statistic, header: MainNavbar }
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
