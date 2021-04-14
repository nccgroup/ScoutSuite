import React, { useContext } from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';
import Collapsible from 'react-collapsible';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import size from 'lodash/size';
import isEmpty from 'lodash/isEmpty';

import { PartialContext } from '../context';
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

  const { path_to_issues } = useContext(PartialContext);
  const hasError = path_to_issues.some(path => path.includes(policyPath));

  if (isEmpty(policy)) return null;

  const policyTitle = (
    <h4 className="policy-title">
      {name}
    </h4>
  );

  const displayJson = object => 
    JSON.stringify(object, null, 2)
      .replace(/ /gm, '&nbsp;')
      .replace(/\n/gm, '<br/>');

  const renderJson = (json, errorPath) => (
    <PartialValue 
      value={displayJson(json)}
      errorPath={errorPath}
      renderValue={value => (
        renderWithInnerHtml(
          value,
        )
      )}
    />
  );

  const policyContent = (
    <code>
      {'{'}
      {Object.entries(policy).map(([key, value], i) => (
        <div 
          key={i}
          className={cx({ 'inline': typeof(value) === 'string' })}
        >
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
                  {renderJson(object, `${policyPath}.Statement.${i}`)}
                </Collapsible>
              ))}
              ]
            </>
          ) : (
            <>
              {renderJson(value)}
            </>
          )}
          {i < size(policy) - 1 && ','}
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
          open={defaultOpen || hasError}
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
