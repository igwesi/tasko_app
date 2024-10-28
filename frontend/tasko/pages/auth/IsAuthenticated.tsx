"use client"
import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import useAuth from '@/app/hooks/useAuth';
import { AuthActions } from '@/app/auth/utils';
import Loading from '@/components/Loader';

const { removeTokens, getToken } = AuthActions();
const IsAuthenticated = ({ children }:Readonly<{children: React.ReactNode;}>) => {
  const router = useRouter();
  const { isAuthenticated,  isLoading} = useAuth();

  useEffect(() => {
    const token = getToken("access")
    if (!token) {
      removeTokens()
      router.push('/auth/login');
    }
  }, [isLoading, isAuthenticated, router]);

  if (isLoading) {
    return <Loading />
  }
  return isAuthenticated ? children : null;
};

export default IsAuthenticated;