import React from 'react';
import PropTypes from 'prop-types';

import './style.scss';

const propTypes = {
  title: PropTypes.string.isRequired,
  leftPane: PropTypes.element.isRequired,
  children: PropTypes.element.isRequired,
};

const SelectedItemContainer = props => {
  const {
    title,
    leftPane,
    children,
  } = props;

  return (
    <div className="selected-item-container">
      <div className="header">
        <h3>{title}</h3>
      </div>
      <div className="content">
        <div className="left-pane">
          {leftPane}
        </div>
        {children}
      </div>
    </div>
  );
};

SelectedItemContainer.propTypes = propTypes;

export default SelectedItemContainer;
