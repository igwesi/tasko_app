"use client"
import React, {useState, useEffect } from "react";
import { AuthActions } from "@/app/auth/utils";
import Logout from "../auth/Logout";
import Loading from "@/components/Loader";

const Profile = () => {
    const [isLoading, setLoading ] = useState(true);
    const [user, setUser] = useState({
        email: ''
    })
    const { getUser } = AuthActions();
 
    useEffect(()=>{
        getUser().then((response) => {
            if(response.status === "success"){
                setUser(response.user);
                setLoading(false);
            }
        });
    }, [getUser]);

    if(isLoading){
        return <Loading/>
    }
    
    return (
        <>
            <div className="card w-full" id="profile">
                <div className="card-header">
                    <h3 className="text font-bold">Profile</h3>
                </div>

                <div className="card-body">
                    <p>Email: {user.email}</p>
                </div>
                <div className="flex flex-row card-footer gap-4">
                    <a href="#" className="btn btn-primary">Edit Profile</a>
                    <Logout/>
                </div>
            </div>
        </>
    )
}

export default Profile