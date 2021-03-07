import React from 'react';
import PropTypes from 'prop-types';
import { Link, useLocation } from '@reach/router';
import cx from 'classnames';

const propTypes = {
  children: PropTypes.element.isRequired,
  link: PropTypes.string,
};

const MenuElement = props => {
  const {
    children,
    link
  } = props;
  
  const location = useLocation();

  const hasLink = link != undefined && link != null; 

  return (
    <li className={cx('menu-element', location.pathname.startsWith('/' + link) && 'is-selected')}>
      {hasLink && <Link to={'/' + link}>{children}</Link>}
      <div>
        {!hasLink && children}
      </div>
    </li>
  );
};

MenuElement.propTypes = propTypes;

export default MenuElement;
