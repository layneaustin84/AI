import React, { useState } from 'react'
import { apiClient } from '../api'
import ToneSelector from './ToneSelector'

export default function BatchUpload({
  profiles,
  selectedTone,
  onToneChange,
  docTypes,
  selectedDocType,
  onDocTypeChange,
  onSuccess,
}) {
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [error, setError] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    const droppedFiles = Array.from(e.dataTransfer.files).filter((file) =>
      file.type.startsWith('text/')
    )
    setFiles((prev) => [...prev, ...droppedFiles])
  }

  const handleFileInput = (e) => {
    const selectedFiles = Array.from(e.target.files)
    setFiles((prev) => [...prev, ...selectedFiles])
  }

  const removeFile = (index) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const handleSubmit = async () => {
    if (files.length === 0) {
      setError('Please select at least one file')
      return
    }

    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const { data } = await apiClient.batchHumanize(
        files,
        selectedTone,
        selectedDocType || undefined
      )
      setResults(data)
      setFiles([])
      onSuccess()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process batch')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div className="lg:col-span-2 space-y-6">
        {/* Upload Area */}
        <div
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={`p-8 border-2 border-dashed rounded-lg transition-all ${
            dragActive
              ? 'border-blue-500 bg-blue-500 bg-opacity-10'
              : 'border-gray-700 bg-gray-800 bg-opacity-50'
          }`}
        >
          <div className="text-center">
            <svg
              className="w-12 h-12 mx-auto text-gray-400 mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="text-gray-300 font-semibold">
              Drag and drop your files here
            </p>
            <p className="text-gray-500 text-sm mt-2">or</p>
            <label className="inline-block mt-2">
              <input
                type="file"
                multiple
                accept=".txt,.md,.csv"
                onChange={handleFileInput}
                className="hidden"
              />
              <span className="cursor-pointer text-blue-400 hover:text-blue-300 font-semibold">
                Browse files
              </span>
            </label>
            <p className="text-gray-500 text-xs mt-4">
              Supported: .txt, .md, .csv (up to 50MB per batch)
            </p>
          </div>
        </div>

        {/* File List */}
        {files.length > 0 && (
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
            <h3 className="font-semibold text-white mb-3">
              Selected Files ({files.length})
            </h3>
            <div className="space-y-2">
              {files.map((file, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between p-2 bg-gray-700 rounded"
                >
                  <div className="flex-1">
                    <p className="text-white text-sm">{file.name}</p>
                    <p className="text-gray-500 text-xs">
                      {(file.size / 1024).toFixed(1)} KB
                    </p>
                  </div>
                  <button
                    onClick={() => removeFile(idx)}
                    className="px-2 py-1 text-red-400 hover:text-red-300 text-sm"
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="p-4 bg-red-900 bg-opacity-30 border border-red-500 rounded-lg text-red-200">
            {error}
          </div>
        )}

        {/* Results */}
        {results && (
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
            <h3 className="font-semibold text-white mb-4">Batch Results</h3>
            <div className="grid grid-cols-4 gap-4 mb-6">
              <div className="p-3 bg-gray-700 rounded text-center">
                <div className="text-2xl font-bold text-blue-400">
                  {results.successful}
                </div>
                <div className="text-xs text-gray-400 mt-1">Successful</div>
              </div>
              <div className="p-3 bg-gray-700 rounded text-center">
                <div className="text-2xl font-bold text-red-400">
                  {results.failed}
                </div>
                <div className="text-xs text-gray-400 mt-1">Failed</div>
              </div>
              <div className="p-3 bg-gray-700 rounded text-center">
                <div className="text-2xl font-bold text-purple-400">
                  {results.files_processed}
                </div>
                <div className="text-xs text-gray-400 mt-1">Total</div>
              </div>
              <div className="p-3 bg-gray-700 rounded text-center">
                <div className="text-2xl font-bold text-green-400">
                  {((results.successful / results.files_processed) * 100).toFixed(
                    0
                  )}
                  %
                </div>
                <div className="text-xs text-gray-400 mt-1">Success Rate</div>
              </div>
            </div>

            {/* File Results */}
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {results.results.map((result, idx) => (
                <div
                  key={idx}
                  className={`p-3 rounded border ${
                    result.status === 'success'
                      ? 'bg-green-900 bg-opacity-20 border-green-600'
                      : 'bg-red-900 bg-opacity-20 border-red-600'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-white font-semibold text-sm">
                        {result.filename}
                      </p>
                      {result.status === 'success' && (
                        <p className="text-gray-400 text-xs mt-1">
                          {result.input_length} → {result.output_length} chars
                        </p>
                      )}
                      {result.error && (
                        <p className="text-red-300 text-xs mt-1">{result.error}</p>
                      )}
                    </div>
                    <span
                      className={`text-xs font-semibold px-2 py-1 rounded ${
                        result.status === 'success'
                          ? 'bg-green-600 text-white'
                          : 'bg-red-600 text-white'
                      }`}
                    >
                      {result.status.charAt(0).toUpperCase() +
                        result.status.slice(1)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Submit Button */}
        {files.length > 0 && !results && (
          <button
            onClick={handleSubmit}
            disabled={loading}
            className={`w-full py-3 px-4 rounded-lg font-semibold transition-all ${
              loading
                ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white'
            }`}
          >
            {loading ? 'Processing...' : 'Process Files'}
          </button>
        )}
      </div>

      {/* Sidebar */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 h-fit">
        <ToneSelector
          profiles={profiles}
          selectedTone={selectedTone}
          onToneChange={onToneChange}
          docTypes={docTypes}
          selectedDocType={selectedDocType}
          onDocTypeChange={onDocTypeChange}
        />
      </div>
    </div>
  )
}
