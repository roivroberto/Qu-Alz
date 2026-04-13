"use client"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Brain } from "lucide-react"

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-8 py-6">
        <div className="flex items-center justify-between">
          {/* Logo & Navigation */}
          <div className="flex items-center space-x-12">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-teal-light rounded-xl">
                <Brain className="w-7 h-7 text-teal" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">NeuroQLeap</h1>
                <p className="text-sm text-gray-500">2D MRI Alzheimer's Triage</p>
              </div>
            </div>

            {/* Slim Navigation */}
            <nav className="hidden md:flex items-center space-x-8">
              <Button variant="ghost" className="text-teal font-medium bg-teal-light/50">
                Dashboard
              </Button>
              <Button variant="ghost" className="text-gray-600 hover:text-teal hover:bg-teal-light/30">
                History
              </Button>
              <Button variant="ghost" className="text-gray-600 hover:text-teal hover:bg-teal-light/30">
                Settings
              </Button>
            </nav>
          </div>

          {/* User Avatar */}
          <Avatar className="w-10 h-10 ring-2 ring-teal-light">
            <AvatarImage src="/placeholder.svg?height=40&width=40" />
            <AvatarFallback className="bg-teal-light text-teal text-sm font-medium">DR</AvatarFallback>
          </Avatar>
        </div>
      </div>
    </header>
  )
}
