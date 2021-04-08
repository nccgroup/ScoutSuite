import React, { useState } from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import { TabPane } from '../../../Tabs';
import { PartialTabContext } from '../../context';
import { SEVERITIES } from '../../../../utils/Dashboard';

import './style.scss';


const propTypes = {
  title: PropTypes.string.isRequired,
  isSelected: PropTypes.bool,
  disabled: PropTypes.bool,
  onClick: PropTypes.func,
  children: PropTypes.any.isRequired,
};

const PartialTabPane = (props) => {
  const {
    title,
    isSelected,
    disabled,
    onClick,
    children,
  } = props;

  const [issueLevel, setIssueLevel] = useState('');

  const renderedTitle = issueLevel 
    ? (
      <>
        {title}
        {SEVERITIES[issueLevel].icon}
      </>
    ) : (
      title
    ); 

  return (
    <PartialTabContext.Provider value={setIssueLevel}>
      <TabPane 
        title={renderedTitle}
        className={cx('partial-tab-pane', issueLevel)}
        isSelected={isSelected}
        disabled={disabled}
        onClick={onClick}
      >
        {children}
      </TabPane>
    </PartialTabContext.Provider>
  );
};

PartialTabPane.propTypes = propTypes;

export default PartialTabPane;
