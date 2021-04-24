import React from 'react';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import { useAPI } from '../../../api/useAPI';
import {
  getResourceFilterAttributeEndpoint,
  getFindingFilterAttributeEndpoint,
} from '../../../api/paths';
import { PropTypes } from 'prop-types';
import { useParams } from 'react-router-dom';

const propTypes = {
  filter: PropTypes.shape({
    name: PropTypes.string.isRequired,
    key: PropTypes.string.isRequired,
  }).isRequired,
  selected: PropTypes.string.isRequired,
  handleChange: PropTypes.func.isRequired,
};

const Filter = props => {
  const { service, resource, finding } = useParams();
  const { filter, selected, handleChange } = props;
  const { data, loading } = useAPI(
    finding
      ? getFindingFilterAttributeEndpoint(service, finding, filter.key)
      : getResourceFilterAttributeEndpoint(service, resource, filter.key),
  );

  return (
    <FormControl
      variant="outlined" margin="dense"
      size="small">
      <InputLabel id={`filter-label-${filter.key}`}>{filter.name}</InputLabel>
      <Select
        labelId={`filter-label-${filter.key}`}
        value={selected}
        onChange={handleChange}
        label={filter.name}
        name={filter.key}
      >
        <MenuItem value="">
          <em>None</em>
        </MenuItem>
        {!loading &&
          data &&
          data.map(name => (
            <MenuItem value={name} key={name}>
              {name}
            </MenuItem>
          ))}
      </Select>
    </FormControl>
  );
};

Filter.propTypes = propTypes;

export default Filter;
