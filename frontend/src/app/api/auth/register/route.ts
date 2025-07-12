import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const { name, email, password } = await request.json()

    // Validate input
    if (!name || !email || !password) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      )
    }

    if (password.length < 6) {
      return NextResponse.json(
        { error: 'Password must be at least 6 characters long' },
        { status: 400 }
      )
    }

    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email }
    })

    if (existingUser) {
      return NextResponse.json(
        { error: 'User with this email already exists' },
        { status: 409 }
      )
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12)

    // Create user
    const user = await prisma.user.create({
      data: {
        name,
        email,
        password: hashedPassword,
      },
      select: {
        id: true,
        name: true,
        email: true,
        image: true,
        createdAt: true,
      }
    })

    return NextResponse.json(
      { 
        message: 'User created successfully',
        user 
      },
      { status: 201 }
    )

  } catch (error) {
    console.error('Registration error:', error)
    
    // Handle specific Prisma errors
    if (error instanceof Error) {
      if (error.message.includes('readonly database')) {
        return NextResponse.json(
          { error: 'Database is read-only. Please restart the server.' },
          { status: 500 }
        )
      }
      
      if (error.message.includes('UNIQUE constraint failed')) {
        return NextResponse.json(
          { error: 'User with this email already exists' },
          { status: 409 }
        )
      }
    }
    
    return NextResponse.json(
      { error: 'Internal server error. Please try again.' },
      { status: 500 }
    )
  }
} 