import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import { SnackbarProvider } from 'notistack';

import AppLoader from './components/AppLoader';
import { ExceptionsContextProvider } from './components/Exceptions/context';
import Findings from './pages/Findings';
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import ExternalAttack from './pages/ExternalAttack';
import PasswordPolicy from './pages/PasswordPolicy';
import FindingItems from './pages/FindingItems';
import Layout from './layout';
import ErrorBoundary from './components/ErrorBoundary';


function App() {
  return (
    <AppLoader>
      <SnackbarProvider 
        maxSnack={1}
        preventDuplicate
      >
        <ExceptionsContextProvider>
          <Router>
            <Layout>
              <ErrorBoundary>
                <Switch>
                  <Route
                    path={[
                      '/services/:service/findings/:finding/items/:item',
                      '/services/:service/findings/:finding',
                    ]}
                  >
                    <FindingItems />
                  </Route>
                  <Route path="/services/:service/resources/:resource/:id?">
                    <Resources />
                  </Route>
                  <Route path="/services/:service/findings">
                    <Findings />
                  </Route>
                  <Route
                    path={[
                      '/services/:service/external_attack_surface',
                      '/categories/:category/external_attack_surface',
                    ]}
                  >
                    <ExternalAttack />
                  </Route>
                  <Route path="/services/:service/password_policy">
                    <PasswordPolicy />
                  </Route>
                  <Route path="/" exact>
                    <Dashboard />
                  </Route>
                </Switch>
              </ErrorBoundary>
            </Layout>
          </Router>
        </ExceptionsContextProvider>
      </SnackbarProvider>
    </AppLoader>
  );
}

export default App;
