import { axiosInstance } from "../main";

import { ApiModel }  from "./ApiModel"
import Vocab from "./Vocab"


export default class Lesson extends ApiModel  {
    static IDENTIFIERS = ["id", "slug"]

    id: number | null = null;
    title: string | null = null;
    slug: string | null = null;
    course_id: number | null = null;
    vocabs: Vocab[] = [];
    accomplishment: number | null = null;

    async getAccomplishment(http = axiosInstance) {
        if (this.id == undefined) {
            let result = await Lesson.find("slug", this.slug)
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