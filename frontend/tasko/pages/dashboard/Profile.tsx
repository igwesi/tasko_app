"use client"
import React, {useState, useEffect } from "react";
import { AuthActions } from "@/app/auth/utils";


const Profile = () => {
    const [user, setUser] = useState({
        email: ''
    })
    const { getUser } = AuthActions();
    useEffect(()=>{
        getUser().then((response) => {
            if(response.status === "success"){
                setUser(response.user);
            }
        });
    }, []);
    return (
        <>
            <div className="card" id="profile">
                
                <div className="card-header">
                    <h3 className="text font-bold">Profile</h3>
                </div>

                <div className="card-body">
                    <p>Email: {user.email}</p>
                </div>
                <div className="card-footer">
                    <a href="#" className="btn btn-primary">Edit Profile</a>
                </div>
            </div>
        </>
    )
}

export default Profile