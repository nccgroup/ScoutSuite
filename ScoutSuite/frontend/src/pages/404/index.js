import React from 'react';
import WarningRoundedIcon from '@material-ui/icons/WarningRounded';

import './style.scss';

const ErrorPage = () => {

  return (
    <>
      <div className="page-404">
        <div className="content-404">
          <WarningRoundedIcon />
          <h1>{'Oh, no! It\'s a 404 page :\'('}</h1>
          <p>This usually happens when you make a typo. Maybe check the address you entered?</p>
        </div>
      </div>
    </>
  );
};

export default ErrorPage;
