import React from 'react';
import { Router } from '@reach/router';

import Findings from './pages/Findings';
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import ExternalAttack from './pages/ExternalAttack/index';
import FlaggedItems from './pages/FlaggedItems/index';

function App() {
  return (
    <Router>
      <Dashboard path="/" />
      <Findings path="/services/:service/findings" /> 
      <ExternalAttack path="/services/:service/external-attacks" /> 
      <FlaggedItems path="/services/:service/findings/:finding/items" />
      <FlaggedItems path="/services/:service/findings/:finding/items/:item" />
      <Resources path="/services/:service/:resources" /> 
    </Router>
  );
}

export default App;
