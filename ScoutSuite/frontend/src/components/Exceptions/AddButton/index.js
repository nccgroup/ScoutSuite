import React, { useContext } from 'react';
import { Button } from '@material-ui/core';
import Tooltip from '@material-ui/core/Tooltip';
import AddIcon from '@material-ui/icons/Add';
import { PropTypes } from 'prop-types';
import { ExceptionsContext } from '../context';

const propTypes = {
  service: PropTypes.string.isRequired,
  finding: PropTypes.string.isRequired,
  path: PropTypes.string.isRequired,
};

const AddException = ({ service, finding, path }) => {
  const { addException } = useContext(ExceptionsContext);

  const add = () => addException(service, finding, path);

  return (<Tooltip
    title="Add to exception list"
    placement="top"
    arrow>
    <Button
      size="small"
      startIcon={<AddIcon />}
      className="exception-btn"
      onClick={add}
    >
      Add
    </Button>
  </Tooltip>);
};

AddException.propTypes = propTypes;

export default AddException;