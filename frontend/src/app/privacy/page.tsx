import Link from "next/link"
import { Button } from "@/components/ui/button"
import { ArrowLeft } from "lucide-react"

export default function PrivacyPage() {
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
          <h1 className="text-3xl font-bold text-gray-900 mb-6">Privacy Policy</h1>
          
          <div className="prose prose-gray max-w-none">
            <p className="text-gray-600 mb-6">
              Last updated: {new Date().toLocaleDateString()}
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">1. Information We Collect</h2>
            <p className="text-gray-600 mb-6">
              We collect information you provide directly to us, such as when you create an account, use our services, or contact us. This may include your name, email address, and any other information you choose to provide.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">2. How We Use Your Information</h2>
            <p className="text-gray-600 mb-6">
              We use the information we collect to provide, maintain, and improve our services, to communicate with you, and to develop new features and services.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">3. Information Sharing</h2>
            <p className="text-gray-600 mb-6">
              We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this privacy policy.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">4. Data Security</h2>
            <p className="text-gray-600 mb-6">
              We implement appropriate security measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">5. Cookies and Tracking</h2>
            <p className="text-gray-600 mb-6">
              We may use cookies and similar tracking technologies to enhance your experience on our website and to collect information about how you use our services.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">6. Your Rights</h2>
            <p className="text-gray-600 mb-6">
              You have the right to access, update, or delete your personal information. You may also have the right to restrict or object to certain processing of your information.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">7. Changes to This Policy</h2>
            <p className="text-gray-600 mb-6">
              We may update this privacy policy from time to time. We will notify you of any changes by posting the new privacy policy on this page.
            </p>
            
            <h2 className="text-xl font-semibold text-gray-900 mb-4">8. Contact Us</h2>
            <p className="text-gray-600 mb-6">
              If you have any questions about this privacy policy, please contact us at privacy@curi.com.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
} 