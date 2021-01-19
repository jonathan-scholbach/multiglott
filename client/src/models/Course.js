import { ApiFinder, updateInstanceByData } from "./ApiFinder"


class Course {
    static IDENTIFIERS = ["id", "slug"];

    id = null;
    author_id = null;
    title = null;
    slug = null;
    target_language_id = null;
    target_language = null;
    source_language_id = null;
    source_language = null;
    lessons = null;
    privileges = [];
}


async function findCourse(http, key, value, relatedModels) {
    const finder = new ApiFinder("Course", http)

    if (!Course.IDENTIFIERS.includes(key)){
        throw "Trying to find Course by non-Identifier key " + key
    }
    const data = await finder.find(key, value, relatedModels)

    return updateInstanceByData(new Course(), data)
}


export { Course, findCourse }