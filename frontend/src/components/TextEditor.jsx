import React from 'react'

export default function TextEditor({ value, onChange, placeholder }) {
  return (
    <div>
      <label className="block text-sm font-semibold text-gray-300 mb-2">
        Input Text
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full h-96 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
      />
      <div className="mt-2 text-xs text-gray-400">
        {value.length} characters
      </div>
    </div>
  )
}
