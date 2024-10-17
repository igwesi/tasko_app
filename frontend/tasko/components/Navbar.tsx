"use client"
import React from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { Button } from '@radix-ui/themes'

const Navbar = () => {
    const router = useRouter()
    const pathname = usePathname()

    return (
        <div className='flex flex-row gap-3 justify-between items-center'>
            {
                pathname !== "/" && 
                <Button className='btn btn-sm' onClick={() => router.back()}>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-4">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 15 3 9m0 0 6-6M3 9h12a6 6 0 0 1 0 12h-3" />
                    </svg>
                    Go Back
                </Button>  
            }
        </div>
    )
}
export default Navbar
