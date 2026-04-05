import React from 'react'

export default function StatsPanel({ stats }) {
  if (!stats) {
    return <div className="text-gray-400">Loading statistics...</div>
  }

  const StatCard = ({ label, value, unit, color }) => (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
      <p className="text-gray-400 text-sm mb-2">{label}</p>
      <p className={`text-3xl font-bold ${color}`}>{value}</p>
      {unit && <p className="text-gray-500 text-xs mt-1">{unit}</p>}
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
        <h2 className="text-xl font-bold text-white mb-4">Usage Statistics</h2>

        <div className="space-y-4">
          <StatCard
            label="Total Operations"
            value={stats.total_operations}
            unit="transformations"
            color="text-blue-400"
          />

          <StatCard
            label="Avg Input Length"
            value={stats.avg_input_length}
            unit="characters"
            color="text-purple-400"
          />

          <StatCard
            label="Avg Output Length"
            value={stats.avg_output_length}
            unit="characters"
            color="text-green-400"
          />

          <StatCard
            label="Compression Ratio"
            value={`${(stats.compression_ratio * 100).toFixed(0)}%`}
            unit="output / input"
            color="text-orange-400"
          />

          {stats.last_operation && (
            <div className="mt-6 p-4 bg-gray-700 rounded-lg">
              <p className="text-gray-400 text-sm mb-1">Last Operation</p>
              <p className="text-white text-sm font-mono">
                {new Date(stats.last_operation).toLocaleString()}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
