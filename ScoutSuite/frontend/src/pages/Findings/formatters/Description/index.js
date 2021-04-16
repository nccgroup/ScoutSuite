import React from 'react';
import PropTypes from 'prop-types';
import NoteAddOutlinedIcon from '@material-ui/icons/NoteAddOutlined';
import isEmpty from 'lodash/isEmpty';
import Tooltip from '@material-ui/core/Tooltip';

import { renderWithInnerHtml } from '../../../../utils/Partials';

import './style.scss';
import Modal from '../../../../components/Modal';

const propTypes = {
  value: PropTypes.string.isRequired,
  row: PropTypes.object.isRequired,
};

const Description = props => {
  const {
    value,
    row: { original },
  } = props;
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handlePopoverOpen = event => {
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
      <Tooltip
        title="Click to see finding details" placement="top"
        arrow>
        <span className="findings-desc" onClick={handlePopoverOpen}>
          <NoteAddOutlinedIcon fontSize="inherit" />
        </span>
      </Tooltip>

      <Modal
        title="Finding Description"
        handleClose={handlePopoverClose}
        open={open}
      >
        {renderWithInnerHtml(value)}

        {!isEmpty(original.remediation) && (
          <>
            <h4>Remediation</h4>
            {renderWithInnerHtml(original.remediation)}
          </>
        )}

        {!isEmpty(original.compliance) && (
          <>
            <h4>Compliance</h4>
            <ul>
              {original.compliance.map((compliance, i) => (
                <li key={i}>
                  {compliance.name} version {compliance.version}, reference{' '}
                  {compliance.reference}
                </li>
              ))}
            </ul>
          </>
        )}

        {!isEmpty(original.references) && (
          <>
            <h4>References</h4>
            <ul>
              {original.references.map((ref, i) => (
                <li key={i}>
                  <a
                    href={ref} target="_blank"
                    rel="noreferrer">
                    {ref}
                  </a>
                </li>
              ))}
            </ul>
          </>
        )}
      </Modal>
    </>
  );
};

Description.propTypes = propTypes;

export default Description;
