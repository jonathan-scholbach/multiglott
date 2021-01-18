import { ApiFinder, updateInstanceByData } from "./ApiFinder"

class Lesson {
    static IDENTIFIERS = ["id", "slug"]

    id = null;
    title = null;
    slug = null;
    course_id = null;
    vocabs = [];
    accomplishment = null;
    privileges = [];

    async getAccomplishment(http) {
        if (this.id == undefined) {
            let result = await findLesson("slug", this.slug)
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

async function findLesson(http, key, value, relatedModels = []) {
    const finder = new ApiFinder("Lesson", http)

    if (!Lesson.IDENTIFIERS.includes(key)){
        throw "Trying to find ApiModel by non-Identifier key " + key
    }
    const data = await finder.find(key, value, relatedModels)

    return updateInstanceByData(new Lesson(), data)
}

export { Lesson, findLesson }