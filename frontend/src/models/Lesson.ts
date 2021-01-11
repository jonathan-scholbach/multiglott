import { ApiModel }  from "./ApiModel"
import { Vocab } from "./Vocab"

export { Lesson }


class Lesson extends ApiModel  {
    IDENTIFIERS = ["id", "slug"]

    id?: number
    title?: string
    slug?: string
    vocabs?: Vocab[]
}