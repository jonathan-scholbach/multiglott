import { ApiModel } from "./ApiModel"
import { Lesson } from "./Lesson"



export class Course extends ApiModel {
    id: number | undefined;
    title: string | undefined;
    slug: string | undefined;
    target_language_id: number | undefined;
    target_language: string | undefined;
    source_language_id: number | undefined;
    source_language: string | undefined;
    lessons: Lesson[] | undefined;

    constructor(
        id?: number,
        title?: string,
        slug?: string,
        target_language_id?: number,
        target_language?: string,
        source_language_id?: number,
        source_language?: string,
        lessons?: Lesson[],
    ){
        super(["id", "slug"])
        
        this.id = id
        this.slug=slug
        this.title = title
        this.target_language_id = target_language_id
        this.target_language = target_language
        this.source_language_id = source_language_id
        this.source_language = source_language
        this.lessons = lessons
    }
}
