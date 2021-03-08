import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { Link } from '@reach/router';
import cx from 'classnames';

const propTypes = {
  children: PropTypes.element.isRequired,
  link: PropTypes.string,
  disabled: PropTypes.bool,
  selected: PropTypes.bool,
  setSelected: PropTypes.func,
};

const MenuElement = (props) => {
  const { children, link, disabled, selected, setSelected } = props;
  const isSelected = selected === link;
  const hasLink = link != undefined && link != null;

  useEffect(() => {
    if (location.pathname.startsWith('/' + link)) setSelected(link);
  }, [link]);

  return (
    <li
      className={cx(
        'menu-element',
        isSelected && 'is-selected',
        disabled && 'disabled',
      )}
    >
      {hasLink && !disabled && (
        <Link to={'/' + link} onClick={() => setSelected(link)}>
          {children}
        </Link>
      )}
      {(!hasLink || disabled) && <a>{children}</a>}
    </li>
  );
};

MenuElement.propTypes = propTypes;

export default MenuElement;
