import axios from 'axios';
import * as React from 'react';
// import * as rd3 from 'react-d3-library';
import { initialise, render } from '../lib/Graph';

// const RD3Component = rd3.Component;

interface IGraphProps {
    graphedGroup: string,
    setSelectedGroup: (group: string) => void,
}

interface IGraphState {
    data: HTMLElement | null;
}

class Graph extends React.Component<IGraphProps, IGraphState> {

    constructor(props: IGraphProps) {
        super(props);
        this.state = { data: null };
    }

    public async componentDidMount() {
        // this.setState({ data: node });

        const name = this.props.graphedGroup;
        const othersJSON = (await axios.get('http://localhost:5000/groups')).data;
        // tslint:disable-next-line:no-console
        console.log(othersJSON);
        const relations = (await axios.get('http://localhost:5000/overlaps/' + name)).data;
        // tslint:disable-next-line:no-console
        console.log(relations);


        const main = { "id": name, "size": othersJSON[name].member_count, group: 'main' };

        const nodes = Object.keys(othersJSON).map((key: any) => {
            const value = othersJSON[key];
            return {
                "group": value.category,
                "id": key,
                "overlap": 100 * (relations[key] / Math.min(value.member_count, main.size)),
                "size": value.member_count,
            };
        })

        initialise(nodes, this.props.setSelectedGroup);


        const others = Object.keys(relations).map((key: any) => {
            const value = othersJSON[key];
            return {
                "group": value.category,
                "id": key,
                "overlap": 100 * (relations[key] / Math.min(value.member_count, main.size)),
                "size": value.member_count,
            };
        });

        // const main = { "id": "A", "size": 13000, "group": 0 };
        // const others = [
        //     { "id": "bitfwd", "size": 100, "group": "crypto/project", "distance": 0 },
        //     { "id": "C", "size": 100000, "group": 1, "distance": 88 },
        //     { "id": "D", "size": 1000, "group": 1, "distance": 50 },
        //     { "id": "E", "size": 100, "group": 1, "distance": 55 },
        //     { "id": "F", "size": 15000, "group": 1, "distance": 10 },
        //     { "id": "G", "size": 1000, "group": 1, "distance": 22 },
        //     { "id": "H", "size": 10000, "group": 2, "distance": 100 },
        // ];
        render(main, others);
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