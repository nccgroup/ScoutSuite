import React from 'react';
import PropTypes from 'prop-types';
import Collapsible from 'react-collapsible';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import size from 'lodash/size';

import PartialValue from '../PartialValue';
import { renderWithInnerHtml } from '../../../utils/Partials';

import './style.scss';


const propTypes = {
  name: PropTypes.string,
  policy: PropTypes.object.isRequired,
  policyPath: PropTypes.string,
  defaultOpen: PropTypes.bool,
};

const defaultProps = {
  defaultOpen: false,
};

const Policy = props => {
  const { 
    name, 
    policy, 
    policyPath,
    defaultOpen,
  } = props;

  const displayJson = object => 
    JSON.stringify(object, null, 2)
      .replace(/ /g, '&nbsp;')
      .replace(/\n/g, '<br/>');

  const policyTitle = (
    <h4 className="policy-title">
      {name}
    </h4>
  );

  const policyContent = (
    <code>
      {'{'}
      {Object.entries(policy).map(([key, value], i) => (
        <div key={i}>
          {`"${key}":\xa0`}
          {key === 'Statement' ? (
            <>
              [<br/>
              {value.map((object, i) => (
                <Collapsible
                  key={i}
                  trigger={
                    <>
                      <ExpandMoreIcon fontSize="inherit"/>
                      <span>{'{...}'}</span>
                    </>
                  }
                  triggerWhenOpen={
                    <ExpandLessIcon fontSize="inherit"/>
                  }
                  transitionTime={1}
                  open={true}
                >
                  <PartialValue 
                    value={displayJson(object)}
                    errorPath={`${policyPath}.PolicyDocument.Statement.${i}`}
                    renderValue={value => (
                      renderWithInnerHtml(
                        value,
                      )
                    )}
                  />
                </Collapsible>
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
      {'}'}
    </code>
  );

  return (
    <div className="policy">
      {name ? (
        <Collapsible
          trigger={
            <>
              {policyTitle}
              <ExpandMoreIcon fontSize="inherit"/>
            </>
          }
          triggerWhenOpen={
            <>
              {policyTitle}
              <ExpandLessIcon fontSize="inherit"/>
            </>
          }
          transitionTime={1}
          open={defaultOpen}
        >
          {policyContent}
        </Collapsible>
      ) : (
        policyContent
      )}
    </div>
  );
};

Policy.propTypes = propTypes;
Policy.defaultProps = defaultProps;

export default Policy;
