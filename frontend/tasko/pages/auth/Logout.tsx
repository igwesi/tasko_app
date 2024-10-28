"use client"
import React from 'react'
import { Button } from '@headlessui/react';
import { AuthActions } from '@/app/auth/utils'
import { useRouter } from 'next/navigation';

const Logout = () => {
    const router = useRouter();
    const { logout } = AuthActions();

    const logOut = () =>{
        logout()
        router.push('/auth/login')
    }

    return (
        <>
            <Button onClick={logOut} className="btn bg-red-800 text-white hover:text-black">
                Logout
            </Button>
        </>
    )
}

export default Logout