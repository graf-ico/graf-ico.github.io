import * as React from 'react';

interface ISidebarProps {
    selectedGroup: string,
}

class Sidebar extends React.Component<ISidebarProps, {}> {
    constructor(props: ISidebarProps) {
        super(props);
    }

    public render() {
        return (
            <div id="sidebar">
                <p>{this.props.selectedGroup}</p>
            </div>
        );
    }
}

export default Sidebar;