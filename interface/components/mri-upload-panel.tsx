"use client"

import type React from "react"

import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Upload, FileImage, CheckCircle, Loader2 } from "lucide-react"

interface MriUploadPanelProps {
  onUpload: (file: File) => void
  isAnalyzing: boolean
  uploadedFile: File | null
}

export function MriUploadPanel({ onUpload, isAnalyzing, uploadedFile }: MriUploadPanelProps) {
  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      onUpload(file)
    }
  }

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    const file = event.dataTransfer.files[0]
    if (file) {
      onUpload(file)
    }
  }

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault()
  }

  return (
    <Card className="border-gray-200 shadow-lg">
      <CardContent className="p-10">
        <div className="space-y-8">
          <div className="text-center">
            <h2 className="text-2xl font-semibold text-gray-900 mb-3">Upload MRI Slice</h2>
            <p className="text-gray-600 text-lg">
              Upload a single axial MRI slice for automated Alzheimer's stage detection
            </p>
          </div>

          <div
            className="border-2 border-dashed border-gray-300 rounded-xl p-16 text-center hover:border-teal hover:bg-teal-light/20 transition-all duration-300 bg-gray-50 group cursor-pointer"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
          >
            {uploadedFile ? (
              <div className="space-y-6">
                <div className="flex items-center justify-center">
                  {isAnalyzing ? (
                    <div className="relative">
                      <Loader2 className="w-16 h-16 text-teal animate-spin" />
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="w-8 h-8 bg-teal-light rounded-full animate-pulse"></div>
                      </div>
                    </div>
                  ) : (
                    <div className="relative">
                      <CheckCircle className="w-16 h-16 text-teal" />
                      <div className="absolute -top-1 -right-1 w-6 h-6 bg-emerald-500 rounded-full flex items-center justify-center">
                        <span className="text-white text-xs">✓</span>
                      </div>
                    </div>
                  )}
                </div>
                <div>
                  <p className="font-semibold text-gray-900 text-lg">{uploadedFile.name}</p>
                  <p className="text-gray-500 mt-2">
                    {isAnalyzing ? "Analyzing 2D brain slice..." : "Single slice analysis complete"}
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="relative">
                  <Upload className="w-16 h-16 text-gray-400 mx-auto group-hover:text-teal transition-colors duration-300" />
                  <div className="absolute -top-2 -right-2 w-6 h-6 bg-teal rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-300 animate-bounce">
                    <span className="text-white text-xs flex items-center justify-center h-full">+</span>
                  </div>
                </div>
                <div>
                  <p className="text-xl font-semibold text-gray-700 mb-2">Upload single axial MRI slice (PNG/JPEG)</p>
                  <p className="text-gray-500">One 2D image is all we need for complete Alzheimer's analysis</p>
                </div>
                <div className="flex items-center justify-center space-x-6">
                  <div className="h-px bg-gray-300 flex-1"></div>
                  <span className="text-gray-500 font-medium">or</span>
                  <div className="h-px bg-gray-300 flex-1"></div>
                </div>
                <Input
                  type="file"
                  accept=".png,.jpg,.jpeg"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="mri-upload"
                />
                <Label htmlFor="mri-upload">
                  <Button
                    className="bg-teal hover:bg-teal/90 text-white px-10 py-4 rounded-xl text-lg font-medium shadow-lg hover:shadow-xl transition-all duration-200"
                    asChild
                  >
                    <span className="flex items-center space-x-3">
                      <FileImage className="w-6 h-6" />
                      <span>Upload 2D MRI slice</span>
                    </span>
                  </Button>
                </Label>
              </div>
            )}
          </div>

          {/* Status Line */}
          <div className="flex items-center justify-center space-x-3 text-gray-500">
            <div className="w-2 h-2 bg-teal rounded-full animate-pulse"></div>
            <span className="font-medium">Analysed in {"<"} 2 minutes</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
