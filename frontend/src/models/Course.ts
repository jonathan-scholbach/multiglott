import { ApiFinder, updateInstanceByData } from "./ApiFinder"


import Lesson from "./Lesson"


export default class Course {
    static IDENTIFIERS: string[] = ["id", "slug"];

    id: number | null = null;
    author_id: number | null = null;
    title: string | null = null;
    slug: string | null = null;
    target_language_id: number | null = null;
    target_language: string | null = null;
    source_language_id: number | null = null;
    source_language: string | null = null;
    lessons: Lesson[] | null = null;
}


export async function findCourse(key: string, value: any, relatedModels: string[]): Promise<Course>{
    const finder = new ApiFinder("Course")

    if (!Course.IDENTIFIERS.includes(key)){
        throw "Trying to find Course by non-Identifier key " + key
    }
    const data = await finder.find(key, value, relatedModels)

    return updateInstanceByData(new Course(), data)
}

