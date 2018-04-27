import * as React from 'react';

interface ISidebarProps {
    selectedGroup: string,
    selectedDetails: any,
}

class Sidebar extends React.Component<ISidebarProps, {}> {
    constructor(props: ISidebarProps) {
        super(props);
    }

    public render() {
        return (
            <div id="sidebar">
                <div className="infomation">
                    <p>{this.props.selectedGroup}</p>
                </div>
            </div>
        );
    }
}

export default Sidebar;