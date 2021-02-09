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
    'linebreak-style': ['error', 'unix'],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'react/jsx-uses-vars': 'error',
    'react/jsx-uses-react': 1
  },
  'settings': {
    'react': {
      'pragma': 'React',
      'version': 'detect'
    }
  }
};
