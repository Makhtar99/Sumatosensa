import { useUserPrefStore } from '@/stores/userpref'

export type SensorMeasurements = {
  temperature: number
  humidite: number
  pression: number
  batterie: number
}

export function computeSensorStatus(battery: number): 'Connecté' | 'Batterie faible' | 'Hors ligne' {
  if (battery === 0) return 'Hors ligne'
  if (battery < 20) return 'Batterie faible'
  return 'Connecté'
}

export function computeSensorAlert(measurements: SensorMeasurements): string {
  const { temperature, humidite, pression } = measurements
  const userPref = useUserPrefStore()

  const minTemp = userPref.alertMinTemperatureC
  const maxTemp = userPref.alertMaxTemperatureC
  const minHum = userPref.alertMinHumidite
  const maxHum = userPref.alertMaxHumidite
  const minPress = userPref.alertMinPressionhpa
  const maxPress = userPref.alertMaxPressionhpa

  if (temperature < minTemp) return 'Température trop basse'
  if (temperature > maxTemp) return 'Température trop haute'
  if (humidite < minHum) return 'Humidité trop basse'
  if (humidite > maxHum) return 'Humidité trop haute'
  if (pression < minPress) return 'Pression trop basse'
  if (pression > maxPress) return 'Pression trop haute'
  return ''
}

export function voltageToPercent(voltage?: number): number {
  if (typeof voltage !== 'number') return 0
  const pct = Math.round(((voltage - 2.5) / (3.0 - 2.5)) * 100)
  return Math.max(0, Math.min(100, pct))
}
