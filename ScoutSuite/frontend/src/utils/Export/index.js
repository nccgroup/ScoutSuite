import { Parser } from 'json2csv';

export const exportCSV = (content, name) => {
  const json2csvParser = new Parser();
  const csv = json2csvParser.parse(content);
  exportFile(csv, name + '.csv');
};

export const exportJSON = (content, name) => {
  exportFile(JSON.stringify(content, null, 2), name + '.json');
};

const exportFile = (content, name) => {
  var dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(content);
  var downloadAnchorNode = document.createElement('a');
  downloadAnchorNode.setAttribute('href', dataStr);
  downloadAnchorNode.setAttribute('download', name);
  document.body.appendChild(downloadAnchorNode); // required for firefox
  downloadAnchorNode.click();
  downloadAnchorNode.remove();
};
