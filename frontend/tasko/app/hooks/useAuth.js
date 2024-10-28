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
    const Authenticate = () => {
      setIsLoading(true);
      axios.create(
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
        setIsAuthenticated(false);
        setIsLoading(false);
        console.error('Error while fetching user', error);
      })
    };
    Authenticate();
  }, []);
  return { isAuthenticated, user, setIsAuthenticated, isLoading };
};

export default useAuth;