"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Loader2 } from "lucide-react"

interface EntanglementMeterProps {
  value?: number
  isAnalyzing: boolean
}

export function EntanglementMeter({ value, isAnalyzing }: EntanglementMeterProps) {
  const getEESInterpretation = (value?: number) => {
    if (!value) return ""
    if (value < 0.3) return "low feature coupling — routine monitoring"
    if (value < 0.7) return "moderate feature coupling — closer monitoring advised"
    return "high feature coupling — immediate attention recommended"
  }

  return (
    <Card className="border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
      <CardContent className="p-8">
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-gray-900">Entanglement-Entropy Score</h3>

          {isAnalyzing ? (
            <div className="flex items-center justify-center py-8">
              <div className="text-center space-y-4">
                <Loader2 className="w-8 h-8 text-teal animate-spin mx-auto" />
                <p className="text-gray-600 font-medium">Computing EES from 2D features...</p>
              </div>
            </div>
          ) : value !== undefined ? (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <span className="text-3xl font-bold text-gray-900 tabular-nums">{value.toFixed(2)}</span>
                <span className="text-gray-500 font-medium">0.0 - 1.0</span>
              </div>

              <div className="space-y-2">
                <Progress
                  value={value * 100}
                  className="h-4 bg-gray-200"
                  style={{
                    transition: "all 1.5s ease-out",
                  }}
                />
                <div className="flex justify-between text-xs text-gray-500 font-medium">
                  <span>0.0</span>
                  <span>1.0</span>
                </div>
              </div>

              <p className="text-gray-600 font-medium">
                EES {value.toFixed(2)} · {getEESInterpretation(value)}
              </p>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">Upload single 2D MRI slice to compute EES</div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
