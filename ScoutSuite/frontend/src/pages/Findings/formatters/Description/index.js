import React from 'react';
import { PropTypes } from 'prop-types';
import Popover from '@material-ui/core/Popover';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';

import './style.scss';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired,
};

const Description = (props) => {
  const { value } = props;
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handlePopoverOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handlePopoverClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);

  if (value === 'No description available.') {
    return <span className="findings-no-desc">{value}</span>;
  }

  return (
    <>
      <span className="findings-desc" onClick={handlePopoverOpen}>
        <InfoOutlinedIcon fontSize="inherit" />  Finding description.
      </span>

      <Popover
        open={open}
        anchorEl={anchorEl}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'left',
        }}
        onClose={handlePopoverClose}
        disableRestoreFocus
      >
        <div dangerouslySetInnerHTML={{ __html: value }}></div>
      </Popover>
    </>
  );
};

Description.propTypes = propTypes;

export default Description;
