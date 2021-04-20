import React from 'react';
import PropTypes from 'prop-types';
import { Chip } from '@material-ui/core';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  pro_feature: PropTypes.bool.isRequired,
};

const MenuGroup = props => {
  const { title, children, pro_feature } = props;

  return (
    <li className="menu-group">
      <div className="title">
        {title} {'  '}

        {pro_feature && (
          <Chip
            label="PRO"
            variant="outlined"
            size="small"
            color="secondary"
          />
        )}
      </div>
      <ul>{children}</ul>
    </li>
  );
};

MenuGroup.propTypes = propTypes;

export default MenuGroup;
