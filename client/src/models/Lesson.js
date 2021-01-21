import { findApiModel } from "./ApiModel";
import { ApiModel } from "./ApiModel"


export default class Lesson extends ApiModel {
    static IDENTIFIERS = ["id", "slug"]

    id = null;
    title = null;
    slug = null;
    course_id = null;
    vocabs = [];
    accomplishment = null;
    privileges = [];

    constructor(
        id=null, 
        title, 
        slug, 
        course_id, 
        vocabs = [], 
        accomplishment = null, 
        privileges = []
    ){
        super()

        this.id = id
        this.title = title
        this.slug = slug
        this.course_id = course_id
        this.vocabs = vocabs 
        this.accomplishment = accomplishment
        this.privileges = privileges
    }

    async getAccomplishment(http) {
        if (this.id == undefined) {
            let result = await findApiModel("slug", Lesson, this.slug)
            this.id = result.id
        }
        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.accomplishment
    }

    async getNextVocab(http) {
        var url = "/me/lesson/" + this.id

        let response = await http.get(url)
        return response.data.vocab
    }
}
