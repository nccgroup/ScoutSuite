import React from 'react';
import { Router } from '@reach/router';

import Findings from './pages/Findings';
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import ExternalAttack from './pages/ExternalAttack/index';
import FindingItems from './pages/FindingItems/index';
import Layout from './layout/index';

function App() {
  return (
    <Layout>
      <Router>
        <Dashboard path="/" />
        <Findings path="/services/:service/findings" />
        <ExternalAttack path="/services/:service/external-attacks" />
        <FindingItems path="/services/:service/findings/:finding/items" />
        <FindingItems path="/services/:service/findings/:finding/items/:item" />
        <Resources path="/services/:service/resources/:resource" />
        <Resources path="/services/:service/resources/:resource/:id" />
      </Router>
    </Layout>
  );
}

export default App;
