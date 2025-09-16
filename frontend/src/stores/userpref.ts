import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

// Fonction utilitaire pour stocker dans le localStorage
function usePersistentRef<T>(key: string, defaultValue: T) {
  const storedValue = localStorage.getItem(key)
  let parsed: T

  try {
    parsed = storedValue !== null ? JSON.parse(storedValue) : defaultValue
  } catch {
    parsed = defaultValue
  }

  const state = ref<T>(parsed)

  watch(
    state,
    (newValue) => {
      localStorage.setItem(key, JSON.stringify(newValue))
    },
    { deep: true }
  )

  return state
}

    export const useUserPrefStore = defineStore('userPref', () => {
    // Température
    const tempUnit = usePersistentRef<"Celsius" | "Fahrenheit">("temperatureUnit", "Celsius")

    // Autres unités
    const pressureUnit = usePersistentRef<string>("pressureUnit", "hPa")
    const humidityUnit = usePersistentRef<string>("humidityUnit", "%")

    // Affichage
    const decimalDisplay = usePersistentRef<boolean>("decimalDisplay", true)
    const lang = usePersistentRef<string>("lang", "fr")

    // Alertes
    const alertMinHumidite = usePersistentRef<number>("alertMinHumidite", 30)
    const alertMaxHumidite = usePersistentRef<number>("alertMaxHumidite", 70)
    const alertMinTemperatureC = usePersistentRef<number>("alertMinTemperatureC", 0)
    const alertMaxTemperatureC = usePersistentRef<number>("alertMaxTemperatureC", 28)
    const alertMinTemperatureF = usePersistentRef<number>("alertMinTemperatureF", 32)
    const alertMaxTemperatureF = usePersistentRef<number>("alertMaxTemperatureF", 82)
    
    const alertMinPressionhpa = usePersistentRef<number>("alertMinPressionhpa", 980)
    const alertMaxPressionhpa = usePersistentRef<number>("alertMaxPressionhpa", 1050)
    const alertMinPressionbar = usePersistentRef<number>("alertMinPressionbar", 0.98)
    const alertMaxPressionbar = usePersistentRef<number>("alertMaxPressionbar", 1.05)
    const alertMinPressionInHg = usePersistentRef<number>("alertMinPressionInHg", 28.9)
    const alertMaxPressionInHg = usePersistentRef<number>("alertMaxPressionInHg", 31.0)

    const alertByEmail = usePersistentRef<boolean>("alertByEmail", false)
    const alertFrequency = usePersistentRef<string>("alertFrequency", "En temps réel")

    // Noms capteurs
    const sensor1name = usePersistentRef<string>("sensor1name", "Salon")
    const sensor2name = usePersistentRef<string>("sensor2name", "Chambre parentale")
    const sensor3name = usePersistentRef<string>("sensor3name", "Grenier")

    // form d'inscription
    const hasDoneOnboarding = usePersistentRef<boolean>("hasDoneOnboarding", false)

    const userCity = usePersistentRef<string>("userCity", "Paris")

    return {
        tempUnit,
        pressureUnit,
        humidityUnit,
        decimalDisplay,
        lang,
        alertMinHumidite,
        alertMaxHumidite,
        alertMinTemperatureC,
        alertMaxTemperatureC,
        alertMinTemperatureF,
        alertMaxTemperatureF,
        alertMinPressionhpa,
        alertMaxPressionhpa,
        alertMinPressionbar,
        alertMaxPressionbar,
        alertMinPressionInHg,
        alertMaxPressionInHg,
        alertByEmail,
        alertFrequency,
        sensor1name,
        sensor2name,
        sensor3name,
        hasDoneOnboarding,
        userCity
    }
})
