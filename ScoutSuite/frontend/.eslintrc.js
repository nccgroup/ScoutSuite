module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
    'node': true
  },
  'extends': ['eslint:recommended', 'plugin:react/recommended'],
  'parserOptions': {
    'ecmaFeatures': {
      'jsx': true,
      'modules': true
    },
    'ecmaVersion': 12,
    'sourceType': 'module'
  },
  'plugins': ['react'],
  'rules': {
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'eol-last': ['warn', 'always'],
    'react/jsx-uses-vars': 'error',
    'react/jsx-uses-react': 1,
    'no-debugger': 0,
    'react/jsx-first-prop-new-line': [1, 'multiline'],
    'react/jsx-max-props-per-line': [1,
      {
        'maximum': 2
      }
    ]
  },
  'settings': {
    'react': {
      'pragma': 'React',
      'version': 'detect'
    }
  }
};
