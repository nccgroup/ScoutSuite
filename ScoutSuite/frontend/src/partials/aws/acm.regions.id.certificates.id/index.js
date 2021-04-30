import React from 'react';
import PropTypes from 'prop-types';
import isEmpty from 'lodash/isEmpty';

import { partialDataShape, valueOrNone } from '../../../utils/Partials';
import { Partial, PartialValue } from '../../../components/Partial';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';
import InformationsWrapper from '../../../components/InformationsWrapper';
import Informations from './Informations';


const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const LambdaFunctions = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <Informations />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Validation">
          <PartialValue 
            label="Domain Validation Options"
            valuePath="DomainValidationOptions"
            renderValue={value => (
              <ul>
                {value.map((
                  {
                    DomainName,
                    ValidationDomain,
                    ValidationMethod,
                    ValidationStatus,
                  }, i
                ) => (
                  <li key={i}>
                    {`${DomainName} - ${ValidationDomain} - ${ValidationMethod} - ${ValidationStatus}`}
                  </li>
                ))}
              </ul>
            )}
          />
        </TabPane>
        <TabPane title="Keys">
          <div>
            <PartialValue 
              label="Key Algorithm"
              valuePath="KeyAlgorithm"
              renderValue={valueOrNone}
            />
            <PartialValue 
              label="Signature Algorithm"
              valuePath="SignatureAlgorithm"
              renderValue={valueOrNone}
            />
            <PartialValue 
              label="Key Usages"
              valuePath="KeyUsages"
              errorPath="ExtendedKeyUsages"
              renderValue={value => (
                <ul>
                  {isEmpty(value) ? (
                    <li>None</li>
                  ) : (
                    value.map((usage, i) => (
                      <li key={i}>
                        {`${usage.Name} - ${usage.OID}`}
                      </li>
                    ))
                  )}
                </ul>
              )}
            />
            <PartialValue 
              label="In Use By"
              valuePath="InUseBys"
              errorPath="InUseBy"
              renderValue={value => (
                <ul>
                  {isEmpty(value) ? (
                    <li>None</li>
                  ) : (
                    value.map((usedBy, i) => (
                      <li key={i}>
                        {usedBy}
                      </li>
                    ))
                  )}
                </ul>
              )}
            />
          </div>
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

LambdaFunctions.propTypes = propTypes;

export default LambdaFunctions;
