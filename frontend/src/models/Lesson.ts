import { ApiModel }  from "./ApiModel"
import { Vocab } from "./Vocab"


export default class Lesson extends ApiModel  {
    IDENTIFIERS = ["id", "slug"]

    id: number | undefined
    title: string | undefined
    slug: string | undefined
    vocabs: Vocab[] | undefined

    async getAccomplishment(http): number {
        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.accomplishment
    }

    async nextVocable(http) {
        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.vocab
    }
}