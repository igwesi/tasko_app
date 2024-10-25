import axios from 'axios';

const api = axios.create({
    baseURL: process.env.BACKEND_API,
    headers: {
        'Content-Type': 'application/json',
    },
});


export const get = async(url:string) => {
    const response = await api.get(url);
    return response;
}

export const post = (url:string, data:any) => {
    return api.post(url, data);
}

export const fetchTasks = async () => {
    try {
        const response = await api.get('/tasks');
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export const createTask = async (task:any) => {
    try {
        const response = await api.post('/tasks', task);
        return response.data;
    } catch (error) {
        console.error(error);
    }
}