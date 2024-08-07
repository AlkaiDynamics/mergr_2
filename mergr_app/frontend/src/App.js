## frontend/src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Chat from './components/Chat';
import Profile from './components/Profile';
import ProjectManagement from './components/ProjectManagement';
import axios from 'axios';

// Set up default Axios configuration
axios.defaults.baseURL = 'http://localhost:8000/api';
axios.defaults.headers.common['Content-Type'] = 'application/json';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/chat" component={Chat} />
          <Route path="/profile" component={Profile} />
          <Route path="/project-management" component={ProjectManagement} />
          <Route path="/" component={Home} />
        </Switch>
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <h1>Welcome to the Project Management and Collaboration App</h1>
      <p>Please navigate to the desired section using the links above.</p>
    </div>
  );
}

export default App;
