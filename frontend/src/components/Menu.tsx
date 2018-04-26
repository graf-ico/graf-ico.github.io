import * as React from 'react';

import { Button, FormControl, FormGroup, Nav, Navbar, NavItem } from 'react-bootstrap'

class Menu extends React.Component {
    public render() {
        return (
            <Navbar>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a href="#home">/ico/nnected</a>
                    </Navbar.Brand>
                </Navbar.Header>
                <Nav>
                    <NavItem eventKey={1} href="#">
                        About
                     </NavItem>
                </Nav>
                <Navbar.Collapse>
                    <Navbar.Form pullRight={true}>
                        <FormGroup>
                            <FormControl type="text" placeholder="Search" />
                        </FormGroup>{' '}
                        <Button type="submit">Submit</Button>
                    </Navbar.Form>
                </Navbar.Collapse>
                {/* <Nav pullRight={true}>
                    <FormGroup>
                        <FormControl type="text" placeholder="Search" />
                    </FormGroup>{' '}
                </Nav> */}
            </Navbar>
        );
    }
}

export default Menu;