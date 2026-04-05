import React from 'react'

export default function ToneSelector({
  profiles,
  selectedTone,
  onToneChange,
  docTypes,
  selectedDocType,
  onDocTypeChange,
}) {
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-3">
          Tone Profile
        </label>
        <div className="grid grid-cols-2 gap-2">
          {Object.entries(profiles).map(([key, profile]) => (
            <button
              key={key}
              onClick={() => onToneChange(key)}
              className={`p-3 rounded-lg text-left text-sm transition-all ${
                selectedTone === key
                  ? 'bg-blue-600 border border-blue-400 text-white'
                  : 'bg-gray-800 border border-gray-700 text-gray-300 hover:border-gray-600'
              }`}
            >
              <div className="font-semibold">{profile.name}</div>
              <div className="text-xs opacity-75 truncate">
                {profile.description}
              </div>
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-semibold text-gray-300 mb-3">
          Document Type (Optional)
        </label>
        <select
          value={selectedDocType}
          onChange={(e) => onDocTypeChange(e.target.value)}
          className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">Auto-detect</option>
          {docTypes.map((docType) => (
            <option key={docType.type} value={docType.type}>
              {docType.type.charAt(0).toUpperCase() + docType.type.slice(1)} (
              {docType.default_profile})
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
