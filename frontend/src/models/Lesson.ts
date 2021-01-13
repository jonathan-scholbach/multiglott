import { ApiModel }  from "./ApiModel"
import { Vocab } from "./Vocab"


export default class Lesson extends ApiModel  {
    static IDENTIFIERS = ["id", "slug"]

    id: number | null = null;
    title: string | null = null;
    slug: string | null = null;
    course_id: number | null = null;
    vocabs: Vocab[] = [];
    

    async getAccomplishment(http): number {
        if (this.id == undefined) {
            await this.constructor.find()
        }
        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.accomplishment
    }

    async getNextVocable(http) {
        if (this.id == undefined) {
            await this.constructor.find()
        }

        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.vocab
    }
}