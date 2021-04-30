import React from 'react';
import PropTypes from 'prop-types';
import get from 'lodash/get';
import isEmpty from 'lodash/isEmpty';

import DetailedValue from '../../components/DetailedValue';
import ResourceLink from '../../components/ResourceLink';


export const partialDataShape = {
  item: PropTypes.object.isRequired,
  path_to_issues: PropTypes.arrayOf(PropTypes.string).isRequired,
};

/**
 * Convert a boolean to enabled or disabled
 * @param value
 * @returns {string}
 */
export const convertBoolToEnable = value => value ? 'Enabled' : 'Disabled';

/**
 * Convert a boolean to a checkmark or x
 * @param value
 * @returns {string}
 */
export const convertBoolToCheckmark = value => value ? '✔' : '✖';

/**
 * Convert a boolean to a readable boolean
 * @param title
 * @returns {string}
 */
export const convertBoolToString = value => value ? 'true' : 'false';

/**
 * Convert value to never if invalid
 * @param value 
 * @returns {any|string}
 */
export const convertValueOrNever = value => value ? value : 'Never';

/**
 * Convert a list of value to a list of chips
 * @param list 
 * @returns {array|string}
 */
export const convertListToChips = list => 
  !isEmpty(list) 
    ? list.map((item, index) => <span className="chip" key={index}>{item}</span>) 
    : 'None';

/**
 * Convert a boolean to a 'yes' or 'no'
 * @param value
 * @returns {string}
 */
export const convertBoolToYesOrNo = value => value ? 'Yes' : 'No';

/**
 * Return the value or the string 'None' if it doesn't
 * @param value
 * @returns {any}
 */
export const valueOrNone = value => {
  if (value === undefined || value === null || value === '' || value === [] || value === {}) {
    return 'None';
  }

  return value;
};

/**
 * Return the concatenation of 2 paths
 * @param pathA
 * @param pathB
 * @returns {string}
 */
export const concatPaths = (pathA, pathB) => pathA.length > 0 ? `${pathA}.${pathB}` : pathB;

/**
 * Format Date
 * @param time
 * @returns {string}
 */
export const formatDate = time => {
  if (!time || time === '') {
    return 'No date available';
  }
  else if (typeof time === 'number') {
    return new Date(time * 1000).toString();
  } else if (typeof time === 'string') {
    return new Date(time).toString();
  } else {
    return 'Invalid date format';
  }
};

/**
 * Render div with content set throught innerHTML
 * @param innerHtml 
 * @param props 
 * @returns {HTMLDivElement}
 */
export const renderWithInnerHtml = (innerHtml, props) => (
  <div
    dangerouslySetInnerHTML={{ __html: innerHtml }}
    {...props}
  />
);

/**
 * Render the items in an object as an unordered list
 * @param resources 
 * @param accessor 
 * @returns {HTMLUListElement}
 */
export const renderList = (items, accessor, renderValue) => {
  if (!items || items.length === 0) return <span>None</span>;

  return (
    <ul>
      {items.map((item, i) => {
        const value = get(item, accessor, item);
        return (
          <li key={i}>
            {renderValue ? renderValue(value) : value}
          </li>
        );
      })}
    </ul>
  );
};

/**
 * Render a Security Group object as a link
 * @param securityGroup 
 * @returns {ResourceLink}
 */
export const renderSecurityGroupLink = ({ GroupId }) => (
  <ResourceLink
    service="ec2"
    resource="security_groups"
    id={GroupId}
  />
);

/**
 * Render a Policy id as a link
 * @param id 
 * @returns {ResourceLink}
 */
export const renderPolicyLink = id => (
  <ResourceLink
    service="iam"
    resource="policies"
    id={id}
  />
);

/**
 * Render a FlowLog id as a link
 * @param id 
 * @returns {ResourceLink}
 */
export const renderFlowlogLink = id => (
  <ResourceLink
    service="vpc"
    resource="flow_logs"
    id={id}
    name={id}
  />
);

