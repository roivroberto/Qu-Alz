"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Loader2 } from "lucide-react"

interface StageBadgeCardProps {
  stage?: "No" | "Very-Mild" | "Mild" | "Moderate"
  confidence?: number
  isAnalyzing: boolean
}

export function StageBadgeCard({ stage, confidence, isAnalyzing }: StageBadgeCardProps) {
  const getStageColor = (stage?: string) => {
    switch (stage) {
      case "No":
        return "bg-emerald-100 text-emerald-800 border-emerald-200"
      case "Very-Mild":
        return "bg-amber-100 text-amber-800 border-amber-200"
      case "Mild":
        return "bg-orange-100 text-orange-800 border-orange-200"
      case "Moderate":
        return "bg-coral-100 text-coral-800 border-coral-200"
      default:
        return "bg-gray-100 text-gray-600 border-gray-200"
    }
  }

  const getConfidenceColor = (confidence?: number) => {
    if (!confidence) return "stroke-gray-300"
    if (confidence >= 80) return "stroke-emerald-500"
    if (confidence >= 60) return "stroke-amber-500"
    return "stroke-orange-500"
  }

  return (
    <Card className="border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
      <CardContent className="p-8">
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-gray-900">Stage Detection</h3>

          {isAnalyzing ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center space-y-4">
                <Loader2 className="w-10 h-10 text-teal animate-spin mx-auto" />
                <p className="text-gray-600 font-medium">Analyzing 2D slice patterns...</p>
              </div>
            </div>
          ) : stage ? (
            <div className="space-y-6">
              {/* Confidence Ring */}
              <div className="relative w-36 h-36 mx-auto">
                <svg className="w-36 h-36 transform -rotate-90" viewBox="0 0 120 120">
                  <circle
                    cx="60"
                    cy="60"
                    r="50"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="6"
                    className="text-gray-200"
                  />
                  <circle
                    cx="60"
                    cy="60"
                    r="50"
                    fill="none"
                    strokeWidth="6"
                    strokeLinecap="round"
                    className={`${getConfidenceColor(confidence)} transition-all duration-1000 ease-out`}
                    strokeDasharray={`${((confidence || 0) / 100) * 314} 314`}
                    style={{
                      animation: "drawCircle 1.5s ease-out",
                    }}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">{confidence}%</div>
                    <div className="text-xs text-gray-500 font-medium">confidence</div>
                  </div>
                </div>
              </div>

              {/* Stage Badge */}
              <div className="text-center">
                <Badge
                  className={`text-xl px-6 py-3 font-semibold ${getStageColor(stage)} shadow-sm`}
                  variant="outline"
                >
                  {stage}
                </Badge>
                <p className="text-gray-600 mt-3 font-medium">
                  Stage detected: {stage} · Confidence {confidence}%
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">Upload single 2D MRI slice to detect stage</div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
