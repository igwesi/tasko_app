import { ApiActions } from "@/api";
import Cookies from "js-cookie";

const { post, get} = ApiActions();

const storeToken = (token:string, type: "access" | "refresh") => {
    Cookies.set(type + "Token", token);
};

const getToken = (type:string) => {
    return Cookies.get(type + "Token");
};

const accessToken = () =>{
    const token = getToken("access")
    return token;
}

const removeTokens = () => {
    Cookies.remove("accessToken");
    Cookies.remove("refreshToken");
};
  

const formatResponse = (response:any) =>{
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

const handleJWTRefresh = async() => {
    try{
        const response = await post('/token/refresh', getToken("refresh"));
        return response.data;
    }catch(error){
        console.error("Error while refreshing token", error);
    }
};

const register = async (email:string, password:string) => {
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
};

const login = async(email:string, password:string): Promise<any> => {
    const json = {
        'email':email,
        'password':password
    }
    const response = await post('/user/login/', json);
    return response.data;
};

const getUser = async () => {
    try {
        const response = (await get('/user/me'));
        return response.data;
    } catch (error) {
        console.error(error);
    }
};

const logout = async () => {
    removeTokens();
    return true;
};

export const AuthActions = () => {
    return {
        get,
        login,
        logout,
        getUser,
        register,
        storeToken,
        accessToken,
        getToken,
        removeTokens,
        handleJWTRefresh,
    };
};