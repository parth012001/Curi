import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Sparkles, Search, Shield, Users, Star, ArrowRight } from "lucide-react"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-100">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6 max-w-7xl mx-auto">
        <div className="flex items-center space-x-2">
          <Sparkles className="w-8 h-8 text-pink-600" />
          <span className="text-2xl font-bold text-gray-900">Curi</span>
        </div>
        <div className="flex items-center space-x-4">
          <Link href="/auth/signin">
            <Button variant="ghost">Sign In</Button>
          </Link>
          <Link href="/auth/signin">
            <Button className="bg-pink-600 hover:bg-pink-700">
              Get Started
            </Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="px-6 py-20 max-w-7xl mx-auto text-center">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Discover Your Perfect
            <span className="text-pink-600"> Beauty Products</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Get personalized beauty recommendations powered by AI. Find products that match your skin type, 
            concerns, and preferences with intelligent analysis of thousands of reviews.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/auth/signin">
              <Button size="lg" className="bg-pink-600 hover:bg-pink-700 text-lg px-8 py-4">
                Start Your Journey
                <ArrowRight className="ml-2 w-5 h-5" />
              </Button>
            </Link>
            <Link href="/demo">
              <Button size="lg" variant="outline" className="text-lg px-8 py-4">
                Try Demo
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="px-6 py-20 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-16">
            Why Choose Curi?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-pink-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Smart Search</h3>
              <p className="text-gray-600">
                Natural language queries that understand your beauty needs and preferences.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Star className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">AI-Powered Insights</h3>
              <p className="text-gray-600">
                Get detailed analysis of product reviews and user experiences.
              </p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Shield className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-3">Trusted Recommendations</h3>
              <p className="text-gray-600">
                Based on real user reviews and verified product information.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 bg-gradient-to-r from-pink-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center text-white">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Find Your Perfect Products?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of users who have discovered their ideal beauty routine with Curi.
          </p>
          <Link href="/auth/signin">
            <Button size="lg" className="bg-white text-pink-600 hover:bg-gray-100 text-lg px-8 py-4">
              Get Started Now
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-12 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-2 mb-4">
            <Sparkles className="w-6 h-6 text-pink-400" />
            <span className="text-xl font-bold">Curi</span>
          </div>
          <p className="text-gray-400">
            © 2024 Curi. Intelligent beauty product research powered by AI.
          </p>
        </div>
      </footer>
    </div>
  )
}
