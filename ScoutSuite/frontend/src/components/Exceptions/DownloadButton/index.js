import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import { Button } from '@material-ui/core';
import AddIcon from '@material-ui/icons/Add';
import isEmpty from 'lodash/isEmpty';

import { ExceptionsContext } from '../context';
import { useAPI } from '../../../api/useAPI';

import './style.scss';


const propTypes = {
  service: PropTypes.string,
  finding: PropTypes.string,
  path: PropTypes.string,
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
      <Button
        disabled={isEmpty(exceptions)}
        size="small"
        startIcon={<AddIcon />}
        onClick={download}
        variant="outlined"
        fullWidth
      >
        Export Exceptions
      </Button>
    </div>
    
  );
};

DownloadException.propTypes = propTypes;

export default DownloadException;
