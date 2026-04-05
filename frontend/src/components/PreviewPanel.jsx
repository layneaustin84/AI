import React, { useState } from 'react'

export default function PreviewPanel({ result, loading }) {
  const [copyMessage, setCopyMessage] = useState('')

  const handleCopy = (text, label) => {
    navigator.clipboard.writeText(text)
    setCopyMessage(`${label} copied to clipboard!`)
    setTimeout(() => setCopyMessage(''), 2000)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-800 rounded-lg border border-gray-700">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Processing...</p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-800 rounded-lg border border-gray-700">
        <p className="text-gray-400">Results will appear here...</p>
      </div>
    )
  }

  const getResultKey = () => {
    if (result.humanized) return 'humanized'
    if (result.summary) return 'summary'
    if (result.takeaways) return 'takeaways'
    return null
  }

  const resultKey = getResultKey()
  const resultText = result[resultKey]
  const label =
    resultKey === 'humanized'
      ? 'Humanized'
      : resultKey === 'summary'
        ? 'Summary'
        : 'Takeaways'

  return (
    <div className="space-y-4">
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="block text-sm font-semibold text-gray-300">
            {label} Output
          </label>
          {result.tone && (
            <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded">
              {result.tone}
            </span>
          )}
        </div>
        <div className="relative">
          <div className="w-full h-96 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-gray-100 overflow-y-auto whitespace-pre-wrap break-words">
            {resultText}
          </div>
          <button
            onClick={() => handleCopy(resultText, label)}
            className="absolute top-3 right-3 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded transition-all"
          >
            Copy
          </button>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
          <div className="text-xs text-gray-400 mb-1">Input</div>
          <div className="text-xl font-bold text-blue-400">
            {result.input_length}
          </div>
          <div className="text-xs text-gray-500">characters</div>
        </div>
        <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
          <div className="text-xs text-gray-400 mb-1">Output</div>
          <div className="text-xl font-bold text-purple-400">
            {result.output_length}
          </div>
          <div className="text-xs text-gray-500">characters</div>
        </div>
        <div className="p-3 bg-gray-800 rounded-lg border border-gray-700">
          <div className="text-xs text-gray-400 mb-1">Ratio</div>
          <div className="text-xl font-bold text-green-400">
            {(
              (result.output_length / result.input_length) *
              100
            ).toFixed(0)}%
          </div>
          <div className="text-xs text-gray-500">compression</div>
        </div>
      </div>

      {/* Copy Message */}
      {copyMessage && (
        <div className="p-3 bg-green-900 border border-green-500 rounded-lg text-green-200 text-sm">
          ✓ {copyMessage}
        </div>
      )}
    </div>
  )
}
