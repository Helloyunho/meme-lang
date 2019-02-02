const Stringg = require('./string')

module.exports = (value, visit) => {
  let a = visit.visit(value[0])
  let result = a.toString()
  return new Stringg(result)
}
