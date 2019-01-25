const Stringg = require('./string')
const Numberr = require('./number')
const Booleann = require('./boolean')
const Arrayy = require('./array')

module.exports = (a) => {
  if (typeof a === 'string') {
    return new Stringg(a)
  } else if (typeof a === 'number') {
    return new Numberr(a)
  } else if (typeof a === 'boolean') {
    return new Booleann(a)
  } else if (Array.isArray(a)) {
    return new Arrayy(a)
  }
}
