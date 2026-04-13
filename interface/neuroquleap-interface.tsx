"use client"

import { useState } from "react"
import { Header } from "./components/header"
import { MriUploadPanel } from "./components/mri-upload-panel"
import { StageBadgeCard } from "./components/stage-badge-card"
import { RiskCard } from "./components/risk-card"
import { EntanglementMeter } from "./components/entanglement-meter"
import { HeatMapViewer } from "./components/heatmap-viewer"
import { QuickActions } from "./components/quick-actions"

// Mock results data
const mockResults = {
  stage: "Very-Mild" as const,
  confidence: 82,
  riskPercentage: 35,
  riskRange: [28, 42] as [number, number],
  eesValue: 0.29,
  analysisComplete: true,
}

export default function NeuroQLeapInterface() {
  const [results, setResults] = useState<typeof mockResults | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleMriUpload = async (file: File) => {
    setUploadedFile(file)
    setIsAnalyzing(true)
    setResults(null)

    // Simulate analysis
    await new Promise((resolve) => setTimeout(resolve, 3500))

    setResults(mockResults)
    setIsAnalyzing(false)
  }

  return (
    <div className="min-h-screen bg-canvas">
      <Header />

      <main className="max-w-7xl mx-auto px-8 py-12 space-y-12">
        {/* MRI Upload Section */}
        <div className="max-w-3xl mx-auto">
          <MriUploadPanel onUpload={handleMriUpload} isAnalyzing={isAnalyzing} uploadedFile={uploadedFile} />
        </div>

        {/* Results Grid */}
        {(results || isAnalyzing) && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Left Column */}
            <div className="space-y-8">
              <StageBadgeCard stage={results?.stage} confidence={results?.confidence} isAnalyzing={isAnalyzing} />
              <RiskCard percentage={results?.riskPercentage} range={results?.riskRange} isAnalyzing={isAnalyzing} />
              <EntanglementMeter value={results?.eesValue} isAnalyzing={isAnalyzing} />
            </div>

            {/* Middle & Right Columns */}
            <div className="lg:col-span-2 space-y-8">
              <HeatMapViewer isAnalyzing={isAnalyzing} uploadedFile={uploadedFile} />
              <QuickActions disabled={!results?.analysisComplete} isAnalyzing={isAnalyzing} />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
