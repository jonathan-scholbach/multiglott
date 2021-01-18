import { axiosInstance } from "../main";

const DEFAULT_HTTP = axiosInstance
const DEFAULT_ENDPOINT = "/query/"


class ApiFinder {
    entity_type: string;
    endpoint: string;
    http: any;

    constructor(
        entity_type: string, 
        endpoint: string = DEFAULT_ENDPOINT, 
        http = DEFAULT_HTTP,
    ) {
        this.http = http
        if (!endpoint.startsWith("/")) {
            endpoint = "/" + endpoint
        }
        if (!endpoint.endsWith("/")) {
            endpoint = endpoint + "/"
        }
        this.endpoint = endpoint
        this.entity_type = entity_type
    }

    async find(key: string, value: any, relatedModels: string[] = []){
        const body = {
            entity_type: this.entity_type,
            key: key,
            value: value,
            related_models: relatedModels
        }
        
        const response = await this.http.post(
            this.endpoint,
            body,
            {
                headers: {
                    "Content-Type": "application/json"
                }
            }
        
        )
        return response.data
    }
    async update(key: string, value: any, data: Object){
        let body = {
            entity_type: this.entity_type,
            key: key,
            value: value,
            data: data
        }

        let response = await this.http.put(
            this.endpoint,
            body,
            {
                headers: {
                    "Content-Type": "application/json"
                }
            }
        )

        return response.data
    }
}

function updateInstanceByData<C>(instance: C, data: object): C {
    // Replace members of instance with corresponding values from data, 
    //     ignoring superfluous key-value pairs in data.
    for (let key of Object.getOwnPropertyNames(instance)){
        if (Object.keys(data).includes(key)){
            instance[key as keyof C] = data[key as keyof typeof data]
        }    
    }

    return instance
}

export { ApiFinder, updateInstanceByData }
