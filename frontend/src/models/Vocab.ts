import { ApiModel } from "./ApiModel"


export default class Vocab extends ApiModel {
    IDENITFIERS = ["id"]

    id: number | null = null;
    source: string[] | null = null;
    target: string[] | null = null;
    hint: string | null = null;
}