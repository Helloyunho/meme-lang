/* eslint-env mocha */
const L = require('./lexer')
const P = require('./parser')
const S = require('./symbol')
const Builtin = require('./builtin')
const Module = require('./module')
const chai = require('chai')
const expect = chai.expect
const should = chai.should()

describe('import modules', () => {
  it('It must return random module', done => {
    let l = L('import random')
    let p = new P(l).parse()
    let s = new S()
    s.visit(p)
    expect(s.currentState.lookup('random').value).to.equal(Module.random)
    done()
  })
})

describe('assign variable', () => {
  it('It must to 3', done => {
    let l = L('a = 3')
    let p = new P(l).parse()
    let s = new S()
    s.visit(p)
    expect(s.currentState.lookup('a').value).to.equal(3)
    done()
  })
})

describe('get variable', () => {
  it('It must to 3', done => {
    let l = L('a = 3; print(a)')
    let p = new P(l).parse()
    let s = new S()
    s.visit(p)
    done()
  })
})

describe('convert to number', () => {
  it('It must to 3', done => {
    let l = L('print(num(\'3\'))')
    let p = new P(l).parse()
    let s = new S()
    s.visit(p)
    done()
  })
})
