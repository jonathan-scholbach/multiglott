import { axiosInstance } from "../main";


interface FindRequestBody{
    entity_type: string;
    key: string;
    value: any;
    related_models: string[];
}


enum Privilege{
    CAN_READ = "CAN_READ",
    CAN_EDIT = "CAN_EDIT",
    CAN_DELETE = "CAN_DELETE",
}


class ApiFinder {
    endpoint: string;
    entity_type: string;
    http: any;

    constructor(entity_type: string, endpoint: string = "/query/", http = axiosInstance) {
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

    async find(key: string, value: any, relatedModels: string[] = []) {
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
}


export class ApiModel  {
    static ENTITY_TYPE: string | null = null;
    static IDENTIFIERS: string[];
    
    privileges: Privilege[] = [];

    static entity_type(): string {
        if (this.ENTITY_TYPE !== null) {
            return this.ENTITY_TYPE
        }

        return this.name
    }

    static async find(key: string, value: any, relatedModels: string[] = []){
        let finder = new ApiFinder(this.entity_type())
        if (! this.IDENTIFIERS.includes(key)){
            throw "Trying to find ApiModel by non-Identifier key " + key
        }
        let data = await finder.find(key, value, relatedModels)
        
        var instance = new this;
        
        Object.getOwnPropertyNames(instance).forEach((key) => {
            if (data[key] != undefined){
                instance[key] = data[key]
            }
        })

        return instance
    }

}
