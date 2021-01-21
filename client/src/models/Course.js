import { ApiModel, ApiConnector, updateInstanceByData } from "./ApiModel"


export default class Course extends ApiModel {
    static IDENTIFIERS = ["id", "slug"];

    id = null;
    author_id = null;
    title = null;
    slug = null;
    target_language_id = null;
    target_language = null;
    source_language_id = null;
    source_language = null;
    lessons = [];
    lesson_order = [];
    privileges = [];

    constructor(
        id = null,
        author_id = null,
        title = null,
        slug = null,
        target_language_id = null,
        target_language = null,
        source_language_id = null,
        source_language = null,
        lessons = [],
        lesson_order = [],
        privileges = []
    ){
        super()

        this.id = id
        this.author_id = author_id
        this.title = title
        this.slug = slug
        this.target_language_id = target_language_id
        this.target_language = target_language
        this.source_language_id = source_language_id
        this.source_language = source_language
        this.lessons = lessons
        this.lesson_order = lesson_order
        this.privileges = privileges
    }
}
