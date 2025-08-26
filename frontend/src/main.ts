import './assets/styles/main.css'

const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | null
const theme = savedTheme ?? 'light'
document.documentElement.setAttribute('data-theme', theme)

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import Primevue from 'primevue/config'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.component('DataTable', DataTable)
app.component('PrimevueColumn', Column)
app.component('PrimevueButton', Button)

app
    .use(createPinia())
    .use(router)
    .use(Primevue)
    .mount('#app')
