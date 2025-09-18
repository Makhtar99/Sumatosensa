import { ref, watch, onMounted, computed, type Ref } from "vue"

const isClient = typeof window !== "undefined"

// localStorage 
export function usePersistentRef<T>(key: string, defaultValue: T): Ref<T> {
  const state = ref<T>(defaultValue) as Ref<T>

  const load = () => {
    if (!isClient) return
    const raw = window.localStorage.getItem(key)
    if (raw !== null) {
      try { state.value = JSON.parse(raw) } catch {}
    }
  }

  const save = (value: T) => {
    if (!isClient) return
    try { window.localStorage.setItem(key, JSON.stringify(value)) } catch {}
  }

  if (isClient) {
    try {
      const raw = window.localStorage.getItem(key)
      if (raw !== null) state.value = JSON.parse(raw)
    } catch {}
  }

  onMounted(load)
  watch(state, (v) => save(v), { deep: true })

  return state
}

// localStorage 
export function bindPersistentRef<T>(r: Ref<T>, key: string): void {
  const load = () => {
    if (!isClient) return
    const raw = window.localStorage.getItem(key)
    if (raw !== null) {
      try { r.value = JSON.parse(raw) } catch {}
    }
  }

  const save = (value: T) => {
    if (!isClient) return
    try { window.localStorage.setItem(key, JSON.stringify(value)) } catch {}
  }

  if (isClient) {
    try {
      const raw = window.localStorage.getItem(key)
      if (raw !== null) r.value = JSON.parse(raw)
    } catch {}
  }

  onMounted(load)
  watch(r, (v) => save(v), { deep: true })
}

  //Conversion °C <-> °F

export function useTemperatureUnit(
  celsiusValue: Ref<number>,
  unit: Ref<"Celsius" | "Fahrenheit">
) {
// temperature conversion
  const temperature = computed({
    get() {
      if (unit.value === "Celsius") return celsiusValue.value
      return celsiusValue.value * 9/5 + 32
    },
    set(v: number) {
      if (unit.value === "Celsius") celsiusValue.value = v
      else celsiusValue.value = (v - 32) * 5/9
    }
  })

  return temperature
}
