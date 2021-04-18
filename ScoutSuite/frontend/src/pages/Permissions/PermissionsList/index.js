import React, { useState, useMemo } from 'react';
import PropTypes from 'prop-types';

// import { makeTitle } from '../../../utils/Partials';
// import ResourceLink from '../../../components/ResourceLink';
import Table from '../../../components/Table';

const propTypes = {
  service: PropTypes.string.isRequired,
  list: PropTypes.object.isRequired,
};

// TODO: Optimize component (3k+ items maybe use a table instead)
const PermissionsList = props => {
  const { list } = props;
  const listMemo = useMemo(() => Object.entries(list).map(([key, values]) => ({ name: key, ...values })), [list]);
  const [items, setItems] = useState(listMemo);

  console.log(list, items);

  const fetchData = React.useCallback(({ search }) => {
    if (search)
      setItems(
        items.filter(item =>
          item.name.toLowerCase().includes(search.toLowerCase()),
        ),
      );
    else setItems(items);
  }, []);

  // const renderPolicies = (policies, arn, resource, id) =>
  //   Object.entries(policies || {}).map(([policy, { condition }], i) => (
  //     <div key={i}>
  //       <div>
  //         {`${arn} granted in `}
  //         <ResourceLink
  //           service={service}
  //           resource={resource}
  //           id={id || policy}
  //           name={id || policy}
  //         />
  //       </div>
  //       {condition && <div>{`Condition: ${condition}`}</div>}
  //     </div>
  //   ));

  // const renderPermissionInfos = infos => (
  //   <div className="informations-card">
  //     {/* IAM Resource Type */}
  //     {Object.entries(infos).map(([type, entity], i) => (
  //       <div key={i} className="type">
  //         <span>{makeTitle(type)}</span>
  //         <ul>
  //           {/* Effect */}
  //           {Object.entries(entity).map(([effect, resources], i) => (
  //             <div key={i}>
  //               <li>{makeTitle(effect)}</li>
  //               <ul>
  //                 {/* IAM Resource ID */}
  //                 {Object.entries(resources).map(
  //                   ([resourceId, accesses], i) => (
  //                     <div key={i}>
  //                       <li>
  //                         <ResourceLink
  //                           service={service}
  //                           resource={type}
  //                           id={resourceId}
  //                           name={resourceId}
  //                         />
  //                       </li>
  //                       <ul>
  //                         {/* Resource/NotResource */}
  //                         {Object.entries(accesses).map(([key, arns], i) => (
  //                           <div key={i}>
  //                             <li>{key}</li>
  //                             <ul>
  //                               {/* Resource ARN */}
  //                               {Object.entries(arns).map(
  //                                 ([arn, { inline_policies, policies }], i) => (
  //                                   <div key={i}>
  //                                     {renderPolicies(
  //                                       inline_policies,
  //                                       arn,
  //                                       type,
  //                                       resourceId,
  //                                     )}
  //                                     {renderPolicies(
  //                                       policies,
  //                                       arn,
  //                                       'policies',
  //                                     )}
  //                                   </div>
  //                                 ),
  //                               )}
  //                             </ul>
  //                           </div>
  //                         ))}
  //                       </ul>
  //                     </div>
  //                   ),
  //                 )}
  //               </ul>
  //             </div>
  //           ))}
  //         </ul>
  //       </div>
  //     ))}
  //   </div>
  // );

  const columns = [{ name: 'Name', key: 'name' }];

  const initialState = {
    pageSize: 10,
  };

  return (
    <div className="permissions">
      <div className="table-card">
        <Table
          columns={columns}
          data={items}
          initialState={initialState}
          fetchData={fetchData}
        />
      </div>

      {/* {Object.entries(list).map(([name, infos], i) => (
        <div key={i}>
          <h3>{name}</h3>
          <hr/>
          {renderPermissionInfos(infos)}
        </div>
      ))} */}
    </div>
  );
};

PermissionsList.propTypes = propTypes;

export default PermissionsList;
