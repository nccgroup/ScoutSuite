import React from 'react';
import PropTypes from 'prop-types';
import size from 'lodash/size';

import PartialValue from '../PartialValue';
import { renderWithInnerHtml } from '../../../utils/Partials';

import './style.scss';


const propTypes = {
  name: PropTypes.string,
  policy: PropTypes.object.isRequired,
};

const Policy = props => {
  const { name, policy } = props;

  const displayJson = object => 
    JSON.stringify(object, null, 2)
      .replace(/ /g, '&nbsp;')
      .replace(/\n/g, '<br/>');

  return (
    <div className="policy">
      {name && (
        <h4 className="policy-name">
          {name}
        </h4>
      )}
      <code> 
        {Object.entries(policy).map(([key, value], i) => (
          <div key={i}>
            {`"${key}":\xa0`}
            {key === 'Statement' ? (
              <>
                [<br/>
                {value.map((object, i) => (
                  <PartialValue 
                    key={i}
                    value={displayJson(object)}
                    errorPath={`Statement.${i}`}
                    renderValue={value => (
                      renderWithInnerHtml(
                        value, 
                        { className: 'inner-code' },
                      )
                    )}
                  />
                ))}
                ]
              </>
            ) : (
              <>
                {displayJson(value)}
              </>
            )}
            {i !== size(policy) - 1 && ','}
            <br/>
          </div>    
        ))}
      </code>
    </div>
  );
};

Policy.propTypes = propTypes;

export default Policy;
