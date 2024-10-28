"use client"
import axios from 'axios';
import { useState, useEffect } from 'react';
import { AuthActions } from '@/app/auth/utils';
import { BACKEND_API } from '@/app/constants';


const useAuth = () => {
  const { getToken } = AuthActions();
  const [user, setUser] = useState({
    email: '',
  })
  const [isLoading, setIsLoading] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  useEffect(() => {
    const Authenticate = async() => {
      setIsLoading(true);
      await axios.create(
        {
          baseURL: BACKEND_API,
          headers: {
            'Authorization': `Bearer ${getToken('access')}`,
          },
        }
      ).get("/user/me/")
        .then(async(response) => {
        const data = await response.data;
        if (data.status === "success") {
          setIsAuthenticated(true);
          setUser(data.user);
        }else{
          setIsAuthenticated(false);
        }
        setIsLoading(false);
      }).catch((error)=>{
        if(error.response.status === 401){
          console.log("Token Expired");
        }
        setIsAuthenticated(false);
        setIsLoading(false);
      })
    };
    Authenticate();
  }, [getToken]);
  return { isAuthenticated, user, setIsAuthenticated, isLoading, setIsLoading };
};

export default useAuth;