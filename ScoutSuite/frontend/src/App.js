import React from 'react';
import { Router } from '@reach/router';

import Findings from './pages/Findings';
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import ExternalAttack from './pages/ExternalAttack/index';
import FlaggedItems from './pages/FlaggedItems/index';
import Layout from './layout/index';

function App() {
  return (
    <Layout>
      <Router>
        <Dashboard path="/" />
        <Findings path="/services/:service/findings" />
        <ExternalAttack path="/services/:service/external-attacks" />
        <FlaggedItems path="/services/:service/findings/:finding/items" />
        <FlaggedItems path="/services/:service/findings/:finding/items/:item" />
        <Resources path="/services/:service/resources/:resources" />
      </Router>
    </Layout>
  );
}

export default App;
