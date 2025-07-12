import { withAuth } from "next-auth/middleware"
import { NextResponse } from "next/server"

export default withAuth(
  function middleware(req) {
    // Add any additional middleware logic here
    return NextResponse.next()
  },
  {
    callbacks: {
      authorized: ({ token }) => !!token
    },
  }
)

export const config = {
  matcher: [
    // Protect these routes
    "/chat",
    "/dashboard",
    "/profile",
    // Exclude auth pages, demo, and API routes
    "/((?!auth|demo|api|_next/static|_next/image|favicon.ico).*)",
  ]
} 