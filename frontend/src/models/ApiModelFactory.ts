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

function updateInstanceByData<Schema>(instance: Schema, data: object) {
    // Replace members of instance with corresponding values from data, 
    //     ignoring superfluous key-value pairs in data.
    for (let key of Object.getOwnPropertyNames(instance)){
        if (Object.keys(data).includes(key)){
            instance[key as keyof Schema] = data[key as keyof typeof data]
        }    
    }
}



class BaseSchema{
    id: string | null = null;
}

function apiModelFactory<Schema extends BaseSchema>(
    schema: typeof Schema,
    entityType: string,
    identifiers: string[]
){
    const finder = new ApiFinder(entityType)

    class Model extends schema {
        static async find(
            {key, value, relatedModels}: 
            {key: string, value: any, relatedModels: string[] = []
        ): Promise<typeof schema> {
            if (!identifiers.includes(key){
                throw "Trying to find ApiModel by non-Identifier key " + key
            }
            let data = await finder.find(key, value, relatedModels)

            return Object.assign(new schema(), data)
        }
            
        async update(key: string, value: any, data: Object){
            const response = await finder.update(key, value, data)
            updateInstanceByData(this, response)
        }

    }

    return Model
}

class VocabSchema extends BaseSchema {
    target: string | null = null;
    source: string | null = null;
    hint: string | null = null;
}

class LessonSchema extends BaseSchema {
    id: string | null = null;
    title: string | null = null;
    slug: string | null = null;
    course_id: number | null = null;
    vocabs: VocabSchema[] = [];
    accomplishment: number | null = null;

}

export const Lesson = new apiModelFactory(
    LessonSchema, 
    "Lesson", 
    ["id", "slug"]
)