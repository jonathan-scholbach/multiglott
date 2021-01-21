import { ApiModel, ApiConnector, updateInstanceByData } from "./ApiModel"


export default class Vocab extends ApiModel {
    static IDENTIFIERS = ["id"];
    
    id = null;
    source = null;
    target = null;
    hint = null;
    privileges = [];

    constructor(id=null, source, target, hint, privileges = []){
        super()

        this.id = id
        this.source = source
        this.target = target
        this.hint = hint
        this.privileges = privileges
    }
}

export async function findVocab(http, key, value, relatedModels = []) {
    const finder = new ApiConnector("Vocab", http)

    if (!Vocab.IDENTIFIERS.includes(key)) {
        throw "Trying to find Vocab by non-Identifier key " + key
    }
    const data = await finder.find(key, value, relatedModels)
    return updateInstanceByData(new Vocab(), data)
}