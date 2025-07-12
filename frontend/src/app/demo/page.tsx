import { ChatInterface } from "@/components/chat/chat-interface"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"

export default function DemoPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-100">
      {/* Header */}
      <div className="p-6 max-w-7xl mx-auto">
        <Link href="/">
          <Button variant="ghost" className="mb-4">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
        </Link>
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Try Curi Demo</h1>
          <p className="text-gray-600">
            Experience our AI-powered beauty product recommendations without signing up
          </p>
        </div>
      </div>

      {/* Chat Interface */}
      <div className="flex items-center justify-center p-4">
        <div className="w-full max-w-3xl rounded-3xl shadow-2xl bg-white/80 backdrop-blur-lg border border-gray-100 overflow-hidden">
          <ChatInterface />
        </div>
      </div>

      {/* CTA */}
      <div className="text-center py-8">
        <p className="text-gray-600 mb-4">
          Love what you see? Create an account to save your preferences and chat history.
        </p>
        <Link href="/auth/signin">
          <Button className="bg-pink-600 hover:bg-pink-700">
            Create Account
          </Button>
        </Link>
      </div>
    </div>
  )
} 