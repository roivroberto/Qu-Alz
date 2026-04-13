"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"
import { AlertTriangle, Clock, Target, Brain, TrendingUp, FileText } from "lucide-react"

interface ResultsPanelProps {
  results: {
    riskScore: number
    timeToConversion: number
    confidenceLevel: number
    confidenceRange: [number, number]
    brainRegions: Array<{ region: string; atrophy: number }>
    trajectory: Array<{ year: number; riskScore: number }>
  } | null
}

export function ResultsPanel({ results }: ResultsPanelProps) {
  if (!results) {
    return (
      <div className="flex items-center justify-center h-96 text-gray-500">
        <div className="text-center">
          <Brain className="w-16 h-16 mx-auto mb-4 text-gray-300" />
          <p className="text-lg font-medium">No prediction results yet</p>
          <p className="text-sm">Upload MRI scan and enter patient data to run prediction</p>
        </div>
      </div>
    )
  }

  const getRiskLevel = (score: number) => {
    if (score < 30) return { level: "Low", color: "bg-green-100 text-green-800" }
    if (score < 70) return { level: "Moderate", color: "bg-yellow-100 text-yellow-800" }
    return { level: "High", color: "bg-red-100 text-red-800" }
  }

  const riskLevel = getRiskLevel(results.riskScore)

  return (
    <div className="space-y-6">
      {/* Risk Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2 text-sm">
              <Target className="w-4 h-4 text-teal-600" />
              <span>Alzheimer's Risk Score</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold text-gray-900">{results.riskScore}%</span>
                <Badge className={riskLevel.color}>{riskLevel.level}</Badge>
              </div>
              <Progress value={results.riskScore} className="h-2" />
              <p className="text-xs text-gray-500">
                Confidence: {results.confidenceRange[0]}% - {results.confidenceRange[1]}%
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2 text-sm">
              <Clock className="w-4 h-4 text-teal-600" />
              <span>Time to Conversion</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-baseline space-x-1">
                <span className="text-3xl font-bold text-gray-900">{results.timeToConversion}</span>
                <span className="text-lg text-gray-600">years</span>
              </div>
              <p className="text-sm text-gray-600">Estimated time to MCI/AD conversion</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2 text-sm">
              <AlertTriangle className="w-4 h-4 text-teal-600" />
              <span>Confidence Level</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-baseline space-x-1">
                <span className="text-3xl font-bold text-gray-900">{results.confidenceLevel}%</span>
              </div>
              <Progress value={results.confidenceLevel} className="h-2" />
              <p className="text-sm text-gray-600">Model prediction confidence</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Brain Heatmap */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="w-5 h-5 text-teal-600" />
            <span>Brain Atrophy Analysis</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-medium text-gray-700">Regional Atrophy Levels</h4>
              {results.brainRegions.map((region, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{region.region}</span>
                    <span className="text-gray-600">{region.atrophy}%</span>
                  </div>
                  <Progress value={region.atrophy} className="h-2" />
                </div>
              ))}
            </div>
            <div className="flex items-center justify-center bg-gray-50 rounded-lg p-8">
              <div className="text-center">
                <Brain className="w-24 h-24 mx-auto mb-4 text-teal-200" />
                <p className="text-sm text-gray-600">3D Brain Visualization</p>
                <p className="text-xs text-gray-500">Interactive heatmap would appear here</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Clinical Insights */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-teal-600" />
            <span>Clinical Insights & Recommendations</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <h4 className="font-medium text-yellow-800 mb-2">Key Findings</h4>
              <ul className="text-sm text-yellow-700 space-y-1">
                <li>• Significant hippocampal atrophy detected (78% left, 74% right)</li>
                <li>• APOE ε3/ε4 genotype increases conversion risk</li>
                <li>• Current MMSE score suggests mild cognitive decline</li>
              </ul>
            </div>
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-medium text-blue-800 mb-2">Recommendations</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• Consider cognitive training interventions</li>
                <li>• Monitor progression with 6-month follow-ups</li>
                <li>• Evaluate for clinical trial eligibility</li>
                <li>• Lifestyle modifications: exercise, Mediterranean diet</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Disease Trajectory */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-teal-600" />
            <span>Disease Progression Trajectory</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={results.trajectory}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="year" />
                <YAxis domain={[0, 100]} />
                <Tooltip
                  formatter={(value) => [`${value}%`, "Risk Score"]}
                  labelFormatter={(label) => `Year ${label}`}
                />
                <Line
                  type="monotone"
                  dataKey="riskScore"
                  stroke="#0d9488"
                  strokeWidth={3}
                  dot={{ fill: "#0d9488", strokeWidth: 2, r: 4 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <p className="text-sm text-gray-600 mt-4">
            Projected risk progression over the next 10 years based on current biomarkers and clinical data.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
