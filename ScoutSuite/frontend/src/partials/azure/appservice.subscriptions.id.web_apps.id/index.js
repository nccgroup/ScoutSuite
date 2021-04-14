import React from 'react';
import PropTypes from 'prop-types';

import InformationsWrapper from '../../../components/InformationsWrapper';
import { Partial, PartialValue } from '../../../components/Partial';
import {
  partialDataShape,
  valueOrNone,
  convertBoolToEnable,
  formatDate,
  renderList,
} from '../../../utils/Partials';
import { TabsMenu, TabPane } from '../../../components/Partial/PartialTabs';

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
  item: PropTypes.object,
};

const WebApps = props => {
  const { data, item } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <InformationsWrapper>
        <PartialValue
          label="Name" valuePath="name"
          renderValue={valueOrNone} />

        <PartialValue
          label="Resource Group"
          valuePath="resource_group"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Repository Site Name"
          valuePath="repository_site_name"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Location"
          valuePath="location"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Last Modified Time"
          valuePath="last_modified_time_utc"
          errorPath="last_modified_time_utc"
          renderValue={formatDate}
        />

        <PartialValue
          label="State"
          valuePath="state"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Usage State"
          valuePath="usage_state"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Availability State"
          valuePath="availability_state"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Kind" valuePath="kind"
          renderValue={valueOrNone} />

        <PartialValue
          label="Programming Language"
          valuePath="programming_language"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Programming Language Version"
          valuePath="programming_language_version"
          renderValue={valueOrNone}
        />

        <PartialValue
          label="Tags" valuePath="tags"
          renderValue={renderList} />
      </InformationsWrapper>

      <TabsMenu>
        <TabPane title="Configuration">
          <PartialValue
            label="Authentication"
            valuePath="authentication_enabled"
            renderValue={convertBoolToEnable}
          />

          <PartialValue
            label="HTTPS-Only Traffic"
            valuePath="https_only"
            renderValue={convertBoolToEnable}
          />

          <PartialValue
            label="HTTPS 2.0 Support"
            valuePath="http_2_enabled"
            renderValue={convertBoolToEnable}
          />

          <PartialValue
            label="HTTP Logging"
            valuePath="http_logging_enabled"
            renderValue={convertBoolToEnable}
          />
          <PartialValue
            label="FTP Deployment"
            valuePath="ftp_deployment_enabled"
            renderValue={convertBoolToEnable}
          />

          <PartialValue
            label="Minimum TLS Version Supported"
            valuePath="minimum_tls_version_supported"
            errorPath="minimum_tls_supported"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Client Certificates"
            valuePath="client_cert_enabled"
            renderValue={convertBoolToEnable}
          />
        </TabPane>

        <TabPane title="Identities" disabled={item.identity}>
          <PartialValue
            label="System Assigned Identity"
            valuePath="identity.principal_id"
            errorPath="identity.managed_principal_id"
            renderValue={valueOrNone}
          />

          {item.identity.user_assigned_identities && (
            <div>
              <b>User Assigned Identities</b>
              {renderList(
                item.identity.user_assigned_identities,
                '',
                user => user.principal_id,
              )}
            </div>
          )}
        </TabPane>

        <TabPane title="Networking">
          <PartialValue
            label="Default Host Name"
            valuePath="default_host_name"
            renderValue={valueOrNone}
          />

          <PartialValue
            label="Outbound IP Addresses"
            valuePath="outbound_ip_addresses"
            renderValue={renderList(item.outbound_ip_addresses)}
          />

          <PartialValue
            label="Possible Outbound IP Addresses"
            valuePath="possible_outbound_ip_addresses"
            renderValue={renderList(item.possible_outbound_ip_addresses)}
          />
        </TabPane>
      </TabsMenu>
    </Partial>
  );
};

WebApps.propTypes = propTypes;

export default WebApps;
