
export type ProjectName = string;

export interface IProjectDetails {
    category: string,
    member_count: number,
    telegram_description: string,
    title: string,
    image?: any,
}

export interface IProjects { [project: string]: IProjectDetails }

export interface IOverlaps { [project: string]: number }

export interface INodeData {
    "group": string,
    "id": string,
    "overlap": number,
    "size": number,
    "image": any,
}