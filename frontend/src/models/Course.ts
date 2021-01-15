import { ApiModel } from "./ApiModel"
import Lesson from "./Lesson"



export default class Course extends ApiModel {
    static IDENTIFIERS = ["id", "slug"]

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
