import React, { useState } from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.oneOfType([
    PropTypes.element,
    PropTypes.arrayOf(PropTypes.element),
  ]).isRequired,
}

const SubMenu = props => {
  const { 
    title,
    children,
  } = props;

  const [isSelected, setIsSelected] = useState(false);
  const className = cx('sub-menu', {'is-selected': isSelected})

  return (
    <li className={className} onClick={() => setIsSelected(true)}>
      <div className="title">
        {title}
      </div>
      {isSelected && (
        <ul>
          {children}
        </ul>
      )}
    </li>
  );
}

SubMenu.propTypes = propTypes;

export default SubMenu
