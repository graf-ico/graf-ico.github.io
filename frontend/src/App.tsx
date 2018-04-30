import * as React from 'react';
import { Col } from 'react-bootstrap';
import './styles/App.css';

import Graph from './components/Graph'
// import Menu from './components/Menu'
import Sidebar from './components/Sidebar'

import * as api from './lib/api';

import { IProjectDetails, IProjects, ProjectName } from './types';

// import logo from './logo.svg';

interface IAppState {
  graphedGroup: ProjectName,
  selectedGroup: ProjectName,
  projects: IProjects,
}

class App extends React.Component<{}, IAppState> {

  constructor(props: {}) {
    super(props);
    this.state = {
      graphedGroup: 'republicprotocol',
      projects: {},
      selectedGroup: 'republicprotocol',
    };
  }

  public async componentDidMount() {
    const projects: IProjects = await api.getProjects();
    for (const key of Object.keys(projects)) {
      try {
        projects[key].image = require('../public/logos/' + key + '.png')
      } catch (err) {
        // tslint:disable-next-line:no-console
        console.log('No image for ' + key);
      }
    }
    this.setState({ projects });
  }

  public setSelectedGroup = (group: string) => {
    this.setState({ selectedGroup: group });
  }

  public setGraphedGroup = (group: string) => {
    this.setState({ graphedGroup: group });
  }

  public render() {
    let selectedDetails: IProjectDetails | undefined;
    if (this.state.projects) {
      selectedDetails = this.state.projects[this.state.selectedGroup];
      // tslint:disable-next-line:no-console
      console.log(selectedDetails);
    }

    return (
      <div className="App">
        <div id="content">
          <Graph data={this.state.projects} setSelectedGroup={this.setSelectedGroup} graphedGroup={this.state.graphedGroup} />
          <Col md={4} className='col' id="side-col" >
            {/* <Menu /> */}
            <Sidebar selectedDetails={selectedDetails} selectedGroup={this.state.selectedGroup} setGraphedGroup={this.setGraphedGroup} />
          </Col>
        </div>
      </div>
    );
  }
}

export default App;
