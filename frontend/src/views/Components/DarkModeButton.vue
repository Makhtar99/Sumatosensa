<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMediaQuery } from '@vueuse/core'
import Sun from '@/assets/svg/sun.svg'
import Moon from '@/assets/svg/moon.svg'

const isDark = ref(false)
const isTelephone = useMediaQuery('(max-width: 768px)')

const readTheme = () => document.documentElement.getAttribute('data-theme') === 'dark'
const applyTheme = (dark: boolean) => {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  localStorage.setItem('theme', dark ? 'dark' : 'light')
  isDark.value = dark
}

const toggle = () => applyTheme(!isDark.value)

onMounted(() => {
  isDark.value = readTheme()
})
</script>

 <template>
  <div>
    <button type="button" @click="toggle" class="flex justify-center items-center space-x-2 gap-2">
      <img v-if="!isTelephone" :src="isDark ? Sun : Moon" alt="Toggle Dark Mode" class="w-5 h-5" />
      {{ isDark ? 'Clair' : 'Sombre' }}
    </button>
  </div>
</template>