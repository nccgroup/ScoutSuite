import React from 'react';
import PropTypes from 'prop-types';
import CloseOutlinedIcon from '@material-ui/icons/CloseOutlined';
import InfoOutlinedIcon from '@material-ui/icons/InfoOutlined';

import { renderWithInnerHtml } from '../../../../utils/Partials';

import './style.scss';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired,
};

const Description = (props) => {
  const { value, row: { original } } = props;
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

      {open && <>
        <div className="desc-bg" onClick={handlePopoverClose}></div>
        <div className="desc-overlay">
          <div className="desc-header">
            <h4>Finding Description</h4>
            <CloseOutlinedIcon onClick={handlePopoverClose} />
          </div>
          
          {renderWithInnerHtml(value)}

          {original.remediation && <>
            <h4>Remediation</h4>
            {renderWithInnerHtml(original.remediation)}
          </>}

          {original.references && <>
            <h4>References</h4>
            <ul>
              {original.references.map((ref, i) => (
                <li key={i}>
                  <a href={ref} target="_blank" rel="noreferrer" >
                    {ref}
                  </a>
                </li>)
              )}
            </ul>
          </>}
        </div>
      </>}
    </>
  );
};

Description.propTypes = propTypes;

export default Description;
