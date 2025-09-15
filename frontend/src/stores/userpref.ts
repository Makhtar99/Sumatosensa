import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

// Fonction utilitaire pour stocker dans le localStorage
function usePersistentRef<T>(key: string, defaultValue: T) {
    const storedValue = localStorage.getItem(key)
    const state = ref<T>(storedValue ? JSON.parse(storedValue) : defaultValue)

    watch(state, (newValue) => {
        localStorage.setItem(key, JSON.stringify(newValue))
    }, { deep: true })

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
    const alertHumidite = usePersistentRef<number>("alertHumidite", 30)
    const alertTemperature = usePersistentRef<number>("alertTemperature", 28)
    const alertByEmail = usePersistentRef<boolean>("alertByEmail", false)
    const alertFrequency = usePersistentRef<string>("alertFrequency", "En temps réel")

    // Noms capteurs
    const sensor1name = usePersistentRef<string>("sensor1name", "Salon")
    const sensor2name = usePersistentRef<string>("sensor2name", "Chambre parentale")
    const sensor3name = usePersistentRef<string>("sensor3name", "Grenier")

    return {
        tempUnit,
        pressureUnit,
        humidityUnit,
        decimalDisplay,
        lang,
        alertHumidite,
        alertTemperature,
        alertByEmail,
        alertFrequency,
        sensor1name,
        sensor2name,
        sensor3name
    }
})
