import axios from 'axios';
import * as React from 'react';
// import * as rd3 from 'react-d3-library';
import { render, setNodes } from '../lib/Graph';

import { INodeData, IOverlaps, IProjectDetails, IProjects, ProjectName } from '../types';

// const RD3Component = rd3.Component;

interface IGraphProps {
    graphedGroup: ProjectName,
    data: IProjects,
    setSelectedGroup: (group: ProjectName) => void,
}

interface IGraphState {
    data: HTMLElement | null;
}

class Graph extends React.Component<IGraphProps, IGraphState> {

    constructor(props: IGraphProps) {
        super(props);
        this.state = { data: null };
    }

    public async componentWillReceiveProps(props: IGraphProps) {

        if (props.data !== this.props.data) {
            const nodes: INodeData[] = Object.keys(props.data).map((key: ProjectName) => {
                const value: IProjectDetails = props.data[key];
                return {
                    group: value.category,
                    id: key,
                    image: value.image,
                    overlap: 0,
                    size: value.member_count,
                };
            })

            setNodes(nodes, props.setSelectedGroup)
        }

        // tslint:disable-next-line:no-console
        console.log("Received new props!")

        if (props.data && (props.graphedGroup !== this.props.graphedGroup) ||
            (Object.keys(this.props.data).length === 0 && props.graphedGroup)) {
            const relations: IOverlaps = (await axios.get('http://localhost:5000/overlaps/' + props.graphedGroup)).data;
            const main: INodeData = {
                group: 'main',
                id: props.graphedGroup,
                image: props.data[props.graphedGroup].image,
                overlap: 0,
                size: props.data[props.graphedGroup].member_count,
            };

            const others: INodeData[] = Object.keys(relations).map((key: ProjectName) => {
                const value = props.data[key];
                return {
                    group: value.category,
                    id: key,
                    image: value.image,
                    overlap: 100 * (relations[key] / Math.min(value.member_count, main.size)),
                    size: value.member_count,
                };
            });

            render(main, others);
        }
    }

    public render() {
        return (
            <div id="graph">
                <svg id="graph-svg" height="1000" width="500" />
            </div>
        )
    }
};

export default Graph;