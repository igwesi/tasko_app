import axios from 'axios';
import Cookies from 'js-cookie';
import { ACCESS_TOKEN, BACKEND_API } from "@/app/constants";


const api = axios.create({
    baseURL: process.env.BACKEND_API,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
});

if(Cookies.get(ACCESS_TOKEN)) {
    api.interceptors.request.use((config) => {
        config.headers['Authorization'] = `Bearer ${Cookies.get(ACCESS_TOKEN)}`;
        return config;
    });
}

// Centralized error handling function
const handleError = (error: any) => {
    return Promise.reject(error.response?.data || error.message);
};

const get = (url:string): Promise<any> => {
    return api.get(url);
}

// Function to perform POST requests with authorization
const post = (url: string, data: any): Promise<any> => {
    return api.post(url, data);
};

export const ApiActions = () => ({
    get,
    post
});