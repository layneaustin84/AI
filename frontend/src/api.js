import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiClient = {
  // Profiles
  getProfiles: () => api.get('/profiles'),
  getTypes: () => api.get('/types'),
  getProfile: (name) => api.get(`/profile/${name}`),

  // Humanize
  humanize: (text, tone, docType, instruction) =>
    api.post('/humanize', {
      text,
      tone,
      doc_type: docType,
      instruction,
    }),

  // Summarize
  summarize: (text) => api.post('/summarize', { text }),

  // Takeaways
  takeaways: (text) => api.post('/takeaways', { text }),

  // Batch
  batchHumanize: (files, tone, docType) => {
    const formData = new FormData()
    files.forEach((file) => formData.append('files', file))
    formData.append('tone', tone)
    if (docType) formData.append('doc_type', docType)

    return api.post('/batch', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  // History
  getHistory: (limit = 50) => api.get('/history', { params: { limit } }),
  getStats: () => api.get('/stats'),

  // Utilities
  ping: () => api.get('/ping'),
  info: () => api.get('/info'),
}

export default api
