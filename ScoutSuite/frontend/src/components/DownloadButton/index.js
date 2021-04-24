import React from 'react';
import GetAppOutlinedIcon from '@material-ui/icons/GetAppOutlined';
import { Button } from '@material-ui/core';
import { PropTypes } from 'prop-types';

import './style.scss';
import { BASE_URL } from '../../api/api';

const propTypes = {
  service: PropTypes.string.isRequired,
  resource: PropTypes.string.isRequired,
  finding: PropTypes.string.isRequired,
  type: PropTypes.string.isRequired,
};

const DownloadButton = ({ service, resource, finding, type }) => {
  const source = finding ? `findings/${finding}/items` : `resources/${resource}`;
  const link = `${BASE_URL}/api/services/${service}/${source}/download`;

  return (
    <form
      method="get"
      action={link}
    >
      <input 
        type="hidden" name="type" 
        value={type} 
      />
      <Button
        className="download-btn"
        variant="outlined"
        type="submit"
        size="normal"
        startIcon={<GetAppOutlinedIcon />}
      >
        {type.toUpperCase()}
      </Button>
    </form>
  );
};

DownloadButton.propTypes = propTypes;

export default DownloadButton;
