import { axiosInstance } from "../main";


interface ApiFindMethod {
    (
        key: string, 
        value: any, 
        relatedModels: string[], 
        endpoint: string
    ): ApiModel;
}


interface ApiUpdateMethod {
    (key: string, value: any, data: object, endpoint: string): ApiModel
}


interface ApiModel {
    entityType: string;
    identifiers: string[];
    find: ApiFindMethod;
    update: ApiUpdateMethod;
}

class ApiFinder {
    entity_type: string;
    endpoint: string;
    http: any;
    find: any;
    update: any;

    constructor(
        entity_type: string, 
        endpoint: string = "/query/", 
        http = axiosInstance
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

    find = async(key: string, value: any, relatedModels: string[] = []) => {
        let body: FindRequestBody = {
            entity_type: this.entity_type,
            key: key,
            value: value,
            related_models: relatedModels
        }
        
        let response = await this.http.post(
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
    
    update = async (key: string, value: any, data: Object) => {
        let body: PutRequestBody = {
            entity_type: this.entity_type,
            key: key,
            value: value,
            data: data
        }

        let response = await self.http.put(
            self.endpoint,
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

class ApiModel{
    identifiers: string[];
    finder: ApiFinder;
    find: object;
}

function ApiModelFactory<T>(
    entity_type: string, 
    identifiers: string[], 
    model: T
): <Model extends T>{
    
    var self = this
    var apiFinder = new ApiFinder(entity_type)

    class Model implements ApiModel extends model{
        identifiers = identifiers
        finder = apiFinder
    }
        
    const find = async (
        {key, value, relatedModels}: 
        {key: string, value: any, relatedModels: string[]
    ) => {
        if (!this.identifiers.includes(key){
            throw "Trying to find ApiModel by non-Identifier key " + key
        }
        let data = await this.finder.find(key, value, relatedModels)
    }
    api_model.find = find

    const update = async (data: Object) => {

        var key: string
        var value: any

        for (let idKey in this.cls().IDENTIFIERS){
            if (this[idKey] != undefined){
                key = idKey
                value = this[idKey]
                break
            }
        }
        
        let response = await finder.update(key, value, data)
        console.log(response)
    }

}
