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
  const { data: serverExceptions } = useAPI('exceptions');

  const download = () => {
    let mergedExceptions = serverExceptions;

    Object.entries(exceptions).forEach(([service, findings]) => {
      Object.entries(findings).forEach(([finding, rules]) => {
        const findingsList =
          mergedExceptions[service] && mergedExceptions[service][finding]
            ? [...mergedExceptions[service][finding], ...rules]
            : rules;

        mergedExceptions = {
          ...mergedExceptions,
          [service]: {
            ...mergedExceptions[service],
            [finding]: findingsList,
          },
        };
      });
    });

    var dataStr =
      'data:text/json;charset=utf-8,' +
      encodeURIComponent(JSON.stringify(mergedExceptions, null, 2));
    var downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute('href', dataStr);
    downloadAnchorNode.setAttribute(
      'download',
      `exceptions-${provider.provider_code}.json`,
    );
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
