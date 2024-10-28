import React from 'react'
import useAuth from '@/app/hooks/useAuth';

const Profile = () => {
    const { user } = useAuth();
    return (
        <div className='border border-slate-500' id="profile">
        <h1 className='font-bold'>Greetings!</h1>
        {user && (
            <div className=''>
                <h2>Email: {user.email}</h2>
            </div>
        )}
        </div>
    )
}

export default Profile