/**
 * Generates a function with the 'service' and 'resource' set in order 
 * to render the links in a list when given to the 'renderList' function
 * @param {string} service 
 * @param {string} type 
 * @returns {function}
 */
// eslint-disable-next-line
export const renderResourceLink = (service, type) => (resource) => (
  <ResourceLink
    service={service}
    resource={type}
    id={resource.id}
    name={resource.name}
  />
);

/**
 * Render tags in an unordered list
 * @param tags 
 * @returns {HTMLUListElement}
 */
export const renderAwsTags = tags => (
  <ul>
    {tags.map((tag, i) => (
      <li key={i}>
        <DetailedValue
          label={tag.Key}
          value={tag.Value}
        />
      </li>
    ))}
  </ul>
);

/**
 * Format title
 * @param title
 * @returns {string}
 */
export const makeTitle = title => {
  if (typeof (title) !== 'string') {
    return title.toString();
  }
  title = title.toLowerCase();
  if (['acm', 'ec2', 'ecr', 'ecs', 'efs', 'eks', 'iam', 'kms', 'rds', 'sns', 'ses', 'sqs', 'vpc', 'elb', 'elbv2', 'emr'].indexOf(title) !== -1) {
    return title.toUpperCase();
  } else if (title === 'cloudtrail') {
    return 'CloudTrail';
  } else if (title === 'cloudwatch') {
    return 'CloudWatch';
  } else if (title === 'cloudformation') {
    return 'CloudFormation';
  } else if (title === 'config') {
    return 'Config';
  } else if (title === 'cognito') {
    return 'Cognito';
  } else if (title === 'awslambda') {
    return 'Lambda';
  } else if (title === 'docdb') {
    return 'DocumentDB';
  } else if (title === 'dynamodb') {
    return 'DynamoDB';
  } else if (title === 'guardduty') {
    return 'GuardDuty';
  } else if (title === 'secretsmanager') {
    return 'Secrets Manager';
  } else if (title === 'elasticache') {
    return 'ElastiCache';
  } else if (title === 'redshift') {
    return 'RedShift';
  } else if (title === 'cloudstorage') {
    return 'Cloud Storage';
  } else if (title === 'cloudsql') {
    return 'Cloud SQL';
  } else if (title === 'stackdriverlogging') {
    return 'Stackdriver Logging';
  } else if (title === 'stackdrivermonitoring') {
    return 'Stackdriver Monitoring';
  } else if (title === 'computeengine') {
    return 'Compute Engine';
  } else if (title === 'kubernetesengine') {
    return 'Kubernetes Engine';
  } else if (title === 'aad') {
    return 'Azure Active Directory';
  } else if (title === 'rbac') {
    return 'Azure RBAC';
  } else if (title === 'storageaccounts') {
    return 'Storage Accounts';
  } else if (title === 'sqldatabase') {
    return 'SQL Database';
  } else if (title === 'virtualmachines') {
    return 'Virtual Machines';
  } else if (title === 'securitycenter') {
    return 'Security Center';
  } else if (title === 'network') {
    return 'Network';
  } else if (title === 'keyvault') {
    return 'Key Vault';
  } else if (title === 'appgateway') {
    return 'Application Gateway';
  } else if (title === 'rediscache') {
    return 'Redis Cache';
  } else if (title === 'appservice') {
    return 'App Services';
  } else if (title === 'loadbalancer') {
    return 'Load Balancer';
  } else if (title === 'ram') {
    return 'RAM';
  } else if (title === 'actiontrail') {
    return 'ActionTrail';
  } else if (title === 'ecs') {
    return 'ECS';
  } else if (title === 'oss') {
    return 'OSS';
  } else if (title === 'objectstorage') {
    return 'Object Storage';
  } else {
    return (title.charAt(0).toUpperCase() + title.substr(1).toLowerCase()).split('_').join(' ');
  }
};
