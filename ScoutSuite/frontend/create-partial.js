var fs = require('fs');
const { prompt } = require('enquirer');
const Store = require('data-store');

const parseFile = async (provider, filename) => {
  const path =
    `../output/data/html/partials/${provider}/${filename}`;
  var file = fs.readFileSync(path, 'utf8');

  const rg = /<div class="list-group-item">(?<list>.*)<\/div>/gms;
  const listGroup = rg.exec(file);

  const sections = [];

  let regexpNames = /class="list-group-item-heading">(?<sectionName>.*?)<\/h4>(?<sectionContent>.*?)(?:<h4|$)/gs;
  let match = regexpNames.exec(listGroup.groups.list);
  do {
    sections.push({
      name: match.groups.sectionName,
      content: match.groups.sectionContent,
    });
  } while ((match = regexpNames.exec(listGroup.groups.list)) !== null);

  const sectionsParsed = [];

  let index = 0;

  for (const { name, content } of sections) {
    sectionsParsed.push({ name, values: [] });

    let regexpNames = /<div class="list-group-item-text item-margin">(?:\n[\t ]*)?(?<name>[\w ]+):(?<content>(?: |\n\t*)<span id="(?<id>.*?)">(?:.*?){{(?<value>.*?)}}(?:.*?))<\/div>/gms;
    let match = regexpNames.exec(content);
    do {

      if (match) {
        sectionsParsed[index].values.push({
          name: match.groups.name,
          id: match.groups.id,
          value: match.groups.value,
          content: match.groups.content,
        });
      }
    } while ((match = regexpNames.exec(content)) !== null);

    index++;
  }

  return sectionsParsed;
};

const template = (CompName, informations, tabs, renderers) => {

  const tabsRender = tabs.map(({ name, output }) => `
    <TabPane title="${name}">
      ${output}
    </TabPane>
  `).join('\n');

  return `
import React from 'react';
import PropTypes from 'prop-types';

import { Partial, PartialValue } from '../../../components/Partial';
import { 
  partialDataShape,
  ${renderers ? renderers.join(', \n  ') : renderers}
} from '../../../utils/Partials';
${tabs.length > 0 ? 'import { TabsMenu, TabPane } from \'../../../components/Partial/PartialTabs\';' : ''}

const propTypes = {
  data: PropTypes.shape(partialDataShape).isRequired,
};

const ${CompName} = props => {
  const { data } = props;

  if (!data) return null;

  return (
    <Partial data={data}>
      <div>
${informations}
      </div>

      ${tabsRender ? `<TabsMenu>
        ${tabsRender}
      </TabsMenu> ` : ''}
    </Partial>
  );
};

${CompName}.propTypes = propTypes;

export default ${CompName};`;
};

const createValue = (label, valuePath, renderer, addTab) => {
  let extra = '';

  if (renderer) {
    extra += `renderValue={${renderer}}`;
  }

  if (extra.length > 0) extra += `\n${addTab ? '  ' : ''}        `;

  return `${addTab ? '  ' : ''}      <PartialValue
${addTab ? '  ' : ''}        label="${label}"
${addTab ? '  ' : ''}        valuePath="${valuePath}"
${addTab ? '  ' : ''}        ${extra}/>

`;
};

const notNormalValue = (label, valuePath, content, addTab) => {
  return `${addTab ? '  ' : ''}        {/* *** NOT NORMAL RENDERING *** 
${addTab ? '  ' : ''}           LABEL: ${label}
${addTab ? '  ' : ''}           valuePath: ${valuePath}
${content}
${addTab ? '  ' : ''}        */}

`;
};

const getRendererName = (name) => {
  switch (name) {
  case 'value_or_none':
    return 'valueOrNone';
  case 'convert_bool_to_enabled':
    return 'convertBoolToEnable';
  case 'format_date':
    return 'formatDate';
  default:
    return 'DOESNOTEXIST';
  }
};

const createPartialValues = (values, addTab) => {
  let output = '';
  let renderers = [];

  values.map(({ name, value, content }) => {
    //const errorId = id.split('.').slice(-1);
    const valueParts = value.split(' ');
    let valuePath = '';
    let renderer = null;

    if (valueParts[1] && valueParts[0] !== '#each') {
      valuePath = valueParts[1];
      renderer = getRendererName(valueParts[0]);
      if (!renderers.includes(renderer) && renderer !== 'DOESNOTEXIST') renderers.push(renderer);

      if (renderer === 'DOESNOTEXIST') renderer = `{/* NO RENDERER FOR ${valueParts[0]} */}`;

      output += createValue(name, valuePath, renderer, addTab);
    } else if (valueParts[1] && valueParts[0] === '#each') {
      output += notNormalValue(name, valueParts[1], content);
    } else {
      valuePath = value;
      output += createValue(name, valuePath, renderer, addTab);
    }
    
  });
  return {
    output,
    renderers,
  };
};

const createTemplate = async (sections, Name) => {

  let informations = '';
  let finalRenderers = new Set();
  let tabs = [];

  for (const section of sections) {

    if (section.name === 'Information') {
      const { output, renderers } = createPartialValues(section.values, true);
      renderers.forEach((item) => finalRenderers.add(item));

      informations = output;
    } else {
      const { output, renderers } = createPartialValues(section.values, false);
      renderers.forEach((item) => finalRenderers.add(item)); 

      tabs.push({ name: section.name, output });
    }
  }

  return template(Name, informations, tabs, Array.from(finalRenderers));
};


const cliQuestions = async () => {
  const responses = await prompt([
    {
      type: 'select',
      name: 'provider',
      message: 'Select the provider',
      choices: ['aws', 'azure', 'gcp']
    },
    {
      type: 'input',
      name: 'filename',
      message: 'What is the filename of the old file name?',
      history: {
        store: new Store({ path: `${__dirname}/.cli/filename.json` }),
        autosave: true
      }
    },
    {
      type: 'input',
      name: 'folder_name',
      message: 'What is the name of the new partial?',
      history: {
        store: new Store({ path: `${__dirname}/.cli/folder_name.json` }),
        autosave: true
      }
    },
    {
      type: 'input',
      name: 'component_name',
      message: 'What is the name of the new component?',
      history: {
        store: new Store({ path: `${__dirname}/.cli/component_name.json` }),
        autosave: true
      }
    },
  ]);

  return responses;
};

const createNewFiles = async (provider, folder, content) => {
  if (!fs.existsSync(`src/partials/${provider}/${folder}`)){
    fs.mkdirSync(`src/partials/${provider}/${folder}`);
  }

  fs.writeFileSync(`src/partials/${provider}/${folder}/index.js`, content, 'utf8');
};


const start = async () => {
  const responses = await cliQuestions();
  const sections = await parseFile(responses.provider, responses.filename);
  const rendered = await createTemplate(sections, responses.component_name);
  await createNewFiles(responses.provider, responses.folder_name, rendered);
};


start();
