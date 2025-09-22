const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: {
    id: number
    username: string
    email: string
    role: string
    is_active: boolean
    created_at: string
  }
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface RegisterResponse {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
  created_at: string
}

export interface User {
  id: number
  username: string
  email: string
  role: string
  is_active: boolean
  created_at: string
}

export interface AdminDashboard {
  total_sensors: number
  active_sensors: number
  unresolved_alerts: number
  total_users: number
}

export interface Sensor {
  id: number
  mac_address: string
  name: string
  is_active: boolean
  battery_level: number | null
  firmware_version: string | null
  last_seen: string | null
  created_at: string
  updated_at: string
  last_measurement: {
    temperature: number | null
    humidity: number | null
    pressure: number | null
    battery_voltage: number | null
    time: string | null
  } | null
}

export interface Measurement {
  time: string
  temperature: number | null
  humidity: number | null
  pressure: number | null
  acceleration_x: number | null
  acceleration_y: number | null
  acceleration_z: number | null
  rssi: number | null
  battery_voltage: number | null
  movement_counter: number | null
}

export interface SensorMeasurementsResponse {
  sensor_id: number
  sensor_name: string
  sensor_mac: string
  measurement_count: number
  measurements: Measurement[]
}

export interface SensorLatestResponse {
  sensor_id: number
  sensor_name: string
  sensor_mac: string
  measurement: (Measurement & { age_seconds: number }) | null
  message?: string
}

export interface SensorStatsResponse {
  sensor_id: number
  sensor_name: string
  period_hours: number
  measurement_count: number
  statistics: {
    temperature: {
      average: number
      minimum: number
      maximum: number
    }
    humidity: {
      average: number
      minimum: number
      maximum: number
    }
    pressure: {
      average: number
      minimum: number
      maximum: number
    }
    battery: {
      average: number
    }
  }
}

class ApiService {
  private baseUrl: string
  private token: string | null = null

  constructor() {
    this.baseUrl = API_BASE_URL
    this.token = localStorage.getItem('access_token')
  }

  setToken(token: string) {
    this.token = token
    localStorage.setItem('access_token', token)
  }

  removeToken() {
    this.token = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_role')
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    }

    if (this.token) {
      headers.Authorization = `Bearer ${this.token}`
    }

    const response = await fetch(url, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Network error' }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
  }

  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await this.request<LoginResponse>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    })
    this.setToken(response.access_token)
    return response
  }

  async register(payload: RegisterRequest): Promise<RegisterResponse> {
    return this.request<RegisterResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  }

  async logout(): Promise<void> {
    try {
      await this.request('/auth/logout', { method: 'POST' })
    } finally {
      this.removeToken()
    }
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/auth/me')
  }

  async getAdminDashboard(): Promise<AdminDashboard> {
    return this.request<AdminDashboard>('/admin/dashboard')
  }

  async getUsers(): Promise<User[]> {
    return this.request<User[]>('/admin/users')
  }

  async checkHealth(): Promise<{ status: string }> {
    return this.request<{ status: string }>('/health')
  }

  async getSensors(activeOnly: boolean = true): Promise<Sensor[]> {
    return this.request<Sensor[]>(`/sensors?active_only=${activeOnly}`)
  }

  async getSensor(sensorId: number): Promise<Sensor> {
    return this.request<Sensor>(`/sensors/${sensorId}`)
  }

  async getSensorMeasurements(
    sensorId: number,
    options: {
      limit?: number
      hours?: number
      startDate?: string
      endDate?: string
    } = {}
  ): Promise<SensorMeasurementsResponse> {
    const params = new URLSearchParams()
    if (options.limit) params.append('limit', options.limit.toString())
    if (options.hours) params.append('hours', options.hours.toString())
    if (options.startDate) params.append('start_date', options.startDate)
    if (options.endDate) params.append('end_date', options.endDate)

    const queryString = params.toString()
    const endpoint = `/sensors/${sensorId}/measurements${queryString ? `?${queryString}` : ''}`

    return this.request<SensorMeasurementsResponse>(endpoint)
  }

  async getSensorLatest(sensorId: number): Promise<SensorLatestResponse> {
    return this.request<SensorLatestResponse>(`/sensors/${sensorId}/latest`)
  }

  async getSensorStats(sensorId: number, hours: number = 24): Promise<SensorStatsResponse> {
    return this.request<SensorStatsResponse>(`/sensors/${sensorId}/stats?hours=${hours}`)
  }
}

export const apiService = new ApiService()
