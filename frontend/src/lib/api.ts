import axios from 'axios';

import { IOverlaps, IProjects, ProjectName } from "../types";

const URL = 'https://grafico.***REMOVED***.com';

export const getRelations = async (group: ProjectName): Promise<IOverlaps> => {
    return (await axios.get(URL + '/overlaps/' + group)).data;
}

export const getProjects = async (): Promise<IProjects> => {
    return (await axios.get(URL + '/groups')).data;
}