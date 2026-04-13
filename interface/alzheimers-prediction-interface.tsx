"use client"

import { useState } from "react"
import { PatientSidebar } from "./components/patient-sidebar"
import { InputPanel } from "./components/input-panel"
import { ResultsPanel } from "./components/results-panel"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Brain, Activity } from "lucide-react"

// Enhanced mock patient data
const mockPatient = {
  id: "P-2024-001",
  name: "Margaret Johnson",
  age: 72,
  gender: "Female",
  dateOfBirth: "1952-03-15",
  phone: "(555) 123-4567",
  email: "m.johnson@email.com",
  lastVisit: "2024-01-15",
  diagnosis: "Mild Cognitive Impairment (MCI)",
  riskLevel: "Moderate" as const,
}

// Enhanced mock prediction results
const mockResults = {
  riskScore: 68,
  timeToConversion: 3.2,
  confidenceLevel: 87,
  confidenceRange: [62, 74] as [number, number],
  brainRegions: [
    { region: "Hippocampus (Left)", atrophy: 78 },
    { region: "Hippocampus (Right)", atrophy: 74 },
    { region: "Entorhinal Cortex", atrophy: 65 },
    { region: "Temporal Lobe", atrophy: 52 },
    { region: "Parietal Cortex", atrophy: 41 },
    { region: "Frontal Cortex", atrophy: 28 },
    { region: "Precuneus", atrophy: 38 },
    { region: "Posterior Cingulate", atrophy: 45 },
  ],
  trajectory: [
    { year: 0, riskScore: 68 },
    { year: 1, riskScore: 72 },
    { year: 2, riskScore: 76 },
    { year: 3, riskScore: 81 },
    { year: 4, riskScore: 85 },
    { year: 5, riskScore: 88 },
    { year: 6, riskScore: 91 },
    { year: 7, riskScore: 93 },
    { year: 8, riskScore: 95 },
    { year: 9, riskScore: 96 },
    { year: 10, riskScore: 97 },
  ],
}

export default function AlzheimersPredictionInterface() {
  const [results, setResults] = useState<typeof mockResults | null>(mockResults)
  const [isLoading, setIsLoading] = useState(false)

  const handleRunPrediction = async (formData: any) => {
    setIsLoading(true)
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 3000))
    setResults(mockResults)
    setIsLoading(false)
  }

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Patient Sidebar */}
      <PatientSidebar patient={mockPatient} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-8 py-6">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-teal-100 rounded-lg">
              <Brain className="w-6 h-6 text-teal-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Alzheimer's Disease Prediction</h1>
              <p className="text-sm text-gray-600">AI-powered risk assessment and progression modeling</p>
            </div>
          </div>
        </header>

        {/* Content */}
        <div className="flex-1 p-8">
          <Tabs defaultValue="prediction" className="space-y-6">
            <TabsList className="grid w-full grid-cols-2 max-w-md">
              <TabsTrigger value="prediction" className="flex items-center space-x-2">
                <Brain className="w-4 h-4" />
                <span>Prediction</span>
              </TabsTrigger>
              <TabsTrigger value="results" className="flex items-center space-x-2">
                <Activity className="w-4 h-4" />
                <span>Results</span>
              </TabsTrigger>
            </TabsList>

            <TabsContent value="prediction" className="space-y-6">
              <div className="max-w-2xl">
                <InputPanel onRunPrediction={handleRunPrediction} isLoading={isLoading} />
              </div>
            </TabsContent>

            <TabsContent value="results" className="space-y-6">
              <ResultsPanel results={results} />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
