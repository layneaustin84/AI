import React, { useState, useEffect } from 'react'
import { apiClient } from './api'
import ToneSelector from './components/ToneSelector'
import TextEditor from './components/TextEditor'
import PreviewPanel from './components/PreviewPanel'
import BatchUpload from './components/BatchUpload'
import HistoryLog from './components/HistoryLog'
import StatsPanel from './components/StatsPanel'

export default function App() {
  const [activeTab, setActiveTab] = useState('humanize')
  const [text, setText] = useState('')
  const [selectedTone, setSelectedTone] = useState('friendly')
  const [selectedDocType, setSelectedDocType] = useState('')
  const [customInstruction, setCustomInstruction] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [profiles, setProfiles] = useState({})
  const [docTypes, setDocTypes] = useState([])
  const [history, setHistory] = useState([])
  const [stats, setStats] = useState(null)

  // Load profiles and doc types on mount
  useEffect(() => {
    loadProfiles()
    loadDocTypes()
    loadHistory()
    loadStats()
  }, [])

  const loadProfiles = async () => {
    try {
      const { data } = await apiClient.getProfiles()
      setProfiles(data.profiles)
    } catch (err) {
      console.error('Failed to load profiles:', err)
    }
  }

  const loadDocTypes = async () => {
    try {
      const { data } = await apiClient.getTypes()
      setDocTypes(data.types)
    } catch (err) {
      console.error('Failed to load doc types:', err)
    }
  }

  const loadHistory = async () => {
    try {
      const { data } = await apiClient.getHistory(20)
      setHistory(data.operations)
    } catch (err) {
      console.error('Failed to load history:', err)
    }
  }

  const loadStats = async () => {
    try {
      const { data } = await apiClient.getStats()
      setStats(data)
    } catch (err) {
      console.error('Failed to load stats:', err)
    }
  }

  const handleHumanize = async () => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const { data } = await apiClient.humanize(
        text,
        selectedTone,
        selectedDocType || undefined,
        customInstruction || undefined
      )
      setResult(data)
      loadHistory()
      loadStats()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to humanize text')
    } finally {
      setLoading(false)
    }
  }

  const handleSummarize = async () => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const { data } = await apiClient.summarize(text)
      setResult({ ...data, operation: 'summarize' })
      loadHistory()
      loadStats()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to summarize text')
    } finally {
      setLoading(false)
    }
  }

  const handleTakeaways = async () => {
    if (!text.trim()) {
      setError('Please enter some text')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const { data } = await apiClient.takeaways(text)
      setResult({ ...data, operation: 'takeaways' })
      loadHistory()
      loadStats()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to extract takeaways')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <header className="bg-black bg-opacity-50 border-b border-gray-700 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
                Personal Agent
              </h1>
              <p className="text-gray-400 text-sm mt-1">
                AI-powered text transformation studio
              </p>
            </div>
            <div className="text-right">
              <p className="text-gray-400 text-sm">Powered by Gemini API</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b border-gray-700">
          {['humanize', 'summarize', 'batch', 'history'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-3 font-semibold text-sm transition-all ${
                activeTab === tab
                  ? 'border-b-2 border-blue-500 text-blue-400'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 p-4 bg-red-900 bg-opacity-30 border border-red-500 rounded-lg text-red-200">
            {error}
          </div>
        )}

        {/* Tab Content */}
        {activeTab === 'humanize' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Input Panel */}
            <div className="space-y-6">
              <ToneSelector
                profiles={profiles}
                selectedTone={selectedTone}
                onToneChange={setSelectedTone}
                docTypes={docTypes}
                selectedDocType={selectedDocType}
                onDocTypeChange={setSelectedDocType}
              />

              <TextEditor
                value={text}
                onChange={setText}
                placeholder="Enter text to humanize..."
              />

              <div>
                <label className="block text-sm font-semibold text-gray-300 mb-2">
                  Custom Instruction (Optional)
                </label>
                <textarea
                  value={customInstruction}
                  onChange={(e) => setCustomInstruction(e.target.value)}
                  placeholder="Add any specific instructions..."
                  className="w-full h-20 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <button
                onClick={handleHumanize}
                disabled={loading}
                className={`w-full py-3 px-4 rounded-lg font-semibold transition-all ${
                  loading
                    ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white'
                }`}
              >
                {loading ? 'Humanizing...' : 'Humanize Text'}
              </button>

              <div className="flex gap-2">
                <button
                  onClick={handleSummarize}
                  disabled={loading}
                  className="flex-1 py-2 px-4 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-all disabled:opacity-50"
                >
                  Summarize
                </button>
                <button
                  onClick={handleTakeaways}
                  disabled={loading}
                  className="flex-1 py-2 px-4 rounded-lg bg-gray-800 hover:bg-gray-700 text-white transition-all disabled:opacity-50"
                >
                  Takeaways
                </button>
              </div>
            </div>

            {/* Output Panel */}
            <PreviewPanel result={result} loading={loading} />
          </div>
        )}

        {activeTab === 'summarize' && (
          <div className="max-w-4xl">
            <TextEditor
              value={text}
              onChange={setText}
              placeholder="Enter text to summarize..."
            />
            <button
              onClick={handleSummarize}
              disabled={loading}
              className="mt-4 w-full py-3 px-4 rounded-lg font-semibold bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white transition-all disabled:opacity-50"
            >
              {loading ? 'Summarizing...' : 'Summarize'}
            </button>
            {result && result.operation === 'summarize' && (
              <PreviewPanel result={result} loading={false} />
            )}
          </div>
        )}

        {activeTab === 'batch' && (
          <BatchUpload
            profiles={profiles}
            selectedTone={selectedTone}
            onToneChange={setSelectedTone}
            docTypes={docTypes}
            selectedDocType={selectedDocType}
            onDocTypeChange={setSelectedDocType}
            onSuccess={() => {
              loadHistory()
              loadStats()
            }}
          />
        )}

        {activeTab === 'history' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <HistoryLog operations={history} />
            </div>
            <div>
              <StatsPanel stats={stats} />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
