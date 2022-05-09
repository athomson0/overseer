import axios from 'axios';

const API_BASE = 'http://127.0.0.1:5000'

const apiClient = axios.create({
    baseURL: API_BASE,
    headers: {
        "Content-type": "application/json"
    }
});

export default apiClient;

