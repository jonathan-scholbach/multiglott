import { ApiModel } from "./ApiModel"
import { Lesson } from "./Lesson"



export default class Course extends ApiModel {
    static IDENTIFIERS = ["id", "slug"]

    id: number | undefined = null;
    author_id: number | undefined = null;
    title: string | undefined = null;
    slug: string | undefined = null;
    target_language_id: number | undefined = null;
    target_language: string | undefined = null;
    source_language_id: number | undefined = null;
    source_language: string | undefined = null;
    lessons: Lesson[] | undefined = null;
}
