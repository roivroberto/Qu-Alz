"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Slider } from "@/components/ui/slider"
import { Loader2 } from "lucide-react"

interface HeatMapViewerProps {
  isAnalyzing: boolean
  uploadedFile: File | null
}

export function HeatMapViewer({ isAnalyzing, uploadedFile }: HeatMapViewerProps) {
  const [currentSlice, setCurrentSlice] = useState([0])

  return (
    <Card className="border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
      <CardContent className="p-8">
        <div className="space-y-8">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-semibold text-gray-900">2D Grad-CAM Heat Map</h3>
            <div className="text-gray-500 font-medium">
              {uploadedFile ? `Analyzing: ${uploadedFile.name}` : "Slice analysis"}
            </div>
          </div>

          {isAnalyzing ? (
            <div className="flex items-center justify-center h-96 bg-gray-50 rounded-xl">
              <div className="text-center space-y-6">
                <Loader2 className="w-16 h-16 text-teal animate-spin mx-auto" />
                <p className="text-gray-600 font-medium text-lg">Processing single 2D slice...</p>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {/* MRI Viewer */}
              <div className="relative h-96 bg-gray-900 rounded-xl overflow-hidden group">
                {uploadedFile ? (
                  <img
                    src={URL.createObjectURL(uploadedFile) || "/placeholder.svg"}
                    alt="Uploaded axial MRI slice"
                    className="w-full h-full object-contain opacity-90 transition-opacity duration-300"
                  />
                ) : (
                  <img
                    src="/placeholder.svg?height=384&width=500"
                    alt="Axial MRI Brain Slice"
                    className="w-full h-full object-contain opacity-90 transition-opacity duration-300"
                  />
                )}

                {/* Grad-CAM Overlay */}
                <div className="absolute inset-0 bg-gradient-radial from-coral-500/40 via-coral-400/20 to-transparent rounded-xl mix-blend-multiply opacity-80 group-hover:opacity-90 transition-opacity duration-300"></div>

                {/* Hippocampus Highlight */}
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                  <div className="w-20 h-16 bg-coral-500/50 rounded-full border-2 border-coral-400 animate-pulse"></div>
                </div>

                {/* Analysis indicator */}
                <div className="absolute top-4 left-4 bg-black/50 text-white px-3 py-1 rounded-lg text-sm font-medium">
                  2D Analysis Complete
                </div>
              </div>

              {/* Neighboring Slices Slider */}
              <div className="space-y-3">
                <div className="flex items-center justify-between text-sm text-gray-600 font-medium">
                  <span>Slice -5</span>
                  <span>Current uploaded slice</span>
                  <span>Slice +5</span>
                </div>
                <Slider
                  value={currentSlice}
                  onValueChange={setCurrentSlice}
                  max={10}
                  min={0}
                  step={1}
                  className="w-full"
                  disabled={!uploadedFile}
                />
                <p className="text-center text-sm text-gray-500">
                  {uploadedFile
                    ? "View ±5 neighboring slices if available"
                    : "Upload a slice to enable neighboring slice navigation"}
                </p>
              </div>

              {/* Legend */}
              <div className="flex items-center justify-center space-x-8 text-sm">
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 bg-coral-500/70 rounded shadow-sm"></div>
                  <span className="text-gray-600 font-medium">High attention</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 bg-coral-400/50 rounded shadow-sm"></div>
                  <span className="text-gray-600 font-medium">Moderate attention</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-4 h-4 bg-gray-300 rounded shadow-sm"></div>
                  <span className="text-gray-600 font-medium">Normal tissue</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}
