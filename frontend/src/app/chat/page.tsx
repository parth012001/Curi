import { ChatInterface } from "@/components/chat/chat-interface"

export default function ChatPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-100 flex items-center justify-center p-4">
      <div className="w-full max-w-3xl rounded-3xl shadow-2xl bg-white/80 backdrop-blur-lg border border-gray-100 overflow-hidden">
        <ChatInterface />
      </div>
    </main>
  )
} 