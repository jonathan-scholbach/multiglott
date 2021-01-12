import { axiosInstance } from "../main";


interface GetRequestBody{
    key: string;
    value: any;
}


enum Privilege{
    CAN_READ = "CAN_READ",
    CAN_EDIT = "CAN_EDIT",
    CAN_DELETE = "CAN_DELETE",
}


class ApiGetter {
    endpoint: string;
    http: any;

    constructor(endpoint: string, http = axiosInstance) {
        this.http = http
        if (!endpoint.startsWith("/")) {
            endpoint = "/" + endpoint
        }
        this.endpoint = endpoint
    }

    async get(value: any, key: string = "id") {
        let body: GetRequestBody = {
            key: key,
            value: value
        }

        this.http.get(
            this.endpoint,
            body,
            {
                headers: {
                    "Content-Type": "application/json"
                }
            }
        ).then(
            (response) => {
                return response.data
            }
        ).catch((error) => {
            console.log(error)
        })
    }


}


export class ApiModel  {
    ENDPOINT: string
    IDENTIFIERS: string[]
    
    getter: ApiGetter
    privileges: Privilege[] | undefined

    constructor(identifiers: string[], endpoint?: string){
        if (!endpoint){
            endpoint = this.constructor.name.toLowerCase() + "s"
        }
        this.ENDPOINT = endpoint
        this.IDENTIFIERS = identifiers 
        this.getter = new ApiGetter(this.ENDPOINT)
    }

    find(){
        var data = {}
        for (let identifier of this.IDENTIFIERS){
            if (identifier in this){
                data = this.getter.get(this[identifier], identifier)
                break
            }
        }
        if (!data){
            throw "Missing identifier while trying to find " + this.constructor.name
        }
        
        Object.getOwnPropertyNames(this).forEach((key) => {
            if (key in data){
                this[key] = data[key]
            }
        })
    }
}
