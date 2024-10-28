import axios from 'axios';
import { useState, useEffect } from 'react';
import { AuthActions } from '../auth/utils';
// import { BACKEND_API } from '@/app/constants';


const useAuth = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser ] = useState({
    email: '',
    is_active: Boolean,
    is_staff: Boolean,
  });

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const { getToken } = AuthActions();
  // Simulate checking for authentication
  // Simulate network request delay
  useEffect(() => {
    const Authenticate = async () => {
      setIsLoading(true);
      await axios.create(
        {
          baseURL: process.env.BACKEND_API,
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
  }, [0]);
  return { isAuthenticated, setIsAuthenticated, user, isLoading };
};

export default useAuth;