var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
  NODE_ENV: '"localhost"',
  API_URL: '"https://servicebc-cfms-api-dev.pathfinder.gov.bc.ca/api/v1"'
})
