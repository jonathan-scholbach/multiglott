import { ApiFinder, updateInstanceByData } from "./ApiFinder"


export default class Vocab {
    static IDENTIFIERS: string[] = ["id"];
    id: number | null = null;
    source: string[] | null = null;
    target: string[] | null = null;
    hint: string | null = null;
}

export async function findVocab(key: string, value: any, relatedModels: string[]): Promise<Vocab> {
    const finder = new ApiFinder("Vocab")

    if (!Vocab.IDENTIFIERS.includes(key)) {
        throw "Trying to find Vocab by non-Identifier key " + key
    }
    const data = await finder.find(key, value, relatedModels)
    return updateInstanceByData(new Vocab(), data)
}