import React from 'react';
import PropTypes from 'prop-types';

import { makeTitle } from '../../../../utils/Partials';
import ResourceLink from '../../../../components/ResourceLink';


const propTypes = {
  service: PropTypes.string.isRequired,
  permission: PropTypes.object.isRequired,
};

const PermissionInfos = props => {
  const {
    service,
    permission,
  } = props;

  const renderPolicies = (policies, arn, resource, id) =>
    Object.entries(policies || {}).map(([policy, { condition }], i) => (
      <div key={i}>
        <div>
          {`${arn} granted in `}
          <ResourceLink
            service={service}
            resource={resource}
            id={id || policy}
          />
        </div>
        {condition && <div>{`Condition: ${condition}`}</div>}
      </div>
    ));

  return (
    <div className="informations-card">
      <h3>{permission.name}</h3>
      <hr />
      <ul>
        {/* IAM Resource Type */}
        {Object.entries(permission)
          .filter(([key]) => key !== 'name')
          .map(([type, entity], i) => (
            <div key={i} className="type">
              <span>{makeTitle(type)}</span>
              <ul>
                {/* Effect */}
                {Object.entries(entity).map(([effect, resources], i) => (
                  <div key={i}>
                    <li>{makeTitle(effect)}</li>
                    <ul>
                      {/* IAM Resource ID */}
                      {Object.entries(resources).map(
                        ([resourceId, accesses], i) => (
                          <div key={i}>
                            <li>
                              <ResourceLink
                                service={service}
                                resource={type}
                                id={resourceId}
                              />
                            </li>
                            <ul>
                              {/* Resource/NotResource */}
                              {Object.entries(accesses).map(([key, arns], i) => (
                                <div key={i}>
                                  <li>{key}</li>
                                  <ul>
                                    {/* Resource ARN */}
                                    {Object.entries(arns).map(
                                      ([arn, { inline_policies, policies }], i) => (
                                        <div key={i}>
                                          {renderPolicies(
                                            inline_policies,
                                            arn,
                                            type,
                                            resourceId,
                                          )}
                                          {renderPolicies(
                                            policies,
                                            arn,
                                            'policies',
                                          )}
                                        </div>
                                      ),
                                    )}
                                  </ul>
                                </div>
                              ))}
                            </ul>
                          </div>
                        ),
                      )}
                    </ul>
                  </div>
                ))}
              </ul>
            </div>
          ))
        }
      </ul>
    </div>
  );
};

PermissionInfos.propTypes = propTypes;

export default PermissionInfos;
