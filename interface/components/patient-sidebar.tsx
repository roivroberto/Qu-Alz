"use client"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Calendar, User, Phone, Mail, FileText } from "lucide-react"

interface PatientSidebarProps {
  patient: {
    id: string
    name: string
    age: number
    gender: string
    dateOfBirth: string
    phone: string
    email: string
    lastVisit: string
    diagnosis: string
    riskLevel: "Low" | "Moderate" | "High"
  }
}

export function PatientSidebar({ patient }: PatientSidebarProps) {
  const getRiskColor = (level: string) => {
    switch (level) {
      case "Low":
        return "bg-green-100 text-green-800"
      case "Moderate":
        return "bg-yellow-100 text-yellow-800"
      case "High":
        return "bg-red-100 text-red-800"
      default:
        return "bg-gray-100 text-gray-800"
    }
  }

  return (
    <div className="w-80 bg-white border-r border-gray-200 p-6 space-y-6">
      <div className="text-center">
        <Avatar className="w-20 h-20 mx-auto mb-4">
          <AvatarImage src="/placeholder.svg?height=80&width=80" />
          <AvatarFallback className="text-lg bg-teal-100 text-teal-700">
            {patient.name
              .split(" ")
              .map((n) => n[0])
              .join("")}
          </AvatarFallback>
        </Avatar>
        <h2 className="text-xl font-semibold text-gray-900">{patient.name}</h2>
        <p className="text-sm text-gray-500">Patient ID: {patient.id}</p>
        <Badge className={`mt-2 ${getRiskColor(patient.riskLevel)}`}>{patient.riskLevel} Risk</Badge>
      </div>

      <Separator />

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm font-medium text-gray-700">Patient Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center space-x-3">
            <User className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm font-medium">Age & Gender</p>
              <p className="text-sm text-gray-600">
                {patient.age} years, {patient.gender}
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Calendar className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm font-medium">Date of Birth</p>
              <p className="text-sm text-gray-600">{patient.dateOfBirth}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Phone className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm font-medium">Phone</p>
              <p className="text-sm text-gray-600">{patient.phone}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Mail className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm font-medium">Email</p>
              <p className="text-sm text-gray-600">{patient.email}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="pb-3">
          <CardTitle className="text-sm font-medium text-gray-700">Clinical Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="flex items-center space-x-3">
            <FileText className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm font-medium">Current Diagnosis</p>
              <p className="text-sm text-gray-600">{patient.diagnosis}</p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <Calendar className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm font-medium">Last Visit</p>
              <p className="text-sm text-gray-600">{patient.lastVisit}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
