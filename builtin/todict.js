const lexer = require('../lexer')
const Token = require('../lexer/Token')
const Parser = require('../parser')

module.exports = (value, visit) => {
  let a = visit.visit(value[0]).value
  if (typeof a === 'string') {
    let tokened = lexer(a)
    tokened = tokened.slice(1, tokened.length - 2)
    tokened.push(new Token('None', undefined))
    if (tokened[0].type === '{' && tokened[tokened.length - 2].type === '}') {
      let readyForParse = new Parser(tokened)
      let parsed = readyForParse.exce()
      return visit.visit(parsed)
    }
  }
}
