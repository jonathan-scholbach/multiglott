const DEFAULT_ENDPOINT = "/query/"


class ApiConnector {
    constructor(
        entityType,
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
        this.entityType = entityType
    }

    async find(key, value, relatedModels = []){
        const body = {
            entity_type: this.entityType,
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

    async edit(http, key, value, data){
        const body = {
            entity_type: this.entityType,
            key: key,
            value: value,
            data: data
        }
        
        try {
            let response = await http.put(
                this.endpoint,
                body,
                {
                    headers: {
                        "Content-Type": "application/json"
                    }
                }
            )

            return response.data
        } catch(error){
            console.log(error)
        }
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

class ApiModel {
    async serialized() {
        
        let dict = Object.getOwnPropertyNames(this).reduce(
            (data, key) => {
                data[key] = this[key]
                return data
            }, {})

        return dict
    }

    async update(http, entityType = null) {
        if (entityType === null){ entityType = this.constructor.name }
        const connection = new ApiConnector(entityType, http)
        const serialized = await this.serialized()

        const response = await connection.edit(
            http,
            "id",
            this.id,
            serialized
        )

        return response
    }
}


async function findApiModel(
    http, 
    apiModelClass, 
    key, 
    value, 
    relatedModels=[], 
    entityType = null
){
    // From API, retrieve an ApiModel instance by an identifier key.
    const instance = new apiModelClass()
    
    if (entityType === null){ entityType = instance.constructor.name }
    const connection = new ApiConnector(entityType, http)
    if (!apiModelClass.IDENTIFIERS.includes(key)){
        throw "Trying to find ApiModel " +  entityType + " by non-Identifier key " + key
    }

    const data = await connection.find(key, value, relatedModels)

    return updateInstanceByData(instance, data)
}

export { findApiModel, ApiModel, ApiConnector, updateInstanceByData }
