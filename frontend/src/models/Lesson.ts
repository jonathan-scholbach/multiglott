import { AxiosInstance } from "axios"
import { axiosInstance } from "../main"

import { ApiFinder, updateInstanceByData } from "./ApiFinder"

import VocabSchema from "./Vocab"


export default class Lesson{
    id: number | null = null;
    title: string | null = null;
    slug: string | null = null;
    course_id: number | null = null;
    vocabs: VocabSchema[] = [];
    accomplishment: number | null = null;

    async getAccomplishment(http: AxiosInstance = axiosInstance) {
        if (this.id == undefined) {
            let result = await findLesson("slug", this.slug)
            this.id = result.id
        }
        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.accomplishment
    }

    async getNextVocab(http = axiosInstance) {
        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.vocab
    }
}

async function findLesson(
    key: string, 
    value: any, 
    relatedModels: string[] = []
): Promise<Lesson> {
    const finder = new ApiFinder("Lesson")

    if (!this.IDENTIFIERS.includes(key)){
        throw "Trying to find ApiModel by non-Identifier key " + key
    }
    const data = await finder.find(key, value, relatedModels)

    return updateInstanceByData(new Lesson(), data)
}
