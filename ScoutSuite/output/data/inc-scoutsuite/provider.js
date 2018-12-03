/**
 * Get the whole config dictionary
 * @returns {{aws_account_id, last_run, metadata, provider_code, provider_name, service_groups, service_list, services, sg_map, subnet_map}|*}
 */
function get_scoutsuite_results() {
    return scoutsuite_results;
}