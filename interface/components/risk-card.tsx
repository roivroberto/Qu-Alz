"use client"

import { useState, useEffect } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Loader2, Info } from "lucide-react"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

interface RiskCardProps {
  percentage?: number
  range?: [number, number]
  isAnalyzing: boolean
}

export function RiskCard({ percentage, range, isAnalyzing }: RiskCardProps) {
  const [displayPercentage, setDisplayPercentage] = useState(0)

  useEffect(() => {
    if (percentage !== undefined && !isAnalyzing) {
      let start = 0
      const duration = 2000 // 2 seconds
      const increment = percentage / (duration / 50)

      const timer = setInterval(() => {
        start += increment
        if (start >= percentage) {
          setDisplayPercentage(percentage)
          clearInterval(timer)
        } else {
          setDisplayPercentage(Math.floor(start))
        }
      }, 50)

      return () => clearInterval(timer)
    }
  }, [percentage, isAnalyzing])

  return (
    <Card className="border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
      <CardContent className="p-8">
        <div className="space-y-6">
          <div className="flex items-center space-x-2">
            <h3 className="text-xl font-semibold text-gray-900">Conversion Risk</h3>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger>
                  <Info className="w-4 h-4 text-gray-400 hover:text-teal transition-colors" />
                </TooltipTrigger>
                <TooltipContent>
                  <p>Probability of progressing to dementia within three years.</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>

          {isAnalyzing ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center space-y-4">
                <Loader2 className="w-10 h-10 text-teal animate-spin mx-auto" />
                <p className="text-gray-600 font-medium">Calculating risk from 2D analysis...</p>
              </div>
            </div>
          ) : percentage !== undefined ? (
            <div className="space-y-4">
              <div className="text-center">
                <div className="text-6xl font-bold text-teal mb-2 tabular-nums">{displayPercentage}%</div>
                <p className="text-lg text-gray-700 font-medium">three-year conversion risk</p>
                {range && (
                  <div className="text-gray-600 mt-2">± {Math.abs(range[1] - percentage)}% confidence band</div>
                )}
              </div>

              <div className="text-center pt-6 border-t border-gray-100">
                <p className="text-xs text-gray-500 font-medium">Powered by quantum Entanglement-Entropy</p>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">Upload single 2D MRI slice to calculate risk</div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
