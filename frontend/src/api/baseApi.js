import axios, { AxiosResponse } from "axios";
import Cookies from 'js-cookie';

const delayValue = 1000;
const csrftoken = Cookies.get('csrftoken');

axios.defaults.baseURL = "http://localhost:8000/api/v1";
if (csrftoken) axios.defaults.headers.common['x-csrftoken'] = csrftoken


axios.interceptors.request.use(
    (config) => {
        const token = window.localStorage.getItem("jwt");

        if (token) config.headers.Authorization = `${token}`;

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export const sleep = (ms) => (response) =>
    new Promise((resolve) =>
        setTimeout(() => resolve(response), ms)
    );

export const responseBody = (response) => response.data;

export const requests = {
    get: (url) =>
        axios.get(url).then(sleep(delayValue)).then(responseBody),
    post: (url, body) =>
        axios.post(url, body, { withCredentials: true }).then(sleep(delayValue)).then(responseBody),
    put: (url, body) =>
        axios.put(url, body, { withCredentials: true }).then(sleep(delayValue)).then(responseBody),
    delete: (url) =>
        axios.delete(url, { withCredentials: true }).then(sleep(delayValue)).then(responseBody),
};