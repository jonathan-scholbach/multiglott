import axios from "axios"


export default function apiSetup(store) {
    axios.interceptors.request.use(function(config) {
        const token = store.getters.token
        config.headers.Authorization = token ? `Bearer ${token}` : ''
        config.headers["Access-Control-Allow-Origin"] = "*"
        return config
    }, function(err) {
        return Promise.reject(err)
    });
}