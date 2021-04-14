import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import {ExceptionsContextProvider} from './components/Exceptions/context';
import { SnackbarProvider } from 'notistack';

import Findings from './pages/Findings';
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import ExternalAttack from './pages/ExternalAttack/index';
import FindingItems from './pages/FindingItems/index';
import Layout from './layout/index';
import AppLoader from './components/AppLoader';
import ErrorPage from './pages/404';
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
                  <Route path="/services/:service/external-attacks">
                    <ExternalAttack />
                  </Route>
                  <Route path="/" exact>
                    <Dashboard />
                  </Route>
                  <Route path="*">
                    <ErrorPage />
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
