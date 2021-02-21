import React from 'react';
import PropTypes from 'prop-types';
import { Link, useLocation } from '@reach/router';
import cx from 'classnames';

const propTypes = {
  children: PropTypes.element.isRequired,
  link: PropTypes.string.isRequired
};

const MenuElement = props => {
  const {
    children,
    link
  } = props;
  const location = useLocation();

  return (
    <li className={cx('menu-element', location.pathname.startsWith('/' + link) && 'is-selected')}>
      <div>
        {link && <Link to={'/' + link}>{children}</Link>}
        {!link && children}
      </div>
    </li>
  );
};

MenuElement.propTypes = propTypes;

export default MenuElement;
