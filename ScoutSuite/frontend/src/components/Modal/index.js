import React from 'react';
import { PropTypes } from 'prop-types';
import Dialog from '@material-ui/core/Dialog';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

import './style.scss';

const propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.element.isRequired,
  handleClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
};

const Modal = props => {
  const { handleClose, title, children, open } = props;

  return (
    <Dialog
      onClose={handleClose}
      aria-labelledby="customized-dialog-title"
      open={open}
    >
      <div className="modal-title" onClose={handleClose}>
        <h2>{title}</h2>
        <IconButton aria-label="close" onClick={handleClose}>
          <CloseIcon />
        </IconButton>
      </div>
      <div className="modal-content">{children}</div>
    </Dialog>
  );
};

Modal.propTypes = propTypes;

export default Modal;
