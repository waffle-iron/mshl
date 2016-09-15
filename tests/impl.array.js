include('inc/testing.js')

include('array.js')
include('assert.js')

test.name = 'file operations test'

a = Array()
Assert.equal(a.length, 0, 'new array should be zero-length')

a.push('abc')
Assert.equal(a.length, 1, 'array length error 1')
a.push('xyz')
Assert.equal(a.length, 2, 'array length error 2')
a.push('123')
Assert.equal(a.length, 3, 'array length error 3')
a.insert('qqq', 1)
Assert.equal(a.length, 4, 'array length error 4')

Assert.equal(a[0], 'abc', 'first element could not be read properly')
Assert.equal(a[1], 'qqq', 'second element could not be read properly')
Assert.equal(a[2], 'xyz', 'third element could not be read properly')
Assert.equal(a[3], '123', 'fourth element could not be read properly')

Assert.equal(a.pop(), '123', 'pop seems to have failed 1')
Assert.equal(a.length, 3, 'array length error 5')
Assert.equal(a.pop(), 'xyz', 'pop seems to have failed 2')
Assert.equal(a.length, 2, 'array length error 6')
Assert.equal(a.pop(), 'qqq', 'pop seems to have failed 3')
Assert.equal(a.length, 1, 'array length error 7')
Assert.equal(a.pop(), 'abc', 'pop seems to have failed 4')
Assert.equal(a.length, 0, 'array length error 8')
