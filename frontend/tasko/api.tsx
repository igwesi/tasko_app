import axios from 'axios';
import Cookies from 'js-cookie';
import { ACCESS_TOKEN, BACKEND_API } from "@/app/constants";


// Centralized error handling function
const handleError = (error: any) => {
    console.error(error.response.data.message);
};

const api = axios.create({
    baseURL: BACKEND_API,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
});


if(Cookies.get(ACCESS_TOKEN)) {
    api.interceptors.request.use((config) => {
        config.headers['Authorization'] = `Bearer ${Cookies.get(ACCESS_TOKEN)}`;
        return config;
    }, handleError);
}

const get = async(url:string): Promise<any> => {
    return await api.get(url);
}

// Function to perform POST requests with authorization
const post = async (url: string, data: any): Promise<any> => {
    return await api.post(url, data);
};

export const ApiActions = () => ({
    get,
    post
});