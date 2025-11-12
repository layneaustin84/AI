import React from 'react'

export default function HistoryLog({ operations }) {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleString()
  }

  if (!operations || operations.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400">
        <p>No operations logged yet</p>
      </div>
    )
  }

  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
      <div className="p-6 border-b border-gray-700">
        <h2 className="text-xl font-bold text-white">Operation History</h2>
      </div>
      <div className="divide-y divide-gray-700 max-h-96 overflow-y-auto">
        {operations.map((op, idx) => (
          <div key={idx} className="p-4 hover:bg-gray-700 transition-all">
            <div className="flex items-start justify-between mb-2">
              <div>
                <p className="font-semibold text-white capitalize">
                  {op.operation}
                </p>
                <p className="text-gray-500 text-xs mt-1">
                  {formatTime(op.timestamp)}
                </p>
              </div>
              {op.tone_profile && op.tone_profile !== 'N/A' && (
                <span className="text-xs bg-blue-600 text-white px-2 py-1 rounded">
                  {op.tone_profile}
                </span>
              )}
            </div>
            <div className="grid grid-cols-3 gap-2 text-sm">
              <div className="text-gray-400">
                <span className="text-gray-500">In:</span> {op.input_length}
              </div>
              <div className="text-gray-400">
                <span className="text-gray-500">Out:</span> {op.output_length}
              </div>
              {op.doc_type && (
                <div className="text-gray-400">
                  <span className="text-gray-500">Type:</span> {op.doc_type}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
