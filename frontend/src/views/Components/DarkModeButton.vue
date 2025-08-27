 <template>
  <div class="flex justify-center items-center space-x-2">
    <button type="button" @click="toggle">
    {{ isDark ? 'Mode clair' : 'Mode sombre' }}
  </button>
  
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const isDark = ref(false)

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
