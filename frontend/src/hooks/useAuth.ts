import { useCallback } from 'react'
import toast from 'react-hot-toast'
import { useAuthStore } from '@/store/auth'
import { apiClient } from '@/lib/api-client'

export const useAuth = () => {
  const { user, isAuthenticated, setUser, setTokens, setAccessToken, clearAuth } = useAuthStore()

  const login = useCallback(
    async (email: string, password: string) => {
      try {
        const response = await apiClient.login(email, password)
        const { access_token, refresh_token } = response.data

        apiClient.setToken(access_token)
        setTokens(access_token, refresh_token)

        // Fetch user details
        const userResponse = await apiClient.getCurrentUser()
        setUser(userResponse.data)

        toast.success('Logged in successfully')
        return true
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Login failed')
        return false
      }
    },
    [setTokens, setUser]
  )

  const register = useCallback(
    async (email: string, username: string, full_name: string, password: string) => {
      try {
        await apiClient.register(email, username, full_name, password)
        toast.success('Registration successful. Please log in.')
        return true
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Registration failed')
        return false
      }
    },
    []
  )

  const logout = useCallback(() => {
    clearAuth()
    apiClient.clearToken()
    toast.success('Logged out successfully')
  }, [clearAuth])

  const updateProfile = useCallback(
    async (data: any) => {
      try {
        const response = await apiClient.updateProfile(data)
        setUser(response.data)
        toast.success('Profile updated successfully')
        return true
      } catch (error: any) {
        toast.error(error.response?.data?.detail || 'Update failed')
        return false
      }
    },
    [setUser]
  )

  return {
    user,
    isAuthenticated,
    login,
    register,
    logout,
    updateProfile,
  }
}
