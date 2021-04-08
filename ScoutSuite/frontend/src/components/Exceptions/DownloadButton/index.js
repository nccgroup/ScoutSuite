import React, { useContext } from 'react';
import { Button } from '@material-ui/core';
import Tooltip from '@material-ui/core/Tooltip';
import AddIcon from '@material-ui/icons/Add';
import { PropTypes } from 'prop-types';
import isEmpty from 'lodash/isEmpty';

import { ExceptionsContext } from '../context';
import { useAPI } from '../../../api/useAPI';

import './style.scss';

const propTypes = {
  service: PropTypes.string.isRequired,
  finding: PropTypes.string.isRequired,
  path: PropTypes.string.isRequired,
};

const DownloadException = () => {
  const { exceptions } = useContext(ExceptionsContext);
  const { data: provider } = useAPI('provider');

  const download = () => {
    // TODO: Fetch data from server first (not implement on server-side yet)
    var dataStr =
      'data:text/json;charset=utf-8,' +
      encodeURIComponent(JSON.stringify(exceptions));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute('href', dataStr);
    downloadAnchorNode.setAttribute('download', `${provider.provider_code}-exceptions.json`);
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
  };

  return (
    <div className="download-exceptions">
      <Tooltip
        title="Download all exceptions" placement="top"
        arrow>
        <Button
          disabled={isEmpty(exceptions)}
          size="small"
          startIcon={<AddIcon />}
          onClick={download}
          variant="outlined"
          color="secondary"
          fullWidth
        >
          Export Exceptions
        </Button>
      </Tooltip>
    </div>
    
  );
};

DownloadException.propTypes = propTypes;

export default DownloadException;
