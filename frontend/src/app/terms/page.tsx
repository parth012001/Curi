import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-white to-purple-100">
      <div className="max-w-4xl mx-auto p-6">
        <Link href="/">
          <Button variant="ghost" className="mb-6">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
        </Link>
        
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Terms of Service</h1>
          
          <div className="prose prose-gray max-w-none">
            <p className="text-gray-600 mb-6">
              Last updated: {new Date().toLocaleDateString()}
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">1. Acceptance of Terms</h2>
            <p className="text-gray-600 mb-6">
              By accessing and using Curi, you accept and agree to be bound by the terms and provision of this agreement.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">2. Use License</h2>
            <p className="text-gray-600 mb-6">
              Permission is granted to temporarily use Curi for personal, non-commercial transitory viewing only.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">3. Disclaimer</h2>
            <p className="text-gray-600 mb-6">
              The materials on Curi are provided on an 'as is' basis. Curi makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">4. Limitations</h2>
            <p className="text-gray-600 mb-6">
              In no event shall Curi or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Curi, even if Curi or a Curi authorized representative has been notified orally or in writing of the possibility of such damage.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">5. Revisions and Errata</h2>
            <p className="text-gray-600 mb-6">
              The materials appearing on Curi could include technical, typographical, or photographic errors. Curi does not warrant that any of the materials on its website are accurate, complete or current.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">6. Links</h2>
            <p className="text-gray-600 mb-6">
              Curi has not reviewed all of the sites linked to its website and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by Curi of the site.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">7. Modifications</h2>
            <p className="text-gray-600 mb-6">
              Curi may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these Terms of Service.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
} 