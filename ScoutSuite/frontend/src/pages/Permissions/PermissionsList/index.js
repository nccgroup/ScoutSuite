import React, { useState, useMemo, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import { useParams } from 'react-router-dom';

import { makeTitle } from '../../../utils/Partials';
import ResourceLink from '../../../components/ResourceLink';
import Table from '../../../components/Table';
import Name from './formatters/Name';

const propTypes = {
  service: PropTypes.string.isRequired,
  list: PropTypes.object.isRequired,
};

const PermissionsList = props => {
  const { service, list } = props;
  const params = useParams();

  const listMemo = useMemo(
    () =>
      Object.entries(list).map(([key, values]) => ({ name: key, ...values })),
    [list],
  );
  const [items, setItems] = useState(listMemo);

  const permission = useMemo(
    () => params.id && listMemo.find(item => item.name === decodeURI(params.id)),
    [params.id, listMemo],
  );

  useEffect(() => {
    setItems(listMemo);
  }, [listMemo]);

  const fetchData = useCallback(
    ({ search }) => {
      if (search)
        setItems(
          listMemo.filter(item =>
            item.name.toLowerCase().includes(search.toLowerCase()),
          ),
        );
      else setItems(listMemo);
    },
    [listMemo],
  );

  if (!items) return null;

  const renderPolicies = (policies, arn, resource, id) =>
    Object.entries(policies || {}).map(([policy, { condition }], i) => (
      <div key={i}>
        <div>
          {`${arn} granted in `}
          <ResourceLink
            service={service}
            resource={resource}
            id={id || policy}
            name={id || policy}
          />
        </div>
        {condition && <div>{`Condition: ${condition}`}</div>}
      </div>
    ));

  const renderPermissionInfo = entity => (
    <div className="informations-card">
      <div className="type">
        <h3>{makeTitle(entity.name)}</h3>
        <hr />
        <ul>
          {/* Effect */}
          {Object.entries(entity)
            .filter(([key]) => key !== 'name')
            .map(([effect, resources], i) => (
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
                            resource={effect}
                            id={resourceId}
                            name={resourceId}
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
                                        entity.name,
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
    </div>
  );

  const columns = [{ name: 'Name', key: 'name' }];

  const initialState = {
    pageSize: 10,
  };

  const formatters = {
    name: Name,
  };

  return (
    <div className="permissions">
      <div className="table-card">
        <Table
          columns={columns}
          data={items}
          initialState={initialState}
          formatters={formatters}
          fetchData={fetchData}
        />
      </div>

      {!params.id && (
        <div className="selected-item no-items">No selected permission.</div>
      )}

      {params.id && permission && renderPermissionInfo(permission)}
    </div>
  );
};

PermissionsList.propTypes = propTypes;

export default PermissionsList;
