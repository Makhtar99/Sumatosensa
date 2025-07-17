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

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface RegisterResponse {
  message: string
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
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
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

  async register(data: RegisterRequest): Promise<RegisterResponse> {
    return this.request<RegisterResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }
}

export const apiService = new ApiService()