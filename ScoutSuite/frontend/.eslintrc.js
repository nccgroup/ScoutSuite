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
  'plugins': [
    'react',
    'react-hooks',
  ],
  'rules': {
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'eol-last': ['warn', 'always'],
    'react/jsx-uses-vars': 'error',
    'react/jsx-uses-react': 1,
    'react-hooks/rules-of-hooks': 'error',
    'no-debugger': 0,
  },
  'settings': {
    'react': {
      'pragma': 'React',
      'version': 'detect'
    }
  }
};
