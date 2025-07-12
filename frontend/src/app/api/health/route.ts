import { NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function GET() {
  try {
    // Test database connection
    await prisma.$queryRaw`SELECT 1`
    
    // Get user count
    const userCount = await prisma.user.count()
    
    return NextResponse.json({
      status: 'healthy',
      database: 'connected',
      userCount,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('Health check error:', error)
    return NextResponse.json({
      status: 'unhealthy',
      database: 'disconnected',
      error: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString()
    }, { status: 500 })
  }
} 