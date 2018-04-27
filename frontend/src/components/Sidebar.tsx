import * as React from 'react';
import { IProjectDetails, ProjectName } from '../types';

import '../styles/Sidebar.css';

interface ISidebarProps {
    selectedGroup: ProjectName,
    selectedDetails?: IProjectDetails,
}

class Sidebar extends React.Component<ISidebarProps, {}> {
    constructor(props: ISidebarProps) {
        super(props);
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
                        <p>{this.props.selectedDetails.member_count}</p>
                    </div>
                </div>

                <div className="information">
                    <p>{this.props.selectedDetails.telegram_description}</p>
                </div>
            </div>
        );
    }
}

export default Sidebar;