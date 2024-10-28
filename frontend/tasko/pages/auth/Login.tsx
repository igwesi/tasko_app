"use client"
import React, { useState, useEffect } from 'react'
import { useForm, Resolver } from "react-hook-form";
import { Input, Button } from '@headlessui/react';
import { useRouter } from 'next/navigation';
import { AuthActions } from '@/app/auth/utils';
import useAuth from '@/app/hooks/useAuth';

type FormData = {
  email: string;
  password: string;
};

const resolver: Resolver<FormData> = async (values) => {
  return {
    values: values.email ? values : {},
    errors: !values.email
      ? {
          email: {
            type: 'required',
            message: 'Email is required.',
          },
          password: {
            type:'required',
            message: 'Password is required.',
          },
        }
      : {},
  };
};

const Login = () => {
  const router = useRouter();
  const [error, setError] = useState(null);
  const [isLoading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false);
  const { login, storeToken, removeTokens } = AuthActions()
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({ resolver });
  const { isAuthenticated, setIsAuthenticated } = useAuth();
  
  const onSubmit = async(data: FormData) => {
    setError(null);
    removeTokens();
    setSubmitted(true);
    const res = await login(data.email, data.password);
    if(res.status === "success"){
      storeToken(res['token']['access'], "access");
      storeToken(res['token']['refresh'], "refresh");
      setIsAuthenticated(true);
    }else{
      setSubmitted(false);
      setIsAuthenticated(false);
    }
    setError(res.message)
  }

  if(isAuthenticated){
    router.push('/dashboard')
  }

  if(isLoading){
    return (<h2>Loading ...</h2>)
  }
  
  if(isAuthenticated){
    window.location.href = '/dashboard'
  }

  return (
    <div className="flex flex-col items-center justify-center gap-20">
      <div className="flex flex-col gap-6 md:flex-row w-full">
        <div className="hidden my-auto md:block">
          <div className="mockup-code">
            <pre data-prefix="$"><code>login user</code></pre>
            {submitted?
            <pre data-prefix=">" className="text-warning">
              <code className="items-center my-auto">
               <>Authenticating In<span className="loading loading-dots loading-sm"></span></>
              </code>
            </pre>:null}
            <pre data-prefix=">" className="text-success"><code>
              {error}
            </code></pre>
          </div>
        </div>

        {/* divider */}
        <div className="divider divider-horizontal font-bold" >Tasko</div>

        {/* Form Section */}
        <div className="card bg-base-100 w-full max-w-sm shrink-0 shadow-2xl p-4">
          <div className='font-bold text-xs'><code>Authentication</code></div>

          {/* Form */}
          <form onSubmit={handleSubmit(onSubmit)} className='flex flex-col col-start-3 gap-4'>
            <p className='text-red-500'>{errors.email?.message}</p>
            <div className="input input-bordered flex items-center gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                fill="currentColor"
                className="h-4 w-4 opacity-70">
                <path
                  d="M2.5 3A1.5 1.5 0 0 0 1 4.5v.793c.026.009.051.02.076.032L7.674 8.51c.206.1.446.1.652 0l6.598-3.185A.755.755 0 0 1 15 5.293V4.5A1.5 1.5 0 0 0 13.5 3h-11Z" />
                <path
                  d="M15 6.954 8.978 9.86a2.25 2.25 0 0 1-1.956 0L1 6.954V11.5A1.5 1.5 0 0 0 2.5 13h11a1.5 1.5 0 0 0 1.5-1.5V6.954Z" />
              </svg>
              <Input type='email' placeholder='Email Address' className='grow' defaultValue="john.doe@domain.com" data-focus data-hover {...register("email")}/>
            </div>

            <p className='text-red-500'>{errors.password?.message}</p>
            
            <div className="input input-bordered flex items-center gap-2">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 16 16"
                fill="currentColor"
                className="h-4 w-4 opacity-70">
                <path
                  fillRule="evenodd"
                  d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
                  clipRule="evenodd" />
              </svg>
              <Input type='password' placeholder='********' className='grow' defaultValue="john_45#" data-focus data-hover {...register("password")} />
            </div>
            {!submitted?<Button role="submit" type="submit" className='btn btn-success'>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                  className="h-4 w-4 opacity-70">
                  <path
                    fillRule="evenodd"
                    d="M14 6a4 4 0 0 1-4.899 3.899l-1.955 1.955a.5.5 0 0 1-.353.146H5v1.5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1-.5-.5v-2.293a.5.5 0 0 1 .146-.353l3.955-3.955A4 4 0 1 1 14 6Zm-4-2a.75.75 0 0 0 0 1.5.5.5 0 0 1 .5.5.75.75 0 0 0 1.5 0 2 2 0 0 0-2-2Z"
                    clipRule="evenodd" />
                </svg>
                Log In
              </Button>:
              <button 
                type="button" className="btn disabled:bg-purple-800 disabled:text-white" disabled>
                <span className="loading loading-bars loading-lg"></span>
                Authenticating...
              </button>
            }
          </form>
        </div>
      </div>
    </div>
  )
}

export default Login