import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import './style.scss';
import PartialConditional from '../../Partial/PartialConditional';

const propTypes = {
  title: PropTypes.string.isRequired,
  isSelected: PropTypes.bool,
  onClick: PropTypes.func,
  condition: PropTypes.objectOf({
    valuePath: PropTypes.string.isRequired,
    eq: PropTypes.string,
    neq: PropTypes.string,
  }),
};

const TabPane = (props) => {
  const { title, isSelected, onClick, condition } = props;

  const className = cx('tab-pane', { 'is-selected': isSelected });

  const content = (
    <span className={className} onClick={onClick}>
      {title}
    </span>
  );

  if (condition) {
    return (
      <PartialConditional
        valuePath={condition.valuePath}
        eq={condition.eq}
        neq={condition.neq}
      >
        {content}
      </PartialConditional>
    );
  }

  return content;
};

TabPane.propTypes = propTypes;

export default TabPane;
