import React from 'react';
import { PropTypes } from 'prop-types';

const propTypes = {
  children: PropTypes.node.isRequired
};

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { error: null, errorInfo: null };
  }
  
  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }
  
  render() {
    if (this.state.errorInfo) {
      return (
        <div>
          <h2>Something went wrong loading this component.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.errorInfo.componentStack}
          </details>
        </div>
      );
    }
    
    return this.props.children;
  }  
}

ErrorBoundary.propTypes = propTypes;

export default ErrorBoundary;
