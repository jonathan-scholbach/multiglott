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

    async find(value: any, key: string, relatedModels: string[] = []) {
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
    ENTITY_TYPE: string
    IDENTIFIERS: string[]
    
    finder: ApiFinder
    privileges: Privilege[] | undefined

    constructor(identifiers: string[], entity_type?: string){
        if (!entity_type){
            entity_type = this.constructor.name
        }
        this.ENTITY_TYPE = entity_type
        this.IDENTIFIERS = identifiers
        this.finder = new ApiFinder(this.ENTITY_TYPE)
    }

    async find(relatedModels: string[] = []){
        var data = {}

        for (let identifier of this.IDENTIFIERS){            
            if (this[identifier] != undefined){
                data = await this.finder.find(
                    this[identifier], identifier, relatedModels
                )
                break
            }
        }
        if (!data){
            throw "Missing identifier while trying to find " + this.constructor.name
        }
        
        Object.getOwnPropertyNames(data).forEach((key) => {
            if (data[key] != undefined){
                this[key] = data[key]
            }
        })
    }
}
