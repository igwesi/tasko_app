import { get, post } from '@/api';
export const register = async (email:string, password:string) => {
    const json = {
        'email':email,
        'password':password
    }
    try {
        const response = await post('/user/register/', json);
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

export const login = async (email:string, password:string) => {
    const json = {
        'email':email,
        'password':password
    }
    console.log(json);
    try {
        const response = await post('/user/login/', json);
        return response;
    } catch (error) {
        console.error(error);
    }
}


export const logout = async () => {
    try {
        const response = await get('/user/logout/');
        return response.data;
    } catch (error) {
        console.error(error);
    }
}
