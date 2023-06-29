module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
    es6: true,
  },
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module',
  },
  extends: ['eslint:recommended'],
  rules: {
    // Add your custom rules here
    // Example: 'no-console': 'off'
  },
};

