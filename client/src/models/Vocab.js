import { ApiFinder, updateInstanceByData } from "./ApiFinder"


export default class Vocab {
    static IDENTIFIERS = ["id"];
    
    id = null;
    source = null;
    target = null;
    hint = null;
    privileges = [];

    constructor(id=null, source, target, hint, privileges = []){
        this.id = id
        this.source = source
        this.target = target
        this.hint = hint
        this.privileges = privileges
    }

    async update(http) {
        const finder = new ApiFinder("Vocab", http)
        
        let response = await finder.update(
            "id",
            this.id,
            {
                target: this.target,
                source: this.source,
                hint: this.hint,
            }
        )
        console.log("response ", response.target)
        return response
    }
}

export async function findVocab(http, key, value, relatedModels = []) {
    const finder = new ApiFinder("Vocab", http)

    if (!Vocab.IDENTIFIERS.includes(key)) {
        throw "Trying to find Vocab by non-Identifier key " + key
    }
    const data = await finder.find(key, value, relatedModels)
    return updateInstanceByData(new Vocab(), data)
}