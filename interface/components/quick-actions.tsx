"use client"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Download, Calendar, Loader2 } from "lucide-react"

interface QuickActionsProps {
  disabled: boolean
  isAnalyzing: boolean
}

export function QuickActions({ disabled, isAnalyzing }: QuickActionsProps) {
  const handleDownloadReport = () => {
    // Simulate PDF download
    console.log("Downloading 2D MRI analysis PDF report...")
  }

  const handleScheduleFollowup = () => {
    // Simulate scheduling
    console.log("Opening follow-up scheduler...")
  }

  return (
    <Card className="border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
      <CardContent className="p-8">
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-gray-900">Quick Actions</h3>

          {isAnalyzing ? (
            <div className="flex items-center justify-center py-8">
              <div className="text-center space-y-4">
                <Loader2 className="w-8 h-8 text-teal animate-spin mx-auto" />
                <p className="text-gray-600 font-medium">2D analysis in progress...</p>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <Button
                onClick={handleDownloadReport}
                disabled={disabled}
                className="bg-teal hover:bg-teal/90 text-white py-4 rounded-xl flex items-center space-x-3 text-lg font-medium shadow-lg hover:shadow-xl transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Download className="w-5 h-5" />
                <span>Download PDF Report</span>
              </Button>

              <Button
                onClick={handleScheduleFollowup}
                disabled={disabled}
                variant="outline"
                className="border-2 border-teal/30 text-teal hover:bg-teal-light/30 hover:border-teal py-4 rounded-xl flex items-center space-x-3 text-lg font-medium bg-transparent shadow-sm hover:shadow-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Calendar className="w-5 h-5" />
                <span>Schedule Follow-up</span>
              </Button>
            </div>
          )}

          {disabled && !isAnalyzing && (
            <p className="text-gray-500 text-center font-medium">Complete 2D MRI analysis to enable actions</p>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
