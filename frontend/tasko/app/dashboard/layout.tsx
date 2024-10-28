import React from 'react'
import IsAuthenticated from '@/pages/auth/IsAuthenticated'

export default function Dashboardlayout({
    children,}: Readonly<{
    children: React.ReactNode;
  }>) {  
    return (
        <div>
            <IsAuthenticated>
                {children}
            </IsAuthenticated>
        </div>
     )
}