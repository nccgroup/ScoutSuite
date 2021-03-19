import React from 'react';
import PropTypes from 'prop-types';
import { 
  PieChart, 
  Pie,
  BarChart,
  Bar,
  ResponsiveContainer,
  CartesianGrid,
  Tooltip,
  XAxis,
  YAxis,
  Legend,
} from 'recharts';
import reduce from 'lodash/reduce';
import get from 'lodash/get';
import omitBy from 'lodash/omitBy';
import size from 'lodash/size';

import './style.scss';


const propTypes = {
  services: PropTypes.arrayOf(PropTypes.object).isRequired,
};

const IssuesCharts = props => {
  const { services } = props;

  const height = 400;
  const fillColors = [
    '#24bc74',
    '#4099ff',
    '#ffb44c',
    '#fc6464',
    '#c41230',
  ];

  const issues = reduce(
    services, 
    (sum, service) => ({
      Good: sum.Good + get(service, ['issues', 'Good'], 0),
      Low: sum.Low + get(service, ['issues', 'Low'], 0),
      Medium: sum.Medium + get(service, ['issues', 'Medium'], 0),
      High: sum.High + get(service, ['issues', 'High'], 0),
      Critical: sum.Critical + get(service, ['issues', 'Critical'], 0),
    }), 
    {
      Critical: 0,
      High: 0,
      Medium: 0,
      Low: 0,
      Good: 0,
    },
  );
  const pieData = Object.entries(issues).map(([name, sum], i) => ({
    name: name,
    value: sum,
    fill: fillColors[i],
  }));

  const barData = services.map(service => ({
    name: service.name,
    ...omitBy(service.issues, issue => issue === 0),
  }));

  return (
    <div className="issues-charts">
      <div className="pie-chart">
        <h3>Issues by severity</h3>
        <ResponsiveContainer 
          height={height}
          width="100%"
        >
          <PieChart>
            <Pie
              dataKey="value"
              data={pieData.filter(entry => entry.value > 0)}
              cy="85%"
              startAngle={180}
              endAngle={0}
              innerRadius={110}
              outerRadius={170}
              label
              labelLine={false}
              isAnimationActive={false}
            />
            <Legend verticalAlign="bottom" height={48}/>
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="bar-chart">
        <h3>Issues by service</h3>
        <ResponsiveContainer 
          height={height}
          width="90%"
        >
          <BarChart
            data={barData.filter(entry => size(entry) > 1)}
            margin={{
              top: 20,
              bottom: 20,
            }}
          >
            <CartesianGrid />
            <XAxis 
              dataKey="name"
              height={80}
              padding={{
                left: 10,
                right: 10,
              }}
              interval={1}
              tick={<CustomizedAxisTick />}
            />
            <YAxis />
            <Tooltip 
              labelStyle={{
                fontWeight: 700,
              }}
              itemStyle={{
                fontWeight: 600,
              }}
            />
            <Bar dataKey="Good" stackId="a" fill={fillColors[0]} />
            <Bar dataKey="Low" stackId="a" fill={fillColors[1]} />
            <Bar dataKey="Medium" stackId="a" fill={fillColors[2]} />
            <Bar dataKey="High" stackId="a" fill={fillColors[3]} />
            <Bar dataKey="Critical" stackId="a" fill={fillColors[4]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

const tickPropTypes = {
  y: PropTypes.number, 
  payload: PropTypes.object,
};

const CustomizedAxisTick = props => {
  const { y, payload } = props;

  return (
    <g transform={`translate(${payload.coordinate},${y})`}>
      <text x={0} y={0} dy={16} textAnchor="end" fill="#666" transform="rotate(-40)">
        {payload.value}
      </text>
    </g>
  );
};

IssuesCharts.propTypes = propTypes;
CustomizedAxisTick.propTypes = tickPropTypes;

export default IssuesCharts;
