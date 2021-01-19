const DEFAULT_ENDPOINT = "/query/"


class ApiFinder {
    constructor(
        entity_type,
        http,
        endpoint = DEFAULT_ENDPOINT,
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

    async find(key, value, relatedModels = []){
        const body = {
            entity_type: this.entity_type,
            key: key,
            value: value,
            related_models: relatedModels
        }
        
        let model = await this.http.post(
            this.endpoint,
            body,
            {
                headers: {
                    "Content-Type": "application/json"
                }
            }
        )
        return model.data
    }

    async update(key, value, data){
        const body = {
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
        console.log("APiFInder response ", response)
        return response.data
    }
}

function updateInstanceByData(instance, data) {
    // Replace members of instance with corresponding values from data, 
    //     ignoring superfluous key-value pairs in data.
    for (let key of Object.getOwnPropertyNames(instance)){
        if (Object.keys(data).includes(key)){
            instance[key] = data[key]
        }    
    }

    return instance
}

export { ApiFinder, updateInstanceByData }
