import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import cx from 'classnames';

const propTypes = {
  children: PropTypes.node.isRequired,
  link: PropTypes.string,
  disabled: PropTypes.bool,
  selected: PropTypes.string,
};

const MenuElement = (props) => {
  const { children, link, disabled, selected } = props;
  const isSelected = selected.includes('/' + link);
  const hasLink = link != undefined && link != null;

  return (
    <li
      className={cx(
        'menu-element',
        isSelected && 'is-selected',
        disabled && 'disabled',
      )}
    >
      {hasLink && !disabled && (
        <Link to={'/' + link}>
          {children}
        </Link>
      )}
      {(!hasLink || disabled) && <a>{children}</a>}
    </li>
  );
};

MenuElement.propTypes = propTypes;

export default MenuElement;
