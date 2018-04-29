import * as React from 'react';
import { IProjectDetails, ProjectName } from '../types';

import processString from 'react-process-string';

import '../styles/Sidebar.css';

function renderText(text: string): string {

    const config = [{
        fn: (key: any, result: any) => <span key={key}>
            <a target="_blank" href={`${result[1]}://${result[2]}.${result[3]}${result[4]}`}>{result[2]}.{result[3]}{result[4]}</a>{result[5]}
        </span>,
        regex: /(http|https):\/\/(\S+)\.([a-z]{2,}?)(.*?)( |\,|$|\.)/gim,
    }, {
        fn: (key: any, result: any) => <span key={key}>
            <a target="_blank" href={`http://${result[1]}.${result[2]}${result[3]}`}>{result[1]}.{result[2]}{result[3]}</a>{result[4]}
        </span>,
        regex: /(\S+)\.([a-z]{2,}?)(.*?)( |\,|$|\.)/gim,
    }, {
        fn: (key: any, result: any) => <span key={key}>
            <a target="_blank" href={`https://t.me/${result[1]}`}>{result[0]}</a>
        </span>,
        regex: /\@([a-z0-9_\-]+?)( |\,|$|\.)/gim,
    }];

    return processString(config)(text);

    // Replace links with a tags:
    // text = text.replace(/([-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*))/g, <a>{'$1'}</a>)

    // text = text.replace(/@([A-Za-z0-9_]+)/g, 'https://t.me/$1')
}

interface ISidebarProps {
    selectedGroup: ProjectName,
    selectedDetails?: IProjectDetails,
    setGraphedGroup: (group: ProjectName) => void,
}

class Sidebar extends React.Component<ISidebarProps, {}> {
    constructor(props: ISidebarProps) {
        super(props);
    }

    public setGraphedGroup = () => {
        this.props.setGraphedGroup(this.props.selectedGroup)
    }

    public render() {
        if (!this.props.selectedDetails) {
            return <div id="sidebar" />
        }

        return (
            <div id="sidebar">
                <div className="information information_first">
                    <div className="info_left">
                        <img className="sidebar_logo" src={this.props.selectedDetails.image} />
                    </div>
                    <div className="info_right">
                        <h2>{this.props.selectedDetails.title}</h2>
                        <p>{renderText(`@${this.props.selectedGroup}`)} - {this.props.selectedDetails.member_count} users</p>
                    </div>
                </div>

                <div className="information">
                    <p>{renderText(this.props.selectedDetails.telegram_description)}</p>
                </div>

                <div className="information">
                    <button onClick={this.setGraphedGroup}>SEE OVERLAP WITH OTHER PROJECTS</button>
                </div>
            </div>
        );
    }
}

export default Sidebar;