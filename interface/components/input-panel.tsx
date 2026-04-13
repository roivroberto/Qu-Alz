"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Upload, Brain, FileText, Dna } from "lucide-react"

interface InputPanelProps {
  onRunPrediction: (data: any) => void
  isLoading: boolean
}

export function InputPanel({ onRunPrediction, isLoading }: InputPanelProps) {
  const [formData, setFormData] = useState({
    mriFile: null as File | null,
    mmseScore: "",
    cdrScore: "",
    apoeStatus: "",
  })

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setFormData((prev) => ({ ...prev, mriFile: file }))
    }
  }

  const handleSubmit = () => {
    onRunPrediction(formData)
  }

  const isFormValid = formData.mriFile && formData.mmseScore && formData.cdrScore && formData.apoeStatus

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Brain className="w-5 h-5 text-teal-600" />
            <span>MRI Scan Upload</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-teal-400 transition-colors">
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <div className="space-y-2">
              <p className="text-sm font-medium text-gray-700">
                {formData.mriFile ? formData.mriFile.name : "Upload Brain MRI Scan"}
              </p>
              <p className="text-xs text-gray-500">Supported formats: DICOM, NIfTI (.dcm, .nii, .nii.gz)</p>
              <Input
                type="file"
                accept=".dcm,.nii,.nii.gz"
                onChange={handleFileUpload}
                className="hidden"
                id="mri-upload"
              />
              <Label htmlFor="mri-upload">
                <Button variant="outline" className="cursor-pointer bg-transparent" asChild>
                  <span>Choose File</span>
                </Button>
              </Label>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-teal-600" />
            <span>Cognitive Assessment Scores</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="mmse">MMSE Score (0-30)</Label>
              <Input
                id="mmse"
                type="number"
                min="0"
                max="30"
                placeholder="e.g., 24"
                value={formData.mmseScore}
                onChange={(e) => setFormData((prev) => ({ ...prev, mmseScore: e.target.value }))}
              />
              <p className="text-xs text-gray-500">Mini-Mental State Examination</p>
            </div>
            <div className="space-y-2">
              <Label htmlFor="cdr">CDR Score</Label>
              <Select
                value={formData.cdrScore}
                onValueChange={(value) => setFormData((prev) => ({ ...prev, cdrScore: value }))}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select CDR score" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="0">0 (Normal)</SelectItem>
                  <SelectItem value="0.5">0.5 (Very Mild)</SelectItem>
                  <SelectItem value="1">1 (Mild)</SelectItem>
                  <SelectItem value="2">2 (Moderate)</SelectItem>
                  <SelectItem value="3">3 (Severe)</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-gray-500">Clinical Dementia Rating</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Dna className="w-5 h-5 text-teal-600" />
            <span>Genetic Information</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Label htmlFor="apoe">APOE Genotype</Label>
            <Select
              value={formData.apoeStatus}
              onValueChange={(value) => setFormData((prev) => ({ ...prev, apoeStatus: value }))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Select APOE genotype" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="e2/e2">ε2/ε2 (Protective)</SelectItem>
                <SelectItem value="e2/e3">ε2/ε3 (Low Risk)</SelectItem>
                <SelectItem value="e2/e4">ε2/ε4 (Moderate Risk)</SelectItem>
                <SelectItem value="e3/e3">ε3/ε3 (Average Risk)</SelectItem>
                <SelectItem value="e3/e4">ε3/ε4 (Increased Risk)</SelectItem>
                <SelectItem value="e4/e4">ε4/ε4 (High Risk)</SelectItem>
              </SelectContent>
            </Select>
            <p className="text-xs text-gray-500">Apolipoprotein E genetic variant</p>
          </div>
        </CardContent>
      </Card>

      <Button
        onClick={handleSubmit}
        disabled={!isFormValid || isLoading}
        className="w-full bg-teal-600 hover:bg-teal-700 text-white py-3"
        size="lg"
      >
        {isLoading ? "Running Prediction..." : "Run Alzheimer's Prediction"}
      </Button>
    </div>
  )
}
