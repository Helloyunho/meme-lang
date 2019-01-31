const Parser = require('./parser')
const lexer = require('./lexer')
const Interpreter = require('./symbol')
const repl = require('repl')
const replServer = repl.start({
  prompt: '> '
})

let interpreter = new Interpreter()

replServer.defineCommand('calc', {
  action (data) {
    let result = new Parser(lexer(data))
    result = interpreter.visit(result)
    this.clearBufferedCommand()
    console.log(result)
    this.displayPrompt()
  }
})
