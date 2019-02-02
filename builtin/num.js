const Numberr = require('./number')

module.exports = (value, visit) => {
  let a = visit.visit(value[0])
  let result = a.toNumber()
  return new Numberr(result)
}
