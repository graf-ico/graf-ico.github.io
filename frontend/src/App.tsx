import * as React from 'react';
import { Col } from 'react-bootstrap';
import './App.css';

import Graph from './components/Graph'
// import Menu from './components/Menu'
import Sidebar from './components/Sidebar'

// import logo from './logo.svg';

interface IAppState {
  graphedGroup: string,
  selectedGroup: string,
}

class App extends React.Component<{}, IAppState> {

  constructor(props: {}) {
    super(props);
    this.state = {
      graphedGroup: 'republicprotocol',
      selectedGroup: 'republicprotocol',
    };
  }

  public setSelectedGroup = (group: string) => {
    this.setState({ selectedGroup: group });
  }

  public render() {
    return (
      <div className="App">
        <div id="content">
          <Graph setSelectedGroup={this.setSelectedGroup} graphedGroup={this.state.graphedGroup} />
          <Col md={4} className='col' id="side-col" >
            {/* <Menu /> */}
            <Sidebar selectedGroup={this.state.selectedGroup} />
          </Col>
        </div>
      </div>
    );
  }
}

export default App;
