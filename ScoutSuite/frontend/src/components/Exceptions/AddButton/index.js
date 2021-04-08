import React, { useContext } from 'react';
import { IconButton } from '@material-ui/core';
import Tooltip from '@material-ui/core/Tooltip';
import AddIcon from '@material-ui/icons/Add';
import { PropTypes } from 'prop-types';
import { useSnackbar } from 'notistack';
import get from 'lodash/get';

import { ExceptionsContext } from '../context';


const propTypes = {
  service: PropTypes.string.isRequired,
  finding: PropTypes.string.isRequired,
  path: PropTypes.string.isRequired,
};

const AddException = ({ service, finding, path }) => {
  const { exceptions, addException } = useContext(ExceptionsContext);
  const { enqueueSnackbar } = useSnackbar();

  const add = () => {
    addException(service, finding, path);
    enqueueSnackbar(
      'Exception added. Don\'t forget to export the exceptions!',
      {
        variant: 'success',
        anchorOrigin: {
          vertical: 'bottom',
          horizontal: 'right',
        },
      },
    );
  };

  const exist = get(exceptions, [service, finding], []).includes(path);

  return (
    <Tooltip
      title="Add to exception list" 
      placement="top"
      arrow
    >
      <IconButton
        disabled={exist}
        size="small"
        className="exception-btn"
        onClick={add}
      >
        <AddIcon />
      </IconButton>
    </Tooltip>
  );
};

AddException.propTypes = propTypes;

export default AddException;
