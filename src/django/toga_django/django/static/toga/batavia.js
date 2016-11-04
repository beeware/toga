
fixedConsoleLog = function(msg) {
    console.log.call(console, msg);
};

var batavia = {
    stdout: fixedConsoleLog,
    stderr: fixedConsoleLog,
    core: {},
    types: {},
    modules: {},
    builtins: {},
    vendored: {},
    stdlib: {}
};

// set in PYCFile while parsing python bytecode
batavia.BATAVIA_MAGIC = null;
batavia.BATAVIA_MAGIC_34 = String.fromCharCode(238, 12, 13, 10);
batavia.BATAVIA_MAGIC_35 = String.fromCharCode(22, 13, 13, 10);
batavia.BATAVIA_MAGIC_35a0 = String.fromCharCode(248, 12, 13, 10);
(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}(g.batavia || (g.batavia = {})).vendored = f()}})(function(){var define,module,exports;return (function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
'use strict'

exports.byteLength = byteLength
exports.toByteArray = toByteArray
exports.fromByteArray = fromByteArray

var lookup = []
var revLookup = []
var Arr = typeof Uint8Array !== 'undefined' ? Uint8Array : Array

var code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
for (var i = 0, len = code.length; i < len; ++i) {
  lookup[i] = code[i]
  revLookup[code.charCodeAt(i)] = i
}

revLookup['-'.charCodeAt(0)] = 62
revLookup['_'.charCodeAt(0)] = 63

function placeHoldersCount (b64) {
  var len = b64.length
  if (len % 4 > 0) {
    throw new Error('Invalid string. Length must be a multiple of 4')
  }

  // the number of equal signs (place holders)
  // if there are two placeholders, than the two characters before it
  // represent one byte
  // if there is only one, then the three characters before it represent 2 bytes
  // this is just a cheap hack to not do indexOf twice
  return b64[len - 2] === '=' ? 2 : b64[len - 1] === '=' ? 1 : 0
}

function byteLength (b64) {
  // base64 is 4/3 + up to two characters of the original data
  return b64.length * 3 / 4 - placeHoldersCount(b64)
}

function toByteArray (b64) {
  var i, j, l, tmp, placeHolders, arr
  var len = b64.length
  placeHolders = placeHoldersCount(b64)

  arr = new Arr(len * 3 / 4 - placeHolders)

  // if there are placeholders, only get up to the last complete 4 chars
  l = placeHolders > 0 ? len - 4 : len

  var L = 0

  for (i = 0, j = 0; i < l; i += 4, j += 3) {
    tmp = (revLookup[b64.charCodeAt(i)] << 18) | (revLookup[b64.charCodeAt(i + 1)] << 12) | (revLookup[b64.charCodeAt(i + 2)] << 6) | revLookup[b64.charCodeAt(i + 3)]
    arr[L++] = (tmp >> 16) & 0xFF
    arr[L++] = (tmp >> 8) & 0xFF
    arr[L++] = tmp & 0xFF
  }

  if (placeHolders === 2) {
    tmp = (revLookup[b64.charCodeAt(i)] << 2) | (revLookup[b64.charCodeAt(i + 1)] >> 4)
    arr[L++] = tmp & 0xFF
  } else if (placeHolders === 1) {
    tmp = (revLookup[b64.charCodeAt(i)] << 10) | (revLookup[b64.charCodeAt(i + 1)] << 4) | (revLookup[b64.charCodeAt(i + 2)] >> 2)
    arr[L++] = (tmp >> 8) & 0xFF
    arr[L++] = tmp & 0xFF
  }

  return arr
}

function tripletToBase64 (num) {
  return lookup[num >> 18 & 0x3F] + lookup[num >> 12 & 0x3F] + lookup[num >> 6 & 0x3F] + lookup[num & 0x3F]
}

function encodeChunk (uint8, start, end) {
  var tmp
  var output = []
  for (var i = start; i < end; i += 3) {
    tmp = (uint8[i] << 16) + (uint8[i + 1] << 8) + (uint8[i + 2])
    output.push(tripletToBase64(tmp))
  }
  return output.join('')
}

function fromByteArray (uint8) {
  var tmp
  var len = uint8.length
  var extraBytes = len % 3 // if we have 1 byte left, pad 2 bytes
  var output = ''
  var parts = []
  var maxChunkLength = 16383 // must be multiple of 3

  // go through the array every three bytes, we'll deal with trailing stuff later
  for (var i = 0, len2 = len - extraBytes; i < len2; i += maxChunkLength) {
    parts.push(encodeChunk(uint8, i, (i + maxChunkLength) > len2 ? len2 : (i + maxChunkLength)))
  }

  // pad the end with zeros, but make sure to not forget the extra bytes
  if (extraBytes === 1) {
    tmp = uint8[len - 1]
    output += lookup[tmp >> 2]
    output += lookup[(tmp << 4) & 0x3F]
    output += '=='
  } else if (extraBytes === 2) {
    tmp = (uint8[len - 2] << 8) + (uint8[len - 1])
    output += lookup[tmp >> 10]
    output += lookup[(tmp >> 4) & 0x3F]
    output += lookup[(tmp << 2) & 0x3F]
    output += '='
  }

  parts.push(output)

  return parts.join('')
}

},{}],2:[function(require,module,exports){
(function (global){
/*!
 * The buffer module from node.js, for the browser.
 *
 * @author   Feross Aboukhadijeh <feross@feross.org> <http://feross.org>
 * @license  MIT
 */
/* eslint-disable no-proto */

'use strict'

var base64 = require('base64-js')
var ieee754 = require('ieee754')
var isArray = require('isarray')

exports.Buffer = Buffer
exports.SlowBuffer = SlowBuffer
exports.INSPECT_MAX_BYTES = 50

/**
 * If `Buffer.TYPED_ARRAY_SUPPORT`:
 *   === true    Use Uint8Array implementation (fastest)
 *   === false   Use Object implementation (most compatible, even IE6)
 *
 * Browsers that support typed arrays are IE 10+, Firefox 4+, Chrome 7+, Safari 5.1+,
 * Opera 11.6+, iOS 4.2+.
 *
 * Due to various browser bugs, sometimes the Object implementation will be used even
 * when the browser supports typed arrays.
 *
 * Note:
 *
 *   - Firefox 4-29 lacks support for adding new properties to `Uint8Array` instances,
 *     See: https://bugzilla.mozilla.org/show_bug.cgi?id=695438.
 *
 *   - Chrome 9-10 is missing the `TypedArray.prototype.subarray` function.
 *
 *   - IE10 has a broken `TypedArray.prototype.subarray` function which returns arrays of
 *     incorrect length in some situations.

 * We detect these buggy browsers and set `Buffer.TYPED_ARRAY_SUPPORT` to `false` so they
 * get the Object implementation, which is slower but behaves correctly.
 */
Buffer.TYPED_ARRAY_SUPPORT = global.TYPED_ARRAY_SUPPORT !== undefined
  ? global.TYPED_ARRAY_SUPPORT
  : typedArraySupport()

/*
 * Export kMaxLength after typed array support is determined.
 */
exports.kMaxLength = kMaxLength()

function typedArraySupport () {
  try {
    var arr = new Uint8Array(1)
    arr.__proto__ = {__proto__: Uint8Array.prototype, foo: function () { return 42 }}
    return arr.foo() === 42 && // typed array instances can be augmented
        typeof arr.subarray === 'function' && // chrome 9-10 lack `subarray`
        arr.subarray(1, 1).byteLength === 0 // ie10 has broken `subarray`
  } catch (e) {
    return false
  }
}

function kMaxLength () {
  return Buffer.TYPED_ARRAY_SUPPORT
    ? 0x7fffffff
    : 0x3fffffff
}

function createBuffer (that, length) {
  if (kMaxLength() < length) {
    throw new RangeError('Invalid typed array length')
  }
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    // Return an augmented `Uint8Array` instance, for best performance
    that = new Uint8Array(length)
    that.__proto__ = Buffer.prototype
  } else {
    // Fallback: Return an object instance of the Buffer class
    if (that === null) {
      that = new Buffer(length)
    }
    that.length = length
  }

  return that
}

/**
 * The Buffer constructor returns instances of `Uint8Array` that have their
 * prototype changed to `Buffer.prototype`. Furthermore, `Buffer` is a subclass of
 * `Uint8Array`, so the returned instances will have all the node `Buffer` methods
 * and the `Uint8Array` methods. Square bracket notation works as expected -- it
 * returns a single octet.
 *
 * The `Uint8Array` prototype remains unmodified.
 */

function Buffer (arg, encodingOrOffset, length) {
  if (!Buffer.TYPED_ARRAY_SUPPORT && !(this instanceof Buffer)) {
    return new Buffer(arg, encodingOrOffset, length)
  }

  // Common case.
  if (typeof arg === 'number') {
    if (typeof encodingOrOffset === 'string') {
      throw new Error(
        'If encoding is specified then the first argument must be a string'
      )
    }
    return allocUnsafe(this, arg)
  }
  return from(this, arg, encodingOrOffset, length)
}

Buffer.poolSize = 8192 // not used by this implementation

// TODO: Legacy, not needed anymore. Remove in next major version.
Buffer._augment = function (arr) {
  arr.__proto__ = Buffer.prototype
  return arr
}

function from (that, value, encodingOrOffset, length) {
  if (typeof value === 'number') {
    throw new TypeError('"value" argument must not be a number')
  }

  if (typeof ArrayBuffer !== 'undefined' && value instanceof ArrayBuffer) {
    return fromArrayBuffer(that, value, encodingOrOffset, length)
  }

  if (typeof value === 'string') {
    return fromString(that, value, encodingOrOffset)
  }

  return fromObject(that, value)
}

/**
 * Functionally equivalent to Buffer(arg, encoding) but throws a TypeError
 * if value is a number.
 * Buffer.from(str[, encoding])
 * Buffer.from(array)
 * Buffer.from(buffer)
 * Buffer.from(arrayBuffer[, byteOffset[, length]])
 **/
Buffer.from = function (value, encodingOrOffset, length) {
  return from(null, value, encodingOrOffset, length)
}

if (Buffer.TYPED_ARRAY_SUPPORT) {
  Buffer.prototype.__proto__ = Uint8Array.prototype
  Buffer.__proto__ = Uint8Array
  if (typeof Symbol !== 'undefined' && Symbol.species &&
      Buffer[Symbol.species] === Buffer) {
    // Fix subarray() in ES2016. See: https://github.com/feross/buffer/pull/97
    Object.defineProperty(Buffer, Symbol.species, {
      value: null,
      configurable: true
    })
  }
}

function assertSize (size) {
  if (typeof size !== 'number') {
    throw new TypeError('"size" argument must be a number')
  } else if (size < 0) {
    throw new RangeError('"size" argument must not be negative')
  }
}

function alloc (that, size, fill, encoding) {
  assertSize(size)
  if (size <= 0) {
    return createBuffer(that, size)
  }
  if (fill !== undefined) {
    // Only pay attention to encoding if it's a string. This
    // prevents accidentally sending in a number that would
    // be interpretted as a start offset.
    return typeof encoding === 'string'
      ? createBuffer(that, size).fill(fill, encoding)
      : createBuffer(that, size).fill(fill)
  }
  return createBuffer(that, size)
}

/**
 * Creates a new filled Buffer instance.
 * alloc(size[, fill[, encoding]])
 **/
Buffer.alloc = function (size, fill, encoding) {
  return alloc(null, size, fill, encoding)
}

function allocUnsafe (that, size) {
  assertSize(size)
  that = createBuffer(that, size < 0 ? 0 : checked(size) | 0)
  if (!Buffer.TYPED_ARRAY_SUPPORT) {
    for (var i = 0; i < size; ++i) {
      that[i] = 0
    }
  }
  return that
}

/**
 * Equivalent to Buffer(num), by default creates a non-zero-filled Buffer instance.
 * */
Buffer.allocUnsafe = function (size) {
  return allocUnsafe(null, size)
}
/**
 * Equivalent to SlowBuffer(num), by default creates a non-zero-filled Buffer instance.
 */
Buffer.allocUnsafeSlow = function (size) {
  return allocUnsafe(null, size)
}

function fromString (that, string, encoding) {
  if (typeof encoding !== 'string' || encoding === '') {
    encoding = 'utf8'
  }

  if (!Buffer.isEncoding(encoding)) {
    throw new TypeError('"encoding" must be a valid string encoding')
  }

  var length = byteLength(string, encoding) | 0
  that = createBuffer(that, length)

  var actual = that.write(string, encoding)

  if (actual !== length) {
    // Writing a hex string, for example, that contains invalid characters will
    // cause everything after the first invalid character to be ignored. (e.g.
    // 'abxxcd' will be treated as 'ab')
    that = that.slice(0, actual)
  }

  return that
}

function fromArrayLike (that, array) {
  var length = array.length < 0 ? 0 : checked(array.length) | 0
  that = createBuffer(that, length)
  for (var i = 0; i < length; i += 1) {
    that[i] = array[i] & 255
  }
  return that
}

function fromArrayBuffer (that, array, byteOffset, length) {
  array.byteLength // this throws if `array` is not a valid ArrayBuffer

  if (byteOffset < 0 || array.byteLength < byteOffset) {
    throw new RangeError('\'offset\' is out of bounds')
  }

  if (array.byteLength < byteOffset + (length || 0)) {
    throw new RangeError('\'length\' is out of bounds')
  }

  if (byteOffset === undefined && length === undefined) {
    array = new Uint8Array(array)
  } else if (length === undefined) {
    array = new Uint8Array(array, byteOffset)
  } else {
    array = new Uint8Array(array, byteOffset, length)
  }

  if (Buffer.TYPED_ARRAY_SUPPORT) {
    // Return an augmented `Uint8Array` instance, for best performance
    that = array
    that.__proto__ = Buffer.prototype
  } else {
    // Fallback: Return an object instance of the Buffer class
    that = fromArrayLike(that, array)
  }
  return that
}

function fromObject (that, obj) {
  if (Buffer.isBuffer(obj)) {
    var len = checked(obj.length) | 0
    that = createBuffer(that, len)

    if (that.length === 0) {
      return that
    }

    obj.copy(that, 0, 0, len)
    return that
  }

  if (obj) {
    if ((typeof ArrayBuffer !== 'undefined' &&
        obj.buffer instanceof ArrayBuffer) || 'length' in obj) {
      if (typeof obj.length !== 'number' || isnan(obj.length)) {
        return createBuffer(that, 0)
      }
      return fromArrayLike(that, obj)
    }

    if (obj.type === 'Buffer' && isArray(obj.data)) {
      return fromArrayLike(that, obj.data)
    }
  }

  throw new TypeError('First argument must be a string, Buffer, ArrayBuffer, Array, or array-like object.')
}

function checked (length) {
  // Note: cannot use `length < kMaxLength()` here because that fails when
  // length is NaN (which is otherwise coerced to zero.)
  if (length >= kMaxLength()) {
    throw new RangeError('Attempt to allocate Buffer larger than maximum ' +
                         'size: 0x' + kMaxLength().toString(16) + ' bytes')
  }
  return length | 0
}

function SlowBuffer (length) {
  if (+length != length) { // eslint-disable-line eqeqeq
    length = 0
  }
  return Buffer.alloc(+length)
}

Buffer.isBuffer = function isBuffer (b) {
  return !!(b != null && b._isBuffer)
}

Buffer.compare = function compare (a, b) {
  if (!Buffer.isBuffer(a) || !Buffer.isBuffer(b)) {
    throw new TypeError('Arguments must be Buffers')
  }

  if (a === b) return 0

  var x = a.length
  var y = b.length

  for (var i = 0, len = Math.min(x, y); i < len; ++i) {
    if (a[i] !== b[i]) {
      x = a[i]
      y = b[i]
      break
    }
  }

  if (x < y) return -1
  if (y < x) return 1
  return 0
}

Buffer.isEncoding = function isEncoding (encoding) {
  switch (String(encoding).toLowerCase()) {
    case 'hex':
    case 'utf8':
    case 'utf-8':
    case 'ascii':
    case 'latin1':
    case 'binary':
    case 'base64':
    case 'ucs2':
    case 'ucs-2':
    case 'utf16le':
    case 'utf-16le':
      return true
    default:
      return false
  }
}

Buffer.concat = function concat (list, length) {
  if (!isArray(list)) {
    throw new TypeError('"list" argument must be an Array of Buffers')
  }

  if (list.length === 0) {
    return Buffer.alloc(0)
  }

  var i
  if (length === undefined) {
    length = 0
    for (i = 0; i < list.length; ++i) {
      length += list[i].length
    }
  }

  var buffer = Buffer.allocUnsafe(length)
  var pos = 0
  for (i = 0; i < list.length; ++i) {
    var buf = list[i]
    if (!Buffer.isBuffer(buf)) {
      throw new TypeError('"list" argument must be an Array of Buffers')
    }
    buf.copy(buffer, pos)
    pos += buf.length
  }
  return buffer
}

function byteLength (string, encoding) {
  if (Buffer.isBuffer(string)) {
    return string.length
  }
  if (typeof ArrayBuffer !== 'undefined' && typeof ArrayBuffer.isView === 'function' &&
      (ArrayBuffer.isView(string) || string instanceof ArrayBuffer)) {
    return string.byteLength
  }
  if (typeof string !== 'string') {
    string = '' + string
  }

  var len = string.length
  if (len === 0) return 0

  // Use a for loop to avoid recursion
  var loweredCase = false
  for (;;) {
    switch (encoding) {
      case 'ascii':
      case 'latin1':
      case 'binary':
        return len
      case 'utf8':
      case 'utf-8':
      case undefined:
        return utf8ToBytes(string).length
      case 'ucs2':
      case 'ucs-2':
      case 'utf16le':
      case 'utf-16le':
        return len * 2
      case 'hex':
        return len >>> 1
      case 'base64':
        return base64ToBytes(string).length
      default:
        if (loweredCase) return utf8ToBytes(string).length // assume utf8
        encoding = ('' + encoding).toLowerCase()
        loweredCase = true
    }
  }
}
Buffer.byteLength = byteLength

function slowToString (encoding, start, end) {
  var loweredCase = false

  // No need to verify that "this.length <= MAX_UINT32" since it's a read-only
  // property of a typed array.

  // This behaves neither like String nor Uint8Array in that we set start/end
  // to their upper/lower bounds if the value passed is out of range.
  // undefined is handled specially as per ECMA-262 6th Edition,
  // Section 13.3.3.7 Runtime Semantics: KeyedBindingInitialization.
  if (start === undefined || start < 0) {
    start = 0
  }
  // Return early if start > this.length. Done here to prevent potential uint32
  // coercion fail below.
  if (start > this.length) {
    return ''
  }

  if (end === undefined || end > this.length) {
    end = this.length
  }

  if (end <= 0) {
    return ''
  }

  // Force coersion to uint32. This will also coerce falsey/NaN values to 0.
  end >>>= 0
  start >>>= 0

  if (end <= start) {
    return ''
  }

  if (!encoding) encoding = 'utf8'

  while (true) {
    switch (encoding) {
      case 'hex':
        return hexSlice(this, start, end)

      case 'utf8':
      case 'utf-8':
        return utf8Slice(this, start, end)

      case 'ascii':
        return asciiSlice(this, start, end)

      case 'latin1':
      case 'binary':
        return latin1Slice(this, start, end)

      case 'base64':
        return base64Slice(this, start, end)

      case 'ucs2':
      case 'ucs-2':
      case 'utf16le':
      case 'utf-16le':
        return utf16leSlice(this, start, end)

      default:
        if (loweredCase) throw new TypeError('Unknown encoding: ' + encoding)
        encoding = (encoding + '').toLowerCase()
        loweredCase = true
    }
  }
}

// The property is used by `Buffer.isBuffer` and `is-buffer` (in Safari 5-7) to detect
// Buffer instances.
Buffer.prototype._isBuffer = true

function swap (b, n, m) {
  var i = b[n]
  b[n] = b[m]
  b[m] = i
}

Buffer.prototype.swap16 = function swap16 () {
  var len = this.length
  if (len % 2 !== 0) {
    throw new RangeError('Buffer size must be a multiple of 16-bits')
  }
  for (var i = 0; i < len; i += 2) {
    swap(this, i, i + 1)
  }
  return this
}

Buffer.prototype.swap32 = function swap32 () {
  var len = this.length
  if (len % 4 !== 0) {
    throw new RangeError('Buffer size must be a multiple of 32-bits')
  }
  for (var i = 0; i < len; i += 4) {
    swap(this, i, i + 3)
    swap(this, i + 1, i + 2)
  }
  return this
}

Buffer.prototype.swap64 = function swap64 () {
  var len = this.length
  if (len % 8 !== 0) {
    throw new RangeError('Buffer size must be a multiple of 64-bits')
  }
  for (var i = 0; i < len; i += 8) {
    swap(this, i, i + 7)
    swap(this, i + 1, i + 6)
    swap(this, i + 2, i + 5)
    swap(this, i + 3, i + 4)
  }
  return this
}

Buffer.prototype.toString = function toString () {
  var length = this.length | 0
  if (length === 0) return ''
  if (arguments.length === 0) return utf8Slice(this, 0, length)
  return slowToString.apply(this, arguments)
}

Buffer.prototype.equals = function equals (b) {
  if (!Buffer.isBuffer(b)) throw new TypeError('Argument must be a Buffer')
  if (this === b) return true
  return Buffer.compare(this, b) === 0
}

Buffer.prototype.inspect = function inspect () {
  var str = ''
  var max = exports.INSPECT_MAX_BYTES
  if (this.length > 0) {
    str = this.toString('hex', 0, max).match(/.{2}/g).join(' ')
    if (this.length > max) str += ' ... '
  }
  return '<Buffer ' + str + '>'
}

Buffer.prototype.compare = function compare (target, start, end, thisStart, thisEnd) {
  if (!Buffer.isBuffer(target)) {
    throw new TypeError('Argument must be a Buffer')
  }

  if (start === undefined) {
    start = 0
  }
  if (end === undefined) {
    end = target ? target.length : 0
  }
  if (thisStart === undefined) {
    thisStart = 0
  }
  if (thisEnd === undefined) {
    thisEnd = this.length
  }

  if (start < 0 || end > target.length || thisStart < 0 || thisEnd > this.length) {
    throw new RangeError('out of range index')
  }

  if (thisStart >= thisEnd && start >= end) {
    return 0
  }
  if (thisStart >= thisEnd) {
    return -1
  }
  if (start >= end) {
    return 1
  }

  start >>>= 0
  end >>>= 0
  thisStart >>>= 0
  thisEnd >>>= 0

  if (this === target) return 0

  var x = thisEnd - thisStart
  var y = end - start
  var len = Math.min(x, y)

  var thisCopy = this.slice(thisStart, thisEnd)
  var targetCopy = target.slice(start, end)

  for (var i = 0; i < len; ++i) {
    if (thisCopy[i] !== targetCopy[i]) {
      x = thisCopy[i]
      y = targetCopy[i]
      break
    }
  }

  if (x < y) return -1
  if (y < x) return 1
  return 0
}

// Finds either the first index of `val` in `buffer` at offset >= `byteOffset`,
// OR the last index of `val` in `buffer` at offset <= `byteOffset`.
//
// Arguments:
// - buffer - a Buffer to search
// - val - a string, Buffer, or number
// - byteOffset - an index into `buffer`; will be clamped to an int32
// - encoding - an optional encoding, relevant is val is a string
// - dir - true for indexOf, false for lastIndexOf
function bidirectionalIndexOf (buffer, val, byteOffset, encoding, dir) {
  // Empty buffer means no match
  if (buffer.length === 0) return -1

  // Normalize byteOffset
  if (typeof byteOffset === 'string') {
    encoding = byteOffset
    byteOffset = 0
  } else if (byteOffset > 0x7fffffff) {
    byteOffset = 0x7fffffff
  } else if (byteOffset < -0x80000000) {
    byteOffset = -0x80000000
  }
  byteOffset = +byteOffset  // Coerce to Number.
  if (isNaN(byteOffset)) {
    // byteOffset: it it's undefined, null, NaN, "foo", etc, search whole buffer
    byteOffset = dir ? 0 : (buffer.length - 1)
  }

  // Normalize byteOffset: negative offsets start from the end of the buffer
  if (byteOffset < 0) byteOffset = buffer.length + byteOffset
  if (byteOffset >= buffer.length) {
    if (dir) return -1
    else byteOffset = buffer.length - 1
  } else if (byteOffset < 0) {
    if (dir) byteOffset = 0
    else return -1
  }

  // Normalize val
  if (typeof val === 'string') {
    val = Buffer.from(val, encoding)
  }

  // Finally, search either indexOf (if dir is true) or lastIndexOf
  if (Buffer.isBuffer(val)) {
    // Special case: looking for empty string/buffer always fails
    if (val.length === 0) {
      return -1
    }
    return arrayIndexOf(buffer, val, byteOffset, encoding, dir)
  } else if (typeof val === 'number') {
    val = val & 0xFF // Search for a byte value [0-255]
    if (Buffer.TYPED_ARRAY_SUPPORT &&
        typeof Uint8Array.prototype.indexOf === 'function') {
      if (dir) {
        return Uint8Array.prototype.indexOf.call(buffer, val, byteOffset)
      } else {
        return Uint8Array.prototype.lastIndexOf.call(buffer, val, byteOffset)
      }
    }
    return arrayIndexOf(buffer, [ val ], byteOffset, encoding, dir)
  }

  throw new TypeError('val must be string, number or Buffer')
}

function arrayIndexOf (arr, val, byteOffset, encoding, dir) {
  var indexSize = 1
  var arrLength = arr.length
  var valLength = val.length

  if (encoding !== undefined) {
    encoding = String(encoding).toLowerCase()
    if (encoding === 'ucs2' || encoding === 'ucs-2' ||
        encoding === 'utf16le' || encoding === 'utf-16le') {
      if (arr.length < 2 || val.length < 2) {
        return -1
      }
      indexSize = 2
      arrLength /= 2
      valLength /= 2
      byteOffset /= 2
    }
  }

  function read (buf, i) {
    if (indexSize === 1) {
      return buf[i]
    } else {
      return buf.readUInt16BE(i * indexSize)
    }
  }

  var i
  if (dir) {
    var foundIndex = -1
    for (i = byteOffset; i < arrLength; i++) {
      if (read(arr, i) === read(val, foundIndex === -1 ? 0 : i - foundIndex)) {
        if (foundIndex === -1) foundIndex = i
        if (i - foundIndex + 1 === valLength) return foundIndex * indexSize
      } else {
        if (foundIndex !== -1) i -= i - foundIndex
        foundIndex = -1
      }
    }
  } else {
    if (byteOffset + valLength > arrLength) byteOffset = arrLength - valLength
    for (i = byteOffset; i >= 0; i--) {
      var found = true
      for (var j = 0; j < valLength; j++) {
        if (read(arr, i + j) !== read(val, j)) {
          found = false
          break
        }
      }
      if (found) return i
    }
  }

  return -1
}

Buffer.prototype.includes = function includes (val, byteOffset, encoding) {
  return this.indexOf(val, byteOffset, encoding) !== -1
}

Buffer.prototype.indexOf = function indexOf (val, byteOffset, encoding) {
  return bidirectionalIndexOf(this, val, byteOffset, encoding, true)
}

Buffer.prototype.lastIndexOf = function lastIndexOf (val, byteOffset, encoding) {
  return bidirectionalIndexOf(this, val, byteOffset, encoding, false)
}

function hexWrite (buf, string, offset, length) {
  offset = Number(offset) || 0
  var remaining = buf.length - offset
  if (!length) {
    length = remaining
  } else {
    length = Number(length)
    if (length > remaining) {
      length = remaining
    }
  }

  // must be an even number of digits
  var strLen = string.length
  if (strLen % 2 !== 0) throw new TypeError('Invalid hex string')

  if (length > strLen / 2) {
    length = strLen / 2
  }
  for (var i = 0; i < length; ++i) {
    var parsed = parseInt(string.substr(i * 2, 2), 16)
    if (isNaN(parsed)) return i
    buf[offset + i] = parsed
  }
  return i
}

function utf8Write (buf, string, offset, length) {
  return blitBuffer(utf8ToBytes(string, buf.length - offset), buf, offset, length)
}

function asciiWrite (buf, string, offset, length) {
  return blitBuffer(asciiToBytes(string), buf, offset, length)
}

function latin1Write (buf, string, offset, length) {
  return asciiWrite(buf, string, offset, length)
}

function base64Write (buf, string, offset, length) {
  return blitBuffer(base64ToBytes(string), buf, offset, length)
}

function ucs2Write (buf, string, offset, length) {
  return blitBuffer(utf16leToBytes(string, buf.length - offset), buf, offset, length)
}

Buffer.prototype.write = function write (string, offset, length, encoding) {
  // Buffer#write(string)
  if (offset === undefined) {
    encoding = 'utf8'
    length = this.length
    offset = 0
  // Buffer#write(string, encoding)
  } else if (length === undefined && typeof offset === 'string') {
    encoding = offset
    length = this.length
    offset = 0
  // Buffer#write(string, offset[, length][, encoding])
  } else if (isFinite(offset)) {
    offset = offset | 0
    if (isFinite(length)) {
      length = length | 0
      if (encoding === undefined) encoding = 'utf8'
    } else {
      encoding = length
      length = undefined
    }
  // legacy write(string, encoding, offset, length) - remove in v0.13
  } else {
    throw new Error(
      'Buffer.write(string, encoding, offset[, length]) is no longer supported'
    )
  }

  var remaining = this.length - offset
  if (length === undefined || length > remaining) length = remaining

  if ((string.length > 0 && (length < 0 || offset < 0)) || offset > this.length) {
    throw new RangeError('Attempt to write outside buffer bounds')
  }

  if (!encoding) encoding = 'utf8'

  var loweredCase = false
  for (;;) {
    switch (encoding) {
      case 'hex':
        return hexWrite(this, string, offset, length)

      case 'utf8':
      case 'utf-8':
        return utf8Write(this, string, offset, length)

      case 'ascii':
        return asciiWrite(this, string, offset, length)

      case 'latin1':
      case 'binary':
        return latin1Write(this, string, offset, length)

      case 'base64':
        // Warning: maxLength not taken into account in base64Write
        return base64Write(this, string, offset, length)

      case 'ucs2':
      case 'ucs-2':
      case 'utf16le':
      case 'utf-16le':
        return ucs2Write(this, string, offset, length)

      default:
        if (loweredCase) throw new TypeError('Unknown encoding: ' + encoding)
        encoding = ('' + encoding).toLowerCase()
        loweredCase = true
    }
  }
}

Buffer.prototype.toJSON = function toJSON () {
  return {
    type: 'Buffer',
    data: Array.prototype.slice.call(this._arr || this, 0)
  }
}

function base64Slice (buf, start, end) {
  if (start === 0 && end === buf.length) {
    return base64.fromByteArray(buf)
  } else {
    return base64.fromByteArray(buf.slice(start, end))
  }
}

function utf8Slice (buf, start, end) {
  end = Math.min(buf.length, end)
  var res = []

  var i = start
  while (i < end) {
    var firstByte = buf[i]
    var codePoint = null
    var bytesPerSequence = (firstByte > 0xEF) ? 4
      : (firstByte > 0xDF) ? 3
      : (firstByte > 0xBF) ? 2
      : 1

    if (i + bytesPerSequence <= end) {
      var secondByte, thirdByte, fourthByte, tempCodePoint

      switch (bytesPerSequence) {
        case 1:
          if (firstByte < 0x80) {
            codePoint = firstByte
          }
          break
        case 2:
          secondByte = buf[i + 1]
          if ((secondByte & 0xC0) === 0x80) {
            tempCodePoint = (firstByte & 0x1F) << 0x6 | (secondByte & 0x3F)
            if (tempCodePoint > 0x7F) {
              codePoint = tempCodePoint
            }
          }
          break
        case 3:
          secondByte = buf[i + 1]
          thirdByte = buf[i + 2]
          if ((secondByte & 0xC0) === 0x80 && (thirdByte & 0xC0) === 0x80) {
            tempCodePoint = (firstByte & 0xF) << 0xC | (secondByte & 0x3F) << 0x6 | (thirdByte & 0x3F)
            if (tempCodePoint > 0x7FF && (tempCodePoint < 0xD800 || tempCodePoint > 0xDFFF)) {
              codePoint = tempCodePoint
            }
          }
          break
        case 4:
          secondByte = buf[i + 1]
          thirdByte = buf[i + 2]
          fourthByte = buf[i + 3]
          if ((secondByte & 0xC0) === 0x80 && (thirdByte & 0xC0) === 0x80 && (fourthByte & 0xC0) === 0x80) {
            tempCodePoint = (firstByte & 0xF) << 0x12 | (secondByte & 0x3F) << 0xC | (thirdByte & 0x3F) << 0x6 | (fourthByte & 0x3F)
            if (tempCodePoint > 0xFFFF && tempCodePoint < 0x110000) {
              codePoint = tempCodePoint
            }
          }
      }
    }

    if (codePoint === null) {
      // we did not generate a valid codePoint so insert a
      // replacement char (U+FFFD) and advance only 1 byte
      codePoint = 0xFFFD
      bytesPerSequence = 1
    } else if (codePoint > 0xFFFF) {
      // encode to utf16 (surrogate pair dance)
      codePoint -= 0x10000
      res.push(codePoint >>> 10 & 0x3FF | 0xD800)
      codePoint = 0xDC00 | codePoint & 0x3FF
    }

    res.push(codePoint)
    i += bytesPerSequence
  }

  return decodeCodePointsArray(res)
}

// Based on http://stackoverflow.com/a/22747272/680742, the browser with
// the lowest limit is Chrome, with 0x10000 args.
// We go 1 magnitude less, for safety
var MAX_ARGUMENTS_LENGTH = 0x1000

function decodeCodePointsArray (codePoints) {
  var len = codePoints.length
  if (len <= MAX_ARGUMENTS_LENGTH) {
    return String.fromCharCode.apply(String, codePoints) // avoid extra slice()
  }

  // Decode in chunks to avoid "call stack size exceeded".
  var res = ''
  var i = 0
  while (i < len) {
    res += String.fromCharCode.apply(
      String,
      codePoints.slice(i, i += MAX_ARGUMENTS_LENGTH)
    )
  }
  return res
}

function asciiSlice (buf, start, end) {
  var ret = ''
  end = Math.min(buf.length, end)

  for (var i = start; i < end; ++i) {
    ret += String.fromCharCode(buf[i] & 0x7F)
  }
  return ret
}

function latin1Slice (buf, start, end) {
  var ret = ''
  end = Math.min(buf.length, end)

  for (var i = start; i < end; ++i) {
    ret += String.fromCharCode(buf[i])
  }
  return ret
}

function hexSlice (buf, start, end) {
  var len = buf.length

  if (!start || start < 0) start = 0
  if (!end || end < 0 || end > len) end = len

  var out = ''
  for (var i = start; i < end; ++i) {
    out += toHex(buf[i])
  }
  return out
}

function utf16leSlice (buf, start, end) {
  var bytes = buf.slice(start, end)
  var res = ''
  for (var i = 0; i < bytes.length; i += 2) {
    res += String.fromCharCode(bytes[i] + bytes[i + 1] * 256)
  }
  return res
}

Buffer.prototype.slice = function slice (start, end) {
  var len = this.length
  start = ~~start
  end = end === undefined ? len : ~~end

  if (start < 0) {
    start += len
    if (start < 0) start = 0
  } else if (start > len) {
    start = len
  }

  if (end < 0) {
    end += len
    if (end < 0) end = 0
  } else if (end > len) {
    end = len
  }

  if (end < start) end = start

  var newBuf
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    newBuf = this.subarray(start, end)
    newBuf.__proto__ = Buffer.prototype
  } else {
    var sliceLen = end - start
    newBuf = new Buffer(sliceLen, undefined)
    for (var i = 0; i < sliceLen; ++i) {
      newBuf[i] = this[i + start]
    }
  }

  return newBuf
}

/*
 * Need to make sure that buffer isn't trying to write out of bounds.
 */
function checkOffset (offset, ext, length) {
  if ((offset % 1) !== 0 || offset < 0) throw new RangeError('offset is not uint')
  if (offset + ext > length) throw new RangeError('Trying to access beyond buffer length')
}

Buffer.prototype.readUIntLE = function readUIntLE (offset, byteLength, noAssert) {
  offset = offset | 0
  byteLength = byteLength | 0
  if (!noAssert) checkOffset(offset, byteLength, this.length)

  var val = this[offset]
  var mul = 1
  var i = 0
  while (++i < byteLength && (mul *= 0x100)) {
    val += this[offset + i] * mul
  }

  return val
}

Buffer.prototype.readUIntBE = function readUIntBE (offset, byteLength, noAssert) {
  offset = offset | 0
  byteLength = byteLength | 0
  if (!noAssert) {
    checkOffset(offset, byteLength, this.length)
  }

  var val = this[offset + --byteLength]
  var mul = 1
  while (byteLength > 0 && (mul *= 0x100)) {
    val += this[offset + --byteLength] * mul
  }

  return val
}

Buffer.prototype.readUInt8 = function readUInt8 (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 1, this.length)
  return this[offset]
}

Buffer.prototype.readUInt16LE = function readUInt16LE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 2, this.length)
  return this[offset] | (this[offset + 1] << 8)
}

Buffer.prototype.readUInt16BE = function readUInt16BE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 2, this.length)
  return (this[offset] << 8) | this[offset + 1]
}

Buffer.prototype.readUInt32LE = function readUInt32LE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 4, this.length)

  return ((this[offset]) |
      (this[offset + 1] << 8) |
      (this[offset + 2] << 16)) +
      (this[offset + 3] * 0x1000000)
}

Buffer.prototype.readUInt32BE = function readUInt32BE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 4, this.length)

  return (this[offset] * 0x1000000) +
    ((this[offset + 1] << 16) |
    (this[offset + 2] << 8) |
    this[offset + 3])
}

Buffer.prototype.readIntLE = function readIntLE (offset, byteLength, noAssert) {
  offset = offset | 0
  byteLength = byteLength | 0
  if (!noAssert) checkOffset(offset, byteLength, this.length)

  var val = this[offset]
  var mul = 1
  var i = 0
  while (++i < byteLength && (mul *= 0x100)) {
    val += this[offset + i] * mul
  }
  mul *= 0x80

  if (val >= mul) val -= Math.pow(2, 8 * byteLength)

  return val
}

Buffer.prototype.readIntBE = function readIntBE (offset, byteLength, noAssert) {
  offset = offset | 0
  byteLength = byteLength | 0
  if (!noAssert) checkOffset(offset, byteLength, this.length)

  var i = byteLength
  var mul = 1
  var val = this[offset + --i]
  while (i > 0 && (mul *= 0x100)) {
    val += this[offset + --i] * mul
  }
  mul *= 0x80

  if (val >= mul) val -= Math.pow(2, 8 * byteLength)

  return val
}

Buffer.prototype.readInt8 = function readInt8 (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 1, this.length)
  if (!(this[offset] & 0x80)) return (this[offset])
  return ((0xff - this[offset] + 1) * -1)
}

Buffer.prototype.readInt16LE = function readInt16LE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 2, this.length)
  var val = this[offset] | (this[offset + 1] << 8)
  return (val & 0x8000) ? val | 0xFFFF0000 : val
}

Buffer.prototype.readInt16BE = function readInt16BE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 2, this.length)
  var val = this[offset + 1] | (this[offset] << 8)
  return (val & 0x8000) ? val | 0xFFFF0000 : val
}

Buffer.prototype.readInt32LE = function readInt32LE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 4, this.length)

  return (this[offset]) |
    (this[offset + 1] << 8) |
    (this[offset + 2] << 16) |
    (this[offset + 3] << 24)
}

Buffer.prototype.readInt32BE = function readInt32BE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 4, this.length)

  return (this[offset] << 24) |
    (this[offset + 1] << 16) |
    (this[offset + 2] << 8) |
    (this[offset + 3])
}

Buffer.prototype.readFloatLE = function readFloatLE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 4, this.length)
  return ieee754.read(this, offset, true, 23, 4)
}

Buffer.prototype.readFloatBE = function readFloatBE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 4, this.length)
  return ieee754.read(this, offset, false, 23, 4)
}

Buffer.prototype.readDoubleLE = function readDoubleLE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 8, this.length)
  return ieee754.read(this, offset, true, 52, 8)
}

Buffer.prototype.readDoubleBE = function readDoubleBE (offset, noAssert) {
  if (!noAssert) checkOffset(offset, 8, this.length)
  return ieee754.read(this, offset, false, 52, 8)
}

function checkInt (buf, value, offset, ext, max, min) {
  if (!Buffer.isBuffer(buf)) throw new TypeError('"buffer" argument must be a Buffer instance')
  if (value > max || value < min) throw new RangeError('"value" argument is out of bounds')
  if (offset + ext > buf.length) throw new RangeError('Index out of range')
}

Buffer.prototype.writeUIntLE = function writeUIntLE (value, offset, byteLength, noAssert) {
  value = +value
  offset = offset | 0
  byteLength = byteLength | 0
  if (!noAssert) {
    var maxBytes = Math.pow(2, 8 * byteLength) - 1
    checkInt(this, value, offset, byteLength, maxBytes, 0)
  }

  var mul = 1
  var i = 0
  this[offset] = value & 0xFF
  while (++i < byteLength && (mul *= 0x100)) {
    this[offset + i] = (value / mul) & 0xFF
  }

  return offset + byteLength
}

Buffer.prototype.writeUIntBE = function writeUIntBE (value, offset, byteLength, noAssert) {
  value = +value
  offset = offset | 0
  byteLength = byteLength | 0
  if (!noAssert) {
    var maxBytes = Math.pow(2, 8 * byteLength) - 1
    checkInt(this, value, offset, byteLength, maxBytes, 0)
  }

  var i = byteLength - 1
  var mul = 1
  this[offset + i] = value & 0xFF
  while (--i >= 0 && (mul *= 0x100)) {
    this[offset + i] = (value / mul) & 0xFF
  }

  return offset + byteLength
}

Buffer.prototype.writeUInt8 = function writeUInt8 (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 1, 0xff, 0)
  if (!Buffer.TYPED_ARRAY_SUPPORT) value = Math.floor(value)
  this[offset] = (value & 0xff)
  return offset + 1
}

function objectWriteUInt16 (buf, value, offset, littleEndian) {
  if (value < 0) value = 0xffff + value + 1
  for (var i = 0, j = Math.min(buf.length - offset, 2); i < j; ++i) {
    buf[offset + i] = (value & (0xff << (8 * (littleEndian ? i : 1 - i)))) >>>
      (littleEndian ? i : 1 - i) * 8
  }
}

Buffer.prototype.writeUInt16LE = function writeUInt16LE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 2, 0xffff, 0)
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset] = (value & 0xff)
    this[offset + 1] = (value >>> 8)
  } else {
    objectWriteUInt16(this, value, offset, true)
  }
  return offset + 2
}

Buffer.prototype.writeUInt16BE = function writeUInt16BE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 2, 0xffff, 0)
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset] = (value >>> 8)
    this[offset + 1] = (value & 0xff)
  } else {
    objectWriteUInt16(this, value, offset, false)
  }
  return offset + 2
}

function objectWriteUInt32 (buf, value, offset, littleEndian) {
  if (value < 0) value = 0xffffffff + value + 1
  for (var i = 0, j = Math.min(buf.length - offset, 4); i < j; ++i) {
    buf[offset + i] = (value >>> (littleEndian ? i : 3 - i) * 8) & 0xff
  }
}

Buffer.prototype.writeUInt32LE = function writeUInt32LE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 4, 0xffffffff, 0)
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset + 3] = (value >>> 24)
    this[offset + 2] = (value >>> 16)
    this[offset + 1] = (value >>> 8)
    this[offset] = (value & 0xff)
  } else {
    objectWriteUInt32(this, value, offset, true)
  }
  return offset + 4
}

Buffer.prototype.writeUInt32BE = function writeUInt32BE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 4, 0xffffffff, 0)
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset] = (value >>> 24)
    this[offset + 1] = (value >>> 16)
    this[offset + 2] = (value >>> 8)
    this[offset + 3] = (value & 0xff)
  } else {
    objectWriteUInt32(this, value, offset, false)
  }
  return offset + 4
}

Buffer.prototype.writeIntLE = function writeIntLE (value, offset, byteLength, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) {
    var limit = Math.pow(2, 8 * byteLength - 1)

    checkInt(this, value, offset, byteLength, limit - 1, -limit)
  }

  var i = 0
  var mul = 1
  var sub = 0
  this[offset] = value & 0xFF
  while (++i < byteLength && (mul *= 0x100)) {
    if (value < 0 && sub === 0 && this[offset + i - 1] !== 0) {
      sub = 1
    }
    this[offset + i] = ((value / mul) >> 0) - sub & 0xFF
  }

  return offset + byteLength
}

Buffer.prototype.writeIntBE = function writeIntBE (value, offset, byteLength, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) {
    var limit = Math.pow(2, 8 * byteLength - 1)

    checkInt(this, value, offset, byteLength, limit - 1, -limit)
  }

  var i = byteLength - 1
  var mul = 1
  var sub = 0
  this[offset + i] = value & 0xFF
  while (--i >= 0 && (mul *= 0x100)) {
    if (value < 0 && sub === 0 && this[offset + i + 1] !== 0) {
      sub = 1
    }
    this[offset + i] = ((value / mul) >> 0) - sub & 0xFF
  }

  return offset + byteLength
}

Buffer.prototype.writeInt8 = function writeInt8 (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 1, 0x7f, -0x80)
  if (!Buffer.TYPED_ARRAY_SUPPORT) value = Math.floor(value)
  if (value < 0) value = 0xff + value + 1
  this[offset] = (value & 0xff)
  return offset + 1
}

Buffer.prototype.writeInt16LE = function writeInt16LE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 2, 0x7fff, -0x8000)
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset] = (value & 0xff)
    this[offset + 1] = (value >>> 8)
  } else {
    objectWriteUInt16(this, value, offset, true)
  }
  return offset + 2
}

Buffer.prototype.writeInt16BE = function writeInt16BE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 2, 0x7fff, -0x8000)
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset] = (value >>> 8)
    this[offset + 1] = (value & 0xff)
  } else {
    objectWriteUInt16(this, value, offset, false)
  }
  return offset + 2
}

Buffer.prototype.writeInt32LE = function writeInt32LE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 4, 0x7fffffff, -0x80000000)
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset] = (value & 0xff)
    this[offset + 1] = (value >>> 8)
    this[offset + 2] = (value >>> 16)
    this[offset + 3] = (value >>> 24)
  } else {
    objectWriteUInt32(this, value, offset, true)
  }
  return offset + 4
}

Buffer.prototype.writeInt32BE = function writeInt32BE (value, offset, noAssert) {
  value = +value
  offset = offset | 0
  if (!noAssert) checkInt(this, value, offset, 4, 0x7fffffff, -0x80000000)
  if (value < 0) value = 0xffffffff + value + 1
  if (Buffer.TYPED_ARRAY_SUPPORT) {
    this[offset] = (value >>> 24)
    this[offset + 1] = (value >>> 16)
    this[offset + 2] = (value >>> 8)
    this[offset + 3] = (value & 0xff)
  } else {
    objectWriteUInt32(this, value, offset, false)
  }
  return offset + 4
}

function checkIEEE754 (buf, value, offset, ext, max, min) {
  if (offset + ext > buf.length) throw new RangeError('Index out of range')
  if (offset < 0) throw new RangeError('Index out of range')
}

function writeFloat (buf, value, offset, littleEndian, noAssert) {
  if (!noAssert) {
    checkIEEE754(buf, value, offset, 4, 3.4028234663852886e+38, -3.4028234663852886e+38)
  }
  ieee754.write(buf, value, offset, littleEndian, 23, 4)
  return offset + 4
}

Buffer.prototype.writeFloatLE = function writeFloatLE (value, offset, noAssert) {
  return writeFloat(this, value, offset, true, noAssert)
}

Buffer.prototype.writeFloatBE = function writeFloatBE (value, offset, noAssert) {
  return writeFloat(this, value, offset, false, noAssert)
}

function writeDouble (buf, value, offset, littleEndian, noAssert) {
  if (!noAssert) {
    checkIEEE754(buf, value, offset, 8, 1.7976931348623157E+308, -1.7976931348623157E+308)
  }
  ieee754.write(buf, value, offset, littleEndian, 52, 8)
  return offset + 8
}

Buffer.prototype.writeDoubleLE = function writeDoubleLE (value, offset, noAssert) {
  return writeDouble(this, value, offset, true, noAssert)
}

Buffer.prototype.writeDoubleBE = function writeDoubleBE (value, offset, noAssert) {
  return writeDouble(this, value, offset, false, noAssert)
}

// copy(targetBuffer, targetStart=0, sourceStart=0, sourceEnd=buffer.length)
Buffer.prototype.copy = function copy (target, targetStart, start, end) {
  if (!start) start = 0
  if (!end && end !== 0) end = this.length
  if (targetStart >= target.length) targetStart = target.length
  if (!targetStart) targetStart = 0
  if (end > 0 && end < start) end = start

  // Copy 0 bytes; we're done
  if (end === start) return 0
  if (target.length === 0 || this.length === 0) return 0

  // Fatal error conditions
  if (targetStart < 0) {
    throw new RangeError('targetStart out of bounds')
  }
  if (start < 0 || start >= this.length) throw new RangeError('sourceStart out of bounds')
  if (end < 0) throw new RangeError('sourceEnd out of bounds')

  // Are we oob?
  if (end > this.length) end = this.length
  if (target.length - targetStart < end - start) {
    end = target.length - targetStart + start
  }

  var len = end - start
  var i

  if (this === target && start < targetStart && targetStart < end) {
    // descending copy from end
    for (i = len - 1; i >= 0; --i) {
      target[i + targetStart] = this[i + start]
    }
  } else if (len < 1000 || !Buffer.TYPED_ARRAY_SUPPORT) {
    // ascending copy from start
    for (i = 0; i < len; ++i) {
      target[i + targetStart] = this[i + start]
    }
  } else {
    Uint8Array.prototype.set.call(
      target,
      this.subarray(start, start + len),
      targetStart
    )
  }

  return len
}

// Usage:
//    buffer.fill(number[, offset[, end]])
//    buffer.fill(buffer[, offset[, end]])
//    buffer.fill(string[, offset[, end]][, encoding])
Buffer.prototype.fill = function fill (val, start, end, encoding) {
  // Handle string cases:
  if (typeof val === 'string') {
    if (typeof start === 'string') {
      encoding = start
      start = 0
      end = this.length
    } else if (typeof end === 'string') {
      encoding = end
      end = this.length
    }
    if (val.length === 1) {
      var code = val.charCodeAt(0)
      if (code < 256) {
        val = code
      }
    }
    if (encoding !== undefined && typeof encoding !== 'string') {
      throw new TypeError('encoding must be a string')
    }
    if (typeof encoding === 'string' && !Buffer.isEncoding(encoding)) {
      throw new TypeError('Unknown encoding: ' + encoding)
    }
  } else if (typeof val === 'number') {
    val = val & 255
  }

  // Invalid ranges are not set to a default, so can range check early.
  if (start < 0 || this.length < start || this.length < end) {
    throw new RangeError('Out of range index')
  }

  if (end <= start) {
    return this
  }

  start = start >>> 0
  end = end === undefined ? this.length : end >>> 0

  if (!val) val = 0

  var i
  if (typeof val === 'number') {
    for (i = start; i < end; ++i) {
      this[i] = val
    }
  } else {
    var bytes = Buffer.isBuffer(val)
      ? val
      : utf8ToBytes(new Buffer(val, encoding).toString())
    var len = bytes.length
    for (i = 0; i < end - start; ++i) {
      this[i + start] = bytes[i % len]
    }
  }

  return this
}

// HELPER FUNCTIONS
// ================

var INVALID_BASE64_RE = /[^+\/0-9A-Za-z-_]/g

function base64clean (str) {
  // Node strips out invalid characters like \n and \t from the string, base64-js does not
  str = stringtrim(str).replace(INVALID_BASE64_RE, '')
  // Node converts strings with length < 2 to ''
  if (str.length < 2) return ''
  // Node allows for non-padded base64 strings (missing trailing ===), base64-js does not
  while (str.length % 4 !== 0) {
    str = str + '='
  }
  return str
}

function stringtrim (str) {
  if (str.trim) return str.trim()
  return str.replace(/^\s+|\s+$/g, '')
}

function toHex (n) {
  if (n < 16) return '0' + n.toString(16)
  return n.toString(16)
}

function utf8ToBytes (string, units) {
  units = units || Infinity
  var codePoint
  var length = string.length
  var leadSurrogate = null
  var bytes = []

  for (var i = 0; i < length; ++i) {
    codePoint = string.charCodeAt(i)

    // is surrogate component
    if (codePoint > 0xD7FF && codePoint < 0xE000) {
      // last char was a lead
      if (!leadSurrogate) {
        // no lead yet
        if (codePoint > 0xDBFF) {
          // unexpected trail
          if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD)
          continue
        } else if (i + 1 === length) {
          // unpaired lead
          if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD)
          continue
        }

        // valid lead
        leadSurrogate = codePoint

        continue
      }

      // 2 leads in a row
      if (codePoint < 0xDC00) {
        if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD)
        leadSurrogate = codePoint
        continue
      }

      // valid surrogate pair
      codePoint = (leadSurrogate - 0xD800 << 10 | codePoint - 0xDC00) + 0x10000
    } else if (leadSurrogate) {
      // valid bmp char, but last char was a lead
      if ((units -= 3) > -1) bytes.push(0xEF, 0xBF, 0xBD)
    }

    leadSurrogate = null

    // encode utf8
    if (codePoint < 0x80) {
      if ((units -= 1) < 0) break
      bytes.push(codePoint)
    } else if (codePoint < 0x800) {
      if ((units -= 2) < 0) break
      bytes.push(
        codePoint >> 0x6 | 0xC0,
        codePoint & 0x3F | 0x80
      )
    } else if (codePoint < 0x10000) {
      if ((units -= 3) < 0) break
      bytes.push(
        codePoint >> 0xC | 0xE0,
        codePoint >> 0x6 & 0x3F | 0x80,
        codePoint & 0x3F | 0x80
      )
    } else if (codePoint < 0x110000) {
      if ((units -= 4) < 0) break
      bytes.push(
        codePoint >> 0x12 | 0xF0,
        codePoint >> 0xC & 0x3F | 0x80,
        codePoint >> 0x6 & 0x3F | 0x80,
        codePoint & 0x3F | 0x80
      )
    } else {
      throw new Error('Invalid code point')
    }
  }

  return bytes
}

function asciiToBytes (str) {
  var byteArray = []
  for (var i = 0; i < str.length; ++i) {
    // Node's code seems to be doing this and not & 0x7F..
    byteArray.push(str.charCodeAt(i) & 0xFF)
  }
  return byteArray
}

function utf16leToBytes (str, units) {
  var c, hi, lo
  var byteArray = []
  for (var i = 0; i < str.length; ++i) {
    if ((units -= 2) < 0) break

    c = str.charCodeAt(i)
    hi = c >> 8
    lo = c % 256
    byteArray.push(lo)
    byteArray.push(hi)
  }

  return byteArray
}

function base64ToBytes (str) {
  return base64.toByteArray(base64clean(str))
}

function blitBuffer (src, dst, offset, length) {
  for (var i = 0; i < length; ++i) {
    if ((i + offset >= dst.length) || (i >= src.length)) break
    dst[i + offset] = src[i]
  }
  return i
}

function isnan (val) {
  return val !== val // eslint-disable-line no-self-compare
}

}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})
},{"base64-js":1,"ieee754":3,"isarray":4}],3:[function(require,module,exports){
exports.read = function (buffer, offset, isLE, mLen, nBytes) {
  var e, m
  var eLen = nBytes * 8 - mLen - 1
  var eMax = (1 << eLen) - 1
  var eBias = eMax >> 1
  var nBits = -7
  var i = isLE ? (nBytes - 1) : 0
  var d = isLE ? -1 : 1
  var s = buffer[offset + i]

  i += d

  e = s & ((1 << (-nBits)) - 1)
  s >>= (-nBits)
  nBits += eLen
  for (; nBits > 0; e = e * 256 + buffer[offset + i], i += d, nBits -= 8) {}

  m = e & ((1 << (-nBits)) - 1)
  e >>= (-nBits)
  nBits += mLen
  for (; nBits > 0; m = m * 256 + buffer[offset + i], i += d, nBits -= 8) {}

  if (e === 0) {
    e = 1 - eBias
  } else if (e === eMax) {
    return m ? NaN : ((s ? -1 : 1) * Infinity)
  } else {
    m = m + Math.pow(2, mLen)
    e = e - eBias
  }
  return (s ? -1 : 1) * m * Math.pow(2, e - mLen)
}

exports.write = function (buffer, value, offset, isLE, mLen, nBytes) {
  var e, m, c
  var eLen = nBytes * 8 - mLen - 1
  var eMax = (1 << eLen) - 1
  var eBias = eMax >> 1
  var rt = (mLen === 23 ? Math.pow(2, -24) - Math.pow(2, -77) : 0)
  var i = isLE ? 0 : (nBytes - 1)
  var d = isLE ? 1 : -1
  var s = value < 0 || (value === 0 && 1 / value < 0) ? 1 : 0

  value = Math.abs(value)

  if (isNaN(value) || value === Infinity) {
    m = isNaN(value) ? 1 : 0
    e = eMax
  } else {
    e = Math.floor(Math.log(value) / Math.LN2)
    if (value * (c = Math.pow(2, -e)) < 1) {
      e--
      c *= 2
    }
    if (e + eBias >= 1) {
      value += rt / c
    } else {
      value += rt * Math.pow(2, 1 - eBias)
    }
    if (value * c >= 2) {
      e++
      c /= 2
    }

    if (e + eBias >= eMax) {
      m = 0
      e = eMax
    } else if (e + eBias >= 1) {
      m = (value * c - 1) * Math.pow(2, mLen)
      e = e + eBias
    } else {
      m = value * Math.pow(2, eBias - 1) * Math.pow(2, mLen)
      e = 0
    }
  }

  for (; mLen >= 8; buffer[offset + i] = m & 0xff, i += d, m /= 256, mLen -= 8) {}

  e = (e << mLen) | m
  eLen += mLen
  for (; eLen > 0; buffer[offset + i] = e & 0xff, i += d, e /= 256, eLen -= 8) {}

  buffer[offset + i - d] |= s * 128
}

},{}],4:[function(require,module,exports){
var toString = {}.toString;

module.exports = Array.isArray || function (arr) {
  return toString.call(arr) == '[object Array]';
};

},{}],5:[function(require,module,exports){

module.exports = {
    BigNumber: require('bignumber.js'),
    buffer: require('buffer'),
    // both base64 and ieee754 are dependencies of buffer,
    // but it's good to expose them as first-class vendored
    // libraries so they are usable all through batavia
    // as first-class vendored libs
    base64: require('base64-js'),
    ieee754: require('ieee754'),
}


},{"base64-js":6,"bignumber.js":7,"buffer":2,"ieee754":8}],6:[function(require,module,exports){
arguments[4][1][0].apply(exports,arguments)
},{"dup":1}],7:[function(require,module,exports){
/*! bignumber.js v2.4.0 https://github.com/MikeMcl/bignumber.js/LICENCE */

;(function (globalObj) {
    'use strict';

    /*
      bignumber.js v2.4.0
      A JavaScript library for arbitrary-precision arithmetic.
      https://github.com/MikeMcl/bignumber.js
      Copyright (c) 2016 Michael Mclaughlin <M8ch88l@gmail.com>
      MIT Expat Licence
    */


    var BigNumber, cryptoObj, parseNumeric,
        isNumeric = /^-?(\d+(\.\d*)?|\.\d+)(e[+-]?\d+)?$/i,
        mathceil = Math.ceil,
        mathfloor = Math.floor,
        notBool = ' not a boolean or binary digit',
        roundingMode = 'rounding mode',
        tooManyDigits = 'number type has more than 15 significant digits',
        ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$_',
        BASE = 1e14,
        LOG_BASE = 14,
        MAX_SAFE_INTEGER = 0x1fffffffffffff,         // 2^53 - 1
        // MAX_INT32 = 0x7fffffff,                   // 2^31 - 1
        POWS_TEN = [1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12, 1e13],
        SQRT_BASE = 1e7,

        /*
         * The limit on the value of DECIMAL_PLACES, TO_EXP_NEG, TO_EXP_POS, MIN_EXP, MAX_EXP, and
         * the arguments to toExponential, toFixed, toFormat, and toPrecision, beyond which an
         * exception is thrown (if ERRORS is true).
         */
        MAX = 1E9;                                   // 0 to MAX_INT32

    if ( typeof crypto != 'undefined' ) cryptoObj = crypto;


    /*
     * Create and return a BigNumber constructor.
     */
    function constructorFactory(configObj) {
        var div,

            // id tracks the caller function, so its name can be included in error messages.
            id = 0,
            P = BigNumber.prototype,
            ONE = new BigNumber(1),


            /********************************* EDITABLE DEFAULTS **********************************/


            /*
             * The default values below must be integers within the inclusive ranges stated.
             * The values can also be changed at run-time using BigNumber.config.
             */

            // The maximum number of decimal places for operations involving division.
            DECIMAL_PLACES = 20,                     // 0 to MAX

            /*
             * The rounding mode used when rounding to the above decimal places, and when using
             * toExponential, toFixed, toFormat and toPrecision, and round (default value).
             * UP         0 Away from zero.
             * DOWN       1 Towards zero.
             * CEIL       2 Towards +Infinity.
             * FLOOR      3 Towards -Infinity.
             * HALF_UP    4 Towards nearest neighbour. If equidistant, up.
             * HALF_DOWN  5 Towards nearest neighbour. If equidistant, down.
             * HALF_EVEN  6 Towards nearest neighbour. If equidistant, towards even neighbour.
             * HALF_CEIL  7 Towards nearest neighbour. If equidistant, towards +Infinity.
             * HALF_FLOOR 8 Towards nearest neighbour. If equidistant, towards -Infinity.
             */
            ROUNDING_MODE = 4,                       // 0 to 8

            // EXPONENTIAL_AT : [TO_EXP_NEG , TO_EXP_POS]

            // The exponent value at and beneath which toString returns exponential notation.
            // Number type: -7
            TO_EXP_NEG = -7,                         // 0 to -MAX

            // The exponent value at and above which toString returns exponential notation.
            // Number type: 21
            TO_EXP_POS = 21,                         // 0 to MAX

            // RANGE : [MIN_EXP, MAX_EXP]

            // The minimum exponent value, beneath which underflow to zero occurs.
            // Number type: -324  (5e-324)
            MIN_EXP = -1e7,                          // -1 to -MAX

            // The maximum exponent value, above which overflow to Infinity occurs.
            // Number type:  308  (1.7976931348623157e+308)
            // For MAX_EXP > 1e7, e.g. new BigNumber('1e100000000').plus(1) may be slow.
            MAX_EXP = 1e7,                           // 1 to MAX

            // Whether BigNumber Errors are ever thrown.
            ERRORS = true,                           // true or false

            // Change to intValidatorNoErrors if ERRORS is false.
            isValidInt = intValidatorWithErrors,     // intValidatorWithErrors/intValidatorNoErrors

            // Whether to use cryptographically-secure random number generation, if available.
            CRYPTO = false,                          // true or false

            /*
             * The modulo mode used when calculating the modulus: a mod n.
             * The quotient (q = a / n) is calculated according to the corresponding rounding mode.
             * The remainder (r) is calculated as: r = a - n * q.
             *
             * UP        0 The remainder is positive if the dividend is negative, else is negative.
             * DOWN      1 The remainder has the same sign as the dividend.
             *             This modulo mode is commonly known as 'truncated division' and is
             *             equivalent to (a % n) in JavaScript.
             * FLOOR     3 The remainder has the same sign as the divisor (Python %).
             * HALF_EVEN 6 This modulo mode implements the IEEE 754 remainder function.
             * EUCLID    9 Euclidian division. q = sign(n) * floor(a / abs(n)).
             *             The remainder is always positive.
             *
             * The truncated division, floored division, Euclidian division and IEEE 754 remainder
             * modes are commonly used for the modulus operation.
             * Although the other rounding modes can also be used, they may not give useful results.
             */
            MODULO_MODE = 1,                         // 0 to 9

            // The maximum number of significant digits of the result of the toPower operation.
            // If POW_PRECISION is 0, there will be unlimited significant digits.
            POW_PRECISION = 100,                     // 0 to MAX

            // The format specification used by the BigNumber.prototype.toFormat method.
            FORMAT = {
                decimalSeparator: '.',
                groupSeparator: ',',
                groupSize: 3,
                secondaryGroupSize: 0,
                fractionGroupSeparator: '\xA0',      // non-breaking space
                fractionGroupSize: 0
            };


        /******************************************************************************************/


        // CONSTRUCTOR


        /*
         * The BigNumber constructor and exported function.
         * Create and return a new instance of a BigNumber object.
         *
         * n {number|string|BigNumber} A numeric value.
         * [b] {number} The base of n. Integer, 2 to 64 inclusive.
         */
        function BigNumber( n, b ) {
            var c, e, i, num, len, str,
                x = this;

            // Enable constructor usage without new.
            if ( !( x instanceof BigNumber ) ) {

                // 'BigNumber() constructor call without new: {n}'
                if (ERRORS) raise( 26, 'constructor call without new', n );
                return new BigNumber( n, b );
            }

            // 'new BigNumber() base not an integer: {b}'
            // 'new BigNumber() base out of range: {b}'
            if ( b == null || !isValidInt( b, 2, 64, id, 'base' ) ) {

                // Duplicate.
                if ( n instanceof BigNumber ) {
                    x.s = n.s;
                    x.e = n.e;
                    x.c = ( n = n.c ) ? n.slice() : n;
                    id = 0;
                    return;
                }

                if ( ( num = typeof n == 'number' ) && n * 0 == 0 ) {
                    x.s = 1 / n < 0 ? ( n = -n, -1 ) : 1;

                    // Fast path for integers.
                    if ( n === ~~n ) {
                        for ( e = 0, i = n; i >= 10; i /= 10, e++ );
                        x.e = e;
                        x.c = [n];
                        id = 0;
                        return;
                    }

                    str = n + '';
                } else {
                    if ( !isNumeric.test( str = n + '' ) ) return parseNumeric( x, str, num );
                    x.s = str.charCodeAt(0) === 45 ? ( str = str.slice(1), -1 ) : 1;
                }
            } else {
                b = b | 0;
                str = n + '';

                // Ensure return value is rounded to DECIMAL_PLACES as with other bases.
                // Allow exponential notation to be used with base 10 argument.
                if ( b == 10 ) {
                    x = new BigNumber( n instanceof BigNumber ? n : str );
                    return round( x, DECIMAL_PLACES + x.e + 1, ROUNDING_MODE );
                }

                // Avoid potential interpretation of Infinity and NaN as base 44+ values.
                // Any number in exponential form will fail due to the [Ee][+-].
                if ( ( num = typeof n == 'number' ) && n * 0 != 0 ||
                  !( new RegExp( '^-?' + ( c = '[' + ALPHABET.slice( 0, b ) + ']+' ) +
                    '(?:\\.' + c + ')?$',b < 37 ? 'i' : '' ) ).test(str) ) {
                    return parseNumeric( x, str, num, b );
                }

                if (num) {
                    x.s = 1 / n < 0 ? ( str = str.slice(1), -1 ) : 1;

                    if ( ERRORS && str.replace( /^0\.0*|\./, '' ).length > 15 ) {

                        // 'new BigNumber() number type has more than 15 significant digits: {n}'
                        raise( id, tooManyDigits, n );
                    }

                    // Prevent later check for length on converted number.
                    num = false;
                } else {
                    x.s = str.charCodeAt(0) === 45 ? ( str = str.slice(1), -1 ) : 1;
                }

                str = convertBase( str, 10, b, x.s );
            }

            // Decimal point?
            if ( ( e = str.indexOf('.') ) > -1 ) str = str.replace( '.', '' );

            // Exponential form?
            if ( ( i = str.search( /e/i ) ) > 0 ) {

                // Determine exponent.
                if ( e < 0 ) e = i;
                e += +str.slice( i + 1 );
                str = str.substring( 0, i );
            } else if ( e < 0 ) {

                // Integer.
                e = str.length;
            }

            // Determine leading zeros.
            for ( i = 0; str.charCodeAt(i) === 48; i++ );

            // Determine trailing zeros.
            for ( len = str.length; str.charCodeAt(--len) === 48; );
            str = str.slice( i, len + 1 );

            if (str) {
                len = str.length;

                // Disallow numbers with over 15 significant digits if number type.
                // 'new BigNumber() number type has more than 15 significant digits: {n}'
                if ( num && ERRORS && len > 15 && ( n > MAX_SAFE_INTEGER || n !== mathfloor(n) ) ) {
                    raise( id, tooManyDigits, x.s * n );
                }

                e = e - i - 1;

                 // Overflow?
                if ( e > MAX_EXP ) {

                    // Infinity.
                    x.c = x.e = null;

                // Underflow?
                } else if ( e < MIN_EXP ) {

                    // Zero.
                    x.c = [ x.e = 0 ];
                } else {
                    x.e = e;
                    x.c = [];

                    // Transform base

                    // e is the base 10 exponent.
                    // i is where to slice str to get the first element of the coefficient array.
                    i = ( e + 1 ) % LOG_BASE;
                    if ( e < 0 ) i += LOG_BASE;

                    if ( i < len ) {
                        if (i) x.c.push( +str.slice( 0, i ) );

                        for ( len -= LOG_BASE; i < len; ) {
                            x.c.push( +str.slice( i, i += LOG_BASE ) );
                        }

                        str = str.slice(i);
                        i = LOG_BASE - str.length;
                    } else {
                        i -= len;
                    }

                    for ( ; i--; str += '0' );
                    x.c.push( +str );
                }
            } else {

                // Zero.
                x.c = [ x.e = 0 ];
            }

            id = 0;
        }


        // CONSTRUCTOR PROPERTIES


        BigNumber.another = constructorFactory;

        BigNumber.ROUND_UP = 0;
        BigNumber.ROUND_DOWN = 1;
        BigNumber.ROUND_CEIL = 2;
        BigNumber.ROUND_FLOOR = 3;
        BigNumber.ROUND_HALF_UP = 4;
        BigNumber.ROUND_HALF_DOWN = 5;
        BigNumber.ROUND_HALF_EVEN = 6;
        BigNumber.ROUND_HALF_CEIL = 7;
        BigNumber.ROUND_HALF_FLOOR = 8;
        BigNumber.EUCLID = 9;


        /*
         * Configure infrequently-changing library-wide settings.
         *
         * Accept an object or an argument list, with one or many of the following properties or
         * parameters respectively:
         *
         *   DECIMAL_PLACES  {number}  Integer, 0 to MAX inclusive
         *   ROUNDING_MODE   {number}  Integer, 0 to 8 inclusive
         *   EXPONENTIAL_AT  {number|number[]}  Integer, -MAX to MAX inclusive or
         *                                      [integer -MAX to 0 incl., 0 to MAX incl.]
         *   RANGE           {number|number[]}  Non-zero integer, -MAX to MAX inclusive or
         *                                      [integer -MAX to -1 incl., integer 1 to MAX incl.]
         *   ERRORS          {boolean|number}   true, false, 1 or 0
         *   CRYPTO          {boolean|number}   true, false, 1 or 0
         *   MODULO_MODE     {number}           0 to 9 inclusive
         *   POW_PRECISION   {number}           0 to MAX inclusive
         *   FORMAT          {object}           See BigNumber.prototype.toFormat
         *      decimalSeparator       {string}
         *      groupSeparator         {string}
         *      groupSize              {number}
         *      secondaryGroupSize     {number}
         *      fractionGroupSeparator {string}
         *      fractionGroupSize      {number}
         *
         * (The values assigned to the above FORMAT object properties are not checked for validity.)
         *
         * E.g.
         * BigNumber.config(20, 4) is equivalent to
         * BigNumber.config({ DECIMAL_PLACES : 20, ROUNDING_MODE : 4 })
         *
         * Ignore properties/parameters set to null or undefined.
         * Return an object with the properties current values.
         */
        BigNumber.config = function () {
            var v, p,
                i = 0,
                r = {},
                a = arguments,
                o = a[0],
                has = o && typeof o == 'object'
                  ? function () { if ( o.hasOwnProperty(p) ) return ( v = o[p] ) != null; }
                  : function () { if ( a.length > i ) return ( v = a[i++] ) != null; };

            // DECIMAL_PLACES {number} Integer, 0 to MAX inclusive.
            // 'config() DECIMAL_PLACES not an integer: {v}'
            // 'config() DECIMAL_PLACES out of range: {v}'
            if ( has( p = 'DECIMAL_PLACES' ) && isValidInt( v, 0, MAX, 2, p ) ) {
                DECIMAL_PLACES = v | 0;
            }
            r[p] = DECIMAL_PLACES;

            // ROUNDING_MODE {number} Integer, 0 to 8 inclusive.
            // 'config() ROUNDING_MODE not an integer: {v}'
            // 'config() ROUNDING_MODE out of range: {v}'
            if ( has( p = 'ROUNDING_MODE' ) && isValidInt( v, 0, 8, 2, p ) ) {
                ROUNDING_MODE = v | 0;
            }
            r[p] = ROUNDING_MODE;

            // EXPONENTIAL_AT {number|number[]}
            // Integer, -MAX to MAX inclusive or [integer -MAX to 0 inclusive, 0 to MAX inclusive].
            // 'config() EXPONENTIAL_AT not an integer: {v}'
            // 'config() EXPONENTIAL_AT out of range: {v}'
            if ( has( p = 'EXPONENTIAL_AT' ) ) {

                if ( isArray(v) ) {
                    if ( isValidInt( v[0], -MAX, 0, 2, p ) && isValidInt( v[1], 0, MAX, 2, p ) ) {
                        TO_EXP_NEG = v[0] | 0;
                        TO_EXP_POS = v[1] | 0;
                    }
                } else if ( isValidInt( v, -MAX, MAX, 2, p ) ) {
                    TO_EXP_NEG = -( TO_EXP_POS = ( v < 0 ? -v : v ) | 0 );
                }
            }
            r[p] = [ TO_EXP_NEG, TO_EXP_POS ];

            // RANGE {number|number[]} Non-zero integer, -MAX to MAX inclusive or
            // [integer -MAX to -1 inclusive, integer 1 to MAX inclusive].
            // 'config() RANGE not an integer: {v}'
            // 'config() RANGE cannot be zero: {v}'
            // 'config() RANGE out of range: {v}'
            if ( has( p = 'RANGE' ) ) {

                if ( isArray(v) ) {
                    if ( isValidInt( v[0], -MAX, -1, 2, p ) && isValidInt( v[1], 1, MAX, 2, p ) ) {
                        MIN_EXP = v[0] | 0;
                        MAX_EXP = v[1] | 0;
                    }
                } else if ( isValidInt( v, -MAX, MAX, 2, p ) ) {
                    if ( v | 0 ) MIN_EXP = -( MAX_EXP = ( v < 0 ? -v : v ) | 0 );
                    else if (ERRORS) raise( 2, p + ' cannot be zero', v );
                }
            }
            r[p] = [ MIN_EXP, MAX_EXP ];

            // ERRORS {boolean|number} true, false, 1 or 0.
            // 'config() ERRORS not a boolean or binary digit: {v}'
            if ( has( p = 'ERRORS' ) ) {

                if ( v === !!v || v === 1 || v === 0 ) {
                    id = 0;
                    isValidInt = ( ERRORS = !!v ) ? intValidatorWithErrors : intValidatorNoErrors;
                } else if (ERRORS) {
                    raise( 2, p + notBool, v );
                }
            }
            r[p] = ERRORS;

            // CRYPTO {boolean|number} true, false, 1 or 0.
            // 'config() CRYPTO not a boolean or binary digit: {v}'
            // 'config() crypto unavailable: {crypto}'
            if ( has( p = 'CRYPTO' ) ) {

                if ( v === !!v || v === 1 || v === 0 ) {
                    CRYPTO = !!( v && cryptoObj );
                    if ( v && !CRYPTO && ERRORS ) raise( 2, 'crypto unavailable', cryptoObj );
                } else if (ERRORS) {
                    raise( 2, p + notBool, v );
                }
            }
            r[p] = CRYPTO;

            // MODULO_MODE {number} Integer, 0 to 9 inclusive.
            // 'config() MODULO_MODE not an integer: {v}'
            // 'config() MODULO_MODE out of range: {v}'
            if ( has( p = 'MODULO_MODE' ) && isValidInt( v, 0, 9, 2, p ) ) {
                MODULO_MODE = v | 0;
            }
            r[p] = MODULO_MODE;

            // POW_PRECISION {number} Integer, 0 to MAX inclusive.
            // 'config() POW_PRECISION not an integer: {v}'
            // 'config() POW_PRECISION out of range: {v}'
            if ( has( p = 'POW_PRECISION' ) && isValidInt( v, 0, MAX, 2, p ) ) {
                POW_PRECISION = v | 0;
            }
            r[p] = POW_PRECISION;

            // FORMAT {object}
            // 'config() FORMAT not an object: {v}'
            if ( has( p = 'FORMAT' ) ) {

                if ( typeof v == 'object' ) {
                    FORMAT = v;
                } else if (ERRORS) {
                    raise( 2, p + ' not an object', v );
                }
            }
            r[p] = FORMAT;

            return r;
        };


        /*
         * Return a new BigNumber whose value is the maximum of the arguments.
         *
         * arguments {number|string|BigNumber}
         */
        BigNumber.max = function () { return maxOrMin( arguments, P.lt ); };


        /*
         * Return a new BigNumber whose value is the minimum of the arguments.
         *
         * arguments {number|string|BigNumber}
         */
        BigNumber.min = function () { return maxOrMin( arguments, P.gt ); };


        /*
         * Return a new BigNumber with a random value equal to or greater than 0 and less than 1,
         * and with dp, or DECIMAL_PLACES if dp is omitted, decimal places (or less if trailing
         * zeros are produced).
         *
         * [dp] {number} Decimal places. Integer, 0 to MAX inclusive.
         *
         * 'random() decimal places not an integer: {dp}'
         * 'random() decimal places out of range: {dp}'
         * 'random() crypto unavailable: {crypto}'
         */
        BigNumber.random = (function () {
            var pow2_53 = 0x20000000000000;

            // Return a 53 bit integer n, where 0 <= n < 9007199254740992.
            // Check if Math.random() produces more than 32 bits of randomness.
            // If it does, assume at least 53 bits are produced, otherwise assume at least 30 bits.
            // 0x40000000 is 2^30, 0x800000 is 2^23, 0x1fffff is 2^21 - 1.
            var random53bitInt = (Math.random() * pow2_53) & 0x1fffff
              ? function () { return mathfloor( Math.random() * pow2_53 ); }
              : function () { return ((Math.random() * 0x40000000 | 0) * 0x800000) +
                  (Math.random() * 0x800000 | 0); };

            return function (dp) {
                var a, b, e, k, v,
                    i = 0,
                    c = [],
                    rand = new BigNumber(ONE);

                dp = dp == null || !isValidInt( dp, 0, MAX, 14 ) ? DECIMAL_PLACES : dp | 0;
                k = mathceil( dp / LOG_BASE );

                if (CRYPTO) {

                    // Browsers supporting crypto.getRandomValues.
                    if ( cryptoObj && cryptoObj.getRandomValues ) {

                        a = cryptoObj.getRandomValues( new Uint32Array( k *= 2 ) );

                        for ( ; i < k; ) {

                            // 53 bits:
                            // ((Math.pow(2, 32) - 1) * Math.pow(2, 21)).toString(2)
                            // 11111 11111111 11111111 11111111 11100000 00000000 00000000
                            // ((Math.pow(2, 32) - 1) >>> 11).toString(2)
                            //                                     11111 11111111 11111111
                            // 0x20000 is 2^21.
                            v = a[i] * 0x20000 + (a[i + 1] >>> 11);

                            // Rejection sampling:
                            // 0 <= v < 9007199254740992
                            // Probability that v >= 9e15, is
                            // 7199254740992 / 9007199254740992 ~= 0.0008, i.e. 1 in 1251
                            if ( v >= 9e15 ) {
                                b = cryptoObj.getRandomValues( new Uint32Array(2) );
                                a[i] = b[0];
                                a[i + 1] = b[1];
                            } else {

                                // 0 <= v <= 8999999999999999
                                // 0 <= (v % 1e14) <= 99999999999999
                                c.push( v % 1e14 );
                                i += 2;
                            }
                        }
                        i = k / 2;

                    // Node.js supporting crypto.randomBytes.
                    } else if ( cryptoObj && cryptoObj.randomBytes ) {

                        // buffer
                        a = cryptoObj.randomBytes( k *= 7 );

                        for ( ; i < k; ) {

                            // 0x1000000000000 is 2^48, 0x10000000000 is 2^40
                            // 0x100000000 is 2^32, 0x1000000 is 2^24
                            // 11111 11111111 11111111 11111111 11111111 11111111 11111111
                            // 0 <= v < 9007199254740992
                            v = ( ( a[i] & 31 ) * 0x1000000000000 ) + ( a[i + 1] * 0x10000000000 ) +
                                  ( a[i + 2] * 0x100000000 ) + ( a[i + 3] * 0x1000000 ) +
                                  ( a[i + 4] << 16 ) + ( a[i + 5] << 8 ) + a[i + 6];

                            if ( v >= 9e15 ) {
                                cryptoObj.randomBytes(7).copy( a, i );
                            } else {

                                // 0 <= (v % 1e14) <= 99999999999999
                                c.push( v % 1e14 );
                                i += 7;
                            }
                        }
                        i = k / 7;
                    } else if (ERRORS) {
                        raise( 14, 'crypto unavailable', cryptoObj );
                    }
                }

                // Use Math.random: CRYPTO is false or crypto is unavailable and ERRORS is false.
                if (!i) {

                    for ( ; i < k; ) {
                        v = random53bitInt();
                        if ( v < 9e15 ) c[i++] = v % 1e14;
                    }
                }

                k = c[--i];
                dp %= LOG_BASE;

                // Convert trailing digits to zeros according to dp.
                if ( k && dp ) {
                    v = POWS_TEN[LOG_BASE - dp];
                    c[i] = mathfloor( k / v ) * v;
                }

                // Remove trailing elements which are zero.
                for ( ; c[i] === 0; c.pop(), i-- );

                // Zero?
                if ( i < 0 ) {
                    c = [ e = 0 ];
                } else {

                    // Remove leading elements which are zero and adjust exponent accordingly.
                    for ( e = -1 ; c[0] === 0; c.shift(), e -= LOG_BASE);

                    // Count the digits of the first element of c to determine leading zeros, and...
                    for ( i = 1, v = c[0]; v >= 10; v /= 10, i++);

                    // adjust the exponent accordingly.
                    if ( i < LOG_BASE ) e -= LOG_BASE - i;
                }

                rand.e = e;
                rand.c = c;
                return rand;
            };
        })();


        // PRIVATE FUNCTIONS


        // Convert a numeric string of baseIn to a numeric string of baseOut.
        function convertBase( str, baseOut, baseIn, sign ) {
            var d, e, k, r, x, xc, y,
                i = str.indexOf( '.' ),
                dp = DECIMAL_PLACES,
                rm = ROUNDING_MODE;

            if ( baseIn < 37 ) str = str.toLowerCase();

            // Non-integer.
            if ( i >= 0 ) {
                k = POW_PRECISION;

                // Unlimited precision.
                POW_PRECISION = 0;
                str = str.replace( '.', '' );
                y = new BigNumber(baseIn);
                x = y.pow( str.length - i );
                POW_PRECISION = k;

                // Convert str as if an integer, then restore the fraction part by dividing the
                // result by its base raised to a power.
                y.c = toBaseOut( toFixedPoint( coeffToString( x.c ), x.e ), 10, baseOut );
                y.e = y.c.length;
            }

            // Convert the number as integer.
            xc = toBaseOut( str, baseIn, baseOut );
            e = k = xc.length;

            // Remove trailing zeros.
            for ( ; xc[--k] == 0; xc.pop() );
            if ( !xc[0] ) return '0';

            if ( i < 0 ) {
                --e;
            } else {
                x.c = xc;
                x.e = e;

                // sign is needed for correct rounding.
                x.s = sign;
                x = div( x, y, dp, rm, baseOut );
                xc = x.c;
                r = x.r;
                e = x.e;
            }

            d = e + dp + 1;

            // The rounding digit, i.e. the digit to the right of the digit that may be rounded up.
            i = xc[d];
            k = baseOut / 2;
            r = r || d < 0 || xc[d + 1] != null;

            r = rm < 4 ? ( i != null || r ) && ( rm == 0 || rm == ( x.s < 0 ? 3 : 2 ) )
                       : i > k || i == k &&( rm == 4 || r || rm == 6 && xc[d - 1] & 1 ||
                         rm == ( x.s < 0 ? 8 : 7 ) );

            if ( d < 1 || !xc[0] ) {

                // 1^-dp or 0.
                str = r ? toFixedPoint( '1', -dp ) : '0';
            } else {
                xc.length = d;

                if (r) {

                    // Rounding up may mean the previous digit has to be rounded up and so on.
                    for ( --baseOut; ++xc[--d] > baseOut; ) {
                        xc[d] = 0;

                        if ( !d ) {
                            ++e;
                            xc.unshift(1);
                        }
                    }
                }

                // Determine trailing zeros.
                for ( k = xc.length; !xc[--k]; );

                // E.g. [4, 11, 15] becomes 4bf.
                for ( i = 0, str = ''; i <= k; str += ALPHABET.charAt( xc[i++] ) );
                str = toFixedPoint( str, e );
            }

            // The caller will add the sign.
            return str;
        }


        // Perform division in the specified base. Called by div and convertBase.
        div = (function () {

            // Assume non-zero x and k.
            function multiply( x, k, base ) {
                var m, temp, xlo, xhi,
                    carry = 0,
                    i = x.length,
                    klo = k % SQRT_BASE,
                    khi = k / SQRT_BASE | 0;

                for ( x = x.slice(); i--; ) {
                    xlo = x[i] % SQRT_BASE;
                    xhi = x[i] / SQRT_BASE | 0;
                    m = khi * xlo + xhi * klo;
                    temp = klo * xlo + ( ( m % SQRT_BASE ) * SQRT_BASE ) + carry;
                    carry = ( temp / base | 0 ) + ( m / SQRT_BASE | 0 ) + khi * xhi;
                    x[i] = temp % base;
                }

                if (carry) x.unshift(carry);

                return x;
            }

            function compare( a, b, aL, bL ) {
                var i, cmp;

                if ( aL != bL ) {
                    cmp = aL > bL ? 1 : -1;
                } else {

                    for ( i = cmp = 0; i < aL; i++ ) {

                        if ( a[i] != b[i] ) {
                            cmp = a[i] > b[i] ? 1 : -1;
                            break;
                        }
                    }
                }
                return cmp;
            }

            function subtract( a, b, aL, base ) {
                var i = 0;

                // Subtract b from a.
                for ( ; aL--; ) {
                    a[aL] -= i;
                    i = a[aL] < b[aL] ? 1 : 0;
                    a[aL] = i * base + a[aL] - b[aL];
                }

                // Remove leading zeros.
                for ( ; !a[0] && a.length > 1; a.shift() );
            }

            // x: dividend, y: divisor.
            return function ( x, y, dp, rm, base ) {
                var cmp, e, i, more, n, prod, prodL, q, qc, rem, remL, rem0, xi, xL, yc0,
                    yL, yz,
                    s = x.s == y.s ? 1 : -1,
                    xc = x.c,
                    yc = y.c;

                // Either NaN, Infinity or 0?
                if ( !xc || !xc[0] || !yc || !yc[0] ) {

                    return new BigNumber(

                      // Return NaN if either NaN, or both Infinity or 0.
                      !x.s || !y.s || ( xc ? yc && xc[0] == yc[0] : !yc ) ? NaN :

                        // Return ±0 if x is ±0 or y is ±Infinity, or return ±Infinity as y is ±0.
                        xc && xc[0] == 0 || !yc ? s * 0 : s / 0
                    );
                }

                q = new BigNumber(s);
                qc = q.c = [];
                e = x.e - y.e;
                s = dp + e + 1;

                if ( !base ) {
                    base = BASE;
                    e = bitFloor( x.e / LOG_BASE ) - bitFloor( y.e / LOG_BASE );
                    s = s / LOG_BASE | 0;
                }

                // Result exponent may be one less then the current value of e.
                // The coefficients of the BigNumbers from convertBase may have trailing zeros.
                for ( i = 0; yc[i] == ( xc[i] || 0 ); i++ );
                if ( yc[i] > ( xc[i] || 0 ) ) e--;

                if ( s < 0 ) {
                    qc.push(1);
                    more = true;
                } else {
                    xL = xc.length;
                    yL = yc.length;
                    i = 0;
                    s += 2;

                    // Normalise xc and yc so highest order digit of yc is >= base / 2.

                    n = mathfloor( base / ( yc[0] + 1 ) );

                    // Not necessary, but to handle odd bases where yc[0] == ( base / 2 ) - 1.
                    // if ( n > 1 || n++ == 1 && yc[0] < base / 2 ) {
                    if ( n > 1 ) {
                        yc = multiply( yc, n, base );
                        xc = multiply( xc, n, base );
                        yL = yc.length;
                        xL = xc.length;
                    }

                    xi = yL;
                    rem = xc.slice( 0, yL );
                    remL = rem.length;

                    // Add zeros to make remainder as long as divisor.
                    for ( ; remL < yL; rem[remL++] = 0 );
                    yz = yc.slice();
                    yz.unshift(0);
                    yc0 = yc[0];
                    if ( yc[1] >= base / 2 ) yc0++;
                    // Not necessary, but to prevent trial digit n > base, when using base 3.
                    // else if ( base == 3 && yc0 == 1 ) yc0 = 1 + 1e-15;

                    do {
                        n = 0;

                        // Compare divisor and remainder.
                        cmp = compare( yc, rem, yL, remL );

                        // If divisor < remainder.
                        if ( cmp < 0 ) {

                            // Calculate trial digit, n.

                            rem0 = rem[0];
                            if ( yL != remL ) rem0 = rem0 * base + ( rem[1] || 0 );

                            // n is how many times the divisor goes into the current remainder.
                            n = mathfloor( rem0 / yc0 );

                            //  Algorithm:
                            //  1. product = divisor * trial digit (n)
                            //  2. if product > remainder: product -= divisor, n--
                            //  3. remainder -= product
                            //  4. if product was < remainder at 2:
                            //    5. compare new remainder and divisor
                            //    6. If remainder > divisor: remainder -= divisor, n++

                            if ( n > 1 ) {

                                // n may be > base only when base is 3.
                                if (n >= base) n = base - 1;

                                // product = divisor * trial digit.
                                prod = multiply( yc, n, base );
                                prodL = prod.length;
                                remL = rem.length;

                                // Compare product and remainder.
                                // If product > remainder.
                                // Trial digit n too high.
                                // n is 1 too high about 5% of the time, and is not known to have
                                // ever been more than 1 too high.
                                while ( compare( prod, rem, prodL, remL ) == 1 ) {
                                    n--;

                                    // Subtract divisor from product.
                                    subtract( prod, yL < prodL ? yz : yc, prodL, base );
                                    prodL = prod.length;
                                    cmp = 1;
                                }
                            } else {

                                // n is 0 or 1, cmp is -1.
                                // If n is 0, there is no need to compare yc and rem again below,
                                // so change cmp to 1 to avoid it.
                                // If n is 1, leave cmp as -1, so yc and rem are compared again.
                                if ( n == 0 ) {

                                    // divisor < remainder, so n must be at least 1.
                                    cmp = n = 1;
                                }

                                // product = divisor
                                prod = yc.slice();
                                prodL = prod.length;
                            }

                            if ( prodL < remL ) prod.unshift(0);

                            // Subtract product from remainder.
                            subtract( rem, prod, remL, base );
                            remL = rem.length;

                             // If product was < remainder.
                            if ( cmp == -1 ) {

                                // Compare divisor and new remainder.
                                // If divisor < new remainder, subtract divisor from remainder.
                                // Trial digit n too low.
                                // n is 1 too low about 5% of the time, and very rarely 2 too low.
                                while ( compare( yc, rem, yL, remL ) < 1 ) {
                                    n++;

                                    // Subtract divisor from remainder.
                                    subtract( rem, yL < remL ? yz : yc, remL, base );
                                    remL = rem.length;
                                }
                            }
                        } else if ( cmp === 0 ) {
                            n++;
                            rem = [0];
                        } // else cmp === 1 and n will be 0

                        // Add the next digit, n, to the result array.
                        qc[i++] = n;

                        // Update the remainder.
                        if ( rem[0] ) {
                            rem[remL++] = xc[xi] || 0;
                        } else {
                            rem = [ xc[xi] ];
                            remL = 1;
                        }
                    } while ( ( xi++ < xL || rem[0] != null ) && s-- );

                    more = rem[0] != null;

                    // Leading zero?
                    if ( !qc[0] ) qc.shift();
                }

                if ( base == BASE ) {

                    // To calculate q.e, first get the number of digits of qc[0].
                    for ( i = 1, s = qc[0]; s >= 10; s /= 10, i++ );
                    round( q, dp + ( q.e = i + e * LOG_BASE - 1 ) + 1, rm, more );

                // Caller is convertBase.
                } else {
                    q.e = e;
                    q.r = +more;
                }

                return q;
            };
        })();


        /*
         * Return a string representing the value of BigNumber n in fixed-point or exponential
         * notation rounded to the specified decimal places or significant digits.
         *
         * n is a BigNumber.
         * i is the index of the last digit required (i.e. the digit that may be rounded up).
         * rm is the rounding mode.
         * caller is caller id: toExponential 19, toFixed 20, toFormat 21, toPrecision 24.
         */
        function format( n, i, rm, caller ) {
            var c0, e, ne, len, str;

            rm = rm != null && isValidInt( rm, 0, 8, caller, roundingMode )
              ? rm | 0 : ROUNDING_MODE;

            if ( !n.c ) return n.toString();
            c0 = n.c[0];
            ne = n.e;

            if ( i == null ) {
                str = coeffToString( n.c );
                str = caller == 19 || caller == 24 && ne <= TO_EXP_NEG
                  ? toExponential( str, ne )
                  : toFixedPoint( str, ne );
            } else {
                n = round( new BigNumber(n), i, rm );

                // n.e may have changed if the value was rounded up.
                e = n.e;

                str = coeffToString( n.c );
                len = str.length;

                // toPrecision returns exponential notation if the number of significant digits
                // specified is less than the number of digits necessary to represent the integer
                // part of the value in fixed-point notation.

                // Exponential notation.
                if ( caller == 19 || caller == 24 && ( i <= e || e <= TO_EXP_NEG ) ) {

                    // Append zeros?
                    for ( ; len < i; str += '0', len++ );
                    str = toExponential( str, e );

                // Fixed-point notation.
                } else {
                    i -= ne;
                    str = toFixedPoint( str, e );

                    // Append zeros?
                    if ( e + 1 > len ) {
                        if ( --i > 0 ) for ( str += '.'; i--; str += '0' );
                    } else {
                        i += e - len;
                        if ( i > 0 ) {
                            if ( e + 1 == len ) str += '.';
                            for ( ; i--; str += '0' );
                        }
                    }
                }
            }

            return n.s < 0 && c0 ? '-' + str : str;
        }


        // Handle BigNumber.max and BigNumber.min.
        function maxOrMin( args, method ) {
            var m, n,
                i = 0;

            if ( isArray( args[0] ) ) args = args[0];
            m = new BigNumber( args[0] );

            for ( ; ++i < args.length; ) {
                n = new BigNumber( args[i] );

                // If any number is NaN, return NaN.
                if ( !n.s ) {
                    m = n;
                    break;
                } else if ( method.call( m, n ) ) {
                    m = n;
                }
            }

            return m;
        }


        /*
         * Return true if n is an integer in range, otherwise throw.
         * Use for argument validation when ERRORS is true.
         */
        function intValidatorWithErrors( n, min, max, caller, name ) {
            if ( n < min || n > max || n != truncate(n) ) {
                raise( caller, ( name || 'decimal places' ) +
                  ( n < min || n > max ? ' out of range' : ' not an integer' ), n );
            }

            return true;
        }


        /*
         * Strip trailing zeros, calculate base 10 exponent and check against MIN_EXP and MAX_EXP.
         * Called by minus, plus and times.
         */
        function normalise( n, c, e ) {
            var i = 1,
                j = c.length;

             // Remove trailing zeros.
            for ( ; !c[--j]; c.pop() );

            // Calculate the base 10 exponent. First get the number of digits of c[0].
            for ( j = c[0]; j >= 10; j /= 10, i++ );

            // Overflow?
            if ( ( e = i + e * LOG_BASE - 1 ) > MAX_EXP ) {

                // Infinity.
                n.c = n.e = null;

            // Underflow?
            } else if ( e < MIN_EXP ) {

                // Zero.
                n.c = [ n.e = 0 ];
            } else {
                n.e = e;
                n.c = c;
            }

            return n;
        }


        // Handle values that fail the validity test in BigNumber.
        parseNumeric = (function () {
            var basePrefix = /^(-?)0([xbo])(?=\w[\w.]*$)/i,
                dotAfter = /^([^.]+)\.$/,
                dotBefore = /^\.([^.]+)$/,
                isInfinityOrNaN = /^-?(Infinity|NaN)$/,
                whitespaceOrPlus = /^\s*\+(?=[\w.])|^\s+|\s+$/g;

            return function ( x, str, num, b ) {
                var base,
                    s = num ? str : str.replace( whitespaceOrPlus, '' );

                // No exception on ±Infinity or NaN.
                if ( isInfinityOrNaN.test(s) ) {
                    x.s = isNaN(s) ? null : s < 0 ? -1 : 1;
                } else {
                    if ( !num ) {

                        // basePrefix = /^(-?)0([xbo])(?=\w[\w.]*$)/i
                        s = s.replace( basePrefix, function ( m, p1, p2 ) {
                            base = ( p2 = p2.toLowerCase() ) == 'x' ? 16 : p2 == 'b' ? 2 : 8;
                            return !b || b == base ? p1 : m;
                        });

                        if (b) {
                            base = b;

                            // E.g. '1.' to '1', '.1' to '0.1'
                            s = s.replace( dotAfter, '$1' ).replace( dotBefore, '0.$1' );
                        }

                        if ( str != s ) return new BigNumber( s, base );
                    }

                    // 'new BigNumber() not a number: {n}'
                    // 'new BigNumber() not a base {b} number: {n}'
                    if (ERRORS) raise( id, 'not a' + ( b ? ' base ' + b : '' ) + ' number', str );
                    x.s = null;
                }

                x.c = x.e = null;
                id = 0;
            }
        })();


        // Throw a BigNumber Error.
        function raise( caller, msg, val ) {
            var error = new Error( [
                'new BigNumber',     // 0
                'cmp',               // 1
                'config',            // 2
                'div',               // 3
                'divToInt',          // 4
                'eq',                // 5
                'gt',                // 6
                'gte',               // 7
                'lt',                // 8
                'lte',               // 9
                'minus',             // 10
                'mod',               // 11
                'plus',              // 12
                'precision',         // 13
                'random',            // 14
                'round',             // 15
                'shift',             // 16
                'times',             // 17
                'toDigits',          // 18
                'toExponential',     // 19
                'toFixed',           // 20
                'toFormat',          // 21
                'toFraction',        // 22
                'pow',               // 23
                'toPrecision',       // 24
                'toString',          // 25
                'BigNumber'          // 26
            ][caller] + '() ' + msg + ': ' + val );

            error.name = 'BigNumber Error';
            id = 0;
            throw error;
        }


        /*
         * Round x to sd significant digits using rounding mode rm. Check for over/under-flow.
         * If r is truthy, it is known that there are more digits after the rounding digit.
         */
        function round( x, sd, rm, r ) {
            var d, i, j, k, n, ni, rd,
                xc = x.c,
                pows10 = POWS_TEN;

            // if x is not Infinity or NaN...
            if (xc) {

                // rd is the rounding digit, i.e. the digit after the digit that may be rounded up.
                // n is a base 1e14 number, the value of the element of array x.c containing rd.
                // ni is the index of n within x.c.
                // d is the number of digits of n.
                // i is the index of rd within n including leading zeros.
                // j is the actual index of rd within n (if < 0, rd is a leading zero).
                out: {

                    // Get the number of digits of the first element of xc.
                    for ( d = 1, k = xc[0]; k >= 10; k /= 10, d++ );
                    i = sd - d;

                    // If the rounding digit is in the first element of xc...
                    if ( i < 0 ) {
                        i += LOG_BASE;
                        j = sd;
                        n = xc[ ni = 0 ];

                        // Get the rounding digit at index j of n.
                        rd = n / pows10[ d - j - 1 ] % 10 | 0;
                    } else {
                        ni = mathceil( ( i + 1 ) / LOG_BASE );

                        if ( ni >= xc.length ) {

                            if (r) {

                                // Needed by sqrt.
                                for ( ; xc.length <= ni; xc.push(0) );
                                n = rd = 0;
                                d = 1;
                                i %= LOG_BASE;
                                j = i - LOG_BASE + 1;
                            } else {
                                break out;
                            }
                        } else {
                            n = k = xc[ni];

                            // Get the number of digits of n.
                            for ( d = 1; k >= 10; k /= 10, d++ );

                            // Get the index of rd within n.
                            i %= LOG_BASE;

                            // Get the index of rd within n, adjusted for leading zeros.
                            // The number of leading zeros of n is given by LOG_BASE - d.
                            j = i - LOG_BASE + d;

                            // Get the rounding digit at index j of n.
                            rd = j < 0 ? 0 : n / pows10[ d - j - 1 ] % 10 | 0;
                        }
                    }

                    r = r || sd < 0 ||

                    // Are there any non-zero digits after the rounding digit?
                    // The expression  n % pows10[ d - j - 1 ]  returns all digits of n to the right
                    // of the digit at j, e.g. if n is 908714 and j is 2, the expression gives 714.
                      xc[ni + 1] != null || ( j < 0 ? n : n % pows10[ d - j - 1 ] );

                    r = rm < 4
                      ? ( rd || r ) && ( rm == 0 || rm == ( x.s < 0 ? 3 : 2 ) )
                      : rd > 5 || rd == 5 && ( rm == 4 || r || rm == 6 &&

                        // Check whether the digit to the left of the rounding digit is odd.
                        ( ( i > 0 ? j > 0 ? n / pows10[ d - j ] : 0 : xc[ni - 1] ) % 10 ) & 1 ||
                          rm == ( x.s < 0 ? 8 : 7 ) );

                    if ( sd < 1 || !xc[0] ) {
                        xc.length = 0;

                        if (r) {

                            // Convert sd to decimal places.
                            sd -= x.e + 1;

                            // 1, 0.1, 0.01, 0.001, 0.0001 etc.
                            xc[0] = pows10[ ( LOG_BASE - sd % LOG_BASE ) % LOG_BASE ];
                            x.e = -sd || 0;
                        } else {

                            // Zero.
                            xc[0] = x.e = 0;
                        }

                        return x;
                    }

                    // Remove excess digits.
                    if ( i == 0 ) {
                        xc.length = ni;
                        k = 1;
                        ni--;
                    } else {
                        xc.length = ni + 1;
                        k = pows10[ LOG_BASE - i ];

                        // E.g. 56700 becomes 56000 if 7 is the rounding digit.
                        // j > 0 means i > number of leading zeros of n.
                        xc[ni] = j > 0 ? mathfloor( n / pows10[ d - j ] % pows10[j] ) * k : 0;
                    }

                    // Round up?
                    if (r) {

                        for ( ; ; ) {

                            // If the digit to be rounded up is in the first element of xc...
                            if ( ni == 0 ) {

                                // i will be the length of xc[0] before k is added.
                                for ( i = 1, j = xc[0]; j >= 10; j /= 10, i++ );
                                j = xc[0] += k;
                                for ( k = 1; j >= 10; j /= 10, k++ );

                                // if i != k the length has increased.
                                if ( i != k ) {
                                    x.e++;
                                    if ( xc[0] == BASE ) xc[0] = 1;
                                }

                                break;
                            } else {
                                xc[ni] += k;
                                if ( xc[ni] != BASE ) break;
                                xc[ni--] = 0;
                                k = 1;
                            }
                        }
                    }

                    // Remove trailing zeros.
                    for ( i = xc.length; xc[--i] === 0; xc.pop() );
                }

                // Overflow? Infinity.
                if ( x.e > MAX_EXP ) {
                    x.c = x.e = null;

                // Underflow? Zero.
                } else if ( x.e < MIN_EXP ) {
                    x.c = [ x.e = 0 ];
                }
            }

            return x;
        }


        // PROTOTYPE/INSTANCE METHODS


        /*
         * Return a new BigNumber whose value is the absolute value of this BigNumber.
         */
        P.absoluteValue = P.abs = function () {
            var x = new BigNumber(this);
            if ( x.s < 0 ) x.s = 1;
            return x;
        };


        /*
         * Return a new BigNumber whose value is the value of this BigNumber rounded to a whole
         * number in the direction of Infinity.
         */
        P.ceil = function () {
            return round( new BigNumber(this), this.e + 1, 2 );
        };


        /*
         * Return
         * 1 if the value of this BigNumber is greater than the value of BigNumber(y, b),
         * -1 if the value of this BigNumber is less than the value of BigNumber(y, b),
         * 0 if they have the same value,
         * or null if the value of either is NaN.
         */
        P.comparedTo = P.cmp = function ( y, b ) {
            id = 1;
            return compare( this, new BigNumber( y, b ) );
        };


        /*
         * Return the number of decimal places of the value of this BigNumber, or null if the value
         * of this BigNumber is ±Infinity or NaN.
         */
        P.decimalPlaces = P.dp = function () {
            var n, v,
                c = this.c;

            if ( !c ) return null;
            n = ( ( v = c.length - 1 ) - bitFloor( this.e / LOG_BASE ) ) * LOG_BASE;

            // Subtract the number of trailing zeros of the last number.
            if ( v = c[v] ) for ( ; v % 10 == 0; v /= 10, n-- );
            if ( n < 0 ) n = 0;

            return n;
        };


        /*
         *  n / 0 = I
         *  n / N = N
         *  n / I = 0
         *  0 / n = 0
         *  0 / 0 = N
         *  0 / N = N
         *  0 / I = 0
         *  N / n = N
         *  N / 0 = N
         *  N / N = N
         *  N / I = N
         *  I / n = I
         *  I / 0 = I
         *  I / N = N
         *  I / I = N
         *
         * Return a new BigNumber whose value is the value of this BigNumber divided by the value of
         * BigNumber(y, b), rounded according to DECIMAL_PLACES and ROUNDING_MODE.
         */
        P.dividedBy = P.div = function ( y, b ) {
            id = 3;
            return div( this, new BigNumber( y, b ), DECIMAL_PLACES, ROUNDING_MODE );
        };


        /*
         * Return a new BigNumber whose value is the integer part of dividing the value of this
         * BigNumber by the value of BigNumber(y, b).
         */
        P.dividedToIntegerBy = P.divToInt = function ( y, b ) {
            id = 4;
            return div( this, new BigNumber( y, b ), 0, 1 );
        };


        /*
         * Return true if the value of this BigNumber is equal to the value of BigNumber(y, b),
         * otherwise returns false.
         */
        P.equals = P.eq = function ( y, b ) {
            id = 5;
            return compare( this, new BigNumber( y, b ) ) === 0;
        };


        /*
         * Return a new BigNumber whose value is the value of this BigNumber rounded to a whole
         * number in the direction of -Infinity.
         */
        P.floor = function () {
            return round( new BigNumber(this), this.e + 1, 3 );
        };


        /*
         * Return true if the value of this BigNumber is greater than the value of BigNumber(y, b),
         * otherwise returns false.
         */
        P.greaterThan = P.gt = function ( y, b ) {
            id = 6;
            return compare( this, new BigNumber( y, b ) ) > 0;
        };


        /*
         * Return true if the value of this BigNumber is greater than or equal to the value of
         * BigNumber(y, b), otherwise returns false.
         */
        P.greaterThanOrEqualTo = P.gte = function ( y, b ) {
            id = 7;
            return ( b = compare( this, new BigNumber( y, b ) ) ) === 1 || b === 0;

        };


        /*
         * Return true if the value of this BigNumber is a finite number, otherwise returns false.
         */
        P.isFinite = function () {
            return !!this.c;
        };


        /*
         * Return true if the value of this BigNumber is an integer, otherwise return false.
         */
        P.isInteger = P.isInt = function () {
            return !!this.c && bitFloor( this.e / LOG_BASE ) > this.c.length - 2;
        };


        /*
         * Return true if the value of this BigNumber is NaN, otherwise returns false.
         */
        P.isNaN = function () {
            return !this.s;
        };


        /*
         * Return true if the value of this BigNumber is negative, otherwise returns false.
         */
        P.isNegative = P.isNeg = function () {
            return this.s < 0;
        };


        /*
         * Return true if the value of this BigNumber is 0 or -0, otherwise returns false.
         */
        P.isZero = function () {
            return !!this.c && this.c[0] == 0;
        };


        /*
         * Return true if the value of this BigNumber is less than the value of BigNumber(y, b),
         * otherwise returns false.
         */
        P.lessThan = P.lt = function ( y, b ) {
            id = 8;
            return compare( this, new BigNumber( y, b ) ) < 0;
        };


        /*
         * Return true if the value of this BigNumber is less than or equal to the value of
         * BigNumber(y, b), otherwise returns false.
         */
        P.lessThanOrEqualTo = P.lte = function ( y, b ) {
            id = 9;
            return ( b = compare( this, new BigNumber( y, b ) ) ) === -1 || b === 0;
        };


        /*
         *  n - 0 = n
         *  n - N = N
         *  n - I = -I
         *  0 - n = -n
         *  0 - 0 = 0
         *  0 - N = N
         *  0 - I = -I
         *  N - n = N
         *  N - 0 = N
         *  N - N = N
         *  N - I = N
         *  I - n = I
         *  I - 0 = I
         *  I - N = N
         *  I - I = N
         *
         * Return a new BigNumber whose value is the value of this BigNumber minus the value of
         * BigNumber(y, b).
         */
        P.minus = P.sub = function ( y, b ) {
            var i, j, t, xLTy,
                x = this,
                a = x.s;

            id = 10;
            y = new BigNumber( y, b );
            b = y.s;

            // Either NaN?
            if ( !a || !b ) return new BigNumber(NaN);

            // Signs differ?
            if ( a != b ) {
                y.s = -b;
                return x.plus(y);
            }

            var xe = x.e / LOG_BASE,
                ye = y.e / LOG_BASE,
                xc = x.c,
                yc = y.c;

            if ( !xe || !ye ) {

                // Either Infinity?
                if ( !xc || !yc ) return xc ? ( y.s = -b, y ) : new BigNumber( yc ? x : NaN );

                // Either zero?
                if ( !xc[0] || !yc[0] ) {

                    // Return y if y is non-zero, x if x is non-zero, or zero if both are zero.
                    return yc[0] ? ( y.s = -b, y ) : new BigNumber( xc[0] ? x :

                      // IEEE 754 (2008) 6.3: n - n = -0 when rounding to -Infinity
                      ROUNDING_MODE == 3 ? -0 : 0 );
                }
            }

            xe = bitFloor(xe);
            ye = bitFloor(ye);
            xc = xc.slice();

            // Determine which is the bigger number.
            if ( a = xe - ye ) {

                if ( xLTy = a < 0 ) {
                    a = -a;
                    t = xc;
                } else {
                    ye = xe;
                    t = yc;
                }

                t.reverse();

                // Prepend zeros to equalise exponents.
                for ( b = a; b--; t.push(0) );
                t.reverse();
            } else {

                // Exponents equal. Check digit by digit.
                j = ( xLTy = ( a = xc.length ) < ( b = yc.length ) ) ? a : b;

                for ( a = b = 0; b < j; b++ ) {

                    if ( xc[b] != yc[b] ) {
                        xLTy = xc[b] < yc[b];
                        break;
                    }
                }
            }

            // x < y? Point xc to the array of the bigger number.
            if (xLTy) t = xc, xc = yc, yc = t, y.s = -y.s;

            b = ( j = yc.length ) - ( i = xc.length );

            // Append zeros to xc if shorter.
            // No need to add zeros to yc if shorter as subtract only needs to start at yc.length.
            if ( b > 0 ) for ( ; b--; xc[i++] = 0 );
            b = BASE - 1;

            // Subtract yc from xc.
            for ( ; j > a; ) {

                if ( xc[--j] < yc[j] ) {
                    for ( i = j; i && !xc[--i]; xc[i] = b );
                    --xc[i];
                    xc[j] += BASE;
                }

                xc[j] -= yc[j];
            }

            // Remove leading zeros and adjust exponent accordingly.
            for ( ; xc[0] == 0; xc.shift(), --ye );

            // Zero?
            if ( !xc[0] ) {

                // Following IEEE 754 (2008) 6.3,
                // n - n = +0  but  n - n = -0  when rounding towards -Infinity.
                y.s = ROUNDING_MODE == 3 ? -1 : 1;
                y.c = [ y.e = 0 ];
                return y;
            }

            // No need to check for Infinity as +x - +y != Infinity && -x - -y != Infinity
            // for finite x and y.
            return normalise( y, xc, ye );
        };


        /*
         *   n % 0 =  N
         *   n % N =  N
         *   n % I =  n
         *   0 % n =  0
         *  -0 % n = -0
         *   0 % 0 =  N
         *   0 % N =  N
         *   0 % I =  0
         *   N % n =  N
         *   N % 0 =  N
         *   N % N =  N
         *   N % I =  N
         *   I % n =  N
         *   I % 0 =  N
         *   I % N =  N
         *   I % I =  N
         *
         * Return a new BigNumber whose value is the value of this BigNumber modulo the value of
         * BigNumber(y, b). The result depends on the value of MODULO_MODE.
         */
        P.modulo = P.mod = function ( y, b ) {
            var q, s,
                x = this;

            id = 11;
            y = new BigNumber( y, b );

            // Return NaN if x is Infinity or NaN, or y is NaN or zero.
            if ( !x.c || !y.s || y.c && !y.c[0] ) {
                return new BigNumber(NaN);

            // Return x if y is Infinity or x is zero.
            } else if ( !y.c || x.c && !x.c[0] ) {
                return new BigNumber(x);
            }

            if ( MODULO_MODE == 9 ) {

                // Euclidian division: q = sign(y) * floor(x / abs(y))
                // r = x - qy    where  0 <= r < abs(y)
                s = y.s;
                y.s = 1;
                q = div( x, y, 0, 3 );
                y.s = s;
                q.s *= s;
            } else {
                q = div( x, y, 0, MODULO_MODE );
            }

            return x.minus( q.times(y) );
        };


        /*
         * Return a new BigNumber whose value is the value of this BigNumber negated,
         * i.e. multiplied by -1.
         */
        P.negated = P.neg = function () {
            var x = new BigNumber(this);
            x.s = -x.s || null;
            return x;
        };


        /*
         *  n + 0 = n
         *  n + N = N
         *  n + I = I
         *  0 + n = n
         *  0 + 0 = 0
         *  0 + N = N
         *  0 + I = I
         *  N + n = N
         *  N + 0 = N
         *  N + N = N
         *  N + I = N
         *  I + n = I
         *  I + 0 = I
         *  I + N = N
         *  I + I = I
         *
         * Return a new BigNumber whose value is the value of this BigNumber plus the value of
         * BigNumber(y, b).
         */
        P.plus = P.add = function ( y, b ) {
            var t,
                x = this,
                a = x.s;

            id = 12;
            y = new BigNumber( y, b );
            b = y.s;

            // Either NaN?
            if ( !a || !b ) return new BigNumber(NaN);

            // Signs differ?
             if ( a != b ) {
                y.s = -b;
                return x.minus(y);
            }

            var xe = x.e / LOG_BASE,
                ye = y.e / LOG_BASE,
                xc = x.c,
                yc = y.c;

            if ( !xe || !ye ) {

                // Return ±Infinity if either ±Infinity.
                if ( !xc || !yc ) return new BigNumber( a / 0 );

                // Either zero?
                // Return y if y is non-zero, x if x is non-zero, or zero if both are zero.
                if ( !xc[0] || !yc[0] ) return yc[0] ? y : new BigNumber( xc[0] ? x : a * 0 );
            }

            xe = bitFloor(xe);
            ye = bitFloor(ye);
            xc = xc.slice();

            // Prepend zeros to equalise exponents. Faster to use reverse then do unshifts.
            if ( a = xe - ye ) {
                if ( a > 0 ) {
                    ye = xe;
                    t = yc;
                } else {
                    a = -a;
                    t = xc;
                }

                t.reverse();
                for ( ; a--; t.push(0) );
                t.reverse();
            }

            a = xc.length;
            b = yc.length;

            // Point xc to the longer array, and b to the shorter length.
            if ( a - b < 0 ) t = yc, yc = xc, xc = t, b = a;

            // Only start adding at yc.length - 1 as the further digits of xc can be ignored.
            for ( a = 0; b; ) {
                a = ( xc[--b] = xc[b] + yc[b] + a ) / BASE | 0;
                xc[b] %= BASE;
            }

            if (a) {
                xc.unshift(a);
                ++ye;
            }

            // No need to check for zero, as +x + +y != 0 && -x + -y != 0
            // ye = MAX_EXP + 1 possible
            return normalise( y, xc, ye );
        };


        /*
         * Return the number of significant digits of the value of this BigNumber.
         *
         * [z] {boolean|number} Whether to count integer-part trailing zeros: true, false, 1 or 0.
         */
        P.precision = P.sd = function (z) {
            var n, v,
                x = this,
                c = x.c;

            // 'precision() argument not a boolean or binary digit: {z}'
            if ( z != null && z !== !!z && z !== 1 && z !== 0 ) {
                if (ERRORS) raise( 13, 'argument' + notBool, z );
                if ( z != !!z ) z = null;
            }

            if ( !c ) return null;
            v = c.length - 1;
            n = v * LOG_BASE + 1;

            if ( v = c[v] ) {

                // Subtract the number of trailing zeros of the last element.
                for ( ; v % 10 == 0; v /= 10, n-- );

                // Add the number of digits of the first element.
                for ( v = c[0]; v >= 10; v /= 10, n++ );
            }

            if ( z && x.e + 1 > n ) n = x.e + 1;

            return n;
        };


        /*
         * Return a new BigNumber whose value is the value of this BigNumber rounded to a maximum of
         * dp decimal places using rounding mode rm, or to 0 and ROUNDING_MODE respectively if
         * omitted.
         *
         * [dp] {number} Decimal places. Integer, 0 to MAX inclusive.
         * [rm] {number} Rounding mode. Integer, 0 to 8 inclusive.
         *
         * 'round() decimal places out of range: {dp}'
         * 'round() decimal places not an integer: {dp}'
         * 'round() rounding mode not an integer: {rm}'
         * 'round() rounding mode out of range: {rm}'
         */
        P.round = function ( dp, rm ) {
            var n = new BigNumber(this);

            if ( dp == null || isValidInt( dp, 0, MAX, 15 ) ) {
                round( n, ~~dp + this.e + 1, rm == null ||
                  !isValidInt( rm, 0, 8, 15, roundingMode ) ? ROUNDING_MODE : rm | 0 );
            }

            return n;
        };


        /*
         * Return a new BigNumber whose value is the value of this BigNumber shifted by k places
         * (powers of 10). Shift to the right if n > 0, and to the left if n < 0.
         *
         * k {number} Integer, -MAX_SAFE_INTEGER to MAX_SAFE_INTEGER inclusive.
         *
         * If k is out of range and ERRORS is false, the result will be ±0 if k < 0, or ±Infinity
         * otherwise.
         *
         * 'shift() argument not an integer: {k}'
         * 'shift() argument out of range: {k}'
         */
        P.shift = function (k) {
            var n = this;
            return isValidInt( k, -MAX_SAFE_INTEGER, MAX_SAFE_INTEGER, 16, 'argument' )

              // k < 1e+21, or truncate(k) will produce exponential notation.
              ? n.times( '1e' + truncate(k) )
              : new BigNumber( n.c && n.c[0] && ( k < -MAX_SAFE_INTEGER || k > MAX_SAFE_INTEGER )
                ? n.s * ( k < 0 ? 0 : 1 / 0 )
                : n );
        };


        /*
         *  sqrt(-n) =  N
         *  sqrt( N) =  N
         *  sqrt(-I) =  N
         *  sqrt( I) =  I
         *  sqrt( 0) =  0
         *  sqrt(-0) = -0
         *
         * Return a new BigNumber whose value is the square root of the value of this BigNumber,
         * rounded according to DECIMAL_PLACES and ROUNDING_MODE.
         */
        P.squareRoot = P.sqrt = function () {
            var m, n, r, rep, t,
                x = this,
                c = x.c,
                s = x.s,
                e = x.e,
                dp = DECIMAL_PLACES + 4,
                half = new BigNumber('0.5');

            // Negative/NaN/Infinity/zero?
            if ( s !== 1 || !c || !c[0] ) {
                return new BigNumber( !s || s < 0 && ( !c || c[0] ) ? NaN : c ? x : 1 / 0 );
            }

            // Initial estimate.
            s = Math.sqrt( +x );

            // Math.sqrt underflow/overflow?
            // Pass x to Math.sqrt as integer, then adjust the exponent of the result.
            if ( s == 0 || s == 1 / 0 ) {
                n = coeffToString(c);
                if ( ( n.length + e ) % 2 == 0 ) n += '0';
                s = Math.sqrt(n);
                e = bitFloor( ( e + 1 ) / 2 ) - ( e < 0 || e % 2 );

                if ( s == 1 / 0 ) {
                    n = '1e' + e;
                } else {
                    n = s.toExponential();
                    n = n.slice( 0, n.indexOf('e') + 1 ) + e;
                }

                r = new BigNumber(n);
            } else {
                r = new BigNumber( s + '' );
            }

            // Check for zero.
            // r could be zero if MIN_EXP is changed after the this value was created.
            // This would cause a division by zero (x/t) and hence Infinity below, which would cause
            // coeffToString to throw.
            if ( r.c[0] ) {
                e = r.e;
                s = e + dp;
                if ( s < 3 ) s = 0;

                // Newton-Raphson iteration.
                for ( ; ; ) {
                    t = r;
                    r = half.times( t.plus( div( x, t, dp, 1 ) ) );

                    if ( coeffToString( t.c   ).slice( 0, s ) === ( n =
                         coeffToString( r.c ) ).slice( 0, s ) ) {

                        // The exponent of r may here be one less than the final result exponent,
                        // e.g 0.0009999 (e-4) --> 0.001 (e-3), so adjust s so the rounding digits
                        // are indexed correctly.
                        if ( r.e < e ) --s;
                        n = n.slice( s - 3, s + 1 );

                        // The 4th rounding digit may be in error by -1 so if the 4 rounding digits
                        // are 9999 or 4999 (i.e. approaching a rounding boundary) continue the
                        // iteration.
                        if ( n == '9999' || !rep && n == '4999' ) {

                            // On the first iteration only, check to see if rounding up gives the
                            // exact result as the nines may infinitely repeat.
                            if ( !rep ) {
                                round( t, t.e + DECIMAL_PLACES + 2, 0 );

                                if ( t.times(t).eq(x) ) {
                                    r = t;
                                    break;
                                }
                            }

                            dp += 4;
                            s += 4;
                            rep = 1;
                        } else {

                            // If rounding digits are null, 0{0,4} or 50{0,3}, check for exact
                            // result. If not, then there are further digits and m will be truthy.
                            if ( !+n || !+n.slice(1) && n.charAt(0) == '5' ) {

                                // Truncate to the first rounding digit.
                                round( r, r.e + DECIMAL_PLACES + 2, 1 );
                                m = !r.times(r).eq(x);
                            }

                            break;
                        }
                    }
                }
            }

            return round( r, r.e + DECIMAL_PLACES + 1, ROUNDING_MODE, m );
        };


        /*
         *  n * 0 = 0
         *  n * N = N
         *  n * I = I
         *  0 * n = 0
         *  0 * 0 = 0
         *  0 * N = N
         *  0 * I = N
         *  N * n = N
         *  N * 0 = N
         *  N * N = N
         *  N * I = N
         *  I * n = I
         *  I * 0 = N
         *  I * N = N
         *  I * I = I
         *
         * Return a new BigNumber whose value is the value of this BigNumber times the value of
         * BigNumber(y, b).
         */
        P.times = P.mul = function ( y, b ) {
            var c, e, i, j, k, m, xcL, xlo, xhi, ycL, ylo, yhi, zc,
                base, sqrtBase,
                x = this,
                xc = x.c,
                yc = ( id = 17, y = new BigNumber( y, b ) ).c;

            // Either NaN, ±Infinity or ±0?
            if ( !xc || !yc || !xc[0] || !yc[0] ) {

                // Return NaN if either is NaN, or one is 0 and the other is Infinity.
                if ( !x.s || !y.s || xc && !xc[0] && !yc || yc && !yc[0] && !xc ) {
                    y.c = y.e = y.s = null;
                } else {
                    y.s *= x.s;

                    // Return ±Infinity if either is ±Infinity.
                    if ( !xc || !yc ) {
                        y.c = y.e = null;

                    // Return ±0 if either is ±0.
                    } else {
                        y.c = [0];
                        y.e = 0;
                    }
                }

                return y;
            }

            e = bitFloor( x.e / LOG_BASE ) + bitFloor( y.e / LOG_BASE );
            y.s *= x.s;
            xcL = xc.length;
            ycL = yc.length;

            // Ensure xc points to longer array and xcL to its length.
            if ( xcL < ycL ) zc = xc, xc = yc, yc = zc, i = xcL, xcL = ycL, ycL = i;

            // Initialise the result array with zeros.
            for ( i = xcL + ycL, zc = []; i--; zc.push(0) );

            base = BASE;
            sqrtBase = SQRT_BASE;

            for ( i = ycL; --i >= 0; ) {
                c = 0;
                ylo = yc[i] % sqrtBase;
                yhi = yc[i] / sqrtBase | 0;

                for ( k = xcL, j = i + k; j > i; ) {
                    xlo = xc[--k] % sqrtBase;
                    xhi = xc[k] / sqrtBase | 0;
                    m = yhi * xlo + xhi * ylo;
                    xlo = ylo * xlo + ( ( m % sqrtBase ) * sqrtBase ) + zc[j] + c;
                    c = ( xlo / base | 0 ) + ( m / sqrtBase | 0 ) + yhi * xhi;
                    zc[j--] = xlo % base;
                }

                zc[j] = c;
            }

            if (c) {
                ++e;
            } else {
                zc.shift();
            }

            return normalise( y, zc, e );
        };


        /*
         * Return a new BigNumber whose value is the value of this BigNumber rounded to a maximum of
         * sd significant digits using rounding mode rm, or ROUNDING_MODE if rm is omitted.
         *
         * [sd] {number} Significant digits. Integer, 1 to MAX inclusive.
         * [rm] {number} Rounding mode. Integer, 0 to 8 inclusive.
         *
         * 'toDigits() precision out of range: {sd}'
         * 'toDigits() precision not an integer: {sd}'
         * 'toDigits() rounding mode not an integer: {rm}'
         * 'toDigits() rounding mode out of range: {rm}'
         */
        P.toDigits = function ( sd, rm ) {
            var n = new BigNumber(this);
            sd = sd == null || !isValidInt( sd, 1, MAX, 18, 'precision' ) ? null : sd | 0;
            rm = rm == null || !isValidInt( rm, 0, 8, 18, roundingMode ) ? ROUNDING_MODE : rm | 0;
            return sd ? round( n, sd, rm ) : n;
        };


        /*
         * Return a string representing the value of this BigNumber in exponential notation and
         * rounded using ROUNDING_MODE to dp fixed decimal places.
         *
         * [dp] {number} Decimal places. Integer, 0 to MAX inclusive.
         * [rm] {number} Rounding mode. Integer, 0 to 8 inclusive.
         *
         * 'toExponential() decimal places not an integer: {dp}'
         * 'toExponential() decimal places out of range: {dp}'
         * 'toExponential() rounding mode not an integer: {rm}'
         * 'toExponential() rounding mode out of range: {rm}'
         */
        P.toExponential = function ( dp, rm ) {
            return format( this,
              dp != null && isValidInt( dp, 0, MAX, 19 ) ? ~~dp + 1 : null, rm, 19 );
        };


        /*
         * Return a string representing the value of this BigNumber in fixed-point notation rounding
         * to dp fixed decimal places using rounding mode rm, or ROUNDING_MODE if rm is omitted.
         *
         * Note: as with JavaScript's number type, (-0).toFixed(0) is '0',
         * but e.g. (-0.00001).toFixed(0) is '-0'.
         *
         * [dp] {number} Decimal places. Integer, 0 to MAX inclusive.
         * [rm] {number} Rounding mode. Integer, 0 to 8 inclusive.
         *
         * 'toFixed() decimal places not an integer: {dp}'
         * 'toFixed() decimal places out of range: {dp}'
         * 'toFixed() rounding mode not an integer: {rm}'
         * 'toFixed() rounding mode out of range: {rm}'
         */
        P.toFixed = function ( dp, rm ) {
            return format( this, dp != null && isValidInt( dp, 0, MAX, 20 )
              ? ~~dp + this.e + 1 : null, rm, 20 );
        };


        /*
         * Return a string representing the value of this BigNumber in fixed-point notation rounded
         * using rm or ROUNDING_MODE to dp decimal places, and formatted according to the properties
         * of the FORMAT object (see BigNumber.config).
         *
         * FORMAT = {
         *      decimalSeparator : '.',
         *      groupSeparator : ',',
         *      groupSize : 3,
         *      secondaryGroupSize : 0,
         *      fractionGroupSeparator : '\xA0',    // non-breaking space
         *      fractionGroupSize : 0
         * };
         *
         * [dp] {number} Decimal places. Integer, 0 to MAX inclusive.
         * [rm] {number} Rounding mode. Integer, 0 to 8 inclusive.
         *
         * 'toFormat() decimal places not an integer: {dp}'
         * 'toFormat() decimal places out of range: {dp}'
         * 'toFormat() rounding mode not an integer: {rm}'
         * 'toFormat() rounding mode out of range: {rm}'
         */
        P.toFormat = function ( dp, rm ) {
            var str = format( this, dp != null && isValidInt( dp, 0, MAX, 21 )
              ? ~~dp + this.e + 1 : null, rm, 21 );

            if ( this.c ) {
                var i,
                    arr = str.split('.'),
                    g1 = +FORMAT.groupSize,
                    g2 = +FORMAT.secondaryGroupSize,
                    groupSeparator = FORMAT.groupSeparator,
                    intPart = arr[0],
                    fractionPart = arr[1],
                    isNeg = this.s < 0,
                    intDigits = isNeg ? intPart.slice(1) : intPart,
                    len = intDigits.length;

                if (g2) i = g1, g1 = g2, g2 = i, len -= i;

                if ( g1 > 0 && len > 0 ) {
                    i = len % g1 || g1;
                    intPart = intDigits.substr( 0, i );

                    for ( ; i < len; i += g1 ) {
                        intPart += groupSeparator + intDigits.substr( i, g1 );
                    }

                    if ( g2 > 0 ) intPart += groupSeparator + intDigits.slice(i);
                    if (isNeg) intPart = '-' + intPart;
                }

                str = fractionPart
                  ? intPart + FORMAT.decimalSeparator + ( ( g2 = +FORMAT.fractionGroupSize )
                    ? fractionPart.replace( new RegExp( '\\d{' + g2 + '}\\B', 'g' ),
                      '$&' + FORMAT.fractionGroupSeparator )
                    : fractionPart )
                  : intPart;
            }

            return str;
        };


        /*
         * Return a string array representing the value of this BigNumber as a simple fraction with
         * an integer numerator and an integer denominator. The denominator will be a positive
         * non-zero value less than or equal to the specified maximum denominator. If a maximum
         * denominator is not specified, the denominator will be the lowest value necessary to
         * represent the number exactly.
         *
         * [md] {number|string|BigNumber} Integer >= 1 and < Infinity. The maximum denominator.
         *
         * 'toFraction() max denominator not an integer: {md}'
         * 'toFraction() max denominator out of range: {md}'
         */
        P.toFraction = function (md) {
            var arr, d0, d2, e, exp, n, n0, q, s,
                k = ERRORS,
                x = this,
                xc = x.c,
                d = new BigNumber(ONE),
                n1 = d0 = new BigNumber(ONE),
                d1 = n0 = new BigNumber(ONE);

            if ( md != null ) {
                ERRORS = false;
                n = new BigNumber(md);
                ERRORS = k;

                if ( !( k = n.isInt() ) || n.lt(ONE) ) {

                    if (ERRORS) {
                        raise( 22,
                          'max denominator ' + ( k ? 'out of range' : 'not an integer' ), md );
                    }

                    // ERRORS is false:
                    // If md is a finite non-integer >= 1, round it to an integer and use it.
                    md = !k && n.c && round( n, n.e + 1, 1 ).gte(ONE) ? n : null;
                }
            }

            if ( !xc ) return x.toString();
            s = coeffToString(xc);

            // Determine initial denominator.
            // d is a power of 10 and the minimum max denominator that specifies the value exactly.
            e = d.e = s.length - x.e - 1;
            d.c[0] = POWS_TEN[ ( exp = e % LOG_BASE ) < 0 ? LOG_BASE + exp : exp ];
            md = !md || n.cmp(d) > 0 ? ( e > 0 ? d : n1 ) : n;

            exp = MAX_EXP;
            MAX_EXP = 1 / 0;
            n = new BigNumber(s);

            // n0 = d1 = 0
            n0.c[0] = 0;

            for ( ; ; )  {
                q = div( n, d, 0, 1 );
                d2 = d0.plus( q.times(d1) );
                if ( d2.cmp(md) == 1 ) break;
                d0 = d1;
                d1 = d2;
                n1 = n0.plus( q.times( d2 = n1 ) );
                n0 = d2;
                d = n.minus( q.times( d2 = d ) );
                n = d2;
            }

            d2 = div( md.minus(d0), d1, 0, 1 );
            n0 = n0.plus( d2.times(n1) );
            d0 = d0.plus( d2.times(d1) );
            n0.s = n1.s = x.s;
            e *= 2;

            // Determine which fraction is closer to x, n0/d0 or n1/d1
            arr = div( n1, d1, e, ROUNDING_MODE ).minus(x).abs().cmp(
                  div( n0, d0, e, ROUNDING_MODE ).minus(x).abs() ) < 1
                    ? [ n1.toString(), d1.toString() ]
                    : [ n0.toString(), d0.toString() ];

            MAX_EXP = exp;
            return arr;
        };


        /*
         * Return the value of this BigNumber converted to a number primitive.
         */
        P.toNumber = function () {
            return +this;
        };


        /*
         * Return a BigNumber whose value is the value of this BigNumber raised to the power n.
         * If m is present, return the result modulo m.
         * If n is negative round according to DECIMAL_PLACES and ROUNDING_MODE.
         * If POW_PRECISION is non-zero and m is not present, round to POW_PRECISION using
         * ROUNDING_MODE.
         *
         * The modular power operation works efficiently when x, n, and m are positive integers,
         * otherwise it is equivalent to calculating x.toPower(n).modulo(m) (with POW_PRECISION 0).
         *
         * n {number} Integer, -MAX_SAFE_INTEGER to MAX_SAFE_INTEGER inclusive.
         * [m] {number|string|BigNumber} The modulus.
         *
         * 'pow() exponent not an integer: {n}'
         * 'pow() exponent out of range: {n}'
         *
         * Performs 54 loop iterations for n of 9007199254740991.
         */
        P.toPower = P.pow = function ( n, m ) {
            var k, y, z,
                i = mathfloor( n < 0 ? -n : +n ),
                x = this;

            if ( m != null ) {
                id = 23;
                m = new BigNumber(m);
            }

            // Pass ±Infinity to Math.pow if exponent is out of range.
            if ( !isValidInt( n, -MAX_SAFE_INTEGER, MAX_SAFE_INTEGER, 23, 'exponent' ) &&
              ( !isFinite(n) || i > MAX_SAFE_INTEGER && ( n /= 0 ) ||
                parseFloat(n) != n && !( n = NaN ) ) || n == 0 ) {
                k = Math.pow( +x, n );
                return new BigNumber( m ? k % m : k );
            }

            if (m) {
                if ( n > 1 && x.gt(ONE) && x.isInt() && m.gt(ONE) && m.isInt() ) {
                    x = x.mod(m);
                } else {
                    z = m;

                    // Nullify m so only a single mod operation is performed at the end.
                    m = null;
                }
            } else if (POW_PRECISION) {

                // Truncating each coefficient array to a length of k after each multiplication
                // equates to truncating significant digits to POW_PRECISION + [28, 41],
                // i.e. there will be a minimum of 28 guard digits retained.
                // (Using + 1.5 would give [9, 21] guard digits.)
                k = mathceil( POW_PRECISION / LOG_BASE + 2 );
            }

            y = new BigNumber(ONE);

            for ( ; ; ) {
                if ( i % 2 ) {
                    y = y.times(x);
                    if ( !y.c ) break;
                    if (k) {
                        if ( y.c.length > k ) y.c.length = k;
                    } else if (m) {
                        y = y.mod(m);
                    }
                }

                i = mathfloor( i / 2 );
                if ( !i ) break;
                x = x.times(x);
                if (k) {
                    if ( x.c && x.c.length > k ) x.c.length = k;
                } else if (m) {
                    x = x.mod(m);
                }
            }

            if (m) return y;
            if ( n < 0 ) y = ONE.div(y);

            return z ? y.mod(z) : k ? round( y, POW_PRECISION, ROUNDING_MODE ) : y;
        };


        /*
         * Return a string representing the value of this BigNumber rounded to sd significant digits
         * using rounding mode rm or ROUNDING_MODE. If sd is less than the number of digits
         * necessary to represent the integer part of the value in fixed-point notation, then use
         * exponential notation.
         *
         * [sd] {number} Significant digits. Integer, 1 to MAX inclusive.
         * [rm] {number} Rounding mode. Integer, 0 to 8 inclusive.
         *
         * 'toPrecision() precision not an integer: {sd}'
         * 'toPrecision() precision out of range: {sd}'
         * 'toPrecision() rounding mode not an integer: {rm}'
         * 'toPrecision() rounding mode out of range: {rm}'
         */
        P.toPrecision = function ( sd, rm ) {
            return format( this, sd != null && isValidInt( sd, 1, MAX, 24, 'precision' )
              ? sd | 0 : null, rm, 24 );
        };


        /*
         * Return a string representing the value of this BigNumber in base b, or base 10 if b is
         * omitted. If a base is specified, including base 10, round according to DECIMAL_PLACES and
         * ROUNDING_MODE. If a base is not specified, and this BigNumber has a positive exponent
         * that is equal to or greater than TO_EXP_POS, or a negative exponent equal to or less than
         * TO_EXP_NEG, return exponential notation.
         *
         * [b] {number} Integer, 2 to 64 inclusive.
         *
         * 'toString() base not an integer: {b}'
         * 'toString() base out of range: {b}'
         */
        P.toString = function (b) {
            var str,
                n = this,
                s = n.s,
                e = n.e;

            // Infinity or NaN?
            if ( e === null ) {

                if (s) {
                    str = 'Infinity';
                    if ( s < 0 ) str = '-' + str;
                } else {
                    str = 'NaN';
                }
            } else {
                str = coeffToString( n.c );

                if ( b == null || !isValidInt( b, 2, 64, 25, 'base' ) ) {
                    str = e <= TO_EXP_NEG || e >= TO_EXP_POS
                      ? toExponential( str, e )
                      : toFixedPoint( str, e );
                } else {
                    str = convertBase( toFixedPoint( str, e ), b | 0, 10, s );
                }

                if ( s < 0 && n.c[0] ) str = '-' + str;
            }

            return str;
        };


        /*
         * Return a new BigNumber whose value is the value of this BigNumber truncated to a whole
         * number.
         */
        P.truncated = P.trunc = function () {
            return round( new BigNumber(this), this.e + 1, 1 );
        };



        /*
         * Return as toString, but do not accept a base argument, and include the minus sign for
         * negative zero.
         */
        P.valueOf = P.toJSON = function () {
            var str,
                n = this,
                e = n.e;

            if ( e === null ) return n.toString();

            str = coeffToString( n.c );

            str = e <= TO_EXP_NEG || e >= TO_EXP_POS
                ? toExponential( str, e )
                : toFixedPoint( str, e );

            return n.s < 0 ? '-' + str : str;
        };


        // Aliases for BigDecimal methods.
        //P.add = P.plus;         // P.add included above
        //P.subtract = P.minus;   // P.sub included above
        //P.multiply = P.times;   // P.mul included above
        //P.divide = P.div;
        //P.remainder = P.mod;
        //P.compareTo = P.cmp;
        //P.negate = P.neg;


        if ( configObj != null ) BigNumber.config(configObj);

        return BigNumber;
    }


    // PRIVATE HELPER FUNCTIONS


    function bitFloor(n) {
        var i = n | 0;
        return n > 0 || n === i ? i : i - 1;
    }


    // Return a coefficient array as a string of base 10 digits.
    function coeffToString(a) {
        var s, z,
            i = 1,
            j = a.length,
            r = a[0] + '';

        for ( ; i < j; ) {
            s = a[i++] + '';
            z = LOG_BASE - s.length;
            for ( ; z--; s = '0' + s );
            r += s;
        }

        // Determine trailing zeros.
        for ( j = r.length; r.charCodeAt(--j) === 48; );
        return r.slice( 0, j + 1 || 1 );
    }


    // Compare the value of BigNumbers x and y.
    function compare( x, y ) {
        var a, b,
            xc = x.c,
            yc = y.c,
            i = x.s,
            j = y.s,
            k = x.e,
            l = y.e;

        // Either NaN?
        if ( !i || !j ) return null;

        a = xc && !xc[0];
        b = yc && !yc[0];

        // Either zero?
        if ( a || b ) return a ? b ? 0 : -j : i;

        // Signs differ?
        if ( i != j ) return i;

        a = i < 0;
        b = k == l;

        // Either Infinity?
        if ( !xc || !yc ) return b ? 0 : !xc ^ a ? 1 : -1;

        // Compare exponents.
        if ( !b ) return k > l ^ a ? 1 : -1;

        j = ( k = xc.length ) < ( l = yc.length ) ? k : l;

        // Compare digit by digit.
        for ( i = 0; i < j; i++ ) if ( xc[i] != yc[i] ) return xc[i] > yc[i] ^ a ? 1 : -1;

        // Compare lengths.
        return k == l ? 0 : k > l ^ a ? 1 : -1;
    }


    /*
     * Return true if n is a valid number in range, otherwise false.
     * Use for argument validation when ERRORS is false.
     * Note: parseInt('1e+1') == 1 but parseFloat('1e+1') == 10.
     */
    function intValidatorNoErrors( n, min, max ) {
        return ( n = truncate(n) ) >= min && n <= max;
    }


    function isArray(obj) {
        return Object.prototype.toString.call(obj) == '[object Array]';
    }


    /*
     * Convert string of baseIn to an array of numbers of baseOut.
     * Eg. convertBase('255', 10, 16) returns [15, 15].
     * Eg. convertBase('ff', 16, 10) returns [2, 5, 5].
     */
    function toBaseOut( str, baseIn, baseOut ) {
        var j,
            arr = [0],
            arrL,
            i = 0,
            len = str.length;

        for ( ; i < len; ) {
            for ( arrL = arr.length; arrL--; arr[arrL] *= baseIn );
            arr[ j = 0 ] += ALPHABET.indexOf( str.charAt( i++ ) );

            for ( ; j < arr.length; j++ ) {

                if ( arr[j] > baseOut - 1 ) {
                    if ( arr[j + 1] == null ) arr[j + 1] = 0;
                    arr[j + 1] += arr[j] / baseOut | 0;
                    arr[j] %= baseOut;
                }
            }
        }

        return arr.reverse();
    }


    function toExponential( str, e ) {
        return ( str.length > 1 ? str.charAt(0) + '.' + str.slice(1) : str ) +
          ( e < 0 ? 'e' : 'e+' ) + e;
    }


    function toFixedPoint( str, e ) {
        var len, z;

        // Negative exponent?
        if ( e < 0 ) {

            // Prepend zeros.
            for ( z = '0.'; ++e; z += '0' );
            str = z + str;

        // Positive exponent
        } else {
            len = str.length;

            // Append zeros.
            if ( ++e > len ) {
                for ( z = '0', e -= len; --e; z += '0' );
                str += z;
            } else if ( e < len ) {
                str = str.slice( 0, e ) + '.' + str.slice(e);
            }
        }

        return str;
    }


    function truncate(n) {
        n = parseFloat(n);
        return n < 0 ? mathceil(n) : mathfloor(n);
    }


    // EXPORT


    BigNumber = constructorFactory();
    BigNumber.default = BigNumber.BigNumber = BigNumber;


    // AMD.
    if ( typeof define == 'function' && define.amd ) {
        define( function () { return BigNumber; } );

    // Node.js and other environments that support module.exports.
    } else if ( typeof module != 'undefined' && module.exports ) {
        module.exports = BigNumber;

        // Split string stops browserify adding crypto shim.
        if ( !cryptoObj ) try { cryptoObj = require('cry' + 'pto'); } catch (e) {}

    // Browser.
    } else {
        if ( !globalObj ) globalObj = typeof self != 'undefined' ? self : Function('return this')();
        globalObj.BigNumber = BigNumber;
    }
})(this);

},{}],8:[function(require,module,exports){
arguments[4][3][0].apply(exports,arguments)
},{"dup":3}]},{},[5])(5)
});
// Configure vendored libraries as required here

batavia.vendored.BigNumber.config({
    DECIMAL_PLACES: 324,
    ROUNDING_MODE: batavia.vendored.BigNumber.ROUND_HALF_EVEN
});

function assert(condition, message) {
    if (!condition) {
        throw message || "Assertion failed";
    }
}

batavia.isArray = Array.isArray;
if (!batavia.isArray) {
    batavia.isArray = function (obj) {
        return  Object.prototype.toString.call(obj) === '[object Array]';
    };
}

/*************************************************************************
 * Type comparison defintions that match Python-like behavior.
 *************************************************************************/

batavia.isinstance = function(obj, type) {
    if (type instanceof Array) {
        for (var t in type) {
            if (batavia.isinstance(obj, type[t])) {
                return true;
            }
        }
        return false;
    } else {
        switch (typeof obj) {
            case 'boolean':
                return type === batavia.types.Bool;
            case 'number':
                return type === batavia.types.Int;
            case 'string':
                return type === batavia.types.Str;
            case 'object':
                return obj instanceof type;
            default:
                return false;
        }
    }
};

batavia.isbataviainstance = function(obj) {
    return batavia.isinstance(obj, [
        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
        batavia.types.Int, batavia.types.JSDict, batavia.types.List,
        batavia.types.NoneType, batavia.types.Tuple, batavia.types.Slice,
        batavia.types.Bytes, batavia.types.Bytearray, batavia.types.Type,
        batavia.types.Str, batavia.types.Set, batavia.types.Range,
        batavia.types.FrozenSet, batavia.types.Complex,
        batavia.types.NotImplementedType
    ]);
}

batavia.type_name = function(arg) {
    var type_name;

    switch (typeof arg) {
        case 'boolean':
            type_name = 'bool';
            break;
        case 'number':
            type_name = 'Native number';
            break;
        case 'string':
            type_name = 'str';
            break;
        case 'object':
            if (arg === null || arg === batavia.builtins.None) {
                type_name = 'NoneType';
            } else if (arg.__class__ != null && arg.__class__.__name__) {
                type_name = arg.__class__.__name__;
            } else {
                type_name = 'Native object';
            }
    }

    return type_name;
};

batavia.issubclass = function(cls, type) {
    var t;
    if (type instanceof Array) {
        for (t in type) {
            if (batavia.issubclass(cls, type[t])) {
                return true;
            }
        }
        return false;
    } else {
        switch (typeof cls) {
            case 'boolean':
                return type === batavia.types.Bool;
            case 'number':
                return type === batavia.types.Int;
            case 'string':
                return type === batavia.types.Str;
            case 'object':
                if (type === null || type === batavia.types.NoneType) {
                    return cls === null;
                } else {
                    var mro = cls.mro();
                    for (t in mro) {
                        if (type != null && type.prototype != null && mro[t] === type.prototype.__class__) {
                            return true;
                        }
                    }
                }
                return false;
            default:
                return false;
        }
    }
};

/*************************************************************************
 * sprintf() implementation
 *************************************************************************/
batavia._substitute = function(format, args) {
    var results = [];
    var special_case_types = [
        batavia.types.List,
        batavia.types.Dict,
        batavia.types.Bytes];

    /* This is the general form regex for a sprintf-like string. */
    var re = /\x25(?:([1-9]\d*)\$|\(([^\)]+)\))?(\+)?(0|'[^$])?(-)?(\d+)?(?:\.(\d+))?([b-gijosuxX])/g;
    var match;
    var lastIndex = 0;
    for (var i = 0; i < args.length; i++) {
        var arg = args[i];

        match = re.exec(format);
        if (match) {
            switch (match[8]) {
                case "b":
                    arg = arg.toString(2);
                break;
                case "c":
                    arg = String.fromCharCode(arg);
                break;
                case "d":
                case "i":
                    arg = parseInt(arg, 10);
                break;
                case "j":
                    arg = JSON.stringify(arg, null, match[6] ? parseInt(match[6], 10) : 0);
                break;
                case "e":
                    arg = match[7] ? arg.toExponential(match[7]) : arg.toExponential();
                break;
                case "f":
                    arg = match[7] ? parseFloat(arg).toFixed(match[7]) : parseFloat(arg);
                break;
                case "g":
                    arg = match[7] ? parseFloat(arg).toPrecision(match[7]) : parseFloat(arg);
                break;
                case "o":
                    arg = arg.toString(8);
                break;
                case "s":
                    arg = ((arg = String(arg)) && match[7] ? arg.substring(0, match[7]) : arg);
                break;
                case "u":
                    arg = arg >>> 0;
                break;
                case "x":
                    arg = arg.toString(16);
                break;
                case "X":
                    arg = arg.toString(16).toUpperCase();
                break;
            }

            results.push(format.slice(lastIndex, match.index));
            lastIndex = re.lastIndex;
            results.push(arg);
        } else if (    (args.constructor === Array)
                    && batavia.isinstance(args[0], special_case_types)) {
            return format;
        } else {
            throw new batavia.builtins.TypeError('not all arguments converted during string formatting');
        }
    }
    // Push the rest of the string.
    results.push(format.slice(re.lastIndex));
    return results.join('');
};

/*************************************************************************
 * Class construction
 *************************************************************************/

batavia.make_class = function(args, kwargs) {
    var func = args[0];
    var name = args[1];
    var bases = kwargs.bases || args[2];
    var metaclass = kwargs.metaclass || args[3];
    var kwds = kwargs.kwds || args[4] || [];

    // Create a locals context, and run the class function in it.
    var locals = new batavia.types.Dict();
    var retval = func.__call__.apply(this, [[], [], locals]);

    // Now construct the class, based on the constructed local context.
    var klass = function(vm, args, kwargs) {
        if (this.__init__) {
            this.__init__.__self__ = this;
            this.__init__.__call__.apply(vm, [args, kwargs]);
        }
    };
    klass.__name__ = name;

    if (bases) {
        // load up the base attributes
        if (batavia.isArray(bases)) {
            throw new batavia.builtins.NotImplementedError("multiple inheritance not supported yet");
        }
        var base = bases.__class__;
        for (var attr in base) {
            if (base.hasOwnProperty(attr)) {
                klass[attr] = base[attr];
                klass.prototype[attr] = base[attr];
            }
        }
    }
    for (var attr in locals) {
        if (locals.hasOwnProperty(attr)) {
            klass[attr] = locals[attr];
            klass.prototype[attr] = locals[attr];
        }
    }
    klass.prototype.__class__ = new batavia.types.Type(name, bases);

    var PyObject = function(vm, klass, name) {
        var __new__ = function(args, kwargs) {
            return new klass(vm, args, kwargs);
        };
        __new__.__python__ = true;
        __new__.__class__ = klass;
        return __new__;
    }(this, klass, name);
    PyObject.__class__ = klass;

    return PyObject;
};

/*************************************************************************
 * callable construction
 *************************************************************************/

batavia.make_callable = function(func) {
    var fn = function(args, kwargs, locals) {
        var retval;
        var callargs = batavia.modules.inspect.getcallargs(func, args, kwargs);

        var frame = this.make_frame({
            'code': func.__code__,
            'callargs': callargs,
            'f_globals': func.__globals__,
            'f_locals': locals || new batavia.types.JSDict()
        });

        if (func.__code__.co_flags & batavia.modules.dis.CO_GENERATOR) {
            gen = new batavia.core.Generator(frame, this);
            frame.generator = gen;
            retval = gen;
        } else {
            retval = this.run_frame(frame);
        }
        return retval;
    };
    fn.__python__ = true;
    return fn;
};

batavia.run_callable = function(self, func, posargs, namedargs) {
    // Here you are in JS-land, and you want to call a method on an object
    // but what kind of callable is it?  You may not know if you were passed
    // the function as an argument.

    // TODO: consider separating these out, which might make things more
    //   efficient, but this at least consolidates the use-cases.

    // This gets the right js-callable thing, and runs it in the VirtualMachine.

    // There are a couple of scenarios:
    // 1. You *are* the virtual machine, and you want to call it:
    //    See batavia.VirtualMachine.prototype.call_function
    //    run_callable(<virtualmachine.is_vm=true>, <python method>, ...)
    //    i.e. run_callable(this, func, posargs, namedargs_dict)
    // 2. You are in a JS-implemented type, and the method or object is
    //    e.g. batavia/types/Map.js,Filter.js
    //    run_callable(<python_parent_obj>, <python_method (with func._vm)>, ...)
    //    If you are just passed an anonymous method:
    //    run_callable(<falsish>, <python_method (with func._vm)>, ...)
    // 3. You are in a builtin called by javascript and you also don't
    //    know the provenance of the object/function
    //    e.g. iter() called internally by types/Map.js
    //    see #2 scenario

    //the VM should pass itself in self, but if it already blessed
    //  a method with itself on ._vm just use that.
    var vm = (func._vm) ? func._vm : self;

    if (self && !self.is_vm && func.__python__ && !func.__self__) {
        // In scenarios 2,3 the VM would normally be doing this
        // at the moment of getting the function through LOAD_ATTR
        // but if we call it by JS, then it still needs to be
        // decorated with itself
        func = new batavia.types.Method(self, func);
        // Note, we change func above, so it can get __self__
        // and be affected by the code-path below
    }

    if ('__python__' in func && '__self__' in func) {
        // A python-style method
        // Methods calls get self as an implicit first parameter.
        if (func.__self__) {
            posargs.unshift(func.__self__);
        }

        // The first parameter must be the correct type.
        if (posargs[0] instanceof func.constructor) {
            throw 'unbound method ' + func.__func__.__name__ + '()' +
                ' must be called with ' + func.__class__.__name__ + ' instance ' +
                'as first argument (got ' + posargs[0].prototype + ' instance instead)';
        }
        func = func.__func__.__call__;
    } else if ('__call__' in func) {
        // A Python callable
        func = func.__call__;
    } else if (func.prototype) {
        // If this is a native Javascript class constructor, wrap it
        // in a method that uses the Python calling convention, but
        // instantiates the object.
        if (!func.__python__ && Object.keys(func.prototype).length > 0) {
            func = function(fn) {
                return function(args, kwargs) {
                    var obj = Object.create(fn.prototype);
                    fn.apply(obj, args);
                    return obj;
                };
            }(func);
        }
    }

    var retval = func.apply(vm, [posargs, namedargs]);
    return retval;
};

// make a proxy object that forwards function calls to the parent class
// TODO: forward all function calls
// TODO: support multiple inheritance
batavia.make_super = function(frame, args) {
    // I guess we have to examine the stack to find out which class we are in?
    // this seems suboptimal...
    // what does CPython do?
    if (args.length != 0) {
        throw new batavia.builtins.NotImplementedError("super does not support arguments yet")
    }
    if (frame.f_code.co_name != '__init__') {
        throw new batavia.builtins.NotImplementedError("super not implemented outside of __init__ yet");
    }
    if (frame.f_code.co_argcount == 0) {
        throw new batavia.builtins.TypeError("no self found in super in __init__");
    }
    var self_name = frame.f_code.co_varnames[0];
    var self = frame.f_locals[self_name];
    var klass = self.__class__;
    if (klass.__bases__.length != 1) {
        throw new batavia.builtins.NotImplementedError("super not implemented for multiple inheritance yet");
    }

    var base = klass.__base__;

    var obj = {
        '__init__': function(args, kwargs) {
            return batavia.run_callable(self, base.__init__, args, kwargs);
        }
    };
    obj.__init__.__python__ = true;
    return obj;
};

/************************
 * Working with iterables
 ************************/

// Iterate a python iterable to completion,
// calling a javascript callback on each item that it yields.
batavia.iter_for_each = function(iterobj, callback) {
    try {
        while (true) {
            var next = batavia.run_callable(iterobj, iterobj.__next__, [], null);
            callback(next);
        }
    } catch (err) {
        if (!(err instanceof batavia.builtins.StopIteration)) {
            throw err;
        }
    }
};

batavia.js2py = function(arg) {
    if (batavia.isArray(arg)) {
        // recurse
        var arr = new batavia.types.List();
        for (var i = 0; i < arg.length; i++) {
            arr.append(batavia.js2py(arg[i]));
        }
        return arr;
    }

    switch (typeof arg) {
        case 'boolean':
            return arg;
        case 'number':
            if (Number.isInteger(arg)) {
                return new batavia.types.Int(arg);
            } else {
              return new batavia.types.Float(arg);
            }
        case 'string':
            return new batavia.types.Str(arg);
        case 'object':
            if (arg === null || arg === batavia.types.NoneType) {
                return null;
            } else if (arg.__class__ != null && arg.__class__.__name__) {
                // already a Python object
                return arg;
            } else {
                // this is a generic object; turn it into a dictionary
                var dict = new batavia.types.Dict();
                for (var k in arg) {
                    if (arg.hasOwnProperty(k)) {
                        dict[batavia.js2py(k)] = batavia.js2py(arg[k])
                    }
                }
                return dict;
            }
        default:
            throw new batavia.builtins.BataviaError("Unknown type " + (typeof arg));
    }
}

/*************************************************************************
 * A base Python object
 *************************************************************************/

batavia.types.Object = function() {
    function PyObject(args, kwargs) {
        Object.call(this);
        if (args) {
            this.update(args);
        }
    }

    PyObject.prototype = Object.create(Object.prototype);

    return PyObject;
}();


/*************************************************************************
 * A Python type
 *************************************************************************/

batavia.types.Type = function() {
    function Type(name, bases, dict) {
        this.__name__ = name;
        // TODO: we're kind of sloppy about if we are using an instance of the class or the class itself. We should really think this through. Especially in mro().
        if (bases && batavia.isArray(bases)) {
            this.__base__ = bases[0].__class__;
            this.__bases__ = [];
            for (var base = 0; base < bases.length; base++) {
                this.__bases__.push(bases[base].__class__);
            }
        } else if (bases) {
            this.__base__ = bases.__class__;
            this.__bases__ = [this.__base__];
        } else if (name === 'object' && bases === undefined) {
            this.__base__ = batavia.builtins.None;
            this.__bases__ = [];
        } else {
            this.__base__ = batavia.types.Object.prototype.__class__;
            this.__bases__ = [batavia.types.Object.prototype.__class__];
        }
        this.dict = dict;
    }

    Type.prototype = Object.create(Object.prototype);
    Type.prototype.__class__ = new Type('type');

    Type.prototype.toString = function() {
        return this.__repr__();
    };

    Type.prototype.__repr__ = function() {
        // True primitive types won't have __bases__ defined.
        if (this.__bases__) {
            return "<class '" + this.__name__ + "'>";
        } else {
            return this.__name__;
        }
    };

    Type.prototype.__str__ = function() {
        return this.__repr__();
    };

    Type.prototype.valueOf = function() {
        return this.prototype;
    };

    Type.prototype.mro = function() {
        // Cache the MRO on the __mro__ attribute
        if (this.__mro__ === undefined) {
            // Self is always the first port of call for the MRO
            this.__mro__ = [this];
            if (this.__bases__) {
                // Now traverse and add the base classes.
                for (var b in this.__bases__) {
                    this.__mro__.push(this.__bases__[b]);
                    var submro = this.__bases__[b].mro();
                    for (var sub in submro) {
                        // If the base class is already in the MRO,
                        // push it to the end of the MRO list.
                        var index = this.__mro__.indexOf(submro[sub]);
                        if (index !== -1) {
                            this.__mro__.splice(index, 1);
                        }
                        this.__mro__.push(submro[sub]);
                    }
                }
            } else {
                // Primitives have no base class;
                this.__mro__ = [this];
            }
        }
        return this.__mro__;
    };

    return Type;
}();

batavia.types.Object.__class__ = new batavia.types.Type('object');
batavia.types.Object.prototype.__class__ = batavia.types.Object.__class__;

/*************************************************************************
 * Modify Boolean to behave like a Python bool
 *************************************************************************/

batavia.types.Bool = Boolean;
Boolean.prototype.__class__ = new batavia.types.Type('bool');

/**************************************************
 * Type conversions
 **************************************************/

Boolean.prototype.__bool__ = function() {
    return this.valueOf();
};

Boolean.prototype.__repr__ = function(args, kwargs) {
    return this.__str__();
};

Boolean.prototype.__str__ = function(args, kwargs) {
    if (this.valueOf()) {
        return "True";
    } else {
        return "False";
    }
};

Boolean.prototype.__float__ = function() {
    return new batavia.types.Float(this.valueOf() ? 1.0 : 0.0);
};

/**************************************************
 * Comparison operators
 **************************************************/

Boolean.prototype.__lt__ = function(other) {
    return this.valueOf() < other;
};

Boolean.prototype.__le__ = function(other) {
    return this.valueOf() <= other;
};

Boolean.prototype.__eq__ = function(other) {
    return this.valueOf() == other;
};

Boolean.prototype.__ne__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Str)) {
            return batavia.types.Bool(true);
    }
    return this.valueOf() != other;
};

Boolean.prototype.__gt__ = function(other) {

  var invalid_types = [
    batavia.types.Bytearray,
    batavia.types.Bytes,
    batavia.types.Complex,
    batavia.types.Dict,
    batavia.types.FrozenSet,
    batavia.types.List,
    batavia.types.NoneType,
    batavia.types.NotImplementedType,
    batavia.types.Range,
    batavia.types.Set,
    batavia.types.Slice,
    batavia.types.Str,
    batavia.types.Tuple,
    batavia.types.Type,
  ];

  if (batavia.isinstance(other, invalid_types)) {
      throw new batavia.builtins.TypeError('unorderable types: bool() > ' + batavia.type_name(other) + '()');
    }

    return this.valueOf() > other;
};

Boolean.prototype.__ge__ = function(other) {
    return this.valueOf() >= other;
};

Boolean.prototype.__contains__ = function(other) {
    return false;
};


/**************************************************
 * Unary operators
 **************************************************/

Boolean.prototype.__pos__ = function() {
    return +this.valueOf();
};

Boolean.prototype.__neg__ = function() {
    return -this.valueOf();
};

Boolean.prototype.__not__ = function() {
    return !this.valueOf();
};

Boolean.prototype.__invert__ = function() {
    return ~this.valueOf();
};

Boolean.prototype.__int__ = function() {
    if (this.valueOf() === true) {
        return new batavia.types.Int(1);
    } else {
        return new batavia.types.Int(0);
    }
};

/**************************************************
 * Binary operators
 **************************************************/

Boolean.prototype.__pow__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Bool)) {
        if (this.valueOf() && other.valueOf()) {
            return new batavia.types.Int(1);
        } else if (this.valueOf()) {
            return new batavia.types.Int(1);
        } else if (other.valueOf()) {
            return new batavia.types.Int(0);
        } else {
            return new batavia.types.Int(1);
        }
    } else if (batavia.isinstance(other, [batavia.types.Float, batavia.types.Int])) {
        if (this.valueOf()) {
            if (batavia.isinstance(other, batavia.types.Int) && other.__ge__(new batavia.types.Float(0.0))) {
                return new batavia.types.Int(Math.pow(1, other.valueOf()));
            } else {
                return new batavia.types.Float(Math.pow(1.0, other.valueOf()));
            }
        } else {
            if (other.__lt__(new batavia.types.Float(0.0))) {
                throw new batavia.builtins.ZeroDivisionError("0.0 cannot be raised to a negative power");
            } else if (batavia.isinstance(other, batavia.types.Int)) {
                return new batavia.types.Int(Math.pow(0, other.valueOf()));
            } else {
                return new batavia.types.Float(Math.pow(0.0, other.valueOf()));
            }
        }
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for pow: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__div__ = function(other) {
    return this.__truediv__(other);
};

Boolean.prototype.__floordiv__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Bool)) {
        if (!other.valueOf()) {
            throw new batavia.builtins.ZeroDivisionError("integer division or modulo by zero");
        } else if (this.valueOf() && other.valueOf()) {
            return new batavia.types.Int(1);
        } else {
            return new batavia.types.Int(0);
        }
    } else if (batavia.isinstance(other, [batavia.types.Float, batavia.types.Int])) {
        var thisValue;
        var message = "";

        if (batavia.isinstance(other, batavia.types.Int)) {
            thisValue = this.valueOf() ? 1 : 0;
            message = "integer division or modulo by zero";
        } else {
            thisValue = this.valueOf() ? 1.0 : 0.0;
            message = "float divmod()";
        }

        var roundedVal = Math.floor(thisValue / other);

        if (other === 0) {
            throw new batavia.builtins.ZeroDivisionError(message);
        } else if (batavia.isinstance(other, batavia.types.Int)) {
            return new batavia.types.Int(roundedVal);
        } else {
            return new batavia.types.Float(roundedVal);
        }
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__truediv__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'bool' and '" + batavia.type_name(other) + "'");
};

Boolean.prototype.__mul__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Bool)) {
        if (this.valueOf() && other.valueOf()) {
            return new batavia.types.Int(1);
        } else {
            return new batavia.types.Int(0);
        }
    } else if (batavia.isinstance(other, batavia.types.Float)) {
        return new batavia.types.Float((this.valueOf() ? 1.0 : 0.0) * other.valueOf());
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return new batavia.types.Int((this.valueOf() ? 1 : 0) * other.valueOf());
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'bool' and '" + batavia.type_name(other) + "'");
    }};

Boolean.prototype.__mod__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for %: 'bool' and '" + batavia.type_name(other) + "'");
};

Boolean.prototype.__add__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Bool)) {
        if (this.valueOf() && other.valueOf()) {
            return new batavia.types.Int(2);
        } else if (this.valueOf() || other.valueOf()) {
            return new batavia.types.Int(1);
        } else {
            return new batavia.types.Int(0);
        }
    } else if (batavia.isinstance(other, batavia.types.Float)) {
        return new batavia.types.Float((this.valueOf() ? 1.0 : 0.0) + other.valueOf());
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return new batavia.types.Int(other.val.add(this.valueOf() ? 1 : 0));
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__sub__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Bool)) {
        if (this.valueOf() && other.valueOf()) {
            return new batavia.types.Int(0);
        } else if (this.valueOf()) {
            return new batavia.types.Int(1);
        } else if (other.valueOf()) {
            return new batavia.types.Int(-1);
        } else {
            return new batavia.types.Int(0);
        }
    } else if (batavia.isinstance(other, batavia.types.Float)) {
        return new batavia.types.Float((this.valueOf() ? 1.0 : 0.0) - other.valueOf());
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return new batavia.types.Int(other.val.sub(this.valueOf() ? 1 : 0).neg());
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__getitem__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__getitem__ has not been implemented");
};

Boolean.prototype.__lshift__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Bool)) {
        if (this.valueOf() && other.valueOf()) {
            return new batavia.types.Int(2);
        } else if (this.valueOf()) {
            return new batavia.types.Int(1);
        } else if (other.valueOf()) {
            return new batavia.types.Int(0);
        } else {
            return new batavia.types.Int(0);
        }
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return new batavia.types.Int((this.valueOf() ? 1 : 0) << other.valueOf());
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for <<: 'bool' and '" + batavia.type_name(other) + "'");
    }};

Boolean.prototype.__rshift__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Bool)) {
        if (this.valueOf() && !other.valueOf()) {
            return new batavia.types.Int(1);
        } else {
            return new batavia.types.Int(0);
        }
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return new batavia.types.Int((this.valueOf() ? 1 : 0) >> other.valueOf());
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for >>: 'bool' and '" + batavia.type_name(other) + "'");
    }};

Boolean.prototype.__and__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Int)) {
        return this.__int__().__and__(other);
    } else if (batavia.isinstance(other, batavia.types.Bool)) {
        return new Boolean((this.valueOf() ? 1 : 0) & (other.valueOf() ? 1 : 0));
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__xor__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Int)) {
        return this.__int__().__xor__(other);
    } else if (batavia.isinstance(other, batavia.types.Bool)) {
        return new Boolean((this.valueOf() ? 1 : 0) ^ (other.valueOf() ? 1 : 0));
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ^: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__or__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Int)) {
        return this.__int__().__or__(other);
    } else if (batavia.isinstance(other, batavia.types.Bool)) {
        return new Boolean((this.valueOf() ? 1 : 0) | (other.valueOf() ? 1 : 0));
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__ge__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Float)) {
        return new batavia.types.Float((this.valueOf() ? 1.0 : 0.0) >= other.valueOf());
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return this.__int__().__ge__(other);
    } else if (batavia.isinstance(other, batavia.types.Bool)) {
        return new Boolean((this.valueOf() ? 1 : 0) >= (other.valueOf() ? 1 : 0));
    } else if (batavia.isbataviainstance(other)) {
        throw new batavia.builtins.TypeError("unorderable types: bool() >= " + batavia.type_name(other) + "()");
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__le__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Float)) {
        return new batavia.types.Float((this.valueOf() ? 1.0 : 0.0) <= other.valueOf());
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return this.__int__().__le__(other);
    } else if (batavia.isinstance(other, batavia.types.Bool)) {
        return new Boolean((this.valueOf() ? 1 : 0) <= (other.valueOf() ? 1 : 0));
    } else if (batavia.isbataviainstance(other)) {
        throw new batavia.builtins.TypeError("unorderable types: bool() <= " + batavia.type_name(other) + "()");
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

Boolean.prototype.__lt__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Float)) {
        return new batavia.types.Float((this.valueOf() ? 1.0 : 0.0) < other.valueOf());
    } else if (batavia.isinstance(other, batavia.types.Int)) {
        return this.__int__().__lt__(other);
    } else if (batavia.isinstance(other, batavia.types.Bool)) {
        int_one = new batavia.types.Int(1);
        int_zero= new batavia.types.Int(0);

        return (this.valueOf() ? int_one : int_zero) < (other.valueOf() ? int_one : int_zero);
    } else if (batavia.isbataviainstance(other)) {
        throw new batavia.builtins.TypeError("unorderable types: bool() < " + batavia.type_name(other) + "()");
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'bool' and '" + batavia.type_name(other) + "'");
    }
};

/**************************************************
 * Inplace operators
 **************************************************/

Boolean.prototype.__ifloordiv__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__ifloordiv__ has not been implemented");
};

Boolean.prototype.__itruediv__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__itruediv__ has not been implemented");
};

Boolean.prototype.__iadd__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__iadd__ has not been implemented");
};

Boolean.prototype.__isub__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__isub__ has not been implemented");
};

Boolean.prototype.__imul__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__imul__ has not been implemented");
};

Boolean.prototype.__imod__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__imod__ has not been implemented");
};

Boolean.prototype.__ipow__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__ipow__ has not been implemented");
};

Boolean.prototype.__ilshift__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__ilshift__ has not been implemented");
};

Boolean.prototype.__irshift__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__irshift__ has not been implemented");
};

Boolean.prototype.__iand__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__iand__ has not been implemented");
};

Boolean.prototype.__ixor__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__ixor__ has not been implemented");
};

Boolean.prototype.__ior__ = function(other) {
    throw new batavia.builtins.NotImplementedError("Boolean.__ior__ has not been implemented");
};

/**************************************************
 * Methods
 **************************************************/

Boolean.prototype.copy = function() {
    return this.valueOf();
};

Boolean.prototype.__trunc__ = function() {
    if (this.valueOf()) {
        return new batavia.types.Int(1);
    }
    return new batavia.types.Int(0);
};

/*************************************************************************
 * A Python bytes type
 *************************************************************************/

batavia.types.Bytearray = function() {
    function Bytearray(val) {
        this.val = val;
    }

    Bytearray.prototype = Object.create(Object.prototype);
    Bytearray.prototype.__class__ = new batavia.types.Type('bytearray');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Bytearray.prototype.toString = function () {
        return this.__str__();
    };

    Bytearray.prototype.valueOf = function() {
        return this.val;
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Bytearray.prototype.__bool__ = function() {
        return this.size() !== 0;
    };

    Bytearray.prototype.__repr__ = function() {
        return this.__str__();
    };

    Bytearray.prototype.__str__ = function() {
        return "bytearray(" +  this.val.toString() + ")";
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Bytearray.prototype.__lt__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() < other;
        }
        return false;
    };

    Bytearray.prototype.__le__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() <= other;
        }
        return false;
    };

    Bytearray.prototype.__eq__ = function(other) {
        if (other !== batavia.builtins.None) {
            var val;
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Int, batavia.types.Float])
                    ) {
                return false;
            } else {
                return this.valueOf() === val;
            }
        }
        return this.valueOf() === '';
    };

    Bytearray.prototype.__ne__ = function(other) {
        if (other !== batavia.builtins.None) {
            var val;
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Int, batavia.types.Float])
                    ) {
                return true;
            } else {
                return this.valueOf() !== val;
            }
        }
        return this.valueOf() !== '';
    };

    Bytearray.prototype.__gt__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() > other;
        }
        return false;
    };

    Bytearray.prototype.__ge__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() >= other;
        }
        return false;
    };

    Bytearray.prototype.__contains__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf().hasOwnProperty(other);
        }
        return false;
    };

    /**************************************************
     * Unary operators
     **************************************************/

    Bytearray.prototype.__pos__ = function() {
        return new Bytearray(+this.valueOf());
    };

    Bytearray.prototype.__neg__ = function() {
        return new Bytearray(-this.valueOf());
    };

    Bytearray.prototype.__not__ = function() {
        return new Bytearray(!this.valueOf());
    };

    Bytearray.prototype.__invert__ = function() {
        return new Bytearray(~this.valueOf());
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Bytearray.prototype.__pow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__pow__ has not been implemented");
    };

    Bytearray.prototype.__div__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__div__ has not been implemented");
    };

    Bytearray.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__floordiv__ has not been implemented");
    };

    Bytearray.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__truediv__ has not been implemented");
    };

    Bytearray.prototype.__mul__ = function(other) {
        throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type '" + batavia.type_name(other) + "'");
    };

    Bytearray.prototype.__mod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__mod__ has not been implemented");
    };

    Bytearray.prototype.__add__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__add__ has not been implemented");
    };

    Bytearray.prototype.__sub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__sub__ has not been implemented");
    };

    Bytearray.prototype.__getitem__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__getitem__ has not been implemented");
    };

    Bytearray.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__lshift__ has not been implemented");
    };

    Bytearray.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__rshift__ has not been implemented");
    };

    Bytearray.prototype.__and__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__and__ has not been implemented");
    };

    Bytearray.prototype.__xor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__xor__ has not been implemented");
    };

    Bytearray.prototype.__or__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__or__ has not been implemented");
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    Bytearray.prototype.__idiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__idiv__ has not been implemented");
    };

    Bytearray.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__ifloordiv__ has not been implemented");
    };

    Bytearray.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__itruediv__ has not been implemented");
    };

    Bytearray.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__iadd__ has not been implemented");
    };

    Bytearray.prototype.__isub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__isub__ has not been implemented");
    };

    Bytearray.prototype.__imul__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__imul__ has not been implemented");
    };

    Bytearray.prototype.__imod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__imod__ has not been implemented");
    };

    Bytearray.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__ipow__ has not been implemented");
    };

    Bytearray.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__ilshift__ has not been implemented");
    };

    Bytearray.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__irshift__ has not been implemented");
    };

    Bytearray.prototype.__iand__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__iand__ has not been implemented");
    };

    Bytearray.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__ixor__ has not been implemented");
    };

    Bytearray.prototype.__ior__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytearray.__ior__ has not been implemented");
    };

    /**************************************************
     * Methods
     **************************************************/

    Bytearray.prototype.copy = function() {
        return new Bytearray(this.valueOf());
    };

    /**************************************************/

    return Bytearray;
}();

/*************************************************************************
 * A Python bytes type
 *************************************************************************/

batavia.types.Bytes = function() {
    function Bytes(val) {
        this.val = val;
    }

    Bytes.prototype = Object.create(Object.prototype);
    Bytes.prototype.__class__ = new batavia.types.Type('bytes');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Bytes.prototype.toString = function () {
        return this.__str__();
    };

    Bytes.prototype.valueOf = function() {
        return this.val;
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Bytes.prototype.__bool__ = function() {
        return this.val.length > 0;
    };

    Bytes.prototype.__repr__ = function() {
        return this.__str__();
    };

    Bytes.prototype.__str__ = function() {
        return "b'" + String.fromCharCode.apply(null, this.val) + "'";
    };

    Bytes.prototype.__iter__ = function() {
        return new Bytes.prototype.BytesIterator(this.val);
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Bytes.prototype.__lt__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() < other;
        }
        return false;
    };

    Bytes.prototype.__le__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() <= other;
        }
        return false;
    };

    Bytes.prototype.__eq__ = function(other) {
        if (other !== batavia.builtins.None) {
            var val;
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Int, batavia.types.Float])
                    ) {
                return false;
            } else {
                return this.valueOf() === val;
            }
        }
        return this.valueOf() === '';
    };

    Bytes.prototype.__ne__ = function(other) {
        if (other !== batavia.builtins.None) {
            var val;
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Int, batavia.types.Float])
                    ) {
                return true;
            } else {
                return this.valueOf() !== val;
            }
        }
        return this.valueOf() !== '';
    };

    Bytes.prototype.__gt__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() > other;
        }
        return false;
    };

    Bytes.prototype.__ge__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf() >= other;
        }
        return false;
    };

    Bytes.prototype.__contains__ = function(other) {
        if (other !== batavia.builtins.None) {
            return this.valueOf().hasOwnProperty(other);
        }
        return false;
    };

    /**************************************************
     * Unary operators
     **************************************************/

    Bytes.prototype.__pos__ = function() {
        return new Bytes(+this.valueOf());
    };

    Bytes.prototype.__neg__ = function() {
        return new Bytes(-this.valueOf());
    };

    Bytes.prototype.__not__ = function() {
        return new Bytes(!this.valueOf());
    };

    Bytes.prototype.__invert__ = function() {
        return new Bytes(~this.valueOf());
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Bytes.prototype.__pow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__pow__ has not been implemented");
    };

    Bytes.prototype.__div__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__div__ has not been implemented");
    };

    Bytes.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__floordiv__ has not been implemented");
    };

    Bytes.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__truediv__ has not been implemented");
    };

    Bytes.prototype.__mul__ = function(other) {
        throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type '" + batavia.type_name(other) + "'");
    };

    Bytes.prototype.__mod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__mod__ has not been implemented");
    };

    Bytes.prototype.__add__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__add__ has not been implemented");
    };

    Bytes.prototype.__sub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__sub__ has not been implemented");
    };

    Bytes.prototype.__getitem__ = function(other) {
        return new batavia.types.Int(this.val[batavia.builtins.int(other).valueOf()]);
    };

    Bytes.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__lshift__ has not been implemented");
    };

    Bytes.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__rshift__ has not been implemented");
    };

    Bytes.prototype.__and__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__and__ has not been implemented");
    };

    Bytes.prototype.__xor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__xor__ has not been implemented");
    };

    Bytes.prototype.__or__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__or__ has not been implemented");
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    Bytes.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__ifloordiv__ has not been implemented");
    };

    Bytes.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__itruediv__ has not been implemented");
    };

    Bytes.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__iadd__ has not been implemented");
    };

    Bytes.prototype.__isub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__isub__ has not been implemented");
    };

    Bytes.prototype.__imul__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__imul__ has not been implemented");
    };

    Bytes.prototype.__imod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__imod__ has not been implemented");
    };

    Bytes.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__ipow__ has not been implemented");
    };

    Bytes.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__ilshift__ has not been implemented");
    };

    Bytes.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__irshift__ has not been implemented");
    };

    Bytes.prototype.__iand__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__iand__ has not been implemented");
    };

    Bytes.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__ixor__ has not been implemented");
    };

    Bytes.prototype.__ior__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Bytes.__ior__ has not been implemented");
    };

    /**************************************************
     * Methods
     **************************************************/

    Bytes.prototype.copy = function() {
        return new Bytes(this.valueOf());
    };

    /**************************************************
     * Bytes Iterator
     **************************************************/

    Bytes.prototype.BytesIterator = function(data) {
        Object.call(this);
        this.index = 0;
        this.data = data;
    };

    Bytes.prototype.BytesIterator.prototype = Object.create(Object.prototype);

    Bytes.prototype.BytesIterator.prototype.__iter__ = function() {
        return this;
    };

    Bytes.prototype.BytesIterator.prototype.__next__ = function() {
        if (this.index >= this.data.length) {
            throw new batavia.builtins.StopIteration();
        }
        var retval = this.data[this.index];
        this.index++;
        return new batavia.types.Int(retval);
    };

    Bytes.prototype.BytesIterator.prototype.__str__ = function() {
        return "<bytes_iterator object at 0x99999999>";
    };

    Bytes.prototype.BytesIterator.prototype.constructor = Bytes.prototype.BytesIterator;
    Bytes.prototype.BytesIterator.prototype.__class__ = new batavia.types.Type('bytes_iterator');

    /**************************************************/


    return Bytes;
}();

batavia.types.Code = function() {
    function Code(kwargs) {
        this.co_argcount = kwargs.argcount || 0;
        this.co_kwonlyargcount = kwargs.kwonlyargcount || 0;
        this.co_nlocals = kwargs.nlocals || 0;
        this.co_stacksize = kwargs.stacksize || 0;
        this.co_flags = kwargs.flags || 0;
        this.co_code = kwargs.code;
        this.co_consts = kwargs.consts || [];
        this.co_names = kwargs.names || [];
        this.co_varnames = kwargs.varnames || [];
        this.co_freevars = kwargs.freevars || [];
        this.co_cellvars = kwargs.cellvars || [];
        // co_cell2arg
        this.co_filename = kwargs.filename || '<string>';
        this.co_name = kwargs.name || '<module>';
        this.co_firstlineno = kwargs.firstlineno || 1;
        this.co_lnotab = kwargs.lnotab || '';
        // co_zombieframe
        // co_weakreflist
    }

    Code.prototype = Object.create(Object.prototype);
    Code.prototype.__class__ = new batavia.types.Type('code');

    return Code;
}();

/*************************************************************************
 * A Python complex type
 *************************************************************************/


batavia.types.Complex = function() {
    // Polyfill below from
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is#Polyfill_for_non-ES6_browsers
    if (!Object.is) {
      Object.is = function(x, y) {
        // SameValue algorithm
        if (x === y) { // Steps 1-5, 7-10
          // Steps 6.b-6.e: +0 != -0
          return x !== 0 || 1 / x === 1 / y;
        } else {
          // Step 6.a: NaN == NaN
          return x !== x && y !== y;
        }
      };
    }
    function part_from_str(s) {
        if (s && s.valueOf() == "-0") {
            // console.log("there");
            return new batavia.types.Float(-0);
        } else if (s) {
            // console.log("part_from_str: " + s);
            return new batavia.types.Float(s);
        } else {
            return new batavia.types.Float(0);
        }
    }
    function part_to_str(x) {
        var x_str;
        if (x) {
            x_str = x.valueOf().toString();
            var abs_len = Math.abs(x.valueOf()).toString().length;
            if (abs_len >= 19) {
                // force conversion to scientific
                var new_str = x.valueOf().toExponential();
                if (new_str.length < x_str.length) {
                    x_str = new_str;
                }
            }
        } else if (Object.is(x, -0)) {
            x_str = '-0';
        } else {
            x_str = '0';
        }
        return x_str;
    }
    function Complex(re, im) {
        // console.log(100000, re, im);
        if (batavia.isinstance(re, batavia.types.Str)) {
            // console.log(1000, re, im);
            var regex = /^\(?(-?[\d.]+)?([+-])?(?:([\d.]+)j)?\)?$/i;
            var match = regex.exec(re);
            if (match == null || re == "") {
                throw new batavia.builtins.ValueError("complex() arg is a malformed string");
            }
            this.real = parseFloat(part_from_str(match[1]));
            this.imag = parseFloat(part_from_str(match[3]));
            if (match[2] == '-') {
                this.imag = -this.imag;
            }
        } else if (!batavia.isinstance(re, [batavia.types.Float, batavia.types.Int, batavia.types.Bool, batavia.types.Complex])) {
            throw new batavia.builtins.TypeError(
                "complex() argument must be a string, a bytes-like object or a number, not '" + batavia.type_name(re) + "'"
            );
        } else if (!batavia.isinstance(im, [batavia.types.Float, batavia.types.Int, batavia.types.Bool, batavia.types.Complex])) {
            throw new batavia.builtins.TypeError(
                "complex() argument must be a string, a bytes-like object or a number, not '" + batavia.type_name(im) + "'"
            );
        } else if (typeof re == 'number' && typeof im == 'number') {
            this.real = re;
            this.imag = im;
        } else if (batavia.isinstance(re, [batavia.types.Float, batavia.types.Int, batavia.types.Bool]) &&
            batavia.isinstance(im, [batavia.types.Float, batavia.types.Int, batavia.types.Bool])) {
            // console.log(2000, re, im);
            this.real = re.__float__().valueOf();
            this.imag = im.__float__().valueOf();
        } else if (batavia.isinstance(re, batavia.types.Complex) && !im) {
            // console.log(3000, re, im);
            this.real = re.real;
            this.imag = re.imag;
        } else {
            throw new batavia.builtins.NotImplementedError("Complex initialization from complex argument(s) has not been implemented");
        }
    }

    Complex.prototype = Object.create(Object.prototype);
    Complex.prototype.__class__ = new batavia.types.Type('complex');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Complex.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Complex.prototype.__bool__ = function() {
        return Boolean(this.real || this.imag);
    };

    Complex.prototype.__iter__ = function() {
        return new Complex.prototype.ComplexIterator(this);
    };

    Complex.prototype.__repr__ = function() {
        return this.__str__();
    };

    Complex.prototype.__str__ = function() {
        if (this.real.valueOf() || Object.is(this.real, -0)) {
            return "(" + part_to_str(this.real) + (this.imag >= 0 ? "+" : "-") + part_to_str(Math.abs(this.imag)) + "j)";
        } else {
            return part_to_str(this.imag) + "j";
        }
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Complex.prototype.__lt__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: complex() < " + batavia.type_name(other) + "()");
    };

    Complex.prototype.__le__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: complex() <= " + batavia.type_name(other) + "()");
    };

    Complex.prototype.__eq__ = function(other) {
        if (other !== null && !batavia.isinstance(other, batavia.types.Str)) {
            if (batavia.isinstance(other, batavia.types.Complex)) {
                return this.real.valueOf() == other.real.valueOf() && this.imag.valueOf() == other.imag.valueOf();
            }
            var val;
            if (batavia.isinstance(other, batavia.types.Bool)) {
                val = other.valueOf() ? 1.0 : 0.0;
            } else {
                val = other.valueOf();
            }
            return this.real === val && this.imag == 0;
        }
        return false;
    };

    Complex.prototype.__ne__ = function(other) {
        return !this.__eq__(other);
    };

    Complex.prototype.__gt__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: complex() > " + batavia.type_name(other) + "()");
    };

    Complex.prototype.__ge__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: complex() >= " + batavia.type_name(other) + "()");
    };


    /**************************************************
     * Unary operators
     **************************************************/

    Complex.prototype.__pos__ = function() {
        return new Complex(this.real, this.imag);
    };

    Complex.prototype.__neg__ = function() {
        return new Complex(-this.real, -this.imag);
    };

    Complex.prototype.__not__ = function() {
        return !this.__bool__();
    };

    Complex.prototype.__invert__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary ~: 'complex'");
    };

    Complex.prototype.__abs__ = function() {
        return new batavia.types.Float(Math.sqrt(this.real * this.real + this.imag * this.imag));
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Complex.prototype.__pow__ = function(other) {
        // http://mathworld.wolfram.com/ComplexExponentiation.html
        throw new batavia.builtins.NotImplementedError(
            "Complex.__pow__ has not been implemented yet; if you need it, you need to reevaluate your life-choices."
        );
    };

    function __div__(x, y, inplace) {
        if (batavia.isinstance(y, batavia.types.Int)) {
            if (!y.val.isZero()) {
                return new Complex(x.real / y.__float__().val, x.imag / y.__float__().val);
            } else {
                throw new batavia.builtins.ZeroDivisionError("complex division by zero");
            }
        } else if (batavia.isinstance(y, batavia.types.Float)) {
            if (y.valueOf()) {
                return new Complex(x.real / y.valueOf(), x.imag / y.valueOf());
            } else {
                throw new batavia.builtins.ZeroDivisionError("complex division by zero");
            }
        } else if (batavia.isinstance(y, batavia.types.Bool)) {
            if (y.valueOf()) {
                return new Complex(x.real, x.imag);
            } else {
                throw new batavia.builtins.ZeroDivisionError("complex division by zero");
            }
        } else if (batavia.isinstance(y, batavia.types.Complex)) {
            var den = Math.pow(y.real, 2) + Math.pow(y.imag, 2);
            var num_real = x.real * y.real + x.imag * y.imag;
            var num_imag = x.imag * y.real - x.real * y.imag;
            var real = num_real / den;
            var imag = num_imag / den;
            return new Complex(real, imag);
        } else {
            throw new batavia.builtins.TypeError(
                "unsupported operand type(s) for /" + (inplace ? "=" : "") + ": 'complex' and '" + batavia.type_name(y) + "'"
            );
        }
    }

    Complex.prototype.__div__ = function(other) {
        return this.__truediv__(other);
    };

    Complex.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("can't take floor of complex number.");
    };

    Complex.prototype.__truediv__ = function(other) {
        return __div__(this, other);
    };

    function __mul__(x, y, inplace) {
        if (batavia.isinstance(y, batavia.types.Int)) {
            if (!y.val.isZero()) {
                return new Complex(x.real * y.__float__().val, x.imag * y.__float__().val);
            } else {
                return new Complex(0, 0);
            }
        } else if (batavia.isinstance(y, batavia.types.Float)) {
            if (y.valueOf()) {
                return new Complex(x.real * y.valueOf(), x.imag * y.valueOf());
            } else {
                return new Complex(0, 0);
            }
        } else if (batavia.isinstance(y, batavia.types.Bool)) {
            if (y.valueOf()) {
                return new Complex(x.real, x.imag);
            } else {
                return new Complex(0, 0);
            }
        } else if (batavia.isinstance(y, batavia.types.Complex)) {
            return new Complex(x.real * y.real - x.imag * y.imag, x.real * y.imag + x.imag * y.real);
        } else if (batavia.isinstance(y, [batavia.types.List, batavia.types.Str, batavia.types.Tuple])) {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'complex'");
        } else {
            throw new batavia.builtins.TypeError(
                "unsupported operand type(s) for *" + (inplace ? "=" : "") + ": 'complex' and '" + batavia.type_name(y) + "'"
            );
        }
    }

    Complex.prototype.__mul__ = function(other) {
        return __mul__(this, other);
    };

    Complex.prototype.__mod__ = function(other) {
        throw new batavia.builtins.TypeError("can't mod complex numbers.");
    };

    function __add__(x, y, inplace) {
        if (batavia.isinstance(y, batavia.types.Int)) {
            return new Complex(x.real + y.__float__().val, x.imag);
        } else if (batavia.isinstance(y, batavia.types.Float)) {
            return new Complex(x.real + y.valueOf(), x.imag);
        } else if (batavia.isinstance(y, batavia.types.Bool)) {
            return new Complex(x.real + (y.valueOf() ? 1.0 : 0.0), x.imag);
        } else if (batavia.isinstance(y, batavia.types.Complex)) {
            return new Complex(x.real + y.real, x.imag + y.imag);
        } else {
            throw new batavia.builtins.TypeError(
                "unsupported operand type(s) for +" + (inplace ? "=" : "") + ": 'complex' and '" + batavia.type_name(y) + "'"
            );
        }
    }

    Complex.prototype.__add__ = function(other) {
        return __add__(this, other);
    };

    function __sub__(x, y, inplace) {
        if (batavia.isinstance(y, batavia.types.Int)) {
            return new Complex(x.real - y.__float__().val, x.imag);
        } else if (batavia.isinstance(y, batavia.types.Float)) {
            return new Complex(x.real - y.valueOf(), x.imag);
        } else if (batavia.isinstance(y, batavia.types.Bool)) {
            return new Complex(x.real - (y.valueOf() ? 1.0 : 0.0), x.imag);
        } else if (batavia.isinstance(y, batavia.types.Complex)) {
            return new Complex(x.real - y.real, x.imag - y.imag);
        } else {
            throw new batavia.builtins.TypeError(
                "unsupported operand type(s) for -" + (inplace ? "=" : "") + ": 'complex' and '" + batavia.type_name(y) + "'"
            );
        }
    }

    Complex.prototype.__sub__ = function(other) {
        return __sub__(this, other);
    };

    Complex.prototype.__getitem__ = function(other) {
        throw new batavia.builtins.TypeError("'complex' object is not subscriptable")
    };

    Complex.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for <<: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for >>: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__and__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for &: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__xor__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for ^: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__or__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for |: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    Complex.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.TypeError("can't take floor of complex number.");
    };

    Complex.prototype.__itruediv__ = function(other) {
        return __div__(this, other, true);
    };

    Complex.prototype.__iadd__ = function(other) {
        return __add__(this, other, true);
    };

    Complex.prototype.__isub__ = function(other) {
        return __sub__(this, other, true);
    };

    Complex.prototype.__imul__ = function(other) {
        return __mul__(this, other, true);
    };

    Complex.prototype.__imod__ = function(other) {
        throw new batavia.builtins.TypeError("can't mod complex numbers.");
    };

    Complex.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Complex.__ipow__ has not been implemented");
    };

    Complex.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for <<=: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for >>=: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__iand__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for &=: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for ^=: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    Complex.prototype.__ior__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for |=: 'complex' and '" + batavia.type_name(other) + "'"
        );
    };

    /**************************************************
     * Methods
     **************************************************/

    Complex.prototype.add = function(v) {
        this[v] = null;
    };

    Complex.prototype.copy = function() {
        return new Complex(this);
    };

    Complex.prototype.remove = function(v) {
        delete this[v];
    };

    Complex.prototype.update = function(values) {
        for (var value in values) {
            if (values.hasOwnProperty(value)) {
                this[values[value]] = null;
            }
        }
    };

    /**************************************************
     * Complex Iterator
     **************************************************/

    Complex.prototype.ComplexIterator = function (data) {
        Object.call(this);
        this.index = 0;
        this.data = data;
    };

    Complex.prototype.ComplexIterator.prototype = Object.create(Object.prototype);

    Complex.prototype.ComplexIterator.prototype.__next__ = function() {
        var retval = this.data[this.index];
        if (retval === undefined) {
            throw new batavia.builtins.StopIteration();
        }
        this.index++;
        return retval;
    };

    Complex.prototype.ComplexIterator.prototype.__str__ = function() {
        return "<set_iterator object at 0x99999999>";
    };

    /**************************************************/

    return Complex;
}();
/*************************************************************************
 * A Python dict type wrapping JS objects
 *************************************************************************/

batavia.types.JSDict = function() {
    function JSDict(args, kwargs) {
        Object.call(this);
        if (args) {
            this.update(args);
        }
    }

    JSDict.prototype = Object.create(Object.prototype);
    JSDict.prototype.__class__ = new batavia.types.Type('jsdict');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    JSDict.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    JSDict.prototype.__bool__ = function() {
        return Object.keys(this).length > 0;
    };

    JSDict.prototype.__repr__ = function() {
        return this.__str__();
    };

    JSDict.prototype.__str__ = function() {
        var result = "{", values = [];
        for (var key in this) {
            if (this.hasOwnProperty(key)) {
                values.push(batavia.builtins.repr([key], null) + ": " + batavia.builtins.repr([this[key]], null));
            }
        }
        result += values.join(', ');
        result += "}";
        return result;
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    JSDict.prototype.__lt__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isinstance(other, [
                         batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                         batavia.types.Int, batavia.types.JSDict, batavia.types.List,
                         batavia.types.NoneType, batavia.types.Str, batavia.types.Tuple
                    ])) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() < " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() < other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() < NoneType()");
         }
        return this.valueOf() < other;
    };

    JSDict.prototype.__le__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isinstance(other, [
                         batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                         batavia.types.Int, batavia.types.JSDict, batavia.types.List,
                         batavia.types.NoneType, batavia.types.Str, batavia.types.Tuple
                    ])) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() <= " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() <= other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() <= NoneType()");
         }
    };

    JSDict.prototype.__eq__ = function(other) {
        return this.valueOf() == other;
    };

    JSDict.prototype.__ne__ = function(other) {
        return this.valueOf() != other;
    };

    JSDict.prototype.__gt__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isinstance(other, [
                         batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                         batavia.types.Int, batavia.types.JSDict, batavia.types.List,
                         batavia.types.NoneType, batavia.types.Set, batavia.types.Str,
                         batavia.types.Tuple
                    ])) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() > " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() > other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() > NoneType()");
         }
    };

    JSDict.prototype.__ge__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isinstance(other, [
                         batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                         batavia.types.Int, batavia.types.JSDict, batavia.types.List,
                         batavia.types.NoneType, batavia.types.Str, batavia.types.Tuple
                    ])) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() >= " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() >= other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() >= NoneType()");
         }
    };

    JSDict.prototype.__contains__ = function(other) {
        return this.valueOf().hasOwnProperty(other);
    };

    /**************************************************
     * Unary operators
     **************************************************/

    JSDict.prototype.__pos__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary +: 'jsdict'");
    };

    JSDict.prototype.__neg__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary -: 'jsdict'");
    };

    JSDict.prototype.__not__ = function() {
        return this.__bool__().__not__();
    };

    JSDict.prototype.__invert__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary ~: 'jsdict'");
    };

    /**************************************************
     * Binary operators
     **************************************************/

    JSDict.prototype.__pow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'jsdict' and '" + batavia.type_name(other) + "'");
    };

    JSDict.prototype.__div__ = function(other) {
        return this.__truediv__(other);
    };

    JSDict.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'jsdict' and '" + batavia.type_name(other) + "'");
    };

    JSDict.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'jsdict' and '" + batavia.type_name(other) + "'");
    };

    JSDict.prototype.__mul__ = function(other) {
        if (batavia.isinstance(other, [
                batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                batavia.types.JSDict, batavia.types.Int, batavia.types.NoneType])) {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'jsdict' and '" + batavia.type_name(other) + "'");
        } else {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'jsdict'");
        }
    };

    JSDict.prototype.__mod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__mod__ has not been implemented");
    };

    JSDict.prototype.__add__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'jsdict' and '" + batavia.type_name(other) + "'");
    };

    JSDict.prototype.__sub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'jsdict' and '" + batavia.type_name(other) + "'");
    };

    JSDict.prototype.__setitem__ = function(key, value) {
        this[key] = value;
    };

    JSDict.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__lshift__ has not been implemented");
    };

    JSDict.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__rshift__ has not been implemented");
    };

    JSDict.prototype.__and__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'jsdict' and '" + batavia.type_name(other) + "'");
    };

    JSDict.prototype.__xor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__xor__ has not been implemented");
    };

    JSDict.prototype.__or__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__or__ has not been implemented");
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    JSDict.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ifloordiv__ has not been implemented");
    };

    JSDict.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__itruediv__ has not been implemented");
    };

    JSDict.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__iadd__ has not been implemented");
    };

    JSDict.prototype.__isub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__isub__ has not been implemented");
    };

    JSDict.prototype.__imul__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__imul__ has not been implemented");
    };

    JSDict.prototype.__imod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__imod__ has not been implemented");
    };

    JSDict.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ipow__ has not been implemented");
    };

    JSDict.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ilshift__ has not been implemented");
    };

    JSDict.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__irshift__ has not been implemented");
    };

    JSDict.prototype.__iand__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__iand__ has not been implemented");
    };

    JSDict.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ixor__ has not been implemented");
    };

    JSDict.prototype.__ior__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ior__ has not been implemented");
    };

    JSDict.prototype.__getitem__ = function(other) {
        var value = this[other];
        if (value === undefined) {
            throw new batavia.builtins.KeyError(other === null ? 'None': other.__str__());
        }
        return value;
    };

    JSDict.prototype.__delitem__ = function(key) {
        if (!this.__contains__(key)) {
            throw new batavia.builtins.KeyError(key === null ? 'None': key);
        }
        delete this[key];
    };

    /**************************************************
     * Methods
     **************************************************/

    JSDict.prototype.get = function(key, backup) {
        if (this.__contains__(key)) {
            return this[key];
        } else if (typeof backup === 'undefined') {
            throw new batavia.builtins.KeyError(key === null ? 'None': key);
        } else {
            return backup;
        }
    };

    JSDict.prototype.update = function(values) {
        for (var key in values) {
            if (values.hasOwnProperty(key)) {
                this[key] = values[key];
            }
        }
    };

    JSDict.prototype.copy = function() {
        return new JSDict(this);
    };

    JSDict.prototype.items = function() {
        var result = new batavia.types.List();
        for (var key in this) {
            if (this.hasOwnProperty(key)) {
                result.append(new batavia.types.Tuple([key, this[key]]));
            }
        }
        return result;
    };

    JSDict.prototype.keys = function() {
        var result = [];
        for (var key in this) {
            if (this.hasOwnProperty(key)) {
                result.push(key);
            }
        }
        return new batavia.types.List(result);
    };

    JSDict.prototype.__iter__ = function() {
        return this.keys().__iter__();
    };

    JSDict.prototype.values = function() {
        var result = [];
        for (var key in this) {
            if (this.hasOwnProperty(key)) {
                result.push(this[key]);
            }
        }
        return new batavia.types.List(result);
    };

    JSDict.prototype.clear = function() {
        for (var key in this) {
            delete this[key];
        }
    };

    return JSDict;
}();
/*************************************************************************
 * A Python dict type
 *************************************************************************/

/*
 * Implementation details: we use closed hashing, open addressing,
 * with linear probing and a max load factor of 0.75.
 */

batavia.types.Dict = function() {
    function Dict(args, kwargs) {
        this.data_keys = [];
        this.data_values = [];
        this.size = 0;
        this.mask = 0;

        if (args) {
            this.update(args);
        }
    }

    Dict.prototype.__class__ = new batavia.types.Type('dict');

    var MAX_LOAD_FACTOR = 0.75;
    var INITIAL_SIZE = 8; // after size 0

    /**
     * Sentinel keys for empty and deleted.
     */
    var EMPTY = {
        __hash__: function() {
            return new batavia.types.Int(0);
        },
        __eq__: function(other) {
            return new batavia.types.Bool(this === other);
        }
    };

    var DELETED = {
        __hash__: function() {
            return new batavia.types.Int(0);
        },
        __eq__: function(other) {
            return new batavia.types.Bool(this === other);
        }
    };

    Dict.prototype._increase_size = function() {
        // increase the table size and rehash
        if (this.data_keys.length == 0) {
            this.mask = INITIAL_SIZE - 1;
            this.data_keys = new Array(INITIAL_SIZE);
            this.data_values = new Array(INITIAL_SIZE);

            for (var i = 0; i < INITIAL_SIZE; i++) {
                this.data_keys[i] = EMPTY;
            }
            return;
        }

        var new_keys = new Array(this.data_keys.length * 2);
        var new_values = new Array(this.data_keys.length * 2);
        var new_mask = this.data_keys.length * 2 - 1; // assumes power of two
        for (var i = 0; i < new_keys.length; i++) {
            new_keys[i] = EMPTY;
        }
        batavia.iter_for_each(batavia.builtins.iter([this.items()], null), function(val) {
            var key = val[0];
            var value = val[1];
            var hash = batavia.builtins.hash([key], null);
            var h = hash.int32() & new_mask;
            while (!isEmpty(new_keys[h])) {
                h = (h + 1) & new_mask;
            }
            new_keys[h] = key;
            new_values[h] = value;
        });
        this.data_keys = new_keys;
        this.data_values = new_values;
        this.mask = new_mask;
    };

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Dict.prototype.toString = function() {
        return this.__str__();
    };


    /**************************************************
     * Type conversions
     **************************************************/

    Dict.prototype.__bool__ = function() {
        return this.size > 0;
    };

    Dict.prototype.__repr__ = function() {
        return this.__str__();
    };

    var isDeleted = function(x) {
      return x !== null &&
          batavia.builtins.hash([x], null).__eq__(new batavia.types.Int(0)).valueOf() &&
          x.__eq__(DELETED).valueOf();
    };

    var isEmpty = function(x) {
        return x !== null &&
            batavia.builtins.hash([x], null).__eq__(new batavia.types.Int(0)).valueOf() &&
            x.__eq__(EMPTY).valueOf();
    };


    Dict.prototype.__str__ = function() {
        var result = "{";
        var strings = [];
        for (var i = 0; i < this.data_keys.length; i++) {
            // ignore deleted or empty
            var key = this.data_keys[i];
            if (isEmpty(key) || isDeleted(key)) {
                continue;
            }
            strings.push(batavia.builtins.repr([key], null) + ": " + batavia.builtins.repr([this.data_values[i]], null));
        }
        result += strings.join(", ");
        result += "}";
        return result;
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Dict.prototype.__lt__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isbataviainstance(other)) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() < " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() < other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() < NoneType()");
         }
        return this.valueOf() < other;
    };

    Dict.prototype.__le__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isbataviainstance(other)) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() <= " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() <= other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() <= NoneType()");
         }
    };

    Dict.prototype.__eq__ = function(other) {
        return this.valueOf() == other;
    };

    Dict.prototype.__ne__ = function(other) {
        return this.valueOf() != other;
    };

    Dict.prototype.__gt__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isbataviainstance(other)) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() > " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() > other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() > NoneType()");
         }
    };

    Dict.prototype.__ge__ = function(other) {
         if (other !== batavia.builtins.None) {
             if (batavia.isbataviainstance(other)) {
                 throw new batavia.builtins.TypeError("unorderable types: dict() >= " + batavia.type_name(other) + "()");
             } else {
                 return this.valueOf() >= other.valueOf();
             }
         } else {
             throw new batavia.builtins.TypeError("unorderable types: dict() >= NoneType()");
         }
    };

    /**************************************************
     * Unary operators
     **************************************************/

    Dict.prototype.__pos__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary +: 'dict'");
    };

    Dict.prototype.__neg__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary -: 'dict'");
    };

    Dict.prototype.__not__ = function() {
        return this.__bool__().__not__();
    };

    Dict.prototype.__invert__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary ~: 'dict'");
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Dict.prototype.__pow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'dict' and '" + batavia.type_name(other) + "'");
    };

    Dict.prototype.__div__ = function(other) {
        return this.__truediv__(other);
    };

    Dict.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'dict' and '" + batavia.type_name(other) + "'");
    };

    Dict.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'dict' and '" + batavia.type_name(other) + "'");
    };

    Dict.prototype.__mul__ = function(other) {
        if (batavia.isinstance(other, [
                batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                batavia.types.JSDict, batavia.types.Int, batavia.types.NoneType])) {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'dict' and '" + batavia.type_name(other) + "'");
        } else {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'dict'");
        }
    };

    Dict.prototype.__mod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__mod__ has not been implemented");
    };

    Dict.prototype.__add__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'dict' and '" + batavia.type_name(other) + "'");
    };

    Dict.prototype.__sub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'dict' and '" + batavia.type_name(other) + "'");
    };


    Dict.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__lshift__ has not been implemented");
    };

    Dict.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__rshift__ has not been implemented");
    };

    Dict.prototype.__and__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'dict' and '" + batavia.type_name(other) + "'");
    };

    Dict.prototype.__xor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__xor__ has not been implemented");
    };

    Dict.prototype.__or__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__or__ has not been implemented");
    };

    Dict.prototype.__setitem__ = function(key, value) {
        if (this.size + 1 > this.data_keys.length * MAX_LOAD_FACTOR) {
            this._increase_size();
        }
        var hash = batavia.builtins.hash([key], null);
        var h = hash.int32() & this.mask;
        while (true) {
            var current_key = this.data_keys[h];
            if (isEmpty(current_key) || isDeleted(current_key)) {
                this.data_keys[h] = key;
                this.data_values[h] = value;
                this.size++;
                return;
            } else if (current_key === null && key === null) {
                this.data_keys[h] = key;
                this.data_values[h] = value;
                return;
            } else if (batavia.builtins.hash([current_key], null).__eq__(hash).valueOf() &&
                       current_key.__eq__(key).valueOf()) {
                 this.data_keys[h] = key;
                 this.data_values[h] = value;
            }

            h = (h + 1) & this.mask;
            if (h == (hash.int32() & this.mask)) {
                // we have looped, we'll rehash (should be impossible)
                this._increase_size();
                h = hash.int32() & this.mask;
            }
        }
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    Dict.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ifloordiv__ has not been implemented");
    };

    Dict.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__itruediv__ has not been implemented");
    };

    Dict.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__iadd__ has not been implemented");
    };

    Dict.prototype.__isub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__isub__ has not been implemented");
    };

    Dict.prototype.__imul__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__imul__ has not been implemented");
    };

    Dict.prototype.__imod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__imod__ has not been implemented");
    };

    Dict.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ipow__ has not been implemented");
    };

    Dict.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ilshift__ has not been implemented");
    };

    Dict.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__irshift__ has not been implemented");
    };

    Dict.prototype.__iand__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__iand__ has not been implemented");
    };

    Dict.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ixor__ has not been implemented");
    };

    Dict.prototype.__ior__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Dict.__ior__ has not been implemented");
    };

    Dict.prototype._find_index = function(other) {
        if (this.size === 0) {
            return null;
        }
        var hash = batavia.builtins.hash([other], null);
        var h = hash.int32() & this.mask;
        while (true) {
            var key = this.data_keys[h];
            if (isDeleted(key)) {
                h = (h + 1) & this.mask;
                continue;
            }
            if (isEmpty(key)) {
                return null;
            }
            if (key === null && other === null) {
                return h;
            }
            if (batavia.builtins.hash([key], null).__eq__(hash).valueOf() &&
                ((key === null && other === null) || key.__eq__(other).valueOf())) {
                return h;
            }
            h = (h + 1) & this.mask;

            if (h == (hash.int32() & this.mask)) {
                // we have looped, definitely not here
                return null;
            }
        }
    };

    Dict.prototype.__contains__ = function(key) {
        return new batavia.types.Bool(this._find_index(key) !== null);
    };

    Dict.prototype.__getitem__ = function(key) {
        var i = this._find_index(key);
        if (i === null) {
            throw new batavia.builtins.KeyError(key === null ? 'None': key);
        }
        return this.data_values[i];
    };

    Dict.prototype.__delitem__ = function(key) {
        var i = this._find_index(key);
        if (i === null) {
            throw new batavia.builtins.KeyError(key === null ? 'None': key);
        }
        this.data_keys[i] = DELETED;
        this.data_values[i] = null;
        this.size--;
    };

    /**************************************************
     * Methods
     **************************************************/

    Dict.prototype.get = function(key, backup) {
        var i = this._find_index(key);
        if (i !== null) {
            return this.data_values[i];
        } else if (typeof backup === 'undefined') {
            throw new batavia.builtins.KeyError(key === null ? 'None': key);
        } else {
            return backup;
        }
    };

    Dict.prototype.update = function(values) {
        var updates;
        if (batavia.isinstance(values, [batavia.types.Dict, batavia.types.JSDict])) {
            updates = batavia.builtins.iter([values.items()], null);
        } else {
            updates = batavia.builtins.iter([values], null);
        }
        var i = 0;
        var self = this;
        batavia.iter_for_each(updates, function(val) {
            var pieces = new batavia.types.Tuple(val);
            if (pieces.length != 2) {
                throw new batavia.builtins.ValueError("dictionary update sequence element #" + i + " has length " + pieces.length + "; 2 is required");
            }
            var key = pieces[0];
            var value = pieces[1];
            // we can partially process
            self.__setitem__(key, value);
            i++;
        });
    };

    Dict.prototype.copy = function() {
        return new Dict(this);
    };

    Dict.prototype.items = function() {
        var result = new batavia.types.List();
        for (var i = 0; i < this.data_keys.length; i++) {
            // ignore deleted or empty
            var key = this.data_keys[i];
            if (isEmpty(key) || isDeleted(key)) {
                continue;
            }
            result.append(new batavia.types.Tuple([key, this.data_values[i]]));
        }
        return result;
    };

    Dict.prototype.keys = function() {
        var result = new batavia.types.List();
        for (var i = 0; i < this.data_keys.length; i++) {
            // ignore deleted or empty
            var key = this.data_keys[i];
            if (isEmpty(key) || isDeleted(key)) {
                continue;
            }
            result.append(key);
        }
        return result;
    };

    Dict.prototype.__iter__ = function() {
        return batavia.builtins.iter([this.keys()], null);
    };

    Dict.prototype.values = function() {
        var result = new batavia.types.List();
        for (var i = 0; i < this.data_keys.length; i++) {
            // ignore deleted or empty
            var key = this.data_keys[i];
            if (isEmpty(key) || isDeleted(key)) {
                continue;
            }
            result.append(this.data_values[i]);
        }
        return result;
    };

    Dict.prototype.clear = function() {
        this.size = 0;
        this.mask = 0;
        this.data_keys = [];
        this.data_values = [];
    };

    return Dict;
}();

batavia.types.Ellipsis = {};

/*************************************************************************
 * A Python filter builtin is a type
 *************************************************************************/

batavia.types.filter = function() {
    function filter(args, kwargs) {
        Object.call(this);
        if (args.length < 2) {
            throw new batavia.builtins.TypeError("filter expected 2 arguments, got " + args.length);
        }
        this._func = args[0];
        this._sequence = args[1];
    }

    filter.prototype = Object.create(Object.prototype);
    filter.prototype.__class__ = new batavia.types.Type('filter');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    filter.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    filter.prototype.__iter__ = function() {
        return this;
    };

    filter.prototype.__next__ = function() {
        if (!this._iter) {
            this._iter = batavia.builtins.iter([this._sequence], null);
        }
        if (!batavia.builtins.callable([this._func], null)) {
            throw new batavia.builtins.TypeError(
              batavia.builtins.type(this._func).__name__ + "' object is not callable");
        }

        var sval = false;
        do {
            sval = batavia.run_callable(this._iter, this._iter.__next__, [], null);
        } while (!batavia.run_callable(false, this._func, [sval], null));

        return sval;
    };

    filter.prototype.__str__ = function() {
        return "<filter object at 0x99999999>";
    };

    /**************************************************/

    return filter;
}();

/*************************************************************************
 * A Python float type
 *************************************************************************/

batavia.types.Float = function() {
    function Float(val) {
        this.val = val;
    }

    Float.prototype = Object.create(Object.prototype);
    Float.prototype.__class__ = new batavia.types.Type('float');

    function python_modulo(n, M) {
        return ((n % M) + M) % M;
    }

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Float.prototype.toString = function() {
        return this.__str__();
    };

    Float.prototype.valueOf = function() {
        return this.val;
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Float.prototype.__bool__ = function() {
        return this.val !== 0.0;
    };

    Float.prototype.__repr__ = function() {
        return this.__str__();
    };

    Float.prototype.__str__ = function() {
        if (!isFinite(this.val)) {
            if (isNaN(this.val)) {
                return "nan";
            }
            if (this.val < 0) {
                return "-inf";
            }
            return "inf";
        }
        if (this.val === 0) {
            if (1/this.val === Infinity) {
                return '0.0';
            } else {
                return '-0.0';
            }
        } else if (this.val === Math.round(this. val)) {
            var s = this.val.toString();
            if (s.length >= 19) {
              // force conversion to scientific
              return this.val.toExponential();
            }
            if (s.indexOf('.') < 0) {
              return s + '.0';
            }
            return s;
        } else {
            return this.val.toString();
        }
    };

    Float.prototype.__float__ = function() {
        return this;
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Float.prototype.__lt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Dict, batavia.types.List, batavia.types.Tuple,
                        batavia.types.NoneType, batavia.types.Str, batavia.types.NotImplementedType,
                        batavia.types.Range, batavia.types.Set, batavia.types.Slice
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: float() < " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() < other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: float() < NoneType()");
        }
    };

    Float.prototype.__le__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Dict, batavia.types.List, batavia.types.Tuple,
                        batavia.types.NoneType, batavia.types.Str, batavia.types.NotImplementedType,
                        batavia.types.Range, batavia.types.Set, batavia.types.Slice
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: float() <= " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() <= other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: float() <= NoneType()");
        }
    };

    Float.prototype.__eq__ = function(other) {
        if (other !== null && !batavia.isinstance(other, batavia.types.Str)) {
            var val;
            if (batavia.isinstance(other, batavia.types.Bool)) {
                val = other.valueOf() ? 1.0 : 0.0;
            } else if (batavia.isinstance(other, batavia.types.Int)) {
                val = parseFloat(other.val);
            } else {
                val = other.valueOf();
            }
            return this.valueOf() === val;
        }
        return false;
    };

    Float.prototype.__ne__ = function(other) {
        return !this.__eq__(other);
    };

    Float.prototype.__gt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Dict, batavia.types.List, batavia.types.Tuple,
                        batavia.types.NoneType, batavia.types.Str, batavia.types.NotImplementedType,
                        batavia.types.Range, batavia.types.Set, batavia.types.Slice
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: float() > " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() > other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: float() > NoneType()");
        }
    };

    Float.prototype.__ge__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Dict, batavia.types.List, batavia.types.Tuple,
                        batavia.types.NoneType, batavia.types.Str, batavia.types.NotImplementedType,
                        batavia.types.Range, batavia.types.Set, batavia.types.Slice
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: float() >= " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() >= other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: float() >= NoneType()");
        }
    };

    Float.prototype.__contains__ = function(other) {
        return false;
    };

    /**************************************************
     * Unary operators
     **************************************************/

    Float.prototype.__pos__ = function() {
        return new Float(+this.valueOf());
    };

    Float.prototype.__neg__ = function() {
        return new Float(-this.valueOf());
    };

    Float.prototype.__not__ = function() {
        return new Float(!this.valueOf());
    };

    Float.prototype.__invert__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary ~: 'float'");
    };

    Float.prototype.__abs__ = function() {
        return new Float(Math.abs(this.valueOf()));
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Float.prototype.__pow__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Bool)) {
            return new Float(Math.pow(this.valueOf(), other.valueOf() ? 1 : 0));
        } else if (batavia.isinstance(other, [batavia.types.Float, batavia.types.Int])) {
            if (this.valueOf() == 0 && other.valueOf() < 0) {
                throw new batavia.builtins.ZeroDivisionError("0.0 cannot be raised to a negative power");
            } else {
                return new Float(Math.pow(this.valueOf(), other.valueOf()));
            }
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'float' and '" + batavia.type_name(other) + "'");
        }
    };

    Float.prototype.__div__ = function(other) {
        return this.__truediv__(other);
    };

    Float.prototype.__floordiv__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (!other.val.isZero()) {
                return new Float(Math.floor(this.valueOf() / other.valueOf()));
            } else {
                throw new batavia.builtins.ZeroDivisionError("float divmod()");
            }
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            if (other.valueOf()) {
                return new Float(Math.floor(this.valueOf() / other.valueOf()));
            } else {
                throw new batavia.builtins.ZeroDivisionError("float divmod()");
            }
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return new Float(Math.floor(this.valueOf()));
            } else {
                throw new batavia.builtins.ZeroDivisionError("float divmod()");
            }
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'float' and '" + batavia.type_name(other) + "'");
        }
    };

    Float.prototype.__truediv__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (!other.val.isZero()) {
                return new Float(this.valueOf() / other.valueOf());
            } else {
                throw new batavia.builtins.ZeroDivisionError("float division by zero");
            }
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            if (other.valueOf()) {
                return new Float(this.valueOf() / other.valueOf());
            } else {
                throw new batavia.builtins.ZeroDivisionError("float division by zero");
            }
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return new Float(this.valueOf());
            } else {
                throw new batavia.builtins.ZeroDivisionError("float division by zero");
            }
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'float' and '" + batavia.type_name(other) + "'");
        }
    };

    Float.prototype.__mul__ = function(other) {
        if (other === null) {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'float' and 'NoneType'");
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            return new Float(this.valueOf() * (other.valueOf() ? 1 : 0));
        } else if (batavia.isinstance(other, [batavia.types.Float, batavia.types.Int])) {
            return new batavia.types.Float(this.valueOf() * other.valueOf());
        } else if (batavia.isinstance(other, [batavia.types.List, batavia.types.Str, batavia.types.Tuple])) {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'float'");
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'float' and '" + batavia.type_name(other) + "'");
        }
    };

    Float.prototype.__mod__ = function(other) {
        /* TODO: Fix case for -0.0, which is coming out 0.0 */
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (other.val.isZero()) {
                throw new batavia.builtins.ZeroDivisionError("float modulo");
            } else {
                return new Float(python_modulo(this.valueOf(), parseFloat(other.val)));
            }
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            if (other.valueOf() === 0) {
                throw new batavia.builtins.ZeroDivisionError("float modulo");
            } else {
                return new Float(python_modulo(this.valueOf(), other.valueOf()));
            }
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return new Float(python_modulo(this.valueOf(), other.valueOf()));
            } else {
                throw new batavia.builtins.ZeroDivisionError("float modulo");
            }
        } else {
            throw new batavia.builtins.TypeError(
                "unsupported operand type(s) for %: 'float' and '" + batavia.type_name(other) + "'"
            );
        }
    };

    Float.prototype.__add__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.Int, batavia.types.Float])) {
            return new Float(this.valueOf() + parseFloat(other.valueOf()));
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            return new Float(this.valueOf() + (other.valueOf() ? 1.0 : 0.0));
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'float' and '" + batavia.type_name(other) + "'");
        }
    };

    Float.prototype.__sub__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.Int, batavia.types.Float])) {
            return new Float(this.valueOf() - other.valueOf());
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            return new Float(this.valueOf() - (other.valueOf() ? 1.0 : 0.0));
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'float' and '" + batavia.type_name(other) + "'");
        }
    };

    Float.prototype.__getitem__ = function(other) {
        throw new batavia.builtins.TypeError("'float' object is not subscriptable")
    };

    Float.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for <<: 'float' and '" + batavia.type_name(other) + "'"
        );
    };

    Float.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for >>: 'float' and '" + batavia.type_name(other) + "'"
        );
    };

    Float.prototype.__and__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for &: 'float' and '" + batavia.type_name(other) + "'"
        );
    };

    Float.prototype.__xor__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for ^: 'float' and '" + batavia.type_name(other) + "'"
        );
    };

    Float.prototype.__or__ = function(other) {
        throw new batavia.builtins.TypeError(
            "unsupported operand type(s) for |: 'float' and '" + batavia.type_name(other) + "'"
        );
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    // Call the method named "f" with argument "other"; if a type error is raised, throw a different type error
    Float.prototype.__call_binary_operator__ = function(f, operator_str, other) {
        try {
            return this[f](other);
        } catch (error) {
            if (error instanceof batavia.builtins.TypeError) {
                throw new batavia.builtins.TypeError(
                    "unsupported operand type(s) for " + operator_str + ": 'float' and '" + batavia.type_name(other) + "'");
            } else {
                throw error;
            }
        }
    };

    Float.prototype.__ifloordiv__ = function(other) {
        return this.__call_binary_operator__('__floordiv__', '//=', other);
    };

    Float.prototype.__itruediv__ = function(other) {
        return this.__call_binary_operator__('__truediv__', "/=", other);
    };

    Float.prototype.__iadd__ = function(other) {
        return this.__call_binary_operator__('__add__', "+=", other);
    };

    Float.prototype.__isub__ = function(other) {
        return this.__call_binary_operator__('__sub__', "-=", other);
    };

    Float.prototype.__imul__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.List, batavia.types.Str, batavia.types.Tuple])) {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'float'");
        } else {
            return this.__call_binary_operator__('__mul__', "*=", other);
        }
    };

    Float.prototype.__imod__ = function(other) {
        return this.__call_binary_operator__('__mod__', "%=", other);
    };

    Float.prototype.__ipow__ = function(other) {
        return this.__pow__(other);
    };

    Float.prototype.__ilshift__ = function(other) {
        return this.__call_binary_operator__('__lshift__', "<<=", other);
    };

    Float.prototype.__irshift__ = function(other) {
        return this.__call_binary_operator__('__rshift__', ">>=", other);
    };

    Float.prototype.__iand__ = function(other) {
        return this.__call_binary_operator__('__and__', "&=", other);
    };

    Float.prototype.__ixor__ = function(other) {
        return this.__call_binary_operator__('__xor__', "^=", other);
    };

    Float.prototype.__ior__ = function(other) {
        return this.__call_binary_operator__('__or__', "|=", other);
    };

    /**************************************************
     * Methods
     **************************************************/

    Float.prototype.copy = function() {
        return new Float(this.valueOf());
    };

    Float.prototype.is_integer = function() {
        return new batavia.types.Bool(Number.isInteger(this.valueOf()));
    };

    Float.prototype.__trunc__ = function() {
        return new batavia.types.Int(Math.trunc(this.valueOf()));
    };

    /**************************************************/

    return Float;
}();

batavia.types.Function = function() {
    function Function(name, code, globals, defaults, closure, vm) {
        this.__python__ = true;
        this._vm = vm;
        this.__code__ = code;
        this.__globals__ = globals;
        this.__defaults__ = defaults;
        this.__kwdefaults__ = null;
        this.__closure__ = closure;
        if (code.co_consts.length > 0) {
            this.__doc__ = code.co_consts[0];
        } else {
            this.__doc__ = null;
        }
        this.__name__ = name || code.co_name;
        this.__dict__ = new batavia.types.Dict();
        this.__annotations__ = new batavia.types.Dict();
        this.__qualname__ = this.__name__;

        // var kw = {
        //     'argdefs': this.__defaults__,
        // }
        // if (closure) {
        //     kw['closure'] = tuple(make_cell(0) for _ in closure)
        // }

        this.__call__ = batavia.make_callable(this);

        this.argspec = batavia.modules.inspect.getfullargspec(this);
    }

    Function.prototype = Object.create(Object.prototype);
    Function.prototype.__class__ = new batavia.types.Type('function');

    return Function;
}();


batavia.types.Method = function() {
    function Method(instance, func) {
        batavia.types.Function.call(this, func.__name__, func.__code__, func.__globals__, func.__closure__, func._vm);
        this.__self__ = instance;
        this.__func__ = func;
        this.__class__ = instance.prototype;
    }

    Method.prototype = Object.create(Function.prototype);

    Method.prototype.constructor = Method;

    return Method;
}();

/*************************************************************************
 * A Python int type
 *************************************************************************/

batavia.types.Int = function() {
    function Int(val) {
        Object.call(this);
        this.val = new batavia.vendored.BigNumber(val);
    }

    var MIN_FLOAT = new Int("-179769313486231580793728971405303415079934132710037826936173778980444968292764750946649017977587207096330286416692887910946555547851940402630657488671505820681908902000708383676273854845817711531764475730270069855571366959622842914819860834936475292719074168444365510704342711559699508093042880177904174497791");
    var REASONABLE_SHIFT = new Int("8192");
    var MAX_SHIFT = new Int("9223372036854775807");
    var MAX_INT = new Int("9223372036854775807")
    var MIN_INT = new Int("-9223372036854775808")

    Int.prototype = Object.create(Object.prototype);
    Int.prototype.__class__ = new batavia.types.Type('int');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Int.prototype.int32 = function() {
      if (this.val.gt(MAX_INT.val) || this.val.lt(MIN_INT.val)) {
          throw new batavia.builtins.IndexError("cannot fit 'int' into an index-sized integer");
      }
      return parseInt(this.valueOf());
    }

    Int.prototype.valueOf = function() {
        return this.val.valueOf();
    };

    Int.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Int.prototype.__bool__ = function() {
        return !this.val.isZero();
    };

    Int.prototype.__repr__ = function() {
        return this.__str__();
    };

    Int.prototype.__str__ = function() {
        return this.val.toFixed(0);
    };

    var can_float = function(num) {
        return !(num.gt(batavia.MAX_FLOAT.val) || num.lt(MIN_FLOAT.val));
    };

    Int.prototype.__float__ = function() {
        if (!can_float(this.val)) {
            throw new batavia.builtins.OverflowError("int too large to convert to float");
        }
        return new batavia.types.Float(parseFloat(this.val));
    };

    Int.prototype.__int__ = function() {
        return this;
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Int.prototype.__lt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.Bool)) {
                return this.val.lt(other ? 1 : 0);
            } else if (batavia.isinstance(other, batavia.types.Int)) {
                return this.val.lt(other.val);
            } else if (batavia.isinstance(other, batavia.types.Float)) {
                return this.val.lt(other.valueOf());
            } else {
                throw new batavia.builtins.TypeError("unorderable types: int() < " + batavia.type_name(other) + "()");
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: int() < NoneType()");
        }
    };

    Int.prototype.__le__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.Bool)) {
                return this.val.lte(other ? 1 : 0);
            } else if (batavia.isinstance(other, batavia.types.Int)) {
                return this.val.lte(other.val);
            } else if (batavia.isinstance(other, batavia.types.Float)) {
                return this.val.lte(other.valueOf());
            } else {
                throw new batavia.builtins.TypeError("unorderable types: int() <= " + batavia.type_name(other) + "()");
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: int() <= NoneType()");
        }
    };

    Int.prototype.__eq__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.Float, batavia.types.Int])) {
          return this.val.eq(other.val);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
          return this.val.eq(other ? 1 : 0);
        } else {
          return false;
        }
    };

    Int.prototype.__ne__ = function(other) {
        return !this.__eq__(other);
    };

    Int.prototype.__gt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.Bool)) {
                return this.val.gt(other ? 1 : 0);
            } else if (batavia.isinstance(other, batavia.types.Int)) {
                return this.val.gt(other.val);
            } else if (batavia.isinstance(other, batavia.types.Float)) {
                return this.val.gt(other.valueOf());
            } else {
                throw new batavia.builtins.TypeError("unorderable types: int() > " + batavia.type_name(other) + "()");
            }

        } else {
            throw new batavia.builtins.TypeError("unorderable types: int() > NoneType()");
        }
    };

    Int.prototype.__ge__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.Bool)) {
                return this.val.gte(other ? 1 : 0);
            } else if (batavia.isinstance(other, batavia.types.Int)) {
                return this.val.gte(other.val);
            } else if (batavia.isinstance(other, batavia.types.Float)) {
                return this.val.gte(other.valueOf());
            } else {
                throw new batavia.builtins.TypeError("unorderable types: int() >= " + batavia.type_name(other) + "()");
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: int() >= NoneType()");
        }
    };

    Int.prototype.__contains__ = function(other) {
        return false;
    };

    /**************************************************
     * Unary operators
     **************************************************/

    Int.prototype.__pos__ = function() {
        return this;
    };

    Int.prototype.__neg__ = function() {
        return new Int(this.val.neg());
    };

    Int.prototype.__not__ = function() {
        return new batavia.types.Bool(this.val.isZero());
    };

    Int.prototype.__invert__ = function() {
        return new Int(this.val.neg().sub(1));
    };

    Int.prototype.__abs__ = function() {
        return new Int(this.val.abs());
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Int.prototype.__pow__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return this;
            } else {
                return new Int(1);
            }
        } else if (batavia.isinstance(other, batavia.types.Int)) {
            if (other.val.isNegative()) {
                return this.__float__().__pow__(other);
            } else {
                var y = other.val.toString(2).split('');
                var result = new batavia.vendored.BigNumber(1);
                var base = this.val.add(0);
                while (y.length > 0) {
                  var bit = y.pop();
                  if (bit == 1) {
                    result = result.mul(base);
                  }
                  base = base.mul(base);
                }
                return new Int(result);
            }
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            return this.__float__().__pow__(other);
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__div__ = function(other) {
        return this.__truediv__(other);
    };

    Int.prototype.__floordiv__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (!other.val.isZero()) {
                var quo = this.val.div(other.val);
                var quo_floor = quo.floor();
                var rem = this.val.mod(other.val);

                if (rem.isZero()) {
                  return new Int(quo_floor);
                }
                // we have a fraction leftover
                // check if it is too small for bignumber.js to detect
                if (quo.isInt() && quo.isNegative()) {
                  return new Int(quo.sub(1));
                }
                return new Int(quo_floor);
            } else {
                throw new batavia.builtins.ZeroDivisionError("integer division or modulo by zero");
            }
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            var f = this.__float__();
            if (other.valueOf()) {
                return f.__floordiv__(other);
            } else {
                throw new batavia.builtins.ZeroDivisionError("float divmod()");
            }

        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return new Int(this.val.floor());
            } else {
                throw new batavia.builtins.ZeroDivisionError("integer division or modulo by zero");
            }
        } else if (batavia.isinstance(other, batavia.types.Complex)) {
            throw new batavia.builtins.TypeError("can't take floor of complex number.");
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__truediv__ = function(other) {
        // if it is dividing by another int, we can allow both to be bigger than floats
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (other.val.isZero()) {
                throw new batavia.builtins.ZeroDivisionError("division by zero");
            }
            var result = this.val.div(other.val);
            if (!can_float(result)) {
                throw new batavia.builtins.OverflowError("integer division result too large for a float");
            }
            // check for negative 0
            if (other.val.lt(0) && result.isZero()) {
                return new batavia.types.Float(parseFloat("-0.0"));
            }
            return new Int(result).__float__();
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            return this.__float__().__div__(other);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            return this.__truediv__(new Int(other.valueOf() ? 1 : 0));
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__mul__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            return new Int(this.val.mul(other.val));
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            return this.__float__().__mul__(other.val);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            return new Int(this.val.mul(other.valueOf() ? 1 : 0));
        } else if (batavia.isinstance(other, batavia.types.List)) {
            if (this.val.gt(MAX_INT.val) || this.val.lt(MIN_INT.val)) {
                throw new batavia.builtins.OverflowError("cannot fit 'int' into an index-sized integer");
            }
            if ((other.length == 0) || (this.valueOf() < 0)) {
                return new batavia.types.List();
            }
            if (this.valueOf() > 4294967295) {
                throw new batavia.builtins.MemoryError("");
            }
            result = new batavia.types.List();
            for (var i = 0; i < this.valueOf(); i++) {
                result.extend(other);
            }
            return result;
        } else if (batavia.isinstance(other, batavia.types.Str)) {
            if (this.val.gt(MAX_INT.val) || this.val.lt(MIN_INT.val)) {
                throw new batavia.builtins.OverflowError("cannot fit 'int' into an index-sized integer");
            }
            if (this.val.isNegative()) {
                return '';
            }
            var size = this.val.mul(other.length);
            if (size.gt(MAX_INT.val)) {
                throw new batavia.builtins.OverflowError("repeated string is too long");
            }
            if (other.length == 0) {
                return '';
            }
            if ((this.valueOf() > 4294967295) || (this.valueOf() < -4294967296)) {
                throw new batavia.builtins.MemoryError("");
            }

            result = '';
            for (var i = 0; i < this.valueOf(); i++) {
                result += other.valueOf();
            }
            return result;
        } else if (batavia.isinstance(other, batavia.types.Tuple)) {
            if (this.val.gt(MAX_INT.val) || this.val.lt(MIN_INT.val)) {
                throw new batavia.builtins.OverflowError("cannot fit 'int' into an index-sized integer");
            }
            if ((other.length == 0) || (this.valueOf() < 0)) {
                return new batavia.types.Tuple();
            }
            if (this.valueOf() > 4294967295) {
                throw new batavia.builtins.MemoryError("");
            }
            result = new batavia.types.Tuple();
            for (var i = 0; i < this.valueOf(); i++) {
                result.__add__(other);
            }
            return result;
        } else if (batavia.isinstance(other, batavia.types.Complex)) {
            if (this.val.gt(MAX_INT.val) || this.val.lt(MIN_INT.val)) {
                throw new batavia.builtins.OverflowError("int too large to convert to float");
            }
            else {
                return new batavia.types.Complex(this.val.mul(other.real).toNumber(), this.val.mul(other.imag).toNumber());
            }

        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__mod__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (!other.val.isZero()) {
                return new Int(this.val.mod(other.val).add(other.val).mod(other.val));
            } else {
                throw new batavia.builtins.ZeroDivisionError("integer division or modulo by zero");
            }
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            var f = this.__float__();
            if (other.valueOf()) {
                return f.__mod__(other);
            } else {
                throw new batavia.builtins.ZeroDivisionError("float modulo");
            }
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return new Int(0);
            } else {
                throw new batavia.builtins.ZeroDivisionError("integer division or modulo by zero");
            }
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for %: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__add__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            return new Int(this.val.add(other.val));
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            return this.__float__().__add__(other);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            return new Int(this.val.add(other.valueOf() ? 1 : 0));
        } else if (batavia.isinstance(other, batavia.types.Complex)) {
            if (this.__float__() > batavia.MAX_FLOAT || this.__float__() < batavia.MIN_FLOAT) {
                throw new batavia.builtins.OverflowError("int too large to convert to float");
            } else {
                return new batavia.types.Complex(this.val.add(other.real).toNumber(), other.imag);
            }
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__sub__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            return new Int(this.val.sub(other.val));
        } else if (batavia.isinstance(other, batavia.types.Float)) {
            return this.__float__().__sub__(other);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            return new Int(this.val.sub(other.valueOf() ? 1 : 0));
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__getitem__ = function(index) {
        throw new batavia.builtins.TypeError("'int' object is not subscriptable")
    };

    /**************************************************
     * Bitshift and logical ops
     **************************************************/

    // converts this integer to an binary array for efficient bit operations
    // BUG: javascript bignumber is incredibly inefficient for bit operations
    var toArray = function(self) {
        return self.val.abs().toString(2).split('').map(function (x) { return x - '0' });
    };

    Int.prototype._bits = function() {
        return toArray(this);
    }

    // convert a binary array back into an int
    var fromArray = function(arr) {
        return new Int(new batavia.vendored.BigNumber(arr.join('') || 0, 2));
    };
    // return j with the sign inverted if i is negative.
    var fixSign = function(i, j) {
        if (i.val.isNeg()) {
            return j.__neg__();
        }
        return j;
    };
    // invert the bits of an array
    var invert = function(arr) {
      return arr.map(function(x) { return 1 - x; });
    };
    // add 1 to the bit array
    var plusOne = function(arr) {
        for (var i = arr.length - 1; i >= 0; i--) {
            if (arr[i] == 0) {
                arr[i] = 1;
                return;
            }
            arr[i] = 0;
        }
        arr.reverse();
        arr.push(1);
        arr.reverse();
    };
    // convert the int to an array, and negative ints to their
    // twos complement representation
    var twos_complement = function(n) {
        var arr = toArray(n);
        if (n.val.isNeg()) {
            arr = invert(arr);
            plusOne(arr);
        }
        return arr;
    };
    // extend a to be at least b bits long (by prepending zeros or ones)
    var extend = function(a, b, ones) {
        if (a.length >= b.length) {
          return;
        }
        a.reverse();
        while (a.length < b.length) {
          if (ones) {
            a.push(1);
          } else {
            a.push(0);
          }
        }
        a.reverse();
    };

    Int.prototype.__lshift__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            // Anything beyond ~8192 bits is too inefficient to convert to a binary array
            // due to Bignumber.js.
            if (other.val.gt(REASONABLE_SHIFT.val)) {
                throw new batavia.builtins.OverflowError("batavia: shift too large");
            }
            if (other.val.gt(MAX_SHIFT.val)) {
                throw new batavia.builtins.OverflowError("Python int too large to convert to C ssize_t");
            }
            if (other.valueOf() < 0) {
                throw new batavia.builtins.ValueError("negative shift count");
            }
            var arr = toArray(this);
            for (var i = 0; i < other.valueOf(); i++) {
                arr.push(0);
            }
            return fixSign(this, new Int(fromArray(arr)));
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
              return this.__lshift__(new Int(1));
            } else {
              return this;
            }
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for <<: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__rshift__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (this.val.isNegative()) {
                return this.__invert__().__rshift__(other).__invert__();
            }
            // Anything beyond ~8192 bits is too inefficient to convert to a binary array
            // due to Bignumber.js.
            if (other.val.gt(MAX_INT.val) || other.val.lt(MIN_INT.val)) {
                throw new batavia.builtins.OverflowError("Python int too large to convert to C ssize_t");
            }
            if (other.val.gt(REASONABLE_SHIFT.val)) {
                throw new batavia.builtins.ValueError("batavia: shift too large");
            }
            if (other.val.isNegative()) {
                throw new batavia.builtins.ValueError("negative shift count");
            }
            if (this.val.isZero()) {
                return this;
            }
            var arr = toArray(this);
            if (other.val.gt(arr.length)) {
                return new Int(0);
            }
            return fixSign(this, fromArray(arr.slice(0, arr.length - other.valueOf())));
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
              return this.__rshift__(new Int(1));
            }
            return this;
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for >>: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__and__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            var a = twos_complement(this);
            var b = twos_complement(other);
            extend(a, b, this.val.isNeg());
            extend(b, a, other.val.isNeg());
            var i = a.length - 1;
            var j = b.length - 1;
            var arr = [];
            while (i >= 0 && j >= 0) {
                arr.push(a[i] & b[j]);
                i--;
                j--;
            }
            arr.reverse();
            if (this.val.isNeg() && other.val.isNeg()) {
                arr = invert(arr);
                return fromArray(arr).__add__(new Int(1)).__neg__();
            }
            return fromArray(arr);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return this.__and__(new Int(1));
            }
            return new Int(0);
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__xor__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            if (this.val.isNeg()) {
               return this.__invert__().__xor__(other).__invert__();
            }
            if (other.val.isNeg()) {
              return this.__xor__(other.__invert__()).__invert__();
            }
            var a = twos_complement(this);
            var b = twos_complement(other);
            extend(a, b);
            extend(b, a);
            var i = a.length - 1;
            var j = b.length - 1;
            var arr = [];
            while (i >= 0 && j >= 0) {
                arr.push(a[i] ^ b[j]);
                i--;
                j--;
            }
            arr.reverse();
            return fromArray(arr);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return this.__xor__(new Int(1));
            }
            return this;
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for ^: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    Int.prototype.__or__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
          if (this.val.eq(other.val)) {
              return this;
          }
          if (this.val.eq(-1) || other.val.eq(-1)) {
              return new Int(-1);
          }
          if (this.val.isZero()) {
              return other;
          }
          var a = twos_complement(this);
          var b = twos_complement(other);
          extend(a, b, this.val.isNeg());
          extend(b, a, other.val.isNeg());
          var i = a.length - 1;
          var j = b.length - 1;
          var arr = [];
          while (i >= 0 && j >= 0) {
              arr.push(a[i] | b[j]);
              i--;
              j--;
          }
          arr.reverse();
          if (this.val.isNeg() || other.val.isNeg()) {
              arr = invert(arr);
              return fromArray(arr).__add__(new Int(1)).__neg__();
          }
          return fromArray(arr);
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return this.__or__(new Int(1));
            }
            return this;
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'int' and '" + batavia.type_name(other) + "'");
        }
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    // Call the method named "f" with argument "other"; if a type error is raised, throw a different type error
    Int.prototype.__call_type_error_str__ = function(f, operand_str, other) {
        try {
            return this[f](other);
        } catch (error) {
            if (error instanceof batavia.builtins.TypeError) {
                throw new batavia.builtins.TypeError(
                    "unsupported operand type(s) for " + operand_str + ": 'int' and '" + batavia.type_name(other) + "'");
            } else {
                throw error;
            }
        }
    };


    Int.prototype.__ifloordiv__ = function(other) {
        return this.__call_type_error_str__('__floordiv__', "//=", other);
    };

    Int.prototype.__itruediv__ = function(other) {
        return this.__call_type_error_str__('__truediv__', "/=", other);
    };

    Int.prototype.__iadd__ = function(other) {
        return this.__call_type_error_str__('__add__', "+=", other);
    };

    Int.prototype.__isub__ = function(other) {
        return this.__call_type_error_str__('__sub__', "-=", other);
    };

    Int.prototype.__imul__ = function(other) {
        return this.__call_type_error_str__('__mul__', "*=", other);
    };

    Int.prototype.__imod__ = function(other) {
        return this.__call_type_error_str__('__mod__', "%=", other);
    };

    Int.prototype.__ipow__ = function(other) {
        return this.__pow__(other);
    };

    Int.prototype.__ilshift__ = function(other) {
        return this.__call_type_error_str__('__lshift__', "<<=", other);
    };

    Int.prototype.__irshift__ = function(other) {
        return this.__call_type_error_str__('__rshift__', ">>=", other);
    };

    Int.prototype.__iand__ = function(other) {
        return this.__call_type_error_str__('__and__', "&=", other);
    };

    Int.prototype.__ixor__ = function(other) {
        return this.__call_type_error_str__('__xor__', "^=", other);
    };

    Int.prototype.__ior__ = function(other) {
        return this.__call_type_error_str__('__or__', "|=", other);
    };

    /**************************************************
     * Methods
     **************************************************/

    Int.prototype.copy = function() {
        return new Int(this.valueOf());
    };

    Int.prototype.__trunc__ = function() {
        return this;
    };

    /**************************************************/

    return Int;
}();

batavia.MAX_FLOAT = new batavia.types.Int("179769313486231580793728971405303415079934132710037826936173778980444968292764750946649017977587207096330286416692887910946555547851940402630657488671505820681908902000708383676273854845817711531764475730270069855571366959622842914819860834936475292719074168444365510704342711559699508093042880177904174497791");

/*************************************************************************
 * A Python list type
 *************************************************************************/
batavia.types.List = function() {
    function List() {
        if (arguments.length === 0) {
            this.push.apply(this);
        } else if (arguments.length === 1) {
            // Fast-path for native Array objects.
            if (batavia.isArray(arguments[0])) {
                this.push.apply(this, arguments[0]);
            } else {
                var iterobj = batavia.builtins.iter([arguments[0]], null);
                var self = this;
                batavia.iter_for_each(iterobj, function(val) {
                    self.push(val);
                });
            }
        } else {
            throw new batavia.builtins.TypeError('list() takes at most 1 argument (' + arguments.length + ' given)');
        }
    }

    function Array_() {}

    Array_.prototype = [];

    List.prototype = Object.create(Array_.prototype);
    List.prototype.length = 0;
    List.prototype.__class__ = new batavia.types.Type('list');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    List.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    List.prototype.__iter__ = function() {
        return new List.prototype.ListIterator(this);
    };

    List.prototype.__len__ = function () {
        return this.length;
    };

    List.prototype.__repr__ = function() {
        return this.__str__();
    };

    List.prototype.__str__ = function() {
        return '[' + this.map(function(obj) {
                return batavia.builtins.repr([obj], null);
            }).join(', ') + ']';
    };

    List.prototype.__bool__ = function() {
        return this.length > 0;
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    List.prototype.__lt__ = function(other) {


        if (batavia.isinstance(other, [batavia.types.Bytes, batavia.types.Bytearray])){
            throw new batavia.builtins.TypeError("unorderable types: list() < " + batavia.type_name(other) + "()")
        }

        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.List)) {
                // edge case where this==[]
                if (this.length === 0 && other.length > 0){
                    return true;
                }

                for (var i=0; i<this.length; i++){

                    //other ran out of items.
                    if (other[i] === undefined){
                        return false;
                    }
                    if (this[i].__ne__(other[i])){
                        return this[i].__lt__(other[i]);
                    }
                }
                //got through loop and all values were equal. Determine by comparing length
                return this.length < other.length;
            } else {
                throw new batavia.builtins.TypeError("unorderable types: list() < " + batavia.type_name(other) + "()");
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: list() < NoneType()");
        }
    };

    List.prototype.__le__ = function(other) {


        if (batavia.isinstance(other, [batavia.types.Bytes, batavia.types.Bytearray])){
            throw new batavia.builtins.TypeError("unorderable types: list() <= " + batavia.type_name(other) + "()")
        }

        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.List)) {
                // edge case where this==[]
                if (this.length === 0 && other.length > 0){
                    return true;
                }

                for (var i=0; i<this.length; i++){

                    //other ran out of items.
                    if (other[i] === undefined){
                        return false;
                    }
                    if (this[i].__ne__(other[i])){
                        return this[i].__le__(other[i]);
                    }
                }
                //got through loop and all values were equal. Determine by comparing length
                return this.length <= other.length;
            } else {
                throw new batavia.builtins.TypeError("unorderable types: list() <= " + batavia.type_name(other) + "()");
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: list() <= NoneType()");
        }
    };

    List.prototype.__eq__ = function(other) {
        if (batavia.isinstance(other, batavia.types.List)){
            // must be a list to possibly be equal
            if(this.length !== other.length){
                // lists must have same number of items
                return false
            } else {
                for(var i=0; i<this.length; i++){
                    if(this[i] !== other[i]) {return false;}
                }
                return true;
            }

        } else {
            return false;
        }
    };

    List.prototype.__ne__ = function(other) {
        return this.valueOf() != other;
    };

    List.prototype.__gt__ = function(other) {

        if(batavia.isinstance(other, [batavia.types.Bytes, batavia.types.Bytearray])){
            throw new batavia.builtins.TypeError("unorderable types: list() > " + batavia.type_name(other) + "()")
        }

        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.List)) {
                // edge case where this==[]
                if (this.length === 0 && other.length > 0){
                    return false;
                }

                for(var i=0; i<this.length; i++){

                    //other ran out of items.
                    if (other[i] === undefined) {
                        return true;
                    }
                    if (this[i].__ne__(other[i])){
                        return this[i].__gt__(other[i]);
                    }
                }
                //got through loop and all values were equal. Determine by comparing length
                return this.length > other.length;
            } else {
                throw new batavia.builtins.TypeError("unorderable types: list() > " + batavia.type_name(other) + "()");
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: list() > NoneType()");
        }
    };

    List.prototype.__ge__ = function(other) {

        if (batavia.isinstance(other, [batavia.types.Bytes, batavia.types.Bytearray])){
            throw new batavia.builtins.TypeError("unorderable types: list() >= " + batavia.type_name(other) + "()")
        }

        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, batavia.types.List)) {
                // edge case where this==[]
                if (this.length === 0 && other.length > 0){
                    return false;
                }

                for (var i=0; i<this.length; i++){

                    //other ran out of items.
                    if (other[i] === undefined){
                        return true;
                    }
                    if (this[i].__ne__(other[i])){
                        return this[i].__ge__(other[i]);
                    }
                }
                //got through loop and all values were equal. Determine by comparing length
                return this.length >= other.length;
            } else {
                throw new batavia.builtins.TypeError("unorderable types: list() >= " + batavia.type_name(other) + "()");
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: list() >= NoneType()");
        }
    };

    List.prototype.__contains__ = function(other) {
        return this.valueOf().index(other) !== -1;
    };

    /**************************************************
     * Unary operators
     **************************************************/

    List.prototype.__pos__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary +: 'list'")
    };

    List.prototype.__neg__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary -: 'list'")
    };

    List.prototype.__not__ = function() {
        return this.length == 0;
    };

    List.prototype.__invert__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary ~: 'list'")
    };

    /**************************************************
     * Binary operators
     **************************************************/

    List.prototype.__pow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__div__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__mul__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            result = new List();
            if(other <= 0) {
                return result;
            } else {
                for (var i = 0; i < other; i++) {
                    result.extend(this);
                }
                return result;
            }
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other) {
                return this.copy();
            } else {
                return new List();
            }
        } else {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type '" + batavia.type_name(other) + "'");
        }
    };

    List.prototype.__mod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__add__ = function(other) {
        if (batavia.isinstance(other, batavia.types.List)) {
            result = new List();
                for (var i = 0; i < this.length; i++) {
                    result.push(this[i]);
                }

                for (var i = 0; i < other.length; i++) {
                    result.push(other[i]);
                }

                return result;
        } else {
            throw new batavia.builtins.TypeError('can only concatenate list (not "' + batavia.type_name(other) + '") to list');
        }
    };

    List.prototype.__sub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__getitem__ = function(index) {
        if (batavia.isinstance(index, batavia.types.Int)) {
            var idx = index.int32();
            if (idx < 0) {
                if (-idx > this.length) {
                    throw new batavia.builtins.IndexError("list index out of range");
                } else {
                    return this[this.length + idx];
                }
            } else {
                if (idx >= this.length) {
                    throw new batavia.builtins.IndexError("list index out of range");
                } else {
                    return this[idx];
                }
            }
        } else if (batavia.isinstance(index, batavia.types.Slice)) {
            var start, stop, step;
            start = index.start === null ? undefined : index.start;
            stop = index.stop === null ? undefined : index.stop;
            step = index.step;

            if (step === 0) {
                throw new batavia.builtins.ValueError("slice step cannot be zero");
            }

            // clone list
            var result = Array_.prototype.slice.call(this);

            // handle step
            if (step === undefined || step === 1) {
                return new List(result.slice(start, stop));
            } else if (step > 0) {
                result = result.slice(start, stop);
            } else if (step < 0) {
                // adjust start/stop to swap inclusion/exlusion in slice
                if (start !== undefined && start !== -1) {
                    start = start + 1;
                } else if (start === -1) {
                    start = result.length;
                }
                if (stop !== undefined && stop !== -1) {
                    stop = stop + 1;
                } else if (stop === -1) {
                    stop = result.length;
                }

                result = result.slice(stop, start).reverse();
            }

            var steppedResult = [];
            for (var i = 0; i < result.length; i = i + Math.abs(step)) {
                steppedResult.push(result[i]);
            }

            result = steppedResult;

            return new List(result);
        } else {
            var msg = "list indices must be integers or slices, not ";
            if (batavia.BATAVIA_MAGIC == batavia.BATAVIA_MAGIC_34) {
                msg = "list indices must be integers, not ";
            }
            throw new batavia.builtins.TypeError(msg + batavia.type_name(index));
        }
    };

    List.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for <<: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for >>: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__and__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__xor__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ^: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__or__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'list' and '" + batavia.type_name(other) + "'");
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    List.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__iadd__ = function(other) {
        if(batavia.isinstance(other, [batavia.types.List, batavia.types.Str,
            batavia.types.Tuple])) {
            for(i=0; i< other.length; i++) {
              this.push(other[i]);
            }
            return this;
        } else {
            throw new batavia.builtins.TypeError("'" + batavia.type_name(other) + "' object is not iterable");
        }
    };

    List.prototype.__isub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__imul__ = function(other) {
        if(batavia.isinstance(other, batavia.types.Int)) {
            if(other <= 0) {
                return new List();
            } else {
                list_length = this.length;
                for(i=1; i < other; i++) {
                    for(j=0; j < list_length; j++) {
                        this.push(this[j]);
                    }
                }
                return this;
            }
        } else if(batavia.isinstance(other, batavia.types.Bool)) {
            return other == true ? this : new List();
        } else {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type '" + batavia.type_name(other) + "'");
        }
    };

    List.prototype.__imod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for <<=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for >>=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__iand__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ^=: 'list' and '" + batavia.type_name(other) + "'");
    };

    List.prototype.__ior__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |=: 'list' and '" + batavia.type_name(other) + "'");
    };

    /**************************************************
     * Methods
     **************************************************/

    List.prototype.append = function(value) {
        this.push(value);
    };

    List.prototype.copy = function() {
        return new List(this);
    };

    List.prototype.extend = function(values) {
        if (values.length > 0) {
            this.push.apply(this, values);
        }
    };

    /**************************************************
     * List Iterator
     **************************************************/

    List.prototype.ListIterator = function (data) {
        Object.call(this);
        this.index = 0;
        this.data = data;
    };

    List.prototype.ListIterator.prototype = Object.create(Object.prototype);

    List.prototype.ListIterator.prototype.__iter__ = function() {
        return this;
    };

    List.prototype.ListIterator.prototype.__next__ = function() {
        if (this.index >= this.data.length) {
            throw new batavia.builtins.StopIteration();
        }
        var retval = this.data[this.index];
        this.index++;
        return retval;
    };

    List.prototype.ListIterator.prototype.__str__ = function() {
        return "<list_iterator object at 0x99999999>";
    };

    List.prototype.ListIterator.prototype.constructor = List.prototype.ListIterator;
    List.prototype.ListIterator.prototype.__class__ = new batavia.types.Type('list_iterator');

    /**************************************************/

    return List;
}();

/*************************************************************************
 * A Python map builtin is a type
 *************************************************************************/

batavia.types.map = function() {
    function map(args, kwargs) {
        Object.call(this);
        if (args.length < 2) {
            throw new batavia.builtins.TypeError("map expected 2 arguments, got " + args.length);
        }
        this._func = args[0];
        this._sequence = args[1];
    }

    map.prototype = Object.create(Object.prototype);
    map.prototype.__class__ = new batavia.types.Type('map');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    map.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    map.prototype.__iter__ = function() {
        return this;
    };

    map.prototype.__next__ = function() {
        if (!this._iter) {
            this._iter = batavia.builtins.iter([this._sequence], null);
        }
        if (!batavia.builtins.callable([this._func], null)) {
            throw new batavia.builtins.TypeError(
              batavia.type_name(this._func) + "' object is not callable");
        }

        var sval = batavia.run_callable(this._iter, this._iter.__next__, [], null);
        return batavia.run_callable(false, this._func, [sval], null);
    };

    map.prototype.__str__ = function() {
        return "<map object at 0x99999999>";
    };

    /**************************************************/

    return map;
}();

batavia.types.Module = function() {
    function Module(name, locals) {
        this.__name__ = name;
        for (var key in locals) {
            if (locals.hasOwnProperty(key)) {
                this[key] = locals[key];
            }
        }
    }

    Module.prototype = Object.create(Object.prototype);
    Module.prototype.__class__ = new batavia.types.Type('module');

    return Module;
}();

batavia.types.NoneType = function() {
    function NoneType() {
        Object.call(this);
    }

    NoneType.prototype = Object.create(Object.prototype);
    NoneType.prototype.__class__ = new batavia.types.Type('NoneType');

    NoneType.prototype.__name__ = 'NoneType';

    /**************************************************
     * Type conversions
     **************************************************/

    NoneType.prototype.__bool__ = function() {
        return false;
    };

    NoneType.prototype.__repr__ = function() {
        return "None";
    };

    NoneType.prototype.__str__ = function() {
        return "None";
    };

    /**************************************************
     * Attribute manipulation
     **************************************************/

    NoneType.prototype.__getattr__ = function(attr) {
        throw new batavia.builtins.AttributeError("'NoneType' object has no attribute '" + attr + "'");
    };

    NoneType.prototype.__setattr__ = function(attr, value) {
        throw new batavia.builtins.AttributeError("'NoneType' object has no attribute '" + attr + "'");
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    NoneType.prototype.__lt__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NoneType() < " +  batavia.type_name(other) + "()");
    };

    NoneType.prototype.__le__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NoneType() <= " +  batavia.type_name(other) + "()");
    };

    NoneType.prototype.__eq__ = function(other) {
        return other === this;
    };

    NoneType.prototype.__ne__ = function(other) {
        return other !== this;
    };

    NoneType.prototype.__gt__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NoneType() > " +  batavia.type_name(other) + "()");
    };

    NoneType.prototype.__ge__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NoneType() >= " +  batavia.type_name(other) + "()");
    };

    NoneType.prototype.__contains__ = function(other) {
        return false;
    };

    /**************************************************
     * Unary operators
     **************************************************/

    NoneType.prototype.__pos__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary +: 'NoneType'");
    };

    NoneType.prototype.__neg__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary -: 'NoneType'");
    };

    NoneType.prototype.__not__ = function() {
        return true;
    };

    NoneType.prototype.__invert__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary ~: 'NoneType'");
    };

    /**************************************************
     * Binary operators
     **************************************************/

    NoneType.prototype.__pow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__div__ = function(other) {
        return NoneType.__truediv__(other);
    };

    NoneType.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__mul__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.List, batavia.types.Tuple, batavia.types.Str])) {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'NoneType'");
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'NoneType' and '" + batavia.type_name(other) + "'");
        }
    };

    NoneType.prototype.__mod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__add__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__sub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__getitem__ = function(other) {
        throw new batavia.builtins.TypeError("'NoneType' object is not subscriptable");
    };

    NoneType.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for <<: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for >>: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__and__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__xor__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ^: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__or__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    NoneType.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__isub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__imul__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.List, batavia.types.Tuple, batavia.types.Str])) {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'NoneType'");
        } else {
            throw new batavia.builtins.TypeError("unsupported operand type(s) for *=: 'NoneType' and '" + batavia.type_name(other) + "'");
        }
    };

    NoneType.prototype.__imod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for <<=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for >>=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__iand__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ^=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    NoneType.prototype.__ior__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |=: 'NoneType' and '" + batavia.type_name(other) + "'");
    };

    return NoneType;
}();

/*************************************************************************
 * An implementation of NotImplementedType
 *************************************************************************/

batavia.types.NotImplementedType = function() {
    function NotImplementedType(args, kwargs) {
        Object.call(this);
        if (args) {
            this.update(args);
        }
    }

    NotImplementedType.prototype = Object.create(Object.prototype);
    NotImplementedType.prototype.__class__ = new batavia.types.Type('NotImplementedType');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    NotImplementedType.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    NotImplementedType.prototype.__bool__ = function() {
        return this.valueOf().length !== 0;
    };

    NotImplementedType.prototype.__iter__ = function() {
        return new NotImplementedType.prototype.NotImplementedIterator(this);
    };

    NotImplementedType.prototype.__repr__ = function() {
        return this.__str__();
    };

    NotImplementedType.prototype.__str__ = function() {
        var result = "{", values = [];
        for (var key in this) {
            if (this.hasOwnProperty(key)) {
                values.push(batavia.builtins.repr(key));
            }
        }
        result += values.join(', ');
        result += "}";
        return result;
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    NotImplementedType.prototype.__lt__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NotImplementedType() < " + batavia.type_name(other) + "()");
    };

    NotImplementedType.prototype.__le__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NotImplementedType() <= " + batavia.type_name(other) + "()");
    };

    NotImplementedType.prototype.__eq__ = function(other) {
        return this.valueOf() == other;
    };

    NotImplementedType.prototype.__ne__ = function(other) {
        return this.valueOf() != other;
    };

    NotImplementedType.prototype.__gt__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NotImplementedType() > " + batavia.type_name(other) + "()");
    };

    NotImplementedType.prototype.__ge__ = function(other) {
        throw new batavia.builtins.TypeError("unorderable types: NotImplementedType() >= " + batavia.type_name(other) + "()");
    };

    NotImplementedType.prototype.__contains__ = function(other) {
        return this.valueOf().hasOwnProperty(other);
    };


    /**************************************************
     * Unary operators
     **************************************************/

    NotImplementedType.prototype.__pos__ = function() {
        return new NotImplemented(+this.valueOf());
    };

    NotImplementedType.prototype.__neg__ = function() {
        return new NotImplemented(-this.valueOf());
    };

    NotImplementedType.prototype.__not__ = function() {
        return new NotImplemented(!this.valueOf());
    };

    NotImplementedType.prototype.__invert__ = function() {
        return new NotImplemented(~this.valueOf());
    };

    /**************************************************
     * Binary operators
     **************************************************/

    NotImplementedType.prototype.__pow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__div__ = function(other) {
        throw new batavia.builtins.NotImplementedError("NotImplementedType.__div__ has not been implemented");
    };

    NotImplementedType.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__mul__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.Tuple, batavia.types.Str, batavia.types.List, batavia.types.Bytes,
            batavia.types.Bytearray
        ])) {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'NotImplementedType'")
        }
        throw new batavia.builtins.TypeError("unsupported operand type(s) for *: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__mod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__add__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__sub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__getitem__ = function(other) {
        throw new batavia.builtins.NotImplementedError("NotImplementedType.__getitem__ has not been implemented");
    };

    NotImplementedType.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for <<: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for >>: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__and__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__xor__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ^: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__or__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    NotImplementedType.prototype.__idiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("NotImplementedType.__idiv__ has not been implemented");
    };

    NotImplementedType.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //=: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /=: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +=: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__isub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -=: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__imul__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.Tuple, batavia.types.Str, batavia.types.List, batavia.types.Bytes,
            batavia.types.Bytearray
        ])) {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type 'NotImplementedType'")
        }
        throw new batavia.builtins.TypeError("unsupported operand type(s) for *=: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__imod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %=: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for <<=: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for >>=: 'NotImplementedType' and '" + batavia.type_name(other) + "'");
    };

    NotImplementedType.prototype.__iand__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &=: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ^=: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    NotImplementedType.prototype.__ior__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for |=: 'NotImplementedType' and '" + batavia.type_name(other) + "'")
    };

    /**************************************************/

    return NotImplementedType;
}();
/*************************************************************************
 * An implementation of range
 *************************************************************************/

batavia.types.Range = function() {
    // BUG: Range supports longs.
    function Range(start, stop, step) {
        this.start = start.int32();
        this.step = new batavia.types.Int(step || 1).int32();

        if (stop === undefined) {
            this.start = 0;
            this.stop = start;
        } else {
            this.stop = stop.int32();
        }
    }

    Range.prototype = Object.create(Object.prototype);
    Range.prototype.__class__ = new batavia.types.Type('range');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Range.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Range.prototype.__iter__ = function() {
        return new Range.prototype.RangeIterator(this);
    };

    Range.prototype.__repr__ = function() {
        return this.__str__();
    };

    Range.prototype.__str__ = function() {
        if (this.step) {
            return '(' + this.start + ', ' + this.stop + ', ' + this.step + ')';
        } else {
            return '(' + this.start + ', ' + this.stop + ')';
        }
    };

    /**************************************************
     * Range Iterator
     **************************************************/

    Range.prototype.RangeIterator = function (data) {
        Object.call(this);
        this.data = data;
        this.index = this.data.start.valueOf();
        this.step = this.data.step.valueOf();
    };

    Range.prototype.RangeIterator.prototype = Object.create(Object.prototype);

    Range.prototype.RangeIterator.prototype.__next__ = function() {
        var retval = this.index;
        if ((this.step > 0 && this.index < this.data.stop) ||
            (this.step < 0 && this.index > this.data.stop)) {
            this.index = this.index + this.data.step;
            return new batavia.types.Int(retval);
        }
        throw new batavia.builtins.StopIteration();
    };

    Range.prototype.RangeIterator.prototype.__str__ = function() {
        return "<range_iterator object at 0x99999999>";
    };

    /**************************************************/

    return Range;
}();

/*************************************************************************
 * A Python Set type, with an underlying Dict.
 *************************************************************************/

batavia.types.Set = function() {
    function Set(args, kwargs) {
        this.data = new batavia.types.Dict();
        if (args) {
            this.update(args);
        }
    }

    Set.prototype.__class__ = new batavia.types.Type('set');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Set.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Set.prototype.__bool__ = function() {
        return this.data.__bool__();
    };

    Set.prototype.__iter__ = function() {
        return new batavia.types.SetIterator(this);
    };

    Set.prototype.__repr__ = function() {
        return this.__str__();
    };

    Set.prototype.__str__ = function() {
        var keys = this.data.keys();
        if (keys.length == 0) {
            return "set()";
        }
        return "{" + keys.map(function(x) { return x.__repr__(); }).join(", ") + "}";
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Set.prototype.__lt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: set() < " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() < other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: set() < NoneType()");
        }
    };

    Set.prototype.__le__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: set() <= " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() <= other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: set() <= NoneType()");
        }
    };

    Set.prototype.__eq__ = function(other) {
        if (!batavia.isinstance(other, [batavia.types.FrozenSet, batavia.types.Set])) {
            return new batavia.types.Bool(false);
        }
        if (this.data.keys().length != other.data.keys().length) {
            return new batavia.types.Bool(false);
        }
        var iterobj = batavia.builtins.iter([this], null);
        var equal = true;
        batavia.iter_for_each(iterobj, function(val) {
            equal = equal && other.__contains__(val).valueOf();
        });

        return new batavia.types.Bool(equal);
    };

    Set.prototype.__ne__ = function(other) {
        return this.__eq__(other).__not__();
    };

    Set.prototype.__gt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: set() > " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() > other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: set() > NoneType()");
        }
    };

    Set.prototype.__ge__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: set() >= " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() >= other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: set() >= NoneType()");
        }
    };

    Set.prototype.__contains__ = function(other) {
        return this.data.__contains__(other);
    };


    /**************************************************
     * Unary operators
     **************************************************/

    Set.prototype.__not__ = function() {
        return this.__bool__().__not__();
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Set.prototype.__pow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__pow__ has not been implemented");
    };

    Set.prototype.__div__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__div__ has not been implemented");
    };

    Set.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__floordiv__ has not been implemented");
    };

    Set.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'set' and '" + batavia.type_name(other) + "'");
    };

    Set.prototype.__mul__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'set' and '" + batavia.type_name(other) + "'");
    };

    Set.prototype.__mod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__mod__ has not been implemented");
    };

    Set.prototype.__add__ = function(other) {
		throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'set' and '" + batavia.type_name(other) + "'");
    };

    Set.prototype.__sub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__sub__ has not been implemented");
    };

    Set.prototype.__getitem__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__getitem__ has not been implemented");
    };

    Set.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__lshift__ has not been implemented");
    };

    Set.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__rshift__ has not been implemented");
    };

    Set.prototype.__and__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.FrozenSet, batavia.types.Set])){
            var both = [];
            var iterobj = batavia.builtins.iter([this], null);
            batavia.iter_for_each(iterobj, function(val) {
                if (other.__contains__(val).valueOf()) {
                    both.push(val);
                }
            });
            return new Set(both);
        }
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'set' and '" + batavia.type_name(other) + "'");
    };

    Set.prototype.__xor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__xor__ has not been implemented");
    };

    Set.prototype.__or__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__or__ has not been implemented");
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    Set.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__ifloordiv__ has not been implemented");
    };

    Set.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__itruediv__ has not been implemented");
    };

    Set.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +=: 'set' and '" + batavia.type_name(other) + "'");
    };

    Set.prototype.__isub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__isub__ has not been implemented");
    };

    Set.prototype.__imul__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__imul__ has not been implemented");
    };

    Set.prototype.__imod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__imod__ has not been implemented");
    };

    Set.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__ipow__ has not been implemented");
    };

    Set.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__ilshift__ has not been implemented");
    };

    Set.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__irshift__ has not been implemented");
    };

    Set.prototype.__iand__ = function(other) {
        if (batavia.isinstance(other, [
                batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                batavia.types.List, batavia.types.Int, batavia.types.Range,
                batavia.types.Slice, batavia.types.Str, batavia.types.Tuple,
                batavia.types.NoneType
            ])) {
            throw new batavia.builtins.TypeError(
                "unsupported operand type(s) for &=: 'set' and '" + batavia.type_name(other) + "'");
        }
        if (batavia.isinstance(other, [batavia.types.FrozenSet, batavia.types.Set])) {
            var intersection = new Set();
            var iterobj = batavia.builtins.iter([this], null);
            var self = this;
            batavia.iter_for_each(iterobj, function(val) {
                if (other.__contains__(val).valueOf()) {
                    intersection.add(val);
                }
            });
            return intersection;
        }
        throw new batavia.builtins.NotImplementedError(
            "Set.__iand__ has not been implemented for type '" + batavia.type_name(other) + "'");
    };

    Set.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__ixor__ has not been implemented");
    };

    Set.prototype.__ior__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Set.__ior__ has not been implemented");
    };

    /**************************************************
     * Methods
     **************************************************/

    Set.prototype.add = function(v) {
        this.data.__setitem__(v, v);
    };

    Set.prototype.copy = function() {
        return new Set(this);
    };

    Set.prototype.remove = function(v) {
        this.data.__delitem__(v);
    };

    Set.prototype.update = function(args) {
        var new_args = batavia.js2py(args);
        if (batavia.isinstance(new_args, [batavia.types.FrozenSet, batavia.types.List, batavia.types.Set, batavia.types.Str, batavia.types.Tuple])) {
            var iterobj = batavia.builtins.iter([new_args], null);
            var self = this;
            batavia.iter_for_each(iterobj, function(val) {
                self.data.__setitem__(val, val);
            });
        } else {
            throw new batavia.builtins.TypeError("'" + batavia.type_name(new_args) + "' object is not iterable");
        }
    };

    /**************************************************/

    return Set;
}();
/**************************************************
 * Set Iterator
 **************************************************/

batavia.types.SetIterator = function (data) {
    Object.call(this);
    this.index = 0;
    this.data = data;
    this.keys = data.data.keys();
};

batavia.types.SetIterator.prototype = Object.create(Object.prototype);

batavia.types.SetIterator.prototype.__next__ = function() {
    var key = this.keys[this.index];
    if (key === undefined) {
        throw new batavia.builtins.StopIteration();
    }
    this.index++;
    return key;
};

batavia.types.SetIterator.prototype.__str__ = function() {
    return "<set_iterator object at 0x99999999>";
};
/*************************************************************************
 * An implementation of slice
 *************************************************************************/

batavia.types.Slice = function() {
    function Slice(kwargs) {
        // BUG: slices can support arbitrary-sized arguments.
        this.start = kwargs.start === batavia.builtins.None ? null : kwargs.start.int32();
        this.stop = kwargs.stop === batavia.builtins.None ? null : kwargs.stop.int32();
        this.step = (kwargs.step || 1)|0;
    }

    Slice.prototype = Object.create(Object.prototype);
    Slice.prototype.__class__ = new batavia.types.Type('slice');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Slice.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Slice.prototype.__repr__ = function() {
        return this.__str__();
    };

    Slice.prototype.__str__ = function() {
        if (this.step) {
            return '(' + this.start + ', ' + this.stop + ', ' + this.step + ')';
        } else {
            return '(' + this.start + ', ' + this.stop + ')';
        }
    };

    /**************************************************/

    return Slice;
}();

/*************************************************************************
 * A Python FrozenSet type, with an underlying Dict.
 *************************************************************************/

batavia.types.FrozenSet = function() {
    function FrozenSet(args, kwargs) {
        this.data = new batavia.types.Dict();
        if (args) {
            this._update(args);
        }
    }

    FrozenSet.prototype.__class__ = new batavia.types.Type('frozenset');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    FrozenSet.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    FrozenSet.prototype.__bool__ = function() {
        return this.data.__bool__();
    };

    FrozenSet.prototype.__iter__ = function() {
        return new batavia.types.SetIterator(this);
    };

    FrozenSet.prototype.__repr__ = function() {
        return this.__str__();
    };

    FrozenSet.prototype.__str__ = function() {
        var keys = this.data.keys();
        if (keys.length == 0) {
            return "frozenset()";
        }
        return "frozenset({" +
            keys.map(function(x) { return x.__repr__(); }).join(", ") +
            "})";
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    FrozenSet.prototype.__lt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: frozenset() < " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() < other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: frozenset() < NoneType()");
        }
    };

    FrozenSet.prototype.__le__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: frozenset() <= " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() <= other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: frozenset() <= NoneType()");
        }
    };

    FrozenSet.prototype.__eq__ = function(other) {
        if (!batavia.isinstance(other, [batavia.types.FrozenSet, batavia.types.Set])) {
            return new batavia.types.Bool(false);
        }
        if (this.data.keys().length != other.data.keys().length) {
            return new batavia.types.Bool(false);
        }
        var iterobj = batavia.builtins.iter([this], null);
        var equal = true;
        batavia.iter_for_each(iterobj, function(val) {
            equal = equal && other.__contains__(val).valueOf();
        });

        return new batavia.types.Bool(equal);
    };

    FrozenSet.prototype.__ne__ = function(other) {
        return this.__eq__(other).__not__();
    };

    FrozenSet.prototype.__gt__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: frozenset() > " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() > other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: frozenset() > NoneType()");
        }
    };

    FrozenSet.prototype.__ge__ = function(other) {
        if (other !== batavia.builtins.None) {
            if (batavia.isinstance(other, [
                        batavia.types.Bool, batavia.types.Dict, batavia.types.Float,
                        batavia.types.List, batavia.types.Int, batavia.types.Range,
                        batavia.types.Str, batavia.types.Tuple
                    ])) {
                throw new batavia.builtins.TypeError("unorderable types: frozenset() >= " + batavia.type_name(other) + "()");
            } else {
                return this.valueOf() >= other.valueOf();
            }
        } else {
            throw new batavia.builtins.TypeError("unorderable types: frozenset() >= NoneType()");
        }
    };

    FrozenSet.prototype.__contains__ = function(other) {
        return this.data.__contains__(other);
    };


    /**************************************************
     * Unary operators
     **************************************************/

    FrozenSet.prototype.__not__ = function() {
        return this.__bool__().__not__();
    };

    /**************************************************
     * Binary operators
     **************************************************/

    FrozenSet.prototype.__pow__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__pow__ has not been implemented");
    };

    FrozenSet.prototype.__div__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__div__ has not been implemented");
    };

    FrozenSet.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'frozenset' and '" + batavia.type_name(other) + "'");
    };

    FrozenSet.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'frozenset' and '" + batavia.type_name(other) + "'");
    };

    FrozenSet.prototype.__mul__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'frozenset' and '" + batavia.type_name(other) + "'");
    };

    FrozenSet.prototype.__mod__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__mod__ has not been implemented");
    };

    FrozenSet.prototype.__add__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for +: 'frozenset' and '" + batavia.type_name(other) + "'");
    };

    FrozenSet.prototype.__sub__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__sub__ has not been implemented");
    };

    FrozenSet.prototype.__getitem__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__getitem__ has not been implemented");
    };

    FrozenSet.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__lshift__ has not been implemented");
    };

    FrozenSet.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__rshift__ has not been implemented");
    };

    FrozenSet.prototype.__and__ = function(other) {
        if (batavia.isinstance(other, [batavia.types.FrozenSet, batavia.types.Set])){
            var both = [];
            var iterobj = batavia.builtins.iter([this], null);
            batavia.iter_for_each(iterobj, function(val) {
                if (other.__contains__(val).valueOf()) {
                    both.push(val);
                }
            });
            return new FrozenSet(both);
        }
        throw new batavia.builtins.TypeError("unsupported operand type(s) for &: 'frozenset' and '" + batavia.type_name(other) + "'");
    };

    FrozenSet.prototype.__xor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__xor__ has not been implemented");
    };

    FrozenSet.prototype.__or__ = function(other) {
        throw new batavia.builtins.NotImplementedError("FrozenSet.__or__ has not been implemented");
    };

    /**************************************************
     * Methods
     **************************************************/

    FrozenSet.prototype._update = function(args) {
        var new_args = batavia.js2py(args);
        if (batavia.isinstance(new_args, [batavia.types.FrozenSet, batavia.types.List, batavia.types.Set, batavia.types.Str, batavia.types.Tuple])) {
            var iterobj = batavia.builtins.iter([new_args], null);
            var self = this;
            batavia.iter_for_each(iterobj, function(val) {
                self.data.__setitem__(val, val);
            });
        } else {
            throw new batavia.builtins.TypeError("'" + batavia.type_name(new_args) + "' object is not iterable");
        }
    };

    /**************************************************/

    return FrozenSet;
}();

/*************************************************************************
 * Modify String to behave like a Python String
 *************************************************************************/

batavia.types.Str = String;
String.prototype.__class__ = new batavia.types.Type('str');

/**************************************************
 * Type conversions
 **************************************************/

String.prototype.__bool__ = function() {
    return this.length > 0;
};

String.prototype.__iter__ = function() {
    return new String.prototype.StrIterator(this);
};

String.prototype.__repr__ = function() {
    // we have to replace all non-printable characters
    return "'" + this.toString()
        .replace(/\\/g, "\\\\")
        .replace(/'/g, "\\'")
        .replace(/\x7F/g, "\\x7f")
        .replace(/[\u0000-\u001F]/g, function (match) {
            var code = match.charCodeAt(0);
            switch (code) {
            case 9:
                return "\\t";
            case 10:
                return "\\n";
            case 13:
                return "\\r";
            default:
                var hex = code.toString(16);
                if (hex.length == 1) {
                  hex = "0" + hex;
                }
                return "\\x" + hex;
            }
        }) + "'";
};

String.prototype.__str__ = function() {
    return this.toString();
};

/**************************************************
 * Attribute manipulation
 **************************************************/

String.prototype.__getattr__ = function(attr) {
    if (this[attr] === undefined) {
        throw new batavia.builtins.AttributeError("'str' object has no attribute '" + attr + "'");
    }
    return this[attr];
},

String.prototype.__setattr__ = function(attr, value) {
    throw new batavia.builtins.AttributeError("'str' object has no attribute '" + attr + "'");
},
/**************************************************
 * Comparison operators
 **************************************************/

String.prototype.__lt__ = function(other) {
    if (other !== batavia.builtins.None) {
        if (batavia.isinstance(other, [
                    batavia.types.Bool, batavia.types.Int, batavia.types.Float,
                    batavia.types.List, batavia.types.Dict, batavia.types.Tuple,
                    batavia.types.Bytearray, batavia.types.Bytes, batavia.types.Type,
                    batavia.types.Complex, batavia.types.NotImplementedType,
                    batavia.types.Range, batavia.types.Set, batavia.types.Slice,
                    batavia.types.FrozenSet
                ])) {
            throw new batavia.builtins.TypeError("unorderable types: str() < " + batavia.type_name(other) + "()");
        } else {
            return this.valueOf() < other;
        }
    } else {
        throw new batavia.builtins.TypeError("unorderable types: str() < NoneType()");
    }
};

String.prototype.__le__ = function(other) {
    if (other !== batavia.builtins.None) {
        if (batavia.isinstance(other, [
                    batavia.types.Bool, batavia.types.Int, batavia.types.Float,
                    batavia.types.List, batavia.types.Dict, batavia.types.Tuple,
                    batavia.types.Set, batavia.types.Bytearray, batavia.types.Bytes,
                    batavia.types.Type, batavia.types.Complex, batavia.types.NotImplementedType,
                    batavia.types.Range, batavia.types.Slice, batavia.types.FrozenSet
                ])) {
            throw new batavia.builtins.TypeError("unorderable types: str() <= " + batavia.type_name(other) + "()");
        } else {
            return this.valueOf() <= other;
        }
    } else {
        throw new batavia.builtins.TypeError("unorderable types: str() <= NoneType()");
    }
};

String.prototype.__eq__ = function(other) {
    if (other !== batavia.builtins.None) {
        if (batavia.isinstance(other, [
                    batavia.types.Bool, batavia.types.Int, batavia.types.Float,
                    batavia.types.List, batavia.types.Dict, batavia.types.Tuple
                ])) {
            return false;
        } else {
            return this.valueOf() === other.valueOf();
        }
    } else {
        return false;
    }
};

String.prototype.__ne__ = function(other) {
    if (other !== batavia.builtins.None) {
        if (batavia.isinstance(other, [
                    batavia.types.Bool, batavia.types.Int, batavia.types.Float,
                    batavia.types.List, batavia.types.Dict, batavia.types.Tuple

                ])) {
            return true;
        } else {
            return this.valueOf() !== other.valueOf();
        }
    } else {
        return true;
    }
};

String.prototype.__gt__ = function(other) {
    if (other !== batavia.builtins.None) {
        if (batavia.isinstance(other, [
                    batavia.types.Bool, batavia.types.Int, batavia.types.Float,
                    batavia.types.List, batavia.types.Dict, batavia.types.Tuple,
                    batavia.types.Set, batavia.types.Bytearray, batavia.types.Bytes,
                    batavia.types.Type, batavia.types.Complex,
                    batavia.types.NotImplementedType, batavia.types.Range,
                    batavia.types.Slice, batavia.types.FrozenSet
                ])) {
            throw new batavia.builtins.TypeError("unorderable types: str() > " + batavia.type_name(other) + "()");
        } else {
            return this.valueOf() > other;
        }
    } else {
        throw new batavia.builtins.TypeError("unorderable types: str() > NoneType()");
    }
};

String.prototype.__ge__ = function(other) {
    if (other !== batavia.builtins.None) {
        if (batavia.isinstance(other, [
                    batavia.types.Bool, batavia.types.Int, batavia.types.Float,
                    batavia.types.List, batavia.types.Dict, batavia.types.Tuple,
                    batavia.types.Set, batavia.types.Bytearray, batavia.types.Bytes,
                    batavia.types.Type, batavia.types.Complex, batavia.types.NotImplementedType,
                    batavia.types.Range, batavia.types.Slice, batavia.types.FrozenSet

                ])) {
            throw new batavia.builtins.TypeError("unorderable types: str() >= " + batavia.type_name(other) + "()");
        } else {
            return this.valueOf() >= other;
        }
    } else {
        throw new batavia.builtins.TypeError("unorderable types: str() >= NoneType()");
    }
};

String.prototype.__contains__ = function(other) {
    return false;
};

/**************************************************
 * Unary operators
 **************************************************/

String.prototype.__pos__ = function() {
    throw new batavia.builtins.TypeError("bad operand type for unary +: 'str'");
};

String.prototype.__neg__ = function() {
    throw new batavia.builtins.TypeError("bad operand type for unary -: 'str'");
};

String.prototype.__not__ = function() {
    return this.length == 0;
};

String.prototype.__invert__ = function() {
    throw new batavia.builtins.TypeError("bad operand type for unary ~: 'str'");
};

/**************************************************
 * Binary operators
 **************************************************/

String.prototype.__pow__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'str' and '"+ batavia.type_name(other) + "'");
};

String.prototype.__div__ = function(other) {
    return this.__truediv__(other);
};

String.prototype.__floordiv__ = function(other) {
    if (batavia.isinstance(other, [batavia.types.Complex])){
        throw new batavia.builtins.TypeError("can't take floor of complex number.")
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'str' and '" + batavia.type_name(other) + "'");
    }
};

String.prototype.__truediv__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'str' and '" + batavia.type_name(other) + "'");
};

String.prototype.__mul__ = function(other) {
    var result;
    if (batavia.isinstance(other, batavia.types.Int)) {
        result = '';
        for (var i = 0; i < other.valueOf(); i++) {
            result += this.valueOf();
        }
        return result;
    } else if (batavia.isinstance(other, batavia.types.Bool)) {
        result = other === true ? this.valueOf() : '';
        return result;
    } else {
        throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type '" + batavia.type_name(other) + "'");
    }
};

String.prototype.__mod__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Tuple)) {
        return batavia._substitute(this, other);
    } else {
        return batavia._substitute(this, [other]);
    }
};

String.prototype.__add__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Str)) {
        return this.valueOf() + other.valueOf();
    } else {
        throw new batavia.builtins.TypeError("Can't convert '" + batavia.type_name(other) + "' object to str implicitly");
    }
};

String.prototype.__sub__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'str' and '" + batavia.type_name(other) + "'");
};

String.prototype.__getitem__ = function(index) {
    if (batavia.isinstance(index, batavia.types.Bool)) {
        index = index.__int__();
    }
    if (batavia.isinstance(index, batavia.types.Int)) {
        var idx = index.int32();
        if (idx < 0) {
            if (-idx > this.length) {
                throw new batavia.builtins.IndexError("string index out of range");
            } else {
                return this[this.length + idx];
            }
        } else {
            if (idx >= this.length) {
                throw new batavia.builtins.IndexError("string index out of range");
            } else {
                return this[idx];
            }
        }
    } else if (batavia.isinstance(index, batavia.types.Slice)) {
        var start, stop, step;
        start = index.start === null ? undefined : index.start.valueOf();
        stop = index.stop === null ? undefined : index.stop.valueOf();
        step = index.step.valueOf();

        if (step === 0) {
            throw new batavia.builtins.ValueError("slice step cannot be zero");
        }

        // clone string
        var result = this.valueOf();

        // handle step
        if (step === undefined || step === 1) {
            return result.slice(start, stop);
        } else if (step > 0) {
            result = result.slice(start, stop);
        } else if (step < 0) {
            // adjust start/stop to swap inclusion/exlusion in slice
            if (start !== undefined && start !== -1) {
                start = start + 1;
            } else if (start === -1) {
                start = result.length;
            }
            if (stop !== undefined && stop !== -1) {
                stop = stop + 1;
            } else if (stop === -1) {
                stop = result.length;
            }

            result = result.slice(stop, start).split('').reverse().join('');
        }

        var steppedResult = "";
        for (var i = 0; i < result.length; i = i + Math.abs(step)) {
            steppedResult += result[i];
        }

        result = steppedResult;

        return result;
    } else {
        throw new batavia.builtins.TypeError("string indices must be integers");
    }
};

String.prototype.__lshift__ = function(other) {
    throw new batavia.builtins.TypeError(
        "unsupported operand type(s) for <<: 'str' and '" + batavia.type_name(other) + "'"
    );
};

String.prototype.__rshift__ = function(other) {
    throw new batavia.builtins.TypeError(
        "unsupported operand type(s) for >>: 'str' and '" + batavia.type_name(other) + "'"
    );
};

String.prototype.__and__ = function(other) {
    throw new batavia.builtins.TypeError(
        "unsupported operand type(s) for &: 'str' and '" + batavia.type_name(other) + "'"
    );
};

String.prototype.__xor__ = function(other) {
    throw new batavia.builtins.TypeError(
        "unsupported operand type(s) for ^: 'str' and '" + batavia.type_name(other) + "'"
    );
};

String.prototype.__or__ = function(other) {
    throw new batavia.builtins.TypeError(
        "unsupported operand type(s) for |: 'str' and '" + batavia.type_name(other) + "'"
    );
};

/**************************************************
 * Inplace operators
 **************************************************/

String.prototype.__ifloordiv__ = function(other) {

    if (batavia.isinstance(other, [batavia.types.Complex])){
        throw new batavia.builtins.TypeError("can't take floor of complex number.")
    } else {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //=: 'str' and '" + batavia.type_name(other) + "'");
    }
};

String.prototype.__itruediv__ = function(other) {

    throw new batavia.builtins.TypeError("unsupported operand type(s) for /=: 'str' and '" + batavia.type_name(other) + "'");
};

String.prototype.__iadd__ = function(other) {
    if (batavia.isinstance(other, batavia.types.Str)) {
        return this.valueOf() + other.valueOf();
    } else {
        throw new batavia.builtins.TypeError("Can't convert '" + batavia.type_name(other) + "' object to str implicitly");
    }
};

String.prototype.__isub__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for -=: 'str' and '" + batavia.type_name(other) + "'");
};

String.prototype.__imul__ = function(other) {
    return this.__mul__(other);

};

String.prototype.__imod__ = function(other) {
    if (batavia.isinstance(other, [
            batavia.types.Bool,
            batavia.types.Float,
            batavia.types.FrozenSet,
            batavia.types.Int,
            batavia.types.NoneType,
            batavia.types.Set,
            batavia.types.Str,
            batavia.types.Tuple
        ])) {
        throw new batavia.builtins.TypeError("not all arguments converted during string formatting");
    } else {
        throw new batavia.builtins.NotImplementedError("String.__imod__ has not been implemented");
    }
};

String.prototype.__ipow__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'str' and '" + batavia.type_name(other) + "'");

};

String.prototype.__ilshift__ = function(other) {
    throw new batavia.builtins.TypeError(
        "unsupported operand type(s) for <<=: 'str' and '" + batavia.type_name(other) + "'"
    )
};

String.prototype.__irshift__ = function(other) {


    throw new batavia.builtins.TypeError("unsupported operand type(s) for >>=: 'str' and '" + batavia.type_name(other) + "'");
};

String.prototype.__iand__ = function(other) {

    throw new batavia.builtins.TypeError("unsupported operand type(s) for &=: 'str' and '" + batavia.type_name(other) + "'");

};

String.prototype.__ixor__ = function(other) {

    throw new batavia.builtins.TypeError("unsupported operand type(s) for ^=: 'str' and '" + batavia.type_name(other) + "'");
};

String.prototype.__ior__ = function(other) {
    throw new batavia.builtins.TypeError("unsupported operand type(s) for |=: 'str' and '" + batavia.type_name(other) + "'");

};

/**************************************************
 * Methods
 **************************************************/

String.prototype.join = function(iter) {
    var l = new batavia.types.List(iter);
    for (var i = 0; i < l.length; i++) {
        if (!batavia.isinstance(l[i], batavia.types.Str)) {
            throw new batavia.builtins.TypeError("sequence item " + i + ": expected str instance, " + batavia.type_name(l[i]) + " found");
        }
    }
    return l.join(this);
};

/**************************************************
 * Str Iterator
 **************************************************/

String.prototype.StrIterator = function (data) {
    Object.call(this);
    this.index = 0;
    this.data = data;
};

String.prototype.StrIterator.prototype = Object.create(Object.prototype);

String.prototype.StrIterator.prototype.__next__ = function() {
    var retval = this.data[this.index];
    if (retval === undefined) {
        throw new batavia.builtins.StopIteration();
    }
    this.index++;
    return retval;
};

String.prototype.StrIterator.prototype.__str__ = function() {
    return "<str_iterator object at 0x99999999>";
};

/**************************************************
 * Methods
 **************************************************/

String.prototype.copy = function() {
    return this.valueOf();
};

String.prototype.startswith = function (str) {
    return this.slice(0, str.length) === str;
};

String.prototype.__setattr__ = function (name, val) {
    if (this.__proto__[name] === undefined) {
        throw new batavia.builtins.AttributeError("'str' object has no attribute '" + name + "'");
    } else {
        throw new batavia.builtins.AttributeError("'str' object attribute '" + name + "' is read-only");
    }
};

// Based on https://en.wikipedia.org/wiki/Universal_hashing#Hashing_strings
// and http://www.cse.yorku.ca/~oz/hash.html.
//
// CPython returns signed 64-bit integers. But, JS is awful at 64-bit integers,
// so we return signed 32-bit integers. This shouldn't be a problem, since
// technically we can just return 0 and everything should still work :P
String.prototype.__hash__ = function() {
    // |0 is used to ensure that we return signed 32-bit integers
    var h = 5381|0;
    for (var i = 0; i < this.length; i++) {
        h = ((h * 33)|0) ^ this[i];
    }
    return new batavia.types.Int(h);
};

/*************************************************************************
 * A Python Tuple type
 *************************************************************************/

batavia.types.Tuple = function() {
    function Tuple(length){
        if (arguments.length === 0) {
            this.push.apply(this);
        } else if (arguments.length === 1) {
            // Fast-path for native Array objects.
            if (batavia.isArray(arguments[0])) {
                this.push.apply(this, arguments[0]);
            } else {
                var iterobj = batavia.builtins.iter([arguments[0]], null);
                var self = this;
                batavia.iter_for_each(iterobj, function(val) {
                    self.push(val);
                });
            }
        } else {
            throw new batavia.builtins.TypeError('tuple() takes at most 1 argument (' + arguments.length + ' given)');
        }
    }

    function Array() {}

    Array.prototype = [];

    Tuple.prototype = Object.create(Array.prototype);
    Tuple.prototype.length = 0;
    Tuple.prototype.__class__ = new batavia.types.Type('tuple');

    /**************************************************
     * Javascript compatibility methods
     **************************************************/

    Tuple.prototype.toString = function() {
        return this.__str__();
    };

    /**************************************************
     * Type conversions
     **************************************************/

    Tuple.prototype.__iter__ = function() {
        return new Tuple.prototype.TupleIterator(this);
    };

    Tuple.prototype.__len__ = function () {
        return this.length;
    };

    Tuple.prototype.__repr__ = function() {
        return this.__str__();
    };

    Tuple.prototype.__str__ = function() {
        return '(' + this.map(function(obj) {
                return batavia.builtins.repr([obj], null);
            }).join(', ') + (this.length === 1 ? ',)' : ')');
    };

    /**************************************************
     * Comparison operators
     **************************************************/

    Tuple.prototype.__lt__ = function(other) {
        if (!batavia.isinstance(other, batavia.types.Tuple)) {
            throw new batavia.builtins.TypeError('unorderable types: tuple() < ' + batavia.type_name(other) + '()')
        }
        if (this.length == 0 && other.length > 0) {
            return true;
        }
        for (var i = 0; i < this.length; i++) {
            if (i >= other.length) {
                return false;
            }
            if (this[i].__lt__(other[i])) {
                return true;
            } else if (this[i].__eq__(other[i])) {
                continue;
            } else {
                return false;
            }
        }
        return this.length < other.length;
    };

    Tuple.prototype.__le__ = function(other) {
        return this.__lt__(other) || this.__eq__(other);
    };

    Tuple.prototype.__eq__ = function(other) {
        if (!batavia.isinstance(other, batavia.types.Tuple)) {
            return false;
        }
        if (this.length != other.length) {
            return false;
        }
        for (var i = 0; i < this.length; i++) {
            if (!this[i].__eq__(other[i])) {
                return false;
            }
        }
        return true;
    };

    Tuple.prototype.__ne__ = function(other) {
        return !this.__eq__(other);
    };

    Tuple.prototype.__gt__ = function(other) {
        if (!batavia.isinstance(other, batavia.types.Tuple)) {
            throw new batavia.builtins.TypeError('unorderable types: tuple() > ' + batavia.type_name(other) + '()')
        }
        if (this.length == 0 && other.length > 0) {
            return false;
        }
        for (var i = 0; i < this.length; i++) {
            if (i >= other.length) {
                return true;
            }
            if (this[i].__lt__(other[i])) {
                return false;
            } else if (this[i].__eq__(other[i])) {
                continue;
            } else {
                return true;
            }
        }
        return this.length > other.length;
    };

    Tuple.prototype.__ge__ = function(other) {
      return this.__gt__(other) || this.__eq__(other);
    };

    Tuple.prototype.__contains__ = function(other) {
        return this.valueOf().index(other) !== -1;
    };

    /**************************************************
     * Unary operators
     **************************************************/

    Tuple.prototype.__pos__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary +: 'tuple'");
    };

    Tuple.prototype.__neg__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary -: 'tuple'");
    };

    Tuple.prototype.__not__ = function() {
        return !this.__bool__();
    };

    Tuple.prototype.__invert__ = function() {
        throw new batavia.builtins.TypeError("bad operand type for unary ~: 'tuple'");
    };

    Tuple.prototype.__bool__ = function() {
        return this.length > 0;
    };

    /**************************************************
     * Binary operators
     **************************************************/

    Tuple.prototype.__pow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__div__ = function(other) {
        return this.__truediv__(other);
    };

    Tuple.prototype.__floordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__truediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__mul__ = function(other) {
        if (batavia.isinstance(other, batavia.types.Int)) {
            result = new List();
            for (var i = 0; i < other.valueOf(); i++) {
                result.extend(this);
            }
            return result;
        } else if (batavia.isinstance(other, batavia.types.Bool)) {
            if (other.valueOf()) {
                return this.copy();
            } else {
                return new List();
            }
        } else {
            throw new batavia.builtins.TypeError("can't multiply sequence by non-int of type '" + batavia.type_name(other) + "'");
        }
    };

    Tuple.prototype.__mod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__add__ = function(other) {
		if (!batavia.isinstance(other, batavia.types.Tuple)) {
			throw new batavia.builtins.TypeError('can only concatenate tuple (not "' + batavia.type_name(other) + '") to tuple')
		} else {
			result = new Tuple();
			for (var i = 0; i < this.length; i++){
				result.push(this[i]);
			}

			for (var i = 0; i < other.length; i++){
				result.push(other[i]);
			}

			return result;
		}
    };

    Tuple.prototype.__sub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__getitem__ = function(index) {
    		if (batavia.isinstance(index, batavia.types.Int)) {
            var idx = index.int32();
            if (idx < 0) {
                if (-idx > this.length) {
                    throw new batavia.builtins.IndexError("tuple index out of range");
                } else {
                    return this[this.length + idx];
                }
            } else {
                if (idx >= this.length) {
                    throw new batavia.builtins.IndexError("tuple index out of range");
                } else {
                    return this[idx];
                }
            }
        } else if (batavia.isinstance(index, batavia.types.Slice)) {
            var start, stop, step;
            start = index.start;

            if (index.stop === null) {
                stop = this.length;
            } else {
                stop = index.stop;
            }

            step = index.step;

            if (step != 1) {
                throw new batavia.builtins.NotImplementedError("Tuple.__getitem__ with a stepped slice has not been implemented");
            }

            return new Tuple(Array.prototype.slice.call(this, start, stop));
        } else {
            var msg = "tuple indices must be integers or slices, not ";
            if (batavia.BATAVIA_MAGIC == batavia.BATAVIA_MAGIC_34) {
                msg = "tuple indices must be integers, not ";
            }
            throw new batavia.builtins.TypeError(msg + batavia.type_name(index));
    		}
    };

    Tuple.prototype.__lshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__lshift__ has not been implemented");
    };

    Tuple.prototype.__rshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__rshift__ has not been implemented");
    };

    Tuple.prototype.__and__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__and__ has not been implemented");
    };

    Tuple.prototype.__xor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__xor__ has not been implemented");
    };

    Tuple.prototype.__or__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__or__ has not been implemented");
    };

    /**************************************************
     * Inplace operators
     **************************************************/

    Tuple.prototype.__ifloordiv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for //=: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__itruediv__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for /=: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__iadd__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__iadd__ has not been implemented");
    };

    Tuple.prototype.__isub__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for -=: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__imul__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__imul__ has not been implemented");
    };

    Tuple.prototype.__imod__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for %=: 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__ipow__ = function(other) {
        throw new batavia.builtins.TypeError("unsupported operand type(s) for ** or pow(): 'tuple' and '" + batavia.type_name(other) + "'");
    };

    Tuple.prototype.__ilshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__ilshift__ has not been implemented");
    };

    Tuple.prototype.__irshift__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__irshift__ has not been implemented");
    };

    Tuple.prototype.__iand__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__iand__ has not been implemented");
    };

    Tuple.prototype.__ixor__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__ixor__ has not been implemented");
    };

    Tuple.prototype.__ior__ = function(other) {
        throw new batavia.builtins.NotImplementedError("Tuple.__ior__ has not been implemented");
    };

    /**************************************************
     * Methods
     **************************************************/

    Tuple.prototype.copy = function() {
        return new Tuple(this);
    };

    /**************************************************
     * Tuple Iterator
     **************************************************/

    Tuple.prototype.TupleIterator = function (data) {
        Object.call(this);
        this.index = 0;
        this.data = data;
    };

    Tuple.prototype.TupleIterator.prototype = Object.create(Object.prototype);

    Tuple.prototype.TupleIterator.prototype.__next__ = function() {
        var retval = this.data[this.index];
        if (retval === undefined) {
            throw new batavia.builtins.StopIteration();
        }
        this.index++;
        return retval;
    };

    Tuple.prototype.TupleIterator.prototype.__str__ = function() {
        return "<tuple_iterator object at 0x99999999>";
    };

    /**************************************************/

    return Tuple;
}();
batavia.modules.base64 = {
	__doc__: "",
	__name__: "base64",
	__file__: "base64.js",
	__package__: "",

	b64encode: function(data){
		var data_str = String.fromCharCode.apply(null, data.val)
		var encode = window.btoa(data_str);
		var bytes = [];
		for (var i = 0; i < encode.length; i ++) {
			var code = encode.charCodeAt(i);
			bytes = bytes.concat([code]);
		};
		return new batavia.types.Bytes(bytes)
	},

	b64decode: function(data){
		var data_str = String.fromCharCode.apply(null, data.val)
		if (data_str.length % 4 !== 0){
			throw new batavia.builtins.ValueError("Incorrect padding");
		}
		var encode = window.atob(data_str);
		var bytes = [];
		for (var i = 0; i < encode.length; i ++) {
			var code = encode.charCodeAt(i);
			bytes = bytes.concat([code]);
		};
		return new batavia.types.Bytes(bytes);
	},

	_a85chars: function(){},
	_a85chars2: function(){},
	_b32alphabet: function(){},
	_b32rev: function(){},
	_b32tab2: function(){},
	_b85alphabet: function(){},
	_b85chars: function(){},
	_b85chars2: function(){},
	_b85dec: function(){},
	_bytes_from_decode_data: function(){},
	_input_type_check: function(){},
	_urlsafe_decode_translation: function(){},
	_urlsafe_encode_translation: function(){},
	a85decode: function(){},
	a85encode: function(){},
	b16decode: function(){},
	b16encode: function(){},
	b32decode: function(){},
	b32encode: function(){},
	b85decode: function(){},
	b85encode: function(){},
	binascii: function(){},
	bytes_types: function(){},
	decode: function(){},
	decodebytes: function(){},
	decodestring: function(data){
		return this.b64decode(data);
	},
	encode: function(){},
	encodebytes: function(){},
	encodestring: function(data){},
	main: function(){},
	re: function(){},
	standard_b64decode: function(){},
	standard_b64encode: function(){},
	struct: function(){},
	test: function(){},
	urlsafe_b64decode: function(data){
		var data_str = String.fromCharCode.apply(null, data.val)
		var encode = window.atob(data_str);
		var bytes = [];
		for (var i = 0; i < encode.length; i ++) {
			var code = encode.charCodeAt(i);
			bytes = bytes.concat([code]);
		};
		return new batavia.types.Bytes(bytes)
	},
	urlsafe_b64encode: function(data){
		var data_str = String.fromCharCode.apply(null, data.val)
		var encode = window.btoa(data_str);
		var bytes = [];
		for (var i = 0; i < encode.length; i ++) {
			var code = encode.charCodeAt(i);
			bytes = bytes.concat([code]);
		};
		return new batavia.types.Bytes(bytes);
	},
};

batavia.modules.base64.b64encode.__doc__ = "Decode the Base64 encoded bytes-like object or ASCII string s.\n\nOptional altchars must be a bytes-like object or ASCII string of length 2\n    which specifies the alternative alphabet used instead of the '+' and '/'\n    characters.\n\n    The result is returned as a bytes object.  A binascii.Error is raised if\n    s is incorrectly padded.\n\n    If validate is False (the default), characters that are neither in the\n    normal base-64 alphabet nor the alternative alphabet are discarded prior\n    to the padding check.  If validate is True, these non-alphabet characters\n    in the input result in a binascii.Error.\n    "
batavia.modules.base64.b64decode.__doc__ = "Encode the bytes-like object s using Base64 and return a bytes object.\n\n    Optional altchars should be a byte string of length 2 which specifies an\n    alternative alphabet for the '+' and '/' characters.  This allows an\n    application to e.g. generate url or filesystem safe Base64 strings.\n    "
/*
 * opcode module - potentially shared between dis and other modules which
 * operate on bytecodes (e.g. peephole optimizers).
 */

batavia.modules.dis = {
    CO_GENERATOR: 32,  // flag for "this code uses yield"

    hasconst: {},
    hasname: {},
    hasjrel: {},
    hasjabs: {},
    haslocal: {},
    hascompare: {},
    hasfree: {},
    hasnargs: {},

    opmap: null,
    opname: [],

    unary_ops: {},
    binary_ops: {},
    inplace_ops: {},
    // slice_ops: {},

    def_op: function(name, op) {
        batavia.modules.dis.opname[op] = name;
        batavia.modules.dis.opmap[name] = op;
    },

    def_unary_op: function(name, op) {
        batavia.modules.dis.def_op(name, op);
        batavia.modules.dis.unary_ops[op] = op;
    },

    def_binary_op: function(name, op) {
        batavia.modules.dis.def_op(name, op);
        batavia.modules.dis.binary_ops[op] = op;
    },

    def_inplace_op: function(name, op) {
        batavia.modules.dis.def_op(name, op);
        batavia.modules.dis.inplace_ops[op] = op;
    },

    // def_slice_op: function(name, op) {
    //     batavia.modules.dis.def_op(name, op);
    //     batavia.modules.dis.slice_ops[op] = op;
    // },

    name_op: function(name, op) {
        batavia.modules.dis.def_op(name, op);
        batavia.modules.dis.hasname[op] = op;
    },

    jrel_op: function(name, op) {
        batavia.modules.dis.def_op(name, op);
        batavia.modules.dis.hasjrel[op] = op;
    },

    jabs_op: function(name, op) {
        batavia.modules.dis.def_op(name, op);
        batavia.modules.dis.hasjabs[op] = op;
    },

    init: function() {
        if (batavia.modules.dis.opmap !== null) {
            // Already initialized
            return;
        }

        batavia.modules.dis.opmap = {};

        // Prime the opname list with all possible opnames
        for (var op=0; op < 256; op++) {
            batavia.modules.dis.opname.push('<' + op + '>');
        }

        // Register the known opnames
        batavia.modules.dis.def_op('POP_TOP', 1);
        batavia.modules.dis.def_op('ROT_TWO', 2);
        batavia.modules.dis.def_op('ROT_THREE', 3);
        batavia.modules.dis.def_op('DUP_TOP', 4);
        batavia.modules.dis.def_op('DUP_TOP_TWO', 5);

        batavia.modules.dis.def_op('NOP', 9);
        batavia.modules.dis.NOP = 9;
        batavia.modules.dis.def_unary_op('UNARY_POSITIVE', 10);
        batavia.modules.dis.def_unary_op('UNARY_NEGATIVE', 11);
        batavia.modules.dis.def_unary_op('UNARY_NOT', 12);

        batavia.modules.dis.def_unary_op('UNARY_INVERT', 15);

        batavia.modules.dis.def_binary_op('BINARY_POWER', 19);
        batavia.modules.dis.def_binary_op('BINARY_MULTIPLY', 20);

        batavia.modules.dis.def_binary_op('BINARY_MODULO', 22);
        batavia.modules.dis.def_binary_op('BINARY_ADD', 23);
        batavia.modules.dis.def_binary_op('BINARY_SUBTRACT', 24);
        batavia.modules.dis.def_binary_op('BINARY_SUBSCR', 25);
        batavia.modules.dis.def_binary_op('BINARY_FLOOR_DIVIDE', 26);
        batavia.modules.dis.def_binary_op('BINARY_TRUE_DIVIDE', 27);
        batavia.modules.dis.def_inplace_op('INPLACE_FLOOR_DIVIDE', 28);
        batavia.modules.dis.def_inplace_op('INPLACE_TRUE_DIVIDE', 29);

        batavia.modules.dis.def_op('STORE_MAP', 54);
        batavia.modules.dis.def_inplace_op('INPLACE_ADD', 55);
        batavia.modules.dis.def_inplace_op('INPLACE_SUBTRACT', 56);
        batavia.modules.dis.def_inplace_op('INPLACE_MULTIPLY', 57);

        batavia.modules.dis.def_inplace_op('INPLACE_MODULO', 59);
        batavia.modules.dis.def_op('STORE_SUBSCR', 60);
        batavia.modules.dis.def_op('DELETE_SUBSCR', 61);
        batavia.modules.dis.def_binary_op('BINARY_LSHIFT', 62);
        batavia.modules.dis.def_binary_op('BINARY_RSHIFT', 63);
        batavia.modules.dis.def_binary_op('BINARY_AND', 64);
        batavia.modules.dis.def_binary_op('BINARY_XOR', 65);
        batavia.modules.dis.def_binary_op('BINARY_OR', 66);
        batavia.modules.dis.def_inplace_op('INPLACE_POWER', 67);
        batavia.modules.dis.def_op('GET_ITER', 68);

        batavia.modules.dis.def_op('PRINT_EXPR', 70);
        batavia.modules.dis.def_op('LOAD_BUILD_CLASS', 71);
        batavia.modules.dis.def_op('YIELD_FROM', 72);

        batavia.modules.dis.def_inplace_op('INPLACE_LSHIFT', 75);
        batavia.modules.dis.def_inplace_op('INPLACE_RSHIFT', 76);
        batavia.modules.dis.def_inplace_op('INPLACE_AND', 77);
        batavia.modules.dis.def_inplace_op('INPLACE_XOR', 78);
        batavia.modules.dis.def_inplace_op('INPLACE_OR', 79);
        batavia.modules.dis.def_op('BREAK_LOOP', 80);
        batavia.modules.dis.def_op('WITH_CLEANUP', 81);

        batavia.modules.dis.def_op('RETURN_VALUE', 83);
        batavia.modules.dis.def_op('IMPORT_STAR', 84);

        batavia.modules.dis.def_op('YIELD_VALUE', 86);
        batavia.modules.dis.def_op('POP_BLOCK', 87);
        batavia.modules.dis.def_op('END_FINALLY', 88);
        batavia.modules.dis.def_op('POP_EXCEPT', 89);

        batavia.modules.dis.HAVE_ARGUMENT = 90;              // Opcodes from here have an argument:

        batavia.modules.dis.name_op('STORE_NAME', 90);       // Index in name list
        batavia.modules.dis.name_op('DELETE_NAME', 91);      // ""
        batavia.modules.dis.def_op('UNPACK_SEQUENCE', 92);   // Number of tuple items
        batavia.modules.dis.jrel_op('FOR_ITER', 93);
        batavia.modules.dis.def_op('UNPACK_EX', 94);
        batavia.modules.dis.name_op('STORE_ATTR', 95);       // Index in name list
        batavia.modules.dis.name_op('DELETE_ATTR', 96);      // ""
        batavia.modules.dis.name_op('STORE_GLOBAL', 97);     // ""
        batavia.modules.dis.name_op('DELETE_GLOBAL', 98);    // ""
        batavia.modules.dis.def_op('LOAD_CONST', 100);       // Index in const list
        batavia.modules.dis.hasconst[100] = 100;
        batavia.modules.dis.name_op('LOAD_NAME', 101);       // Index in name list
        batavia.modules.dis.def_op('BUILD_TUPLE', 102);      // Number of tuple items
        batavia.modules.dis.def_op('BUILD_LIST', 103);       // Number of list items
        batavia.modules.dis.def_op('BUILD_SET', 104);        // Number of set items
        batavia.modules.dis.def_op('BUILD_MAP', 105);        // Number of dict entries (upto 255)
        batavia.modules.dis.name_op('LOAD_ATTR', 106);       // Index in name list
        batavia.modules.dis.def_op('COMPARE_OP', 107);       // Comparison operator
        batavia.modules.dis.hascompare[107] = 107;
        batavia.modules.dis.name_op('IMPORT_NAME', 108);     // Index in name list
        batavia.modules.dis.name_op('IMPORT_FROM', 109);     // Index in name list

        batavia.modules.dis.jrel_op('JUMP_FORWARD', 110);    // Number of bytes to skip
        batavia.modules.dis.jabs_op('JUMP_IF_FALSE_OR_POP', 111); // Target byte offset from beginning of code
        batavia.modules.dis.jabs_op('JUMP_IF_TRUE_OR_POP', 112);  // ""
        batavia.modules.dis.jabs_op('JUMP_ABSOLUTE', 113);        // ""
        batavia.modules.dis.jabs_op('POP_JUMP_IF_FALSE', 114);    // ""
        batavia.modules.dis.jabs_op('POP_JUMP_IF_TRUE', 115);     // ""

        batavia.modules.dis.name_op('LOAD_GLOBAL', 116);     // Index in name list

        batavia.modules.dis.jabs_op('CONTINUE_LOOP', 119);   // Target address
        batavia.modules.dis.jrel_op('SETUP_LOOP', 120);      // Distance to target address
        batavia.modules.dis.jrel_op('SETUP_EXCEPT', 121);    // ""
        batavia.modules.dis.jrel_op('SETUP_FINALLY', 122);   // ""

        batavia.modules.dis.def_op('LOAD_FAST', 124);        // Local variable number
        batavia.modules.dis.haslocal[124] = 124;
        batavia.modules.dis.def_op('STORE_FAST', 125);       // Local variable number
        batavia.modules.dis.haslocal[125] = 125;
        batavia.modules.dis.def_op('DELETE_FAST', 126);      // Local variable number
        batavia.modules.dis.haslocal[126] = 126;

        batavia.modules.dis.def_op('RAISE_VARARGS', 130);    // Number of raise arguments (1, 2, or 3);
        batavia.modules.dis.def_op('CALL_FUNCTION', 131);    // #args + (#kwargs << 8);
        batavia.modules.dis.hasnargs[131] = 131;
        batavia.modules.dis.def_op('MAKE_FUNCTION', 132);    // Number of args with default values
        batavia.modules.dis.def_op('BUILD_SLICE', 133);      // Number of items
        batavia.modules.dis.def_op('MAKE_CLOSURE', 134);
        batavia.modules.dis.def_op('LOAD_CLOSURE', 135);
        batavia.modules.dis.hasfree[135] = 135;
        batavia.modules.dis.def_op('LOAD_DEREF', 136);
        batavia.modules.dis.hasfree[136] = 136;
        batavia.modules.dis.def_op('STORE_DEREF', 137);
        batavia.modules.dis.hasfree[137] = 137;
        batavia.modules.dis.def_op('DELETE_DEREF', 138);
        batavia.modules.dis.hasfree[138] = 138;

        batavia.modules.dis.def_op('CALL_FUNCTION_VAR', 140);     // #args + (#kwargs << 8);
        batavia.modules.dis.hasnargs[140] = 140;
        batavia.modules.dis.def_op('CALL_FUNCTION_KW', 141);      // #args + (#kwargs << 8);
        batavia.modules.dis.hasnargs[141] = 141;
        batavia.modules.dis.def_op('CALL_FUNCTION_VAR_KW', 142);  // #args + (#kwargs << 8);
        batavia.modules.dis.hasnargs[142] = 142;

        batavia.modules.dis.jrel_op('SETUP_WITH', 143);

        batavia.modules.dis.def_op('LIST_APPEND', 145);
        batavia.modules.dis.def_op('SET_ADD', 146);
        batavia.modules.dis.def_op('MAP_ADD', 147);

        batavia.modules.dis.def_op('LOAD_CLASSDEREF', 148);
        batavia.modules.dis.hasfree[148] = 148;

        batavia.modules.dis.def_op('EXTENDED_ARG', 144);
        batavia.modules.dis.EXTENDED_ARG = 144;
    }
};
/*
 * Javascript DOM module.
 *
 * This is a wrapper to allow Python code to access DOM objects and methods.
 */


batavia.modules.dom = {
    'window': window,
    'parent': parent,
    'top': top,
    'navigator': navigator,
    'frames': frames,
    'location': location,
    'history': history,
    'document': document,
    'batavia': batavia
};

// Register the DOM module as a builtin.
batavia.builtins.dom = batavia.modules.dom;

/*************************************************************************
 * Marshal
 * This module contains functions that can read and write Python values in
 * a binary format. The format is specific to Python, but independent of
 * machine architecture issues.

 * Not all Python object types are supported; in general, only objects
 * whose value is independent from a particular invocation of Python can be
 * written and read by this module. The following types are supported:
 * None, integers, floating point numbers, strings, bytes, bytearrays,
 * tuples, lists, sets, dictionaries, and code objects, where it
 * should be understood that tuples, lists and dictionaries are only
 * supported as long as the values contained therein are themselves
 * supported; and recursive lists and dictionaries should not be written
 * (they will cause infinite loops).
 *
 * Variables:
 *
 * version -- indicates the format that the module uses. Version 0 is the
 *     historical format, version 1 shares interned strings and version 2
 *     uses a binary format for floating point numbers.
 *     Version 3 shares common object references (New in version 3.4).
 *
 * Functions:
 *
 * dumps() -- write value to a string

 *************************************************************************/

batavia.modules.marshal = {

    /* High water mark to determine when the marshalled object is dangerously deep
     * and risks coring the interpreter.  When the object stack gets this deep,
     * raise an exception instead of continuing.
     * On Windows debug builds, reduce this value.
     * iOS also requires a reduced value.
     */
    MAX_MARSHAL_STACK_DEPTH: 1500,

    TYPE_null: '0'.charCodeAt(),
    TYPE_NONE: 'N'.charCodeAt(),
    TYPE_FALSE: 'F'.charCodeAt(),
    TYPE_TRUE: 'T'.charCodeAt(),
    TYPE_STOPITER: 'S'.charCodeAt(),
    TYPE_ELLIPSIS: '.'.charCodeAt(),
    TYPE_INT: 'i'.charCodeAt(),
    TYPE_FLOAT: 'f'.charCodeAt(),
    TYPE_BINARY_FLOAT: 'g'.charCodeAt(),
    TYPE_COMPLEX: 'x'.charCodeAt(),
    TYPE_BINARY_COMPLEX: 'y'.charCodeAt(),
    TYPE_LONG: 'l'.charCodeAt(),
    TYPE_STRING: 's'.charCodeAt(),
    TYPE_INTERNED: 't'.charCodeAt(),
    TYPE_REF: 'r'.charCodeAt(),
    TYPE_TUPLE: '('.charCodeAt(),
    TYPE_LIST: '['.charCodeAt(),
    TYPE_DICT: '{'.charCodeAt(),
    TYPE_CODE: 'c'.charCodeAt(),
    TYPE_UNICODE: 'u'.charCodeAt(),
    TYPE_UNKNOWN: '?'.charCodeAt(),
    TYPE_SET: '<'.charCodeAt(),
    TYPE_FROZENSET: '>'.charCodeAt(),
    FLAG_REF: 0x80,  // with a type, add obj to index

    TYPE_ASCII: 'a'.charCodeAt(),
    TYPE_ASCII_INTERNED: 'A'.charCodeAt(),
    TYPE_SMALL_TUPLE: ')'.charCodeAt(),
    TYPE_SHORT_ASCII: 'z'.charCodeAt(),
    TYPE_SHORT_ASCII_INTERNED: 'Z'.charCodeAt(),

    /* We assume that Python ints are stored internally in base some power of
       2**15; for the sake of portability we'll always read and write them in base
       exactly 2**15. */

    PyLong_MARSHAL_SHIFT: 15,
    PyLong_MARSHAL_BASE: 1<<15,
    PyLong_MARSHAL_MASK: (1<<15)-1,
    PyLong_MARSHAL_RATIO: 30/15,

    SIZE32_MAX: 0x7FFFFFFF,

    r_string: function(vm, n, p)
    {
        return p.fread(n);

        // var read = -1;
        // var res;

        // if (p.ptr !== null) {
        //     /* Fast path for loads() */
        //     res = p.ptr;
        //     var left = p.end - p.ptr;
        //     if (left < n) {
        //         vm.PyErr_SetString(batavia.builtins.EOFError,
        //                         "marshal data too short");
        //         return null;
        //     }
        //     p.ptr += n;
        //     return res;
        // }
        // if (p.buf === null) {
        //     p.buf = PyMem_MALLOC(n);
        //     if (p.buf === null) {
        //         PyErr_NoMemory();
        //         return null;
        //     }
        //     p.buf_size = n;
        // }
        // else if (p.buf_size < n) {
        //     p.buf = PyMem_REALLOC(p.buf, n);
        //     if (p.buf === null) {
        //         PyErr_NoMemory();
        //         return null;
        //     }
        //     p.buf_size = n;
        // }

        // if (!p.readable) {
        //     assert(p.fp !== null);
        //     read = fread(p.buf, 1, n, p.fp);
        // }
        // else {
        //     _Py_IDENTIFIER(readinto);
        //     var mview;
        //     var buf;

        //     if (PyBuffer_FillInfo(buf, null, p.buf, n, 0, PyBUF_CONTIG) == -1) {
        //         return null;
        //     }
        //     mview = PyMemoryView_FromBuffer(buf);
        //     if (mview === null)
        //         return null;

        //     res = _PyObject_CallMethodId(p.readable, PyId_readinto, "N", mview);
        //     if (res !== null) {
        //         read = PyNumber_AsSsize_t(res, batavia.builtins.ValueError);
        //     }
        // }
        // if (read != n) {
        //     if (!vm.PyErr_Occurred()) {
        //         if (read > n)
        //             vm.PyErr_Format(batavia.builtins.ValueError,
        //                          "read() returned too much data: " +
        //                          "%zd bytes requested, %zd returned",
        //                          n, read);
        //         else
        //             vm.PyErr_SetString(batavia.builtins.EOFError,
        //                             "EOF read where not expected");
        //     }
        //     return null;
        // }
        // return p.buf;
    },

    r_byte: function(vm, p)
    {
        return p.getc();
    },

    r_short: function(vm, p)
    {
        var x = p.getc();
        x |= p.getc() << 8;

        /* Sign-extension, in case short greater than 16 bits */
        x |= -(x & 0x8000);
        return new batavia.types.Int(x);
    },

    read_int32: function(vm, p) {
      var x;
      x = p.getc();
      x |= p.getc() << 8;
      x |= p.getc() << 16;
      x |= p.getc() << 24;

      /* Sign extension for 64-bit machines */
      x |= -(x & 0x80000000);
      return x;
    },

    r_int: function(vm, p) {
        return new batavia.types.Int(this.read_int32(vm, p));
    },

    r_long: function(vm, p) {
        var n = batavia.modules.marshal.read_int32(vm, p);
        if (n === 0) {
          return new batavia.types.Int(0);
        }
        var negative = false;
        if (n < 0) {
          n = -n;
          negative = true;
        }
        var num = new batavia.vendored.BigNumber(0);
        // in little-endian order
        var multiplier = new batavia.vendored.BigNumber(1);
        for (var i = 0; i < n; i++) {
          num = num.add(multiplier.mul(batavia.modules.marshal.r_short(vm, p)));
          multiplier = multiplier.mul(batavia.modules.marshal.PyLong_MARSHAL_BASE);
        }
        if (negative) {
          num = num.neg();
        }
        return new batavia.types.Int(num);
    },

    r_float: function(vm, p)
    {
        buf = p.fread(8);

        var sign;
        var e;
        var fhi, flo;
        var incr = 1;
        var retval;

        /* First byte */
        sign = (buf.charCodeAt(7) >> 7) & 1;
        e = (buf.charCodeAt(7) & 0x7F) << 4;

        /* Second byte */
        e |= (buf.charCodeAt(6) >> 4) & 0xF;
        fhi = (buf.charCodeAt(6) & 0xF) << 24;

        if (e == 2047) {
            throw "can't unpack IEEE 754 special value on non-IEEE platform";
        }

        /* Third byte */
        fhi |= buf.charCodeAt(5) << 16;

        /* Fourth byte */
        fhi |= buf.charCodeAt(4)  << 8;

        /* Fifth byte */
        fhi |= buf.charCodeAt(3);

        /* Sixth byte */
        flo = buf.charCodeAt(2) << 16;

        /* Seventh byte */
        flo |= buf.charCodeAt(1) << 8;

        /* Eighth byte */
        flo |= buf.charCodeAt(0);

        retval = fhi + flo / 16777216.0; /* 2**24 */
        retval /= 268435456.0; /* 2**28 */

        if (e === 0) {
            e = -1022;
        } else {
            retval += 1.0;
            e -= 1023;
        }
        retval = retval * Math.pow(2, e);

        if (sign) {
            retval = -retval;
        }

        return new batavia.types.Float(retval);
    },

    /* allocate the reflist index for a new object. Return -1 on failure */
    r_ref_reserve: function(vm, flag, p) {
        if (flag) { /* currently only FLAG_REF is defined */
            var idx = p.refs.length;
            if (idx >= 0x7ffffffe) {
                vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (index list too large)");
                return -1;
            }
            if (p.refs.push(null) < 0) {
                return -1;
            }
            return idx;
        } else {
            return 0;
        }
    },

    /* insert the new object 'o' to the reflist at previously
     * allocated index 'idx'.
     * 'o' can be null, in which case nothing is done.
     * if 'o' was non-null, and the function succeeds, 'o' is returned.
     * if 'o' was non-null, and the function fails, 'o' is released and
     * null returned. This simplifies error checking at the call site since
     * a single test for null for the function result is enoug,h.
     */
    r_ref_insert: function(vm, o, idx, flag, p) {
        if (o !== null && flag) { /* currently only FLAG_REF is defined */
            var tmp = p.refs[idx];
            p.refs[idx] = o;
        }
        return o;
    },

    /* combination of both above, used when an object can be
     * created whenever it is seen in the file, as opposed to
     * after having loaded its sub-objects.,
     */
    r_ref: function(vm, o, flag, p) {
        assert(flag & batavia.modules.marshal.FLAG_REF);
        if (o === null) {
            return null;
        }
        if (p.refs.push(o) < 0) {
            return null;
        }
        return o;
    },

    r_object: function(vm, p) {
        /* null is a valid return value, it does not necessarily means that
           an exception is set. */
        var retval, v;
        var idx = 0;
        var i, n;
        var ptr;
        var type, code = batavia.modules.marshal.r_byte(vm, p);
        var flag, is_interned = 0;

        if (code === batavia.core.PYCFile.EOF) {
            vm.PyErr_SetString(batavia.builtins.EOFError,
                            "EOF read where object expected");
            return null;
        }

        p.depth++;

        if (p.depth > batavia.modules.marshal.MAX_MARSHAL_STACK_DEPTH) {
            p.depth--;
            vm.PyErr_SetString(batavia.builtins.ValueError, "recursion limit exceeded");
            return null;
        }

        flag = code & batavia.modules.marshal.FLAG_REF;
        type = code & ~batavia.modules.marshal.FLAG_REF;

        // console.log.info("R_OBJECT " + type + ' ' + flag);
        switch (type) {

        case batavia.modules.marshal.TYPE_null:
            retval = null;
            // console.log.info('TYPE_NULL ');
            break;

        case batavia.modules.marshal.TYPE_NONE:
            retval = batavia.builtins.None;
            // console.log.info('TYPE_NONE ' + retval);
            break;

        case batavia.modules.marshal.TYPE_STOPITER:
            retval = batavia.builtins.StopIteration;
            // console.log.info('TYPE_STOPITER');
            break;

        case batavia.modules.marshal.TYPE_ELLIPSIS:
            retval = batavia.types.Ellipsis;
            // console.log.info('TYPE_ELLIPSIS');
            break;

        case batavia.modules.marshal.TYPE_FALSE:
            retval = false;
            // console.log.info('TYPE_FALSE');
            break;

        case batavia.modules.marshal.TYPE_TRUE:
            retval = true;
            // console.log.info('TYPE_TRUE');
            break;

        case batavia.modules.marshal.TYPE_INT:
            retval = batavia.modules.marshal.r_int(vm, p);
            // console.log.info('TYPE_INT ' + retval);
            if (vm.PyErr_Occurred()) {
                break;
            }
            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_LONG:
            retval = batavia.modules.marshal.r_long(vm, p);
            // console.log.info('TYPE_LONG ' + retval);
            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_FLOAT:
            n = batavia.modules.marshal.r_byte(vm, p);
            buf = batavia.modules.marshal.r_string(vm, p, n);
            retval = new batavia.types.Float(parseFloat(buf));
            // console.log.info('TYPE_FLOAT ' + retval);
            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_BINARY_FLOAT:
            buf = p.fread(8);

            var sign;
            var e;
            var fhi, flo;
            var incr = 1;

            /* First byte */
            sign = (buf.charCodeAt(7) >> 7) & 1;
            e = (buf.charCodeAt(7) & 0x7F) << 4;

            /* Second byte */
            e |= (buf.charCodeAt(6) >> 4) & 0xF;
            fhi = (buf.charCodeAt(6) & 0xF) << 24;

            if (e == 2047) {
                throw "can't unpack IEEE 754 special value on non-IEEE platform";
            }

            /* Third byte */
            fhi |= buf.charCodeAt(5) << 16;

            /* Fourth byte */
            fhi |= buf.charCodeAt(4)  << 8;

            /* Fifth byte */
            fhi |= buf.charCodeAt(3);

            /* Sixth byte */
            flo = buf.charCodeAt(2) << 16;

            /* Seventh byte */
            flo |= buf.charCodeAt(1) << 8;

            /* Eighth byte */
            flo |= buf.charCodeAt(0);

            retval = fhi + flo / 16777216.0; /* 2**24 */
            retval /= 268435456.0; /* 2**28 */

            if (e === 0) {
                e = -1022;
            } else {
                retval += 1.0;
                e -= 1023;
            }
            retval = retval * Math.pow(2, e);

            if (sign) {
                retval = -retval;
            }

            // console.log.info('TYPE_BINARY_FLOAT ' + retval);

            retval = new batavia.types.Float(retval);

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_COMPLEX:
            n = batavia.modules.marshal.r_byte(vm, p);
            if (n == batavia.core.PYCFile.EOF) {
                vm.PyErr_SetString(batavia.builtins.EOFError,
                    "EOF read where object expected");
                break;
            }
            buf = batavia.modules.marshal.r_string(vm, p, n);
            real = new batavia.types.Float(parseFloat(buf));
            n = batavia.modules.marshal.r_byte(vm, p);
            if (n == batavia.core.PYCFile.EOF) {
                vm.PyErr_SetString(batavia.builtins.EOFError,
                    "EOF read where object expected");
                break;
            }
            buf = batavia.modules.marshal.r_string(vm, p, n);
            imag = new batavia.types.Float(parseFloat(buf));
            retval = new batavia.types.Complex(real, imag);
            // console.log.info('TYPE_COMPLEX ' + retval);
            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_BINARY_COMPLEX:
            real = batavia.modules.marshal.r_float(vm, p);
            imag = batavia.modules.marshal.r_float(vm, p);
            retval = new batavia.types.Complex(real, imag);
            // console.log.info('TYPE_BINARY_COMPLEX ' + retval);
            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_STRING:
            n = batavia.modules.marshal.read_int32(vm, p);
            // console.log.info('TYPE_STRING ' + n);
            if (vm.PyErr_Occurred()) {
                break;
            }
            if (n < 0 || n > batavia.modules.marshal.SIZE32_MAX) {
                vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (string size out of range)");
                break;
            }
//            retval = batavia.modules.marshal.r_string(vm, n, p);
            var contents = batavia.modules.marshal.r_string(vm, n, p);
            var split = contents.split('').map(function (b) { return b.charCodeAt(); });
            retval = new batavia.types.Bytes(split);

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_ASCII_INTERNED:
        case batavia.modules.marshal.TYPE_ASCII:
            n = batavia.modules.marshal.read_int32(vm, p);
            // console.log.info('TYPE_ASCII ' + n);
            if (n === batavia.core.PYCFile.EOF) {
                vm.PyErr_SetString(batavia.builtins.EOFError,
                    "EOF read where object expected");
                break;
            }
            retval = batavia.modules.marshal.r_string(vm, n, p);

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_SHORT_ASCII_INTERNED:
        case batavia.modules.marshal.TYPE_SHORT_ASCII:
            n = batavia.modules.marshal.r_byte(vm, p);
            // console.log.info('TYPE_SHORT_ASCII ' + n);
            if (n === batavia.core.PYCFile.EOF) {
                vm.PyErr_SetString(batavia.builtins.EOFError,
                    "EOF read where object expected");
                break;
            }
            retval = batavia.modules.marshal.r_string(vm, n, p);

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_INTERNED:
        case batavia.modules.marshal.TYPE_UNICODE:
            n = batavia.modules.marshal.read_int32(vm, p);
            // console.log.info('TYPE_UNICODE ' + n);
            if (n === batavia.core.PYCFile.EOF) {
                vm.PyErr_SetString(batavia.builtins.EOFError,
                    "EOF read where object expected");
                break;
            }
            retval = batavia.modules.marshal.r_string(vm, n, p);

            // Now decode the contents from UTF-8
            retval = decodeURIComponent(escape(retval));

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_SMALL_TUPLE:
            n = batavia.modules.marshal.r_byte(vm, p);
            // console.log.info('TYPE_SMALL_TUPLE ' + n);
            if (vm.PyErr_Occurred()) {
                break;
            }
            retval = new batavia.types.Tuple(new Array(n));

            for (i = 0; i < n; i++) {
                retval[i] = batavia.modules.marshal.r_object(vm, p);
            }

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_TUPLE:
            n = batavia.modules.marshal.read_int32(vm, p);
            // console.log.info('TYPE_TUPLE ' + n);
            if (vm.PyErr_Occurred()) {
                break;
            }
            if (n < 0 || n > batavia.modules.marshal.SIZE32_MAX) {
                vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (tuple size out of range)");
                break;
            }
            retval = new batavia.types.Tuple(new Array(n));

            for (i = 0; i < n; i++) {
                retval[i] = batavia.modules.marshal.r_object(vm, p);
            }

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_LIST:
            n = batavia.modules.marshal.read_int32(vm, p);
            // console.log.info('TYPE_LIST ' + n);
            if (vm.PyErr_Occurred()) {
                break;
            }
            if (n < 0 || n > batavia.modules.marshal.SIZE32_MAX) {
                vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (list size out of range)");
                break;
            }
            retval = new batavia.types.List(new Array(n));
            for (i = 0; i < n; i++) {
                retval[n] = batavia.modules.marshal.r_object(vm, p);
            }

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_DICT:
            // console.log.info('TYPE_DICT ' + n);
            retval = batavia.types.Dict();
            for (;;) {
                var key, val;
                key = r_object(p);
                if (key === undefined)
                    break;
                val = r_object(p);
                if (val === undefined) {
                    break;
                }
                retval[key] = val;
            }
            if (vm.PyErr_Occurred()) {
                retval = null;
            }

            if (flag) {
                batavia.modules.marshal.r_ref(vm, retval, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_SET:
        case batavia.modules.marshal.TYPE_FROZENSET:
            n = batavia.modules.marshal.read_int32(vm, p);
            // console.log.info('TYPE_FROZENSET ' + n);
            if (vm.PyErr_Occurred()) {
                break;
            }
            if (n < 0 || n > batavia.modules.marshal.SIZE32_MAX) {
                vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (set size out of range)");
                break;
            }
            if (type == batavia.modules.marshal.TYPE_SET) {
                retval = batavia.types.Set(null);
                if (flag) {
                   batavia.modules.marshal.r_ref(vm, retval, flag, p);
                }
            } else {
                retval = batavia.types.FrozenSet(null);
                /* must use delayed registration of frozensets because they must
                 * be init with a refcount of 1
                 */
                idx = batavia.modules.marshal.r_ref_reserve(flag, p);
                if (idx < 0) {
                    Py_CLEAR(v); /* signal error */
                }
            }

            for (i = 0; i < n; i++) {
                retval.add(r_object(p));
            }

            if (type != batavia.modules.marshal.TYPE_SET) {
                retval = batavia.modules.marshal.r_ref_insert(retval, idx, flag, p);
            }
            break;

        case batavia.modules.marshal.TYPE_CODE:
            var argcount;
            var kwonlyargcount;
            var nlocals;
            var stacksize;
            var flags;
            var consts;
            var names;
            var varnames;
            var freevars;
            var cellvars;
            var filename;
            var name;
            var firstlineno;
            var lnotab;

            idx = batavia.modules.marshal.r_ref_reserve(vm, flag, p);
            if (idx < 0) {
                break;
            }

            v = null;

            argcount = batavia.modules.marshal.read_int32(vm, p);
            kwonlyargcount = batavia.modules.marshal.read_int32(vm, p);
            nlocals = batavia.modules.marshal.read_int32(vm, p);
            stacksize = batavia.modules.marshal.read_int32(vm, p);
            flags = batavia.modules.marshal.read_int32(vm, p);
            code = batavia.modules.marshal.r_object(vm, p);
            consts = batavia.modules.marshal.r_object(vm, p);
            names = batavia.modules.marshal.r_object(vm, p);
            varnames = batavia.modules.marshal.r_object(vm, p);
            freevars = batavia.modules.marshal.r_object(vm, p);
            cellvars = batavia.modules.marshal.r_object(vm, p);
            filename = batavia.modules.marshal.r_object(vm, p);
            name = batavia.modules.marshal.r_object(vm, p);
            firstlineno = batavia.modules.marshal.read_int32(vm, p);
            lnotab = batavia.modules.marshal.r_object(vm, p);

            if (filename) {
                p.current_filename = filename;
            }

            v = new batavia.types.Code({
                argcount: argcount,
                kwonlyargcount: kwonlyargcount,
                nlocals: nlocals,
                stacksize: stacksize,
                flags: flags,
                code: code,
                consts: consts,
                names: names,
                varnames: varnames,
                freevars: freevars,
                cellvars: cellvars,
                filename: filename,
                name: name,
                firstlineno: firstlineno,
                lnotab: lnotab
            });
            v = batavia.modules.marshal.r_ref_insert(vm, v, idx, flag, p);

            retval = v;
            break;

        case batavia.modules.marshal.TYPE_REF:
            n = batavia.modules.marshal.read_int32(vm, p);
            if (n < 0 || n >= p.refs.length) {
                if (n == -1 && vm.PyErr_Occurred())
                    break;
                vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (invalid reference)");
                break;
            }
            v = p.refs[n];
            if (v === null) {
                vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (invalid reference)");
                break;
            }
            retval = v;
            break;

        default:
            /* Bogus data got written, which isn't ideal.
               This will let you keep working and recover. */

            vm.PyErr_SetString(batavia.builtins.ValueError, "bad marshal data (unknown type code '" + type + "')");
            break;

        }
        p.depth--;
        return retval;
    },

    read_object: function(vm, p) {
        var v;
        if (vm.PyErr_Occurred()) {
            console.log("readobject called with exception set\n");
            return null;
        }
        v = batavia.modules.marshal.r_object(vm, p);

        if (v === null && !vm.PyErr_Occurred()) {
            vm.PyErr_SetString(batavia.builtins.TypeError, "null object in marshal data for object");
        }
        return v;
    },

    /*
     * load_pyc(bytes)
     *
     * Load a Base64 encoded Convert the bytes object to a value. If no valid value is found, raise\n\
     * EOFError, ValueError or TypeError. Extra characters in the input are\n\
     * ignored."
     */

    load_pyc: function(vm, payload) {
        if (payload === null || payload.length === 0) {
            throw new batavia.builtins.BataviaError('Empty PYC payload');
        } else if (payload.startswith('ERROR:')) {
            throw new batavia.builtins.BataviaError('Traceback (most recent call last):\n' + payload.slice(6).split('\\n').join('\n'));
        }
        return batavia.modules.marshal.read_object(vm, new batavia.core.PYCFile(atob(payload)));
    }
};

batavia.modules.inspect = {
    FullArgSpec: function(kwargs) {
        this.args = kwargs.args || [];
        this.varargs = kwargs.getcallargs;
        this.varkw = kwargs.varkw;
        this.defaults = kwargs.defaults || {};
        this.kwonlyargs = kwargs.kwonlyargs || [];
        this.kwonlydefaults = kwargs.kwonlydefaults || {};
        this.annotations = kwargs.annotations || {};
    },

    _signature_get_user_defined_method: function(cls, method_name) {
        // try:
        //     meth = getattr(cls, method_name)
        // catch (err) {
        //     return
        // }
        // else {
        //     if not isinstance(meth, _NonUserDefinedCallables) {
        //         // # Once '__signature__' will be added to 'C'-level
        //         // callables, this check won't be necessary
        //         return meth
        //     }
        // }
    },

    _signature_bound_method: function(sig) {
        // Internal helper to transform signatures for unbound
        // functions to bound methods

        var params = sig.parameters.values();

        if (!params || params[0].kind in (_VAR_KEYWORD, _KEYWORD_ONLY)) {
            throw new batavia.builtins.ValueError('invalid method signature');
        }

        var kind = params[0].kind;
        if (kind in (_POSITIONAL_OR_KEYWORD, _POSITIONAL_ONLY)) {
            // Drop first parameter:
            // '(p1, p2[, ...])' -> '(p2[, ...])'
            params = params.slice(1);
        } else {
            if (kind !== _VAR_POSITIONAL) {
                // Unless we add a new parameter type we never
                // get here
                throw new batavia.builtins.ValueError('invalid argument type');
            }
            // It's a var-positional parameter.
            // Do nothing. '(*args[, ...])' -> '(*args[, ...])'
        }

        return sig.replace(parameters=params);
    },

    _signature_internal: function(obj, follow_wrapper_chains, skip_bound_arg) {
        // if (!callable(obj)) {
        //     throw TypeError('{!r} is not a callable object'.format(obj));
        // }

        // if (isinstance(obj, types.MethodType)) {
            // In this case we skip the first parameter of the underlying
            // function (usually `self` or `cls`).
            // sig = batavia.modules.inspect._signature_internal(obj.__func__, follow_wrapper_chains, skip_bound_arg);
            // if (skip_bound_arg) {
            //     return batavia.modules.inspect._signature_bound_method(sig);
            // } else {
            //     return sig;
            // }
        // }

        // // Was this function wrapped by a decorator?
        // if (follow_wrapper_chains) {
        //     obj = unwrap(obj, stop=function(f) { return hasattr(f, "__signature__"); });
        // }

        // try {
        //     sig = obj.__signature__;
        // } catch (err) {
        // } else {
        //     if (sig !== null) {
        //         if (!isinstance(sig, Signature)) {
        //             throw TypeError(
        //                 'unexpected object {!r} in __signature__ ' +
        //                 'attribute'.format(sig));
        //         }
        //         return sig;
        //     }
        // }
        // try {
        //     partialmethod = obj._partialmethod
        // } catch (err) {
        //     pass
        // } else {
        //     if isinstance(partialmethod, functools.partialmethod):
        //         // Unbound partialmethod (see functools.partialmethod)
        //         // This means, that we need to calculate the signature
        //         // as if it's a regular partial object, but taking into
        //         // account that the first positional argument
        //         // (usually `self`, or `cls`) will not be passed
        //         // automatically (as for boundmethods)

        //         wrapped_sig = batavia.modules.inspect._signature_internal(partialmethod.func,
        //                                           follow_wrapper_chains,
        //                                           skip_bound_arg)
        //         sig = batavia.modules.inspect._signature_get_partial(wrapped_sig, partialmethod, (None,))

        //         first_wrapped_param = tuple(wrapped_sig.parameters.values())[0]
        //         new_params = (first_wrapped_param,) + tuple(sig.parameters.values())

        //         return sig.replace(parameters=new_params)

        // if isfunction(obj) or _signature_is_functionlike(obj):
        //     # If it's a pure Python function, or an object that is duck type
        //     # of a Python function (Cython functions, for instance), then:
            return batavia.modules.inspect.Signature.from_function(obj);

        // if _signature_is_builtin(obj):
        //     return batavia.modules.inspect._signature_from_builtin(Signature, obj,
        //                                    skip_bound_arg=skip_bound_arg)

        // if isinstance(obj, functools.partial):
        //     wrapped_sig = batavia.modules.inspect._signature_internal(obj.func,
        //                                       follow_wrapper_chains,
        //                                       skip_bound_arg)
        //     return batavia.modules.inspect._signature_get_partial(wrapped_sig, obj)

        // sig = None
        // if isinstance(obj, type):
        //     // obj is a class or a metaclass

        //     // First, let's see if it has an overloaded __call__ defined
        //     // in its metaclass
        //     call = batavia.modules.inspect._signature_get_user_defined_method(type(obj), '__call__')
        //     if call is not None:
        //         sig = batavia.modules.inspect._signature_internal(call,
        //                                   follow_wrapper_chains,
        //                                   skip_bound_arg)
        //     else:
        //         # Now we check if the 'obj' class has a '__new__' method
        //         new = _signature_get_user_defined_method(obj, '__new__')
        //         if new is not None:
        //             sig = batavia.modules.inspect._signature_internal(new,
        //                                       follow_wrapper_chains,
        //                                       skip_bound_arg)
        //         else:
        //             # Finally, we should have at least __init__ implemented
        //             init = _signature_get_user_defined_method(obj, '__init__')
        //             if init is not None:
        //                 sig = batavia.modules.inspect._signature_internal(init,
        //                                           follow_wrapper_chains,
        //                                           skip_bound_arg)

        //     if sig is None:
        //         # At this point we know, that `obj` is a class, with no user-
        //         # defined '__init__', '__new__', or class-level '__call__'

        //         for base in obj.__mro__[:-1]:
        //             # Since '__text_signature__' is implemented as a
        //             # descriptor that extracts text signature from the
        //             # class docstring, if 'obj' is derived from a builtin
        //             # class, its own '__text_signature__' may be 'None'.
        //             # Therefore, we go through the MRO (except the last
        //             # class in there, which is 'object') to find the first
        //             # class with non-empty text signature.
        //             try:
        //                 text_sig = base.__text_signature__
        //             except AttributeError:
        //                 pass
        //             else:
        //                 if text_sig:
        //                     # If 'obj' class has a __text_signature__ attribute:
        //                     # return a signature based on it
        //                     return _signature_fromstr(Signature, obj, text_sig)

        //         # No '__text_signature__' was found for the 'obj' class.
        //         # Last option is to check if its '__init__' is
        //         # object.__init__ or type.__init__.
        //         if type not in obj.__mro__:
        //             # We have a class (not metaclass), but no user-defined
        //             # __init__ or __new__ for it
        //             if obj.__init__ is object.__init__:
        //                 # Return a signature of 'object' builtin.
        //                 return signature(object)

        // elif not isinstance(obj, _NonUserDefinedCallables):
        //     # An object with __call__
        //     # We also check that the 'obj' is not an instance of
        //     # _WrapperDescriptor or _MethodWrapper to avoid
        //     # infinite recursion (and even potential segfault)
        //     call = _signature_get_user_defined_method(type(obj), '__call__')
        //     if call is not None:
        //         try:
        //             sig = _signature_internal(call,
        //                                       follow_wrapper_chains,
        //                                       skip_bound_arg)
        //         except ValueError as ex:
        //             msg = 'no signature found for {!r}'.format(obj)
        //             raise ValueError(msg) from ex

        // if sig is not None:
        //     # For classes and objects we skip the first parameter of their
        //     # __call__, __new__, or __init__ methods
        //     if skip_bound_arg:
        //         return _signature_bound_method(sig)
        //     else:
        //         return sig

        // if isinstance(obj, types.BuiltinFunctionType):
        //     # Raise a nicer error message for builtins
        //     msg = 'no signature found for builtin function {!r}'.format(obj)
        //     raise ValueError(msg)

        // raise ValueError('callable {!r} is not supported by signature'.format(obj))
    },

    /*
     * Get the names and default values of a callable object's arguments.
     *
     * A tuple of seven things is returned:
     * (args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults annotations).
     * 'args' is a list of the argument names.
     * 'varargs' and 'varkw' are the names of the * and ** arguments or None.
     * 'defaults' is an n-tuple of the default values of the last n arguments.
     * 'kwonlyargs' is a list of keyword-only argument names.
     * 'kwonlydefaults' is a dictionary mapping names from kwonlyargs to defaults.
     * 'annotations' is a dictionary mapping argument names to annotations.
     *
     * The first four items in the tuple correspond to getargspec().
     */
    getfullargspec: function(func) {
        // try {
            // Re: `skip_bound_arg=false`
            //
            // There is a notable difference in behaviour between getfullargspec
            // and Signature: the former always returns 'self' parameter for bound
            // methods, whereas the Signature always shows the actual calling
            // signature of the passed object.
            //
            // To simulate this behaviour, we "unbind" bound methods, to trick
            // batavia.modules.inspect.signature to always return their first parameter ("self",
            // usually)

            // Re: `follow_wrapper_chains=false`
            //
            // getfullargspec() historically ignored __wrapped__ attributes,
            // so we ensure that remains the case in 3.3+

            var sig = batavia.modules.inspect._signature_internal(func, false, false);

            var args = [];
            var varargs = null;
            var varkw = null;
            var kwonlyargs = [];
            var defaults = [];
            var annotations = {};
            var kwdefaults = {};

            if (sig.return_annotation.length > 0) {
                annotations['return'] = sig.return_annotation;
            }

            for (var p in sig.parameters) {
                if (sig.parameters.hasOwnProperty(p)) {
                    var param = sig.parameters[p];

                    if (param.kind === batavia.modules.inspect.Parameter.POSITIONAL_ONLY) {
                        args.push(param.name);
                    } else if (param.kind === batavia.modules.inspect.Parameter.POSITIONAL_OR_KEYWORD) {
                        args.push(param.name);
                        if (param.default !== undefined) {
                            defaults.push(param.default);
                        }
                    } else if (param.kind === batavia.modules.inspect.Parameter.VAR_POSITIONAL) {
                        varargs = param.name;
                    } else if (param.kind === batavia.modules.inspect.Parameter.KEYWORD_ONLY) {
                        kwonlyargs.push(param.name);
                        if (param.default !== undefined) {
                            kwdefaults[param.name] = param.default;
                        }
                    } else if (param.kind === batavia.modules.inspect.Parameter.VAR_KEYWORD) {
                        varkw = param.name;
                    }

                    if (param.annotation !== undefined) {
                        annotations[param.name] = param.annotation;
                    }
                }
            }

            if (kwdefaults.length === 0) {
                // compatibility with 'func.__kwdefaults__'
                kwdefaults = null;
            }

            if (defaults.length === 0) {
                // compatibility with 'func.__defaults__'
                defaults = null;
            }

            return new batavia.modules.inspect.FullArgSpec({
                'args': args,
                'varargs': varargs,
                'varkw': varkw,
                'defaults': defaults,
                'kwonlyargs': kwonlyargs,
                'kwdefaults': kwdefaults,
                'annotations': annotations
            });

        // } catch (ex) {
            // Most of the times 'signature' will raise ValueError.
            // But, it can also raise AttributeError, and, maybe something
            // else. So to be fully backwards compatible, we catch all
            // possible exceptions here, and reraise a TypeError.
            // raise TypeError('unsupported callable') from ex
            // throw TypeError('unsupported callable');
        // }
    },

    _missing_arguments: function(f_name, argnames, pos, values) {
        throw "Missing arguments";
        // var names = [];
        // for (var name in argnames) {
        //     if (!name in values) {
        //         names.push(name);
        //     }
        // }
        // var missing = names.length;
        // if (missing == 1) {
        //     s = names[0];
        // } else if (missing === 2) {
        //     s = "{} and {}".format(*names)
        // } else {
        //     tail = ", {} and {}".format(*names[-2:])
        //     del names[-2:]
        //     s = ", ".join(names) + tail
        // }
        // raise TypeError("%s() missing %i required %s argument%s: %s" %
        //                 (f_name, missing,
        //                   "positional" if pos else "keyword-only",
        //                   "" if missing == 1 else "s", s))
    },

    _too_many: function(f_name, args, kwonly, varargs, defcount, given, values) {
        throw "FIXME: Too many arguments";
        // atleast = len(args) - defcount
        // kwonly_given = len([arg for arg in kwonly if arg in values])
        // if varargs:
        //     plural = atleast != 1
        //     sig = "at least %d" % (atleast,)
        // elif defcount:
        //     plural = True
        //     sig = "from %d to %d" % (atleast, len(args))
        // else:
        //     plural = len(args) != 1
        //     sig = str(len(args))
        // kwonly_sig = ""
        // if kwonly_given:
        //     msg = " positional argument%s (and %d keyword-only argument%s)"
        //     kwonly_sig = (msg % ("s" if given != 1 else "", kwonly_given,
        //                          "s" if kwonly_given != 1 else ""))
        // raise TypeError("%s() takes %s positional argument%s but %d%s %s given" %
        //         (f_name, sig, "s" if plural else "", given, kwonly_sig,
        //          "was" if given == 1 and not kwonly_given else "were"))
    },

    /*
     * Get the mapping of arguments to values.
     *
     * A dict is returned, with keys the function argument names (including the
     * names of the * and ** arguments, if any), and values the respective bound
     * values from 'positional' and 'named'.
     */
    getcallargs: function(func, positional, named) {
        var arg2value = {};

        // if ismethod(func) and func.__self__ is not None:
        if (func.__self__) {
            // implicit 'self' (or 'cls' for classmethods) argument
            positional = [func.__self__].concat(positional);
        }
        var num_pos = positional.length;
        var num_args = func.argspec.args.length;
        var num_defaults = func.argspec.defaults ? func.argspec.defaults.length : 0;

        var i, arg;
        var n = Math.min(num_pos, num_args);
        for (i = 0; i < n; i++) {
            arg2value[func.argspec.args[i]] = positional[i];
        }

        if (func.argspec.varargs) {
            arg2value[varargs] = positional.slice(n);
        }

        var possible_kwargs = new batavia.types.Set();
        possible_kwargs.update(func.argspec.args);
        possible_kwargs.update(func.argspec.kwonlyargs);

        if (func.argspec.varkw) {
            arg2value[func.argspec.varkw] = {};
        }

        for (var kw in named) {
            if (named.hasOwnProperty(kw)) {
                if (!possible_kwargs.__contains__(new batavia.types.Str(kw)).valueOf()) {
                    if (!func.argspec.varkw) {
                        throw new batavia.builtins.TypeError("%s() got an unexpected keyword argument %r" %
                                    (func.__name__, kw));
                    }
                    arg2value[func.argspec.varkw][kw] = named[kw];
                    continue;
                }
                if (kw in arg2value) {
                    throw new batavia.builtins.TypeError("%s() got multiple values for argument %r" %
                                    (func.__name__, kw));
                }
                arg2value[kw] = named[kw];
            }
        }

        if (num_pos > num_args && (func.argspec.varargs === undefined || func.argspec.varargs.length === 0)) {
            batavia.modules.inspect._too_many(func.__name__, func.argspec.args, func.argspec.kwonlyargs, func.argspec.varargs, num_defaults, num_pos, arg2value);
        }
        if (num_pos < num_args) {
            var req = func.argspec.args.slice(0, num_args - num_defaults);
            for (arg in req) {
                if (req.hasOwnProperty(arg)) {
                    if (!(req[arg] in arg2value)) {
                        batavia.modules.inspect._missing_arguments(func.__name__, req, true, arg2value);
                    }
                }
            }
            for (i = num_args - num_defaults; i < func.argspec.args.length; i++) {
                arg = func.argspec.args[i];
                if (!arg2value.hasOwnProperty(arg)) {
                    arg2value[arg] = func.argspec.defaults[i - num_pos];
                }
            }
        }
        var missing = 0;
        for (var kwarg in func.argspec.kwonlyargs) {
            if (func.argspec.kwonlydefaults.hasOwnProperty(kwarg)) {
                if (!arg2value.hasOwnProperty(kwarg)) {
                    if (func.argspec.kwonlydefaults.hasOwnProperty(kwarg)) {
                        arg2value[kwarg] = func.argspec.kwonlydefaults[kwarg];
                    } else {
                        missing += 1;
                    }
                }
            }
        }
        if (missing) {
            batavia.modules.inspect._missing_arguments(func.__name__, func.argspec.kwonlyargs, false, arg2value);
        }
        return arg2value;
    }
};

batavia.modules.inspect.CO_OPTIMIZED = 0x1;
batavia.modules.inspect.CO_NEWLOCALS = 0x2;
batavia.modules.inspect.CO_VARARGS = 0x4;
batavia.modules.inspect.CO_VARKEYWORDS = 0x8;
batavia.modules.inspect.CO_NESTED = 0x10;
batavia.modules.inspect.CO_GENERATOR = 0x20;
batavia.modules.inspect.CO_NOFREE = 0x40;

/*
Represents a parameter in a function signature.

Has the following public attributes:

* name : str
    The name of the parameter as a string.
* default : object
    The default value for the parameter if specified.  If the
    parameter has no default value, this attribute is set to
    `Parameter.empty`.
* annotation
    The annotation for the parameter if specified.  If the
    parameter has no annotation, this attribute is set to
    `Parameter.empty`.
* kind : str
    Describes how argument values are bound to the parameter.
    Possible values: `Parameter.POSITIONAL_ONLY`,
    `Parameter.POSITIONAL_OR_KEYWORD`, `Parameter.VAR_POSITIONAL`,
    `Parameter.KEYWORD_ONLY`, `Parameter.VAR_KEYWORD`.
*/
batavia.modules.inspect.Parameter = function(kwargs) {
    this.name = kwargs.name;
    this.kind = kwargs.kind;
    this.annotation = kwargs.annotation;
    this.default = kwargs.default;

    // if kind not in (POSITIONAL_ONLY, _POSITIONAL_OR_KEYWORD,
    //                 _VAR_POSITIONAL, _KEYWORD_ONLY, _VAR_KEYWORD):
    //     raise ValueError("invalid value for 'Parameter.kind' attribute")

    // if def is not _empty:
    //     if kind in (_VAR_POSITIONAL, _VAR_KEYWORD):
    //         msg = '{} parameters cannot have def values'.format(kind)
    //         raise ValueError(msg)

    // if name is _empty:
    //     raise ValueError('name is a required attribute for Parameter')

    // if not isinstance(name, str):
    //     raise TypeError("name must be a str, not a {!r}".format(name))

    // if not name.isidentifier():
    //     raise ValueError('{!r} is not a valid parameter name'.format(name))

};

batavia.modules.inspect.Parameter.POSITIONAL_ONLY = 0;
batavia.modules.inspect.Parameter.POSITIONAL_OR_KEYWORD = 1;
batavia.modules.inspect.Parameter.VAR_POSITIONAL = 2;
batavia.modules.inspect.Parameter.KEYWORD_ONLY = 3;
batavia.modules.inspect.Parameter.VAR_KEYWORD = 4;

//    '''Creates a customized copy of the Parameter.'''
batavia.modules.inspect.Parameter.prototype.replace = function(kwargs) {
    var name = kwargs.name || this.name;
    var kind = kwargs.kind || this.kind;
    var annotation = kwargs.annotation || this.annotation;
    var def = kwargs.default || this.default;

    return new batavia.modules.inspect.Paramter(name, kind, def, annotation);
};

    // def __str__(self):
    //     kind = self.kind
    //     formatted = self._name

    //     # Add annotation and default value
    //     if self._annotation is not _empty:
    //         formatted = '{}:{}'.format(formatted,
    //                                    formatannotation(self._annotation))

    //     if self._default is not _empty:
    //         formatted = '{}={}'.format(formatted, repr(self._default))

    //     if kind == _VAR_POSITIONAL:
    //         formatted = '*' + formatted
    //     elif kind == _VAR_KEYWORD:
    //         formatted = '**' + formatted

    //     return formatted

    // def __repr__(self):
    //     return '<{} at {:#x} {!r}>'.format(self.__class__.__name__,
    //                                        id(self), self.name)

    // def __eq__(self, other):
    //     return (issubclass(other.__class__, Parameter) and
    //             self._name == other._name and
    //             self._kind == other._kind and
    //             self._default == other._default and
    //             self._annotation == other._annotation)

    // def __ne__(self, other):
    //     return not self.__eq__(other)

// class BoundArguments:
//     '''Result of `Signature.bind` call.  Holds the mapping of arguments
//     to the function's parameters.

//     Has the following public attributes:

//     * arguments : OrderedDict
//         An ordered mutable mapping of parameters' names to arguments' values.
//         Does not contain arguments' default values.
//     * signature : Signature
//         The Signature object that created this instance.
//     * args : tuple
//         Tuple of positional arguments values.
//     * kwargs : dict
//         Dict of keyword arguments values.
//     '''

//     def __init__(self, signature, arguments):
//         self.arguments = arguments
//         self._signature = signature

//     @property
//     def signature(self):
//         return self._signature

//     @property
//     def args(self):
//         args = []
//         for param_name, param in self._signature.parameters.items():
//             if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
//                 break

//             try:
//                 arg = self.arguments[param_name]
//             except KeyError:
//                 # We're done here. Other arguments
//                 # will be mapped in 'BoundArguments.kwargs'
//                 break
//             else:
//                 if param.kind == _VAR_POSITIONAL:
//                     # *args
//                     args.extend(arg)
//                 else:
//                     # plain argument
//                     args.push(arg)

//         return tuple(args)

//     @property
//     def kwargs(self):
//         kwargs = {}
//         kwargs_started = False
//         for param_name, param in self._signature.parameters.items():
//             if not kwargs_started:
//                 if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
//                     kwargs_started = True
//                 else:
//                     if param_name not in self.arguments:
//                         kwargs_started = True
//                         continue

//             if not kwargs_started:
//                 continue

//             try:
//                 arg = self.arguments[param_name]
//             except KeyError:
//                 pass
//             else:
//                 if param.kind == _VAR_KEYWORD:
//                     # **kwargs
//                     kwargs.update(arg)
//                 else:
//                     # plain keyword argument
//                     kwargs[param_name] = arg

//         return kwargs

//     def __eq__(self, other):
//         return (issubclass(other.__class__, BoundArguments) and
//                 self.signature == other.signature and
//                 self.arguments == other.arguments)

//     def __ne__(self, other):
//         return not self.__eq__(other)


/*
     * A Signature object represents the overall signature of a function.
    It stores a Parameter object for each parameter accepted by the
    function, as well as information specific to the function itself.

    A Signature object has the following public attributes and methods:

    * parameters : OrderedDict
        An ordered mapping of parameters' names to the corresponding
        Parameter objects (keyword-only arguments are in the same order
        as listed in `code.co_varnames`).
    * return_annotation : object
        The annotation for the return type of the function if specified.
        If the function has no annotation for its return type, this
        attribute is set to `Signature.empty`.
    * bind(*args, **kwargs) -> BoundArguments
        Creates a mapping from positional and keyword arguments to
        parameters.
    * bind_partial(*args, **kwargs) -> BoundArguments
        Creates a partial mapping from positional and keyword arguments
        to parameters (simulating 'functools.partial' behavior.)
    */
/* Constructs Signature from the given list of Parameter
 * objects and 'return_annotation'.  All arguments are optional.
 */
batavia.modules.inspect.Signature = function(parameters, return_annotation, __validate_parameters__) {
    this.parameters = {};
    if (parameters !== null) {
        if (__validate_parameters__) {
            // params = OrderedDict()
            // top_kind = _POSITIONAL_ONLY
            // kind_defaults = false

            // for idx, param in enumerate(parameters):
            //     kind = param.kind
            //     name = param.name

            //     if kind < top_kind:
            //         msg = 'wrong parameter order: {!r} before {!r}'
            //         msg = msg.format(top_kind, kind)
            //         raise ValueError(msg)
            //     elif kind > top_kind:
            //         kind_defaults = false
            //         top_kind = kind

            //     if kind in (_POSITIONAL_ONLY, _POSITIONAL_OR_KEYWORD):
            //         if param.default is _empty:
            //             if kind_defaults:
            //                 # No default for this parameter, but the
            //                 # previous parameter of the same kind had
            //                 # a default
            //                 msg = 'non-default argument follows default ' \
            //                       'argument'
            //                 raise ValueError(msg)
            //         else:
            //             # There is a default for this parameter.
            //             kind_defaults = True

            //     if name in params:
            //         msg = 'duplicate parameter name: {!r}'.format(name)
            //         raise ValueError(msg)

            //     params[name] = param
        } else {
            // params = OrderedDict(((param.name, param) for param in parameters));
            for (var p in parameters) {
                if (parameters.hasOwnProperty(p)) {
                    this.parameters[parameters[p].name] = parameters[p];
                }
            }
        }
    }

    this.return_annotation = return_annotation;
};

// batavia.modules.inspect.Signature._parameter_cls = Parameter;
// batavia.modules.inspect.Signature._bound_arguments_cls = BoundArguments;

/*
 * Constructs Signature for the given python function
 */
batavia.modules.inspect.Signature.from_function = function(func) {
    var is_duck_function = false;
    // if (!isfunction(func)) {
    //     if (_signature_is_functionlike(func)) {
    //         is_duck_function = true;
    //     } else {
    //         // If it's not a pure Python function, and not a duck type
    //         // of pure function:
    //         throw TypeError('{!r} is not a Python function'.format(func));
    //     }
    // }

    // Parameter = cls._parameter_cls

    // Parameter information.
    var func_code = func.__code__;
    var pos_count = func_code.co_argcount;
    var arg_names = func_code.co_varnames;
    var positional = arg_names.slice(0, pos_count);
    var keyword_only_count = func_code.co_kwonlyargcount;
    var keyword_only = arg_names.slice(pos_count, pos_count + keyword_only_count);
    var annotations = func.__annotations__;
    var defs = func.__defaults__;
    var kwdefaults = func.__kwdefaults__;

    var pos_default_count;
    if (defs) {
        pos_default_count = defs.length;
    } else {
        pos_default_count = 0;
    }

    var parameters = [];
    var n, name, annotation, def, offset;

    // Non-keyword-only parameters w/o defaults.
    var non_default_count = pos_count - pos_default_count;
    for (n = 0; n < non_default_count; n++) {
        name = positional[n];
        annotation = annotations[name];
        parameters.push(new batavia.modules.inspect.Parameter({
            'name': name,
            'annotation': annotation,
            'kind': batavia.modules.inspect.Parameter.POSITIONAL_OR_KEYWORD
        }));
    }

    // ... w/ defaults.
    for (offset=0, n = non_default_count; n < positional.length; offset++, n++) {
        name = positional[n];
        annotation = annotations[name];
        parameters.push(new batavia.modules.inspect.Parameter({
            'name': name,
            'annotation': annotation,
            'kind': batavia.modules.inspect.Parameter.POSITIONAL_OR_KEYWORD,
            'default': defs[offset]
        }));
    }

    // *args
    if (func_code.co_flags & batavia.modules.inspect.CO_VARARGS) {
        name = arg_names[pos_count + keyword_only_count];
        annotation = annotations[name];
        parameters.push(new batavia.modules.inspect.Parameter({
            'name': name,
            'annotation': annotation,
            'kind': batavia.modules.inspect.Parameter.VAR_POSITIONAL
        }));
    }

    // Keyword-only parameters.
    for (n = 0; n < keyword_only.length; n++) {
        def = null;
        if (kwdefaults !== null) {
            def = kwdefaults[name];
        }

        annotation = annotations[name];
        parameters.push(new batavia.modules.inspect.Parameter({
            'name': name,
            'annotation': annotation,
            'kind': batavia.modules.inspect.Parameter.KEYWORD_ONLY,
            'default': def
        }));
    }

    // **kwargs
    if (func_code.co_flags & batavia.modules.inspect.CO_VARKEYWORDS) {
        var index = pos_count + keyword_only_count;
        if (func_code.co_flags & batavia.modules.inspect.CO_VARARGS) {
            index += 1;
        }

        name = arg_names[index];
        annotation = annotations[name];
        parameters.push(new batavia.modules.inspect.Parameter({
            'name': name,
            'annotation': annotation,
            'kind': batavia.modules.inspect.Parameter.VAR_KEYWORD
        }));
    }

    // Is 'func' is a pure Python function - don't validate the
    //parameters list (for correct order and defaults), it should be OK.
    return new batavia.modules.inspect.Signature(parameters, annotations['return'] || {}, is_duck_function);
};


    // @classmethod
    // def from_builtin(cls, func):
    //     return _signature_from_builtin(cls, func)

    // def replace(self, *, parameters=_void, return_annotation=_void):
    //     '''Creates a customized copy of the Signature.
    //     Pass 'parameters' and/or 'return_annotation' arguments
    //     to override them in the new copy.
    //     '''

    //     if parameters is _void:
    //         parameters = self.parameters.values()

    //     if return_annotation is _void:
    //         return_annotation = self._return_annotation

    //     return type(self)(parameters,
    //                       return_annotation=return_annotation)

    // def __eq__(self, other):
    //     if (not issubclass(type(other), Signature) or
    //                 self.return_annotation != other.return_annotation or
    //                 len(self.parameters) != len(other.parameters)):
    //         return false

    //     other_positions = {param: idx
    //                        for idx, param in enumerate(other.parameters.keys())}

    //     for idx, (param_name, param) in enumerate(self.parameters.items()):
    //         if param.kind == _KEYWORD_ONLY:
    //             try:
    //                 other_param = other.parameters[param_name]
    //             except KeyError:
    //                 return false
    //             else:
    //                 if param != other_param:
    //                     return false
    //         else:
    //             try:
    //                 other_idx = other_positions[param_name]
    //             except KeyError:
    //                 return false
    //             else:
    //                 if (idx != other_idx or
    //                                 param != other.parameters[param_name]):
    //                     return false

    //     return True

    // def __ne__(self, other):
    //     return not self.__eq__(other)

    // def _bind(self, args, kwargs, *, partial=false):
    //     '''Private method.  Don't use directly.'''

    //     arguments = OrderedDict()

    //     parameters = iter(self.parameters.values())
    //     parameters_ex = ()
    //     arg_vals = iter(args)

    //     while True:
    //         # Let's iterate through the positional arguments and corresponding
    //         # parameters
    //         try:
    //             arg_val = next(arg_vals)
    //         except StopIteration:
    //             # No more positional arguments
    //             try:
    //                 param = next(parameters)
    //             except StopIteration:
    //                 # No more parameters. That's it. Just need to check that
    //                 # we have no `kwargs` after this while loop
    //                 break
    //             else:
    //                 if param.kind == _VAR_POSITIONAL:
    //                     # That's OK, just empty *args.  Let's start parsing
    //                     # kwargs
    //                     break
    //                 elif param.name in kwargs:
    //                     if param.kind == _POSITIONAL_ONLY:
    //                         msg = '{arg!r} parameter is positional only, ' \
    //                               'but was passed as a keyword'
    //                         msg = msg.format(arg=param.name)
    //                         raise TypeError(msg) from None
    //                     parameters_ex = (param,)
    //                     break
    //                 elif (param.kind == _VAR_KEYWORD or
    //                                             param.default is not _empty):
    //                     # That's fine too - we have a default value for this
    //                     # parameter.  So, lets start parsing `kwargs`, starting
    //                     # with the current parameter
    //                     parameters_ex = (param,)
    //                     break
    //                 else:
    //                     # No default, not VAR_KEYWORD, not VAR_POSITIONAL,
    //                     # not in `kwargs`
    //                     if partial:
    //                         parameters_ex = (param,)
    //                         break
    //                     else:
    //                         msg = '{arg!r} parameter lacking default value'
    //                         msg = msg.format(arg=param.name)
    //                         raise TypeError(msg) from None
    //         else:
    //             # We have a positional argument to process
    //             try:
    //                 param = next(parameters)
    //             except StopIteration:
    //                 raise TypeError('too many positional arguments') from None
    //             else:
    //                 if param.kind in (_VAR_KEYWORD, _KEYWORD_ONLY):
    //                     # Looks like we have no parameter for this positional
    //                     # argument
    //                     raise TypeError('too many positional arguments')

    //                 if param.kind == _VAR_POSITIONAL:
    //                     # We have an '*args'-like argument, let's fill it with
    //                     # all positional arguments we have left and move on to
    //                     # the next phase
    //                     values = [arg_val]
    //                     values.extend(arg_vals)
    //                     arguments[param.name] = tuple(values)
    //                     break

    //                 if param.name in kwargs:
    //                     raise TypeError('multiple values for argument '
    //                                     '{arg!r}'.format(arg=param.name))

    //                 arguments[param.name] = arg_val

    //     # Now, we iterate through the remaining parameters to process
    //     # keyword arguments
    //     kwargs_param = None
    //     for param in itertools.chain(parameters_ex, parameters):
    //         if param.kind == _VAR_KEYWORD:
    //             # Memorize that we have a '**kwargs'-like parameter
    //             kwargs_param = param
    //             continue

    //         if param.kind == _VAR_POSITIONAL:
    //             # Named arguments don't refer to '*args'-like parameters.
    //             # We only arrive here if the positional arguments ended
    //             # before reaching the last parameter before *args.
    //             continue

    //         param_name = param.name
    //         try:
    //             arg_val = kwargs.pop(param_name)
    //         except KeyError:
    //             # We have no value for this parameter.  It's fine though,
    //             # if it has a default value, or it is an '*args'-like
    //             # parameter, left alone by the processing of positional
    //             # arguments.
    //             if (not partial and param.kind != _VAR_POSITIONAL and
    //                                                 param.default is _empty):
    //                 raise TypeError('{arg!r} parameter lacking default value'. \
    //                                 format(arg=param_name)) from None

    //         else:
    //             if param.kind == _POSITIONAL_ONLY:
    //                 # This should never happen in case of a properly built
    //                 # Signature object (but let's have this check here
    //                 # to ensure correct behaviour just in case)
    //                 raise TypeError('{arg!r} parameter is positional only, '
    //                                 'but was passed as a keyword'. \
    //                                 format(arg=param.name))

    //             arguments[param_name] = arg_val

    //     if kwargs:
    //         if kwargs_param is not None:
    //             // Process our '**kwargs'-like parameter
    //             arguments[kwargs_param.name] = kwargs
    //         else:
    //             raise TypeError('too many keyword arguments')

    //     return self._bound_arguments_cls(self, arguments)

    // def bind(*args, **kwargs):
    //     '''Get a BoundArguments object, that maps the passed `args`
    //     and `kwargs` to the function's signature.  Raises `TypeError`
    //     if the passed arguments can not be bound.
    //     '''
    //     return args[0]._bind(args[1:], kwargs)

    // def bind_partial(*args, **kwargs):
    //     '''Get a BoundArguments object, that partially maps the
    //     passed `args` and `kwargs` to the function's signature.
    //     Raises `TypeError` if the passed arguments can not be bound.
    //     '''
    //     return args[0]._bind(args[1:], kwargs, partial=True)

    // def __str__(self):
    //     result = []
    //     render_pos_only_separator = false
    //     render_kw_only_separator = True
    //     for param in self.parameters.values():
    //         formatted = str(param)

    //         kind = param.kind

    //         if kind == _POSITIONAL_ONLY:
    //             render_pos_only_separator = True
    //         elif render_pos_only_separator:
    //             # It's not a positional-only parameter, and the flag
    //             # is set to 'True' (there were pos-only params before.)
    //             result.push('/')
    //             render_pos_only_separator = false

    //         if kind == _VAR_POSITIONAL:
    //             # OK, we have an '*args'-like parameter, so we won't need
    //             # a '*' to separate keyword-only arguments
    //             render_kw_only_separator = false
    //         elif kind == _KEYWORD_ONLY and render_kw_only_separator:
    //             # We have a keyword-only parameter to render and we haven't
    //             # rendered an '*args'-like parameter before, so add a '*'
    //             # separator to the parameters list ("foo(arg1, *, arg2)" case)
    //             result.push('*')
    //             # This condition should be only triggered once, so
    //             # reset the flag
    //             render_kw_only_separator = false

    //         result.push(formatted)

    //     if render_pos_only_separator:
    //         # There were only positional-only parameters, hence the
    //         # flag was not reset to 'false'
    //         result.push('/')

    //     rendered = '({})'.format(', '.join(result))

    //     if self.return_annotation is not _empty:
    //         anno = formatannotation(self.return_annotation)
    //         rendered += ' -> {}'.format(anno)

    //     return rendered

batavia.modules.math = {
    __doc__: "",
    __file__: "math.js",
    __name__: "math",
    __package__: "",
    e: new batavia.types.Float(Math.E),
    nan: new batavia.types.Float(NaN),
    pi: new batavia.types.Float(Math.PI),
    inf: new batavia.types.Float(Infinity),

    _checkFloat: function(x) {
        if (batavia.isinstance(x, batavia.types.Complex)) {
            throw new batavia.builtins.TypeError("can't convert complex to float");
        } else if (!batavia.isinstance(x, [batavia.types.Bool, batavia.types.Float, batavia.types.Int])) {
            throw new batavia.builtins.TypeError('a float is required');
        }
    },

    acos: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.acos(x.__float__().val));
    },

    acosh: function(x) {
        batavia.modules.math._checkFloat(x);
        var result = Math.acosh(x.__float__().val);
        if (!isFinite(result)) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        return new batavia.types.Float(result);
    },

    asin: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.asin(x.__float__().val));
    },

    asinh: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.asinh(x.__float__().val));
    },

    atan: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.atan(x.__float__().val));
    },

    atan2: function(y, x) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        batavia.modules.math._checkFloat(y);
        var yy = y.__float__().val;
        return new batavia.types.Float(Math.atan2(yy, xx));
    },

    atanh: function(x) {
        batavia.modules.math._checkFloat(x);
        var result = Math.atanh(x.__float__().val);
        if (!isFinite(result)) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        return new batavia.types.Float(Math.atanh(x.__float__().val));
    },

    ceil: function(x) {
        if (batavia.isinstance(x, batavia.types.Int)) {
            return x;
        }
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Int(Math.ceil(x.__float__().val));
    },

    copysign: function(x, y) {
        batavia.modules.math._checkFloat(y);
        var yy = y.__float__().val;
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        if ((xx >= 0) != (yy >= 0)) {
            return x.__float__().__neg__();
        }
        return x.__float__();
    },

    cos: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.cos(x.__float__().val));
    },

    cosh: function(x) {
        batavia.modules.math._checkFloat(x);
        var result = Math.cosh(x.__float__().val);
        if (!isFinite(result)) {
            throw new batavia.builtins.OverflowError("math range error");
        }
        return new batavia.types.Float(Math.cosh(x.__float__().val));
    },

    degrees: function(x) {
        batavia.modules.math._checkFloat(x);
        // multiply by 180 / math.pi
        return new batavia.types.Float(x.__float__().val * 57.295779513082322865);
    },

    // taylor series expansion for erf(x)
    _erf_series: function(x) {
        // From CPython docs:
        //
        // erf(x) = x*exp(-x*x)/sqrt(pi) * [
        //                    2/1 + 4/3 x**2 + 8/15 x**4 + 16/105 x**6 + ...]
        // x**(2k-2) here is 4**k*factorial(k)/factorial(2*k)
        var y = 2.0;
        var num = 4;
        var denom = 2;
        var xk = 1;
        // CPython uses 25 terms.
        for (var i = 2; i < 26; i++) {
            num *= 4;
            num *= i;
            for (var j = 2 * (i - 1) + 1; j <= 2 * i; j++) {
              denom *= j;
            }
            xk *= x * x;
            y += xk * num / denom;
        }
        return y * x * Math.exp(-x * x) / Math.sqrt(Math.PI);
    },

    // continued fraction expansion of 1 - erf(x)
    _erfc_cfrac: function(x) {
        // From CPython docs:
        //
        // erfc(x) = x*exp(-x*x)/sqrt(pi) * [1/(0.5 + x**2 -) 0.5/(2.5 + x**2 - )
        //                               3.0/(4.5 + x**2 - ) 7.5/(6.5 + x**2 - ) ...]
        //
        //    after the first term, the general term has the form:
        //
        //       k*(k-0.5)/(2*k+0.5 + x**2 - ...).

        if (x > 30.0) {
            return 0.0;
        }

        var p_n = 1;
        var p_n_1 = 0.0;
        var q_n = 0.5 + x * x;
        var q_n_1 = 1.0;
        var a = 0.0;
        var coeff = 0.5;

        // CPython uses 50 terms.
        for (var k = 0; k < 50; k++) {
            a += coeff;
            coeff += 2;
            var b = coeff + x * x;

            var t = p_n;
            p_n = b * p_n - a * p_n_1;
            p_n_1 = t;

            t = q_n;
            q_n = b * q_n - a * q_n_1;
            q_n_1 = t;
        }
        return p_n / q_n * x * Math.exp(-x * x) / Math.sqrt(Math.PI);
    },

    erf: function(x) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        // Save the sign of x
        var sign = 1;
        if (xx < 0) {
            sign = -1;
        }
        xx = Math.abs(x);

        var CUTOFF = 1.5;
        var result;
        if (xx < 1.5) {
            result = batavia.modules.math._erf_series(xx);
        } else {
            result = 1.0 - batavia.modules.math._erfc_cfrac(xx);
        }
        return new batavia.types.Float(sign * result);
    },

    erfc: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(1.0 - batavia.modules.math.erf(x).val);
    },

    exp: function(x) {
        batavia.modules.math._checkFloat(x);
        var result = Math.exp(x.__float__().val);
        if (!isFinite(result)) {
            throw new batavia.builtins.OverflowError("math range error");
        }
        return new batavia.types.Float(result);
    },

    expm1: function(x) {
        batavia.modules.math._checkFloat(x);
        var result = Math.expm1(x.__float__().val);
        if (!isFinite(result)) {
            throw new batavia.builtins.OverflowError("math range error");
        }
        return new batavia.types.Float(Math.expm1(x.__float__().val));
    },

    fabs: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.abs(x.__float__().val));
    },

    // efficiently multiply all of the bignumbers in the list together, returning the product
    _mul_list: function(l, start, end) {
        var len = end - start + 1;
        if (len == 0) {
            return new batavia.vendored.BigNumber(1);
        } else if (len == 1) {
            return l[start];
        } else if (len == 2) {
            return l[start].mul(l[start + 1]);
        } else if (len == 3) {
            return l[start].mul(l[start + 1]).mul(l[start + 2]);
        }

        // split into halves and recurse
        var mid = Math.round(start + len/2);
        var a = batavia.modules.math._mul_list(l, start, mid);
        var b = batavia.modules.math._mul_list(l, mid + 1, end);
        return a.mul(b);
    },

    factorial: function(x) {
        var num;

        if (batavia.isinstance(x, batavia.types.Int)) {
            num = x.val;
        } else if (batavia.isinstance(x, batavia.types.Float)) {
            if (!x.is_integer().valueOf()) {
                throw new batavia.builtins.ValueError("factorial() only accepts integral values");
            }
            num = new batavia.vendored.BigNumber(x.valueOf());
        } else if (batavia.isinstance(x, batavia.types.Bool)) {
            return new batavia.types.Int(1);
        } else if (batavia.isinstance(x, batavia.types.Complex)) {
            throw new batavia.builtins.TypeError("can't convert complex to int");
        } else if (x == null) {
            throw new batavia.builtins.TypeError("an integer is required (got type NoneType)");
        } else {
            throw new batavia.builtins.TypeError("an integer is required (got type " + x.__class__.__name__ + ")");
        }

        if (num.isNegative()) {
            throw new batavia.builtins.ValueError("factorial() not defined for negative values");
        }

        if (num.isZero()) {
            return new batavia.types.Int(1);
        }

        // a basic pyramid multiplication
        var nums = [];
        while (!num.isZero()) {
            nums.push(num);
            num = num.sub(1);
        }
        return new batavia.types.Int(batavia.modules.math._mul_list(nums, 0, nums.length - 1));
    },

    floor: function(x) {
        if (batavia.isinstance(x, batavia.types.Int)) {
            return x;
        }
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Int(Math.floor(x.__float__().val));
    },

    fmod: function(x, y) {
        batavia.modules.math._checkFloat(y);
        var yy = y.__float__().val;
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        if (yy === 0.0) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        return new batavia.types.Float(xx % yy);
    },

    frexp: function(x) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        // check for 0, -0, NaN, Inf, -Inf
        if (xx === 0 || !isFinite(xx)) {
            return new batavia.types.Tuple([x.__float__(), new batavia.types.Int(0)]);
        }
        var buff = new batavia.vendored.buffer.Buffer(8);
        buff.writeDoubleLE(x, 0);
        var a = buff.readUInt32LE(0);
        var b = buff.readUInt32LE(4);
        var exp = ((b >> 20) & 0x7ff) - 1022;
        var num;
        // check for denormal number
        if (exp == -1022) {
            // each leading zero increases the exponent
            num = (b & 0xfffff) * 4294967296 + a;
            while ((num != 0) && (num < 0x8000000000000)) {
                exp--;
                num *= 2;
            }
            num = num / 0x10000000000000;
        } else {
          num = 0x10000000000000 + (b & 0xfffff) * 4294967296 + a;
          num = num / 0x20000000000000;
        }
        if (b >> 31) {
            num = -num;
        }
        return new batavia.types.Tuple([new batavia.types.Float(num), new batavia.types.Int(exp)]);
    },

    fsum: function(iterable) {
        var iterobj = batavia.builtins.iter([iterable], null);
        var sum = 0.0;
        batavia.iter_for_each(iterobj, function(val) {
            if (!batavia.isinstance(val, [batavia.types.Bool, batavia.types.Float, batavia.types.Int])) {
                throw new batavia.builtins.TypeError('a float is required');
            }
            sum += val.__float__().val;
        });
        return new batavia.types.Float(sum);
    },

    gamma: function(x) {
        // adapted from public domain code at http://picomath.org/javascript/gamma.js.html

        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;

        if (xx <= 0.0) {
            if (Number.isInteger(xx)) {
                throw new batavia.builtins.ValueError('math domain error');
            }
            // analytic continuation using reflection formula
            // gamma(z) * gamma(1-z) = pi / sin(pi * z)
            return new batavia.types.Float(Math.PI / Math.sin(Math.PI * xx) / batavia.modules.math.gamma(new batavia.types.Float(1 - xx)));
        }

        // Split the function domain into three intervals:
        // (0, 0.001), [0.001, 12), and (12, infinity)

        ///////////////////////////////////////////////////////////////////////////
        // First interval: (0, 0.001)
        //
        // For small x, 1/Gamma(x) has power series x + gamma x^2  - ...
        // So in this range, 1/Gamma(x) = x + gamma x^2 with error on the order of x^3.
        // The relative error over this interval is less than 6e-7.

        var gamma = 0.577215664901532860606512090; // Euler's gamma constant

        if (xx < 0.001) {
            return new batavia.types.Float(1.0 / (x * (1.0 + gamma * x)));
        }

        ///////////////////////////////////////////////////////////////////////////
        // Second interval: [0.001, 12)

        if (xx < 12.0) {
            // The algorithm directly approximates gamma over (1,2) and uses
            // reduction identities to reduce other arguments to this interval.
            var y = xx;
            var n = 0;
            var arg_was_less_than_one = (y < 1.0);

            // Add or subtract integers as necessary to bring y into (1,2)
            // Will correct for this below
            if (arg_was_less_than_one) {
              y += 1.0;
            } else {
                n = Math.floor(y) - 1;  // will use n later
                y -= n;
            }

            // numerator coefficients for approximation over the interval (1,2)
            var p =
            [
                -1.71618513886549492533811E+0,
                 2.47656508055759199108314E+1,
                -3.79804256470945635097577E+2,
                 6.29331155312818442661052E+2,
                 8.66966202790413211295064E+2,
                -3.14512729688483675254357E+4,
                -3.61444134186911729807069E+4,
                 6.64561438202405440627855E+4
            ];
            // denominator coefficients for approximation over the interval (1,2)
            var q =
            [
                -3.08402300119738975254353E+1,
                 3.15350626979604161529144E+2,
                -1.01515636749021914166146E+3,
                -3.10777167157231109440444E+3,
                 2.25381184209801510330112E+4,
                 4.75584627752788110767815E+3,
                -1.34659959864969306392456E+5,
                -1.15132259675553483497211E+5
            ];

            var num = 0.0;
            var den = 1.0;

            var z = y - 1;
            for (var i = 0; i < 8; i++) {
                num = (num + p[i]) * z;
                den = den * z + q[i];
            }
            var result = num / den + 1.0;

            // Apply correction if argument was not initially in (1,2)
            if (arg_was_less_than_one) {
                // Use identity gamma(z) = gamma(z+1)/z
                // The variable "result" now holds gamma of the original y + 1
                // Thus we use y-1 to get back the orginal y.
                result /= (y - 1.0);
            } else {
                // Use the identity gamma(z+n) = z*(z+1)* ... *(z+n-1)*gamma(z)
                for (var i = 0; i < n; i++) {
                    result *= y++;
                }
           }

           return new batavia.types.Float(result);
        }

        ///////////////////////////////////////////////////////////////////////////
        // Third interval: [12, infinity)

        if (xx > 171.624) {
            // Correct answer too large to display.
            throw new batavia.builtins.OverflowError("math range error");
        }

        return batavia.modules.math.exp(batavia.modules.math.lgamma(x));
     },

    gcd: function(x, y) {
        if (!batavia.isinstance(x, [batavia.types.Bool, batavia.types.Int])) {
            throw new batavia.builtins.TypeError("'" + batavia.type_name(x) + "' object cannot be interpreted as an integer");
        }
        if (!batavia.isinstance(y, [batavia.types.Bool, batavia.types.Int])) {
            throw new batavia.builtins.TypeError("'" + batavia.type_name(y) + "' object cannot be interpreted as an integer");
        }
        var xx = x.__trunc__().val.abs();
        var yy = y.__trunc__().val.abs();
        if (xx.isZero()) {
            return y.__trunc__().__abs__();
        } else if (yy.isZero()) {
            return x.__trunc__().__abs__();
        }
        // Standard modulo Euclidean algorithm.
        // TODO: when our binary shifts are more efficient, switch to binary Euclidean algorithm.
        while (!yy.isZero()) {
            var t = yy;
            yy = xx.mod(yy);
            xx = t;
        }
        return new batavia.types.Int(xx);
    },

    hypot: function(x, y) {
        batavia.modules.math._checkFloat(y);
        var yy = y.__float__().val;
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        return new batavia.types.Float(Math.hypot(xx, yy));
    },

    isclose: function(args, kwargs) {
        if (arguments.length != 2) {
            throw new batavia.builtins.BataviaError("Batavia calling convention not used.");
        }
        if (args.length == 0) {
            throw new batavia.builtins.TypeError("Required argument 'a' (pos 1) not found");
        }
        if (args.length == 1) {
            throw new batavia.builtins.TypeError("Required argument 'b' (pos 2) not found");
        }
        if (args.length > 2) {
            throw new batavia.builtins.TypeError("Function takes at most 2 positional arguments (" + args.length + " given)");
        }
        var rel_tol = 1e-09;
        if ('rel_tol' in kwargs) {
            if (!batavia.isinstance(kwargs.rel_tol, [batavia.types.Bool, batavia.types.Float, batavia.types.Int])) {
                throw new batavia.builtins.TypeError("a float is required");
            }
            rel_tol = kwargs.rel_tol.__float__().val;
        }
        var abs_tol = 0.0;
        if ('abs_tol' in kwargs) {
            if (!batavia.isinstance(kwargs.abs_tol, [batavia.types.Bool, batavia.types.Float, batavia.types.Int])) {
                throw new batavia.builtins.TypeError("a float is required");
            }
            abs_tol = kwargs.abs_tol.__float__().val;
        }

        if (abs_tol < 0.0 || rel_tol < 0.0) {
            throw new batavia.builtins.ValueError("tolerances must be non-negative");
        }

        var a = args[0].__float__().val;
        var b = args[1].__float__().val;
        if (a == b) {
            return new batavia.types.Bool(true);
        }
        if ((a == Infinity) || (a == -Infinity) || (b == Infinity) || (b == -Infinity)) {
            return new batavia.types.Bool(false);
        }
        if (isNaN(a) || isNaN(b)) {
            return new batavia.types.Bool(false);
        }
        var delta = Math.abs(a - b);
        if ((delta <= abs_tol) ||
            (delta <= Math.abs(rel_tol * a)) ||
            (delta <= Math.abs(rel_tol * a))) {
            return new batavia.types.Bool(true);
        }
        return new batavia.types.Bool(false);
    },

    isfinite: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Bool(isFinite(x.__float__().val));
    },

    isinf: function(x) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        return new batavia.types.Bool(xx == Infinity || xx == -Infinity);
    },

    isnan: function(x) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        return new batavia.types.Bool(isNaN(xx));
    },

    ldexp: function(x, i) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__();
        if (!batavia.isinstance(i, [batavia.types.Bool, batavia.types.Int])) {
            throw new batavia.builtins.TypeError("Expected an int as second argument to ldexp.");
        }
        if (xx.val == 0.0) {
            return xx;
        }
        var ii = i.__trunc__().val;
        if (ii.lt(-1022 - 53)) {
            ii = -1022 - 53;
        } else {
            ii = ii.valueOf();
        }
        var result = x.__float__().val * Math.pow(2, ii);
        if (!isFinite(result)) {
            throw new batavia.builtins.OverflowError("math range error");
        }
        return new batavia.types.Float(result);
    },

    lgamma: function(x) {
        // adapted from public domain code at http://picomath.org/javascript/gamma.js.html

        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;

        if (xx <= 0.0) {
            if (Number.isInteger(xx)) {
                throw new batavia.builtins.ValueError('math domain error');
            }
            // analytic continuation using reflection formula
            // gamma(z) * gamma(1-z) = pi / sin(pi * z)
            // lgamma(z) + lgamma(1-z) = log(pi / sin |pi * z|)
            return new batavia.types.Float(Math.log(Math.abs(Math.PI / Math.sin(Math.PI * xx))) - batavia.modules.math.lgamma(new batavia.types.Float(1 - xx)));
        }

        if (xx < 12.0) {
            var gx = batavia.modules.math.gamma(x).val;
            return new batavia.types.Float(Math.log(Math.abs(gx)));
        }

        // Abramowitz and Stegun 6.1.41
        // Asymptotic series should be good to at least 11 or 12 figures
        // For error analysis, see Whittiker and Watson
        // A Course in Modern Analysis (1927), page 252

        var c =
        [
             1.0/12.0,
            -1.0/360.0,
             1.0/1260.0,
            -1.0/1680.0,
             1.0/1188.0,
            -691.0/360360.0,
             1.0/156.0,
            -3617.0/122400.0
        ];
        var z = 1.0 / (xx * xx);
        var sum = c[7];
        for (var i = 6; i >= 0; i--) {
            sum *= z;
            sum += c[i];
        }
        var series = sum / xx;

        var halfLogTwoPi = 0.91893853320467274178032973640562;
        var logGamma = (xx - 0.5) * Math.log(xx) - xx + halfLogTwoPi + series;
        return new batavia.types.Float(logGamma);
    },

    log: function(x, base) {
        if (x == null) {
            throw new batavia.builtins.TypeError("a float is required");
        }

        // special case if both arguments are very large integers
        if (batavia.isinstance(x, batavia.types.Int) &&
            batavia.isinstance(base, batavia.types.Int)) {
            return batavia.modules.math._log2_int(x).__div__(batavia.modules.math._log2_int(base));
        }

        // special case if x is bool it should behave like integer
        if (batavia.isinstance(x, batavia.types.Bool)) {
            x = x.valueOf() ? new batavia.types.Int(1) : new batavia.types.Int(0);
        }

        // special base is bool it should behave like integer
        if (batavia.isinstance(base, batavia.types.Bool)) {
            base = base.valueOf() ? new batavia.types.Int(1) : new batavia.types.Int(0);
        }

        batavia.modules.math._checkFloat(x);
        if (x.__le__(new batavia.types.Float(0.0))) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        if (x.__eq__(new batavia.types.Float(1.0)) && batavia.isinstance(base, batavia.types.Int) && base.val.gt(1)) {
            return new batavia.types.Float(0.0);
        }
        if (typeof base !== 'undefined') {
            batavia.modules.math._checkFloat(base);
            if (base.__le__(new batavia.types.Float(0.0))) {
                throw new batavia.builtins.ValueError("math domain error");
            }
            var lg_base;
            if (batavia.isinstance(base, batavia.types.Int)) {
                lg_base = batavia.modules.math._log2_int(base).val;
            } else {
                var bb = base.__float__().val;
                if (bb <= 0.0) {
                    throw new batavia.builtins.ValueError("math domain error");
                }
                lg_base = Math.log2(bb);
            }
            if (lg_base == 0.0) {
                throw new batavia.builtins.ZeroDivisionError("float division by zero");
            }
            return new batavia.types.Float(batavia.modules.math.log2(x).val / lg_base);
        }

        if (batavia.isinstance(x, batavia.types.Int)) {
            if (x.val.isZero() || x.val.isNeg()) {
                throw new batavia.builtins.ValueError("math domain error");
            }
            if (x.__ge__(batavia.MAX_FLOAT)) {
                return batavia.modules.math._log2_int(x).__mul__(new batavia.types.Float(0.6931471805599453));
            }
        }
        return new batavia.types.Float(Math.log(x.__float__().val));
    },

    log10: function(x) {
        batavia.modules.math._checkFloat(x);
        if (batavia.isinstance(x, batavia.types.Int)) {
            if (x.val.isZero() || x.val.isNeg()) {
                throw new batavia.builtins.ValueError("math domain error");
            }
            if (x.__ge__(batavia.MAX_FLOAT)) {
                return batavia.modules.math._log2_int(x) * 0.30102999566398114;
            }
        }
        var xx = x.__float__().val;
        if (xx <= 0.0) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        return new batavia.types.Float(Math.log10(xx));
    },

    log1p: function(x) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        if (xx <= -1.0) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        return new batavia.types.Float(Math.log1p(xx));
    },

    // compute log2 of the (possibly large) integer argument
    _log2_int: function(x) {
        if (x.val.isNeg() || x.val.isZero()) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        var bits = x._bits();
        if (bits.length < 54) {
            return new batavia.types.Float(Math.log2(x.__float__().val));
        }
        // express x as M * (2**exp) where 0 <= M < 1.0
        var exp = bits.length;
        bits = bits.slice(0, 54);
        var num = new batavia.vendored.BigNumber(bits.join('') || 0, 2).valueOf();
        num = num / 18014398509481984.0;
        return new batavia.types.Float(Math.log2(num) + exp);
    },

    log2: function(x) {
        batavia.modules.math._checkFloat(x);
        if (batavia.isinstance(x, batavia.types.Int)) {
            return batavia.modules.math._log2_int(x);
        }
        var result = Math.log2(x.__float__().val);
        if (!isFinite(result)) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        return new batavia.types.Float(Math.log2(x.__float__().val));
    },

    modf: function(x) {
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        var frac = xx % 1;
        var int = Math.round(xx - frac);
        return new batavia.types.Tuple([new batavia.types.Float(frac),
          new batavia.types.Float(int)]);
    },

    pow: function(x, y) {
        batavia.modules.math._checkFloat(y);
        var yy = y.__float__().val;
        batavia.modules.math._checkFloat(x);
        var xx = x.__float__().val;
        var result = Math.pow(x, y);
        if (xx < 0 && !Number.isInteger(yy) && yy != 0.0) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        if (xx == 0.0 && yy < 0.0) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        if (!isFinite(result)) {
            throw new batavia.builtins.OverflowError("math range error");
        }
        return new batavia.types.Float(result);
    },

    radians: function(x) {
        batavia.modules.math._checkFloat(x);
        // multiply by math.pi / 180
        return new batavia.types.Float(x.__float__().val * 0.017453292519943295);
    },

    sin: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.sin(x.__float__().val));
    },

    sinh: function(x) {
      batavia.modules.math._checkFloat(x);
      var result = Math.sinh(x.__float__().val);
      if (!isFinite(result)) {
          throw new batavia.builtins.OverflowError("math range error");
      }
      return new batavia.types.Float(result);
    },

    sqrt: function(x) {
        batavia.modules.math._checkFloat(x);
        var result = Math.sqrt(x.__float__().val);
        if (!isFinite(result)) {
            throw new batavia.builtins.ValueError("math domain error");
        }
        return new batavia.types.Float(result);
    },

    tan: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.tan(x.__float__().val));
    },

    tanh: function(x) {
        batavia.modules.math._checkFloat(x);
        return new batavia.types.Float(Math.tanh(x.__float__().val));
    },

    trunc: function(x) {
        if (x === null) {
            throw new batavia.builtins.TypeError("type NoneType doesn't define __trunc__ method");
        } else if (!x.__trunc__) {
            throw new batavia.builtins.TypeError("type " + batavia.type_name(x) + " doesn't define __trunc__ method");
        }
        return x.__trunc__();
    }
};

batavia.modules.math.isclose.__python__ = true;


// docstrings taken from Python 3, which falls under this license:
// https://docs.python.org/3/license.html
//
batavia.modules.math.acos.__doc__ = 'acos(x)\n\n\nReturn the arc cosine (measured in radians) of x.';
batavia.modules.math.acosh.__doc__ = 'acosh(x)\n\n\nReturn the inverse hyperbolic cosine of x.';
batavia.modules.math.asin.__doc__ = 'asin(x)\n\n\nReturn the arc sine (measured in radians) of x.';
batavia.modules.math.asinh.__doc__ = 'asinh(x)\n\n\nReturn the inverse hyperbolic sine of x.';
batavia.modules.math.atan.__doc__ = 'atan(x)\n\n\nReturn the arc tangent (measured in radians) of x.';
batavia.modules.math.atan2.__doc__ = 'atan2(y, x)\n\n\nReturn the arc tangent (measured in radians) of y/x.\nUnlike atan(y/x), the signs of both x and y are considered.';
batavia.modules.math.atanh.__doc__ = 'atanh(x)\n\n\nReturn the inverse hyperbolic tangent of x.';
batavia.modules.math.ceil.__doc__ = 'ceil(x)\n\n\nReturn the ceiling of x as an int.\nThis is the smallest integral value >= x.';
batavia.modules.math.copysign.__doc__ = 'copysign(x, y)\n\n\nReturn a float with the magnitude (absolute value) of x but the sign \nof y. On platforms that support signed zeros, copysign(1.0, -0.0) \nreturns -1.0.\n';
batavia.modules.math.cos.__doc__ = 'cos(x)\n\n\nReturn the cosine of x (measured in radians).';
batavia.modules.math.cosh.__doc__ = 'cosh(x)\n\n\nReturn the hyperbolic cosine of x.';
batavia.modules.math.degrees.__doc__ = 'degrees(x)\n\n\nConvert angle x from radians to degrees.';
batavia.modules.math.erf.__doc__ = 'erf(x)\n\n\nError function at x.';
batavia.modules.math.erfc.__doc__ = 'erfc(x)\n\n\nComplementary error function at x.';
batavia.modules.math.exp.__doc__ = 'exp(x)\n\n\nReturn e raised to the power of x.';
batavia.modules.math.expm1.__doc__ = 'expm1(x)\n\n\nReturn exp(x)-1.\nThis function avoids the loss of precision involved in the direct evaluation of exp(x)-1 for small x.';
batavia.modules.math.fabs.__doc__ = 'fabs(x)\n\n\nReturn the absolute value of the float x.';
batavia.modules.math.factorial.__doc__ = 'factorial(x) -> Integral\n\n\nFind x!. Raise a ValueError if x is negative or non-integral.';
batavia.modules.math.floor.__doc__ = 'floor(x)\n\n\nReturn the floor of x as an int.\nThis is the largest integral value <= x.';
batavia.modules.math.fmod.__doc__ = 'fmod(x, y)\n\n\nReturn fmod(x, y), according to platform C.  x % y may differ.';
batavia.modules.math.frexp.__doc__ = 'frexp(x)\n\n\nReturn the mantissa and exponent of x, as pair (m, e).\nm is a float and e is an int, such that x = m * 2.**e.\nIf x is 0, m and e are both 0.  Else 0.5 <= abs(m) < 1.0.';
batavia.modules.math.fsum.__doc__ = 'fsum(iterable)\n\n\nReturn an accurate floating point sum of values in the iterable.\nAssumes IEEE-754 floating point arithmetic.';
batavia.modules.math.gamma.__doc__ = 'gamma(x)\n\n\nGamma function at x.';
batavia.modules.math.gcd.__doc__ = 'gcd(x, y) -> int\n\ngreatest common divisor of x and y';
batavia.modules.math.hypot.__doc__ = 'hypot(x, y)\n\n\nReturn the Euclidean distance, sqrt(x*x + y*y).';
batavia.modules.math.isclose.__doc__ = 'is_close(a, b, *, rel_tol=1e-9, abs_tol=0.0) -> bool\n\n\nDetermine whether two floating point numbers are close in value.\n\n\n   rel_tol\n       maximum difference for being considered "close", relative to the\n       magnitude of the input values\n    abs_tol\n       maximum difference for being considered "close", regardless of the\n       magnitude of the input values\n\n\nReturn True if a is close in value to b, and False otherwise.\n\n\nFor the values to be considered close, the difference between them\nmust be smaller than at least one of the tolerances.\n\n\n-inf, inf and NaN behave similarly to the IEEE 754 Standard.  That\nis, NaN is not close to anything, even itself.  inf and -inf are\nonly close to themselves.';
batavia.modules.math.isfinite.__doc__ = 'isfinite(x) -> bool\n\n\nReturn True if x is neither an infinity nor a NaN, and False otherwise.';
batavia.modules.math.isinf.__doc__ = 'isinf(x) -> bool\n\n\nReturn True if x is a positive or negative infinity, and False otherwise.';
batavia.modules.math.isnan.__doc__ = 'isnan(x) -> bool\n\n\nReturn True if x is a NaN (not a number), and False otherwise.';
batavia.modules.math.ldexp.__doc__ = 'ldexp(x, i)\n\n\nReturn x * (2**i).';
batavia.modules.math.lgamma.__doc__ = 'lgamma(x)\n\n\nNatural logarithm of absolute value of Gamma function at x.';
batavia.modules.math.log.__doc__ = 'log(x[, base])\n\n\nReturn the logarithm of x to the given base.\nIf the base not specified, returns the natural logarithm (base e) of x.';
batavia.modules.math.log10.__doc__ = 'log10(x)\n\n\nReturn the base 10 logarithm of x.';
batavia.modules.math.log1p.__doc__ = 'log1p(x)\n\n\nReturn the natural logarithm of 1+x (base e).\nThe result is computed in a way which is accurate for x near zero.';
batavia.modules.math.log2.__doc__ = 'log2(x)\n\n\nReturn the base 2 logarithm of x.';
batavia.modules.math.modf.__doc__ = 'modf(x)\n\n\nReturn the fractional and integer parts of x.  Both results carry the sign\nof x and are floats.';
batavia.modules.math.pow.__doc__ = 'pow(x, y)\n\n\nReturn x**y (x to the power of y).';
batavia.modules.math.radians.__doc__ = 'radians(x)\n\n\nConvert angle x from degrees to radians.';
batavia.modules.math.sin.__doc__ = 'sin(x)\n\n\nReturn the sine of x (measured in radians).';
batavia.modules.math.sinh.__doc__ = 'sinh(x)\n\n\nReturn the hyperbolic sine of x.';
batavia.modules.math.sqrt.__doc__ = 'sqrt(x)\n\n\nReturn the square root of x.';
batavia.modules.math.tan.__doc__ = 'tan(x)\n\n\nReturn the tangent of x (measured in radians).';
batavia.modules.math.tanh.__doc__ = 'tanh(x)\n\n\nReturn the hyperbolic tangent of x.';
batavia.modules.math.trunc.__doc__ = 'trunc(x:Real) -> Integral\n\n\nTruncates x to the nearest Integral toward 0. Uses the __trunc__ magic method.';

batavia.modules.sys = {
    'modules': {}
};

batavia.modules.time = {
    _startTime: new Date().getTime(),
    clock: function() {
        return new batavia.types.Float(new Date().getTime() - batavia.modules.time._startTime);
    },

    time: function() {
        // JS operates in milliseconds, Python in seconds, so divide by 1000
        return new batavia.types.Float(new Date().getTime() / 1000);
    },

    sleep: function(secs) {
        if (secs < 0) {
            throw new batavia.builtins.ValueError('sleep length must be non-negative')
        }

        var start = new Date().getTime();
        while (1) {
            if ((new Date().getTime() - start) / 1000 > secs){
                break;
            }
        }
    }
};

batavia.modules.time.struct_time = function (sequence) {
    /*
        copied from https://docs.python.org/3/library/time.html#time.struct_time

        Index 	Attribute 	Values
        0 	    tm_year 	(for example, 1993)
        1 	    tm_mon 	    range [1, 12]
        2 	    tm_mday 	range [1, 31]
        3 	    tm_hour 	range [0, 23]
        4 	    tm_min 	    range [0, 59]
        5 	    tm_sec 	    range [0, 61]; see (2) in strftime() description
        6 	    tm_wday 	range [0, 6], Monday is 0
        7 	    tm_yday 	range [1, 366]
        8 	    tm_isdst 	0, 1 or -1; see below
        N/A 	tm_zone 	abbreviation of timezone name
        N/A 	tm_gmtoff 	offset east of UTC in seconds
    */


    if (batavia.isinstance(sequence, [batavia.types.Bytearray, batavia.types.Bytes, batavia.types.Dict,
        batavia.types.FrozenSet, batavia.types.List, batavia.types.Range, batavia.types.Set, batavia.types.Str,
        batavia.types.Tuple]
        )){

        if (sequence.length < 9){
            throw new batavia.builtins.TypeError("time.struct_time() takes an at least 9-sequence ("+sequence.length+"-sequence given)")
        } else if (sequence.length > 11) {
            throw new batavia.builtins.TypeError("time.struct_time() takes an at most 11-sequence ("+sequence.length+"-sequence given)")
        }

        // might need to convert sequence to a more manageable type
        if (batavia.isinstance(sequence, [batavia.types.Bytearray])){
            // dict won't work until .keys() is implemented
            // bytearray won't work until .__iter__ is implemented

            throw new batavia.builtins.NotImplementedError("not implemented for "+ batavia.type_name(sequence)+".")

        } else if (batavia.isinstance(sequence, [batavia.types.Bytes, batavia.types.FrozenSet,
            batavia.types.Set, batavia.types.Range])) {

            var items = new batavia.types.Tuple(sequence);

        } else if (batavia.isinstance(sequence, batavia.types.Dict)){

            var items = sequence.keys();

        } else {
            // friendly type, no extra processing needed
            var items = sequence;
        }

        this.n_fields = 11;
        this.n_unnamed_fields = 0;
        this.n_sequence_fields = 9;

       this.push.apply(this, items.slice(0,9));  // only first 9 elements accepted for __getitem__

        var attrs = [ 'tm_year', 'tm_mon', 'tm_mday', 'tm_hour', 'tm_min', 'tm_sec', 'tm_wday', 'tm_yday', 'tm_isdst',
            'tm_zone', 'tm_gmtoff']

        for (var i=0; i<items.length; i++){
            this[attrs[i]] = items[i];
        }

    } else {
        //some other, unacceptable type
        throw new batavia.builtins.TypeError("constructor requires a sequence");
    }
}

batavia.modules.time.struct_time.prototype = new batavia.types.Tuple();

batavia.modules.time.struct_time.prototype.__str__ = function(){
    return "time.struct_time(tm_year="+this.tm_year+", tm_mon="+this.tm_mon+", tm_mday="+this.tm_mday+", tm_hour="+this.tm_hour+", tm_min="+this.tm_min+", tm_sec="+this.tm_sec+", tm_wday="+this.tm_wday+", tm_yday="+this.tm_yday+", tm_isdst="+this.tm_isdst+")"
}

batavia.modules.time.struct_time.prototype.__repr__ = function(){
    return this.__str__()
}

batavia.modules.time.mktime = function(sequence){
    // sequence: struct_time like
    // documentation: https://docs.python.org/3/library/time.html#time.mktime

    //Validations
    if (arguments.length != 1){
        throw new batavia.builtins.TypeError("mktime() takes exactly one argument ("+arguments.length+" given)");
    }

    if (!batavia.isinstance(sequence, [batavia.types.Tuple, batavia.modules.time.struct_time])) {
        throw new batavia.builtins.TypeError("Tuple or struct_time argument required");
    }

    if (sequence.length !== 9){
        throw new batavia.builtins.TypeError("function takes exactly 9 arguments ("+sequence.length+" given)");
    }

    if (sequence[0] < 1900){
        // because the earliest possible date is system dependant, use an arbitrary cut off for now.
        throw new batavia.builtins.OverflowError("mktime argument out of range");
    }

    // all items must be integers
    for (var i=0; i<sequence.length; i++){
        var item = sequence[i];
        if (batavia.isinstance(item, batavia.types.Float)){
            throw new batavia.builtins.TypeError("integer argument expected, got float")
        }
        else if (!batavia.isinstance(item, [batavia.types.Int])){
            throw new batavia.builtins.TypeError("an integer is required (got type " + batavia.type_name(item) + ")");
        }
    }

    var date = new Date(sequence[0], sequence[1] - 1, sequence[2], sequence[3], sequence[4], sequence[5], 0)

    if (isNaN(date)){
        // date is too large per ECMA specs
        // source: http://ecma-international.org/ecma-262/5.1/#sec-15.9.1.1
        throw new batavia.builtins.OverflowError("signed integer is greater than maximum")
    }

    var seconds = date.getTime() / 1000;
    return seconds.toFixed(1);
}

batavia.modules.time.gmtime = function(seconds){
    // https://docs.python.org/3/library/time.html#time.gmtime

    // 0-1 arguments allowed
    if (arguments.length > 1){
        throw new batavia.builtins.TypeError("gmtime() takes at most 1 argument (" + arguments.length + " given)")
    }

    if (arguments.length == 1) {
        // catching bad types
        if (batavia.isinstance(seconds, [batavia.types.Complex])){
            throw new batavia.builtins.TypeError("can't convert " + batavia.type_name(seconds) + " to int")

        } else if (!(batavia.isinstance(seconds, [batavia.types.Int, batavia.types.Float, batavia.types.Bool]))) {
            throw new batavia.builtins.TypeError("an integer is required (got type " + batavia.type_name(seconds) + ")")
        }

        var date = new Date(seconds * 1000)
        if (isNaN(date)){
            // date is too large per ECMA specs
            // source: http://ecma-international.org/ecma-262/5.1/#sec-15.9.1.1
            throw new batavia.builtins.OSError("Value too large to be stored in data type")
        }

    } else if (seconds === undefined){
        var date = new Date();
    }

    var sequence = [date.getUTCFullYear(),
    date.getUTCMonth() + 1,
    date.getUTCDate(),
    date.getUTCHours(),
    date.getUTCMinutes(),
    date.getUTCSeconds(),
    date.getUTCDay() -1
    ]

    // add day of year
    var firstOfYear = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
    var diff = date - firstOfYear;
    var oneDay = 1000 * 60 * 60 * 24;
    var dayOfYear = Math.floor(diff / oneDay);
    sequence.push(dayOfYear + 1);

    sequence.push(0)  // dst for UTC, always off

    return new batavia.modules.time.struct_time(new batavia.types.Tuple(sequence))
}
batavia.core.Block = function(type, handler, level) {
    this.type = type;
    this.handler = handler;
    this.level = level || 0;
};
/*
General builtin format:
// Example: a function that accepts exactly one argument, and no keyword arguments
batavia.builtins.<fn> = function(<args>, <kwargs>) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError("Batavia calling convention not used.");
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("<fn>() doesn't accept keyword arguments.");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError("<fn>() expected exactly 1 argument (" + args.length + " given)");
    }
    // if the function only works with a specific object type, add a test
    var obj = args[0];
    if (!batavia.isinstance(obj, batavia.types.<type>)) {
        throw new batavia.builtins.TypeError(
            "<fn>() expects a <type> (" + batavia.type_name(obj) + " given)");
    }
    // actual code goes here
    Javascript.Function.Stuff();
}
batavia.builtins.<fn>.__doc__ = 'docstring from Python 3.4 goes here, for documentation'
*/

batavia.builtins.__import__ = function(args, kwargs) {
    if (arguments.length !== 2) {
        throw new batavia.builtins.BataviaError("Batavia calling convention not used.");
    }

    // First, check for builtins
    var module;

    if (args[0] == "builtins") {
        module = batavia.builtins;
    }

    // Second, try native modules
    if (module === undefined) {
        module = batavia.modules[args[0]];
    }

    // If there's no native module, try for a pre-loaded module.
    if (module === undefined) {
        module = batavia.modules.sys.modules[args[0]];
    }
    // Check if there is a stdlib (pyc) module.
    if (module === undefined) {
        var payload = batavia.stdlib[args[0]];
        if (payload) {
            var code = batavia.modules.marshal.load_pyc(this, payload);
            // Convert code object to module
            args[1].__name__ = args[0]
            var frame = this.make_frame({
                'code': code,
                'f_globals': args[1]
            });
            this.run_frame(frame);

            module = new batavia.types.Module(name, frame.f_locals);
            batavia.modules.sys.modules[name] = module;
        }
    }

    // If there still isn't a module, try loading one from the DOM.
    if (module === undefined) {
        // Load requested module
        var name_parts = args[0].split('.');
        var name = name_parts[0];
        try {
            var root_module = batavia.modules.sys.modules[name];
            var payload, code, frame;
            if (root_module === undefined) {
                payload = this.loader(name);
                code = batavia.modules.marshal.load_pyc(this, payload);

                // Convert code object to module
                frame = this.make_frame({
                    'code': code,
                    'f_globals': new batavia.types.JSDict({
                        '__builtins__': batavia.builtins,
                        '__name__': name,
                        '__doc__': null,
                        '__package__': null,
                    }),  // args[1],
                    'f_locals': null  // #new batavia.types.JSDict(),
                });
                this.run_frame(frame);

                root_module = new batavia.types.Module(name, frame.f_locals);
                batavia.modules.sys.modules[name] = root_module;
            }

            var sub_module = root_module;
            for (var n = 1; n < name_parts.length; n++) {
                name = name_parts.slice(0, n + 1).join('.');

                var new_sub = batavia.modules.sys.modules[name];
                if (new_sub === undefined) {
                    payload = this.loader(name);
                    code = batavia.modules.marshal.load_pyc(this, payload);

                    // Convert code object to module
                    frame = this.make_frame({
                        'code': code,
                        'f_globals': new batavia.types.JSDict({
                            '__builtins__': batavia.builtins,
                            '__name__': name,
                            '__doc__': null,
                            '__package__': sub_module,
                        }),  // args[1],
                        'f_locals': null  //new batavia.types.JSDict(),
                    });
                    this.run_frame(frame);

                    new_sub = new batavia.types.Module(name, frame.f_locals);
                    sub_module[name_parts[n]] = new_sub;
                    sub_module = new_sub;
                    batavia.modules.sys.modules[name] = sub_module;
                } else {
                    sub_module = new_sub;
                }
            }

            if (args[3] === batavia.builtins.None) {
                // import <mod>
                module = root_module;
            } else if (args[3][0] === "*") {
                // from <mod> import *
                module = new batavia.types.Module(sub_module.__name__);
                for (name in sub_module) {
                    if (sub_module.hasOwnProperty(name)) {
                        module[name] = sub_module[name];
                    }
                }
            } else {
                // from <mod> import <name>, <name>
                module = new batavia.types.Module(sub_module.__name__);
                for (var sn = 0; sn < args[3].length; sn++) {
                    name = args[3][sn];
                    if (sub_module[name] === undefined) {
                        batavia.builtins.__import__.apply(this, [[sub_module.__name__ + '.' + name, this.frame.f_globals, null, batavia.builtins.None, null], null]);
                    }
                    module[name] = sub_module[name];
                }
            }
        } catch (err) {
            // Native module. Look for a name in the global
            // (window) namespace.
            var root_module = window[name];
            batavia.modules.sys.modules[name] = root_module;

            var sub_module = root_module;
            for (var n = 1; n < name_parts.length; n++) {
                name = name_parts.slice(0, n + 1).join('.');
                sub_module = sub_module[name_parts[n]];
                batavia.modules.sys.modules[name] = sub_module;
            }

            if (args[3] === batavia.builtins.None) {
                // import <mod>
                module = root_module;
            } else if (args[3][0] === "*") {
                // from <mod> import *
                module = {};
                for (name in sub_module) {
                    if (sub_module.hasOwnProperty(name)) {
                        module[name] = sub_module[name];
                    }
                }
            } else {
                // from <mod> import <name>, <name>
                module = {};
                for (var nn = 0; nn < args[3].length; nn++) {
                    name = args[3][nn];
                    module[name] = sub_module[name];
                }
            }
        }
    }
    return module;
};

batavia.builtins.abs = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("abs() doesn't accept keyword arguments");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('abs() takes exactly one argument (' + args.length + ' given)');
    }

    var value = args[0];
    if (batavia.isinstance(value, batavia.types.Bool)) {
        return new batavia.types.Int(Math.abs(value.valueOf()));
    } else if (batavia.isinstance(value, [batavia.types.Int,
                                          batavia.types.Float,
                                          batavia.types.Complex])) {
        return value.__abs__();
    } else {
        throw new batavia.builtins.TypeError(
            "bad operand type for abs(): '" + batavia.type_name(value) + "'");
    }
};
batavia.builtins.abs.__doc__ = 'abs(number) -> number\n\nReturn the absolute value of the argument.';

batavia.builtins.all = function(args, kwargs) {
    if (args[0] == null) {
        throw new batavia.builtins.TypeError("'NoneType' object is not iterable");
    }
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("all() doesn't accept keyword arguments");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('all() expected exactly 0 or 1 argument (' + args.length + ' given)');
    }

    if(!args[0].__iter__) {
        throw new batavia.builtins.TypeError("'" + batavia.type_name(args[0]) + "' object is not iterable");
    }

    for (var i = 0; i < args[0].length; i++) {
        if (!args[0][i]) {
           return false;
        }
    }

    return true;
};
batavia.builtins.all.__doc__ = 'all(iterable) -> bool\n\nReturn True if bool(x) is True for all values x in the iterable.\nIf the iterable is empty, return True.';

batavia.builtins.any = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("any() doesn't accept keyword arguments");
    }
    if (args.length === 0) {
        return false;
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('any() expected exactly 0 or 1 arguments (' + args.length + ' given)');
    }

    if (batavia.isinstance(args[0], batavia.types.Tuple)) {
      for (var i = 0; i < args[0].length; i++) {
        if (args[0][i]) {
           return true;
        }
      }
      return false;
    }

    for (var i in args[0]) {
        if (args[0][i]) {
           return true;
        }
    }

    return false;
};
batavia.builtins.any.__doc__ = 'any(iterable) -> bool\n\nReturn True if bool(x) is True for any x in the iterable.\nIf the iterable is empty, return False.';

batavia.builtins.ascii = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'ascii' not implemented");
};

batavia.builtins.bin = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("bin() doesn't accept keyword arguments");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('bin() expected exactly 1 argument (' + args.length + ' given)');
    }

    var obj = args[0];

    if (!batavia.isinstance(obj, batavia.types.Int)) {
        throw new batavia.builtins.TypeError(
            "'" + batavia.type_name(obj) + "' object cannot be interpreted as an integer");
    }

    return "0b" + obj.toString(2);
};
batavia.builtins.bin.__doc__ = "bin(number) -> string\n\nReturn the binary representation of an integer.\n\n   ";

batavia.builtins.bool = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("bool() doesn't accept keyword arguments");
    }
    if (!args || args.length === 0) {
        return false;
    } else if (args.length != 1) {
        throw new batavia.builtins.TypeError('bool() expected exactly 1 argument (' + args.length + ' given)');
    }

    if (args[0] === null) {
        return batavia.types.NoneType.__bool__();
    } else if (args[0].__bool__) {
        return args[0].__bool__();
    } else {
        return !!(args[0].valueOf());
    }
};
batavia.builtins.bool.__doc__ = 'bool(x) -> bool\n\nReturns True when the argument x is true, False otherwise.\nIn CPython, the builtins True and False are the only two instances of the class bool.\nAlso in CPython, the class bool is a subclass of the class int, and cannot be subclassed.\nBatavia implements booleans as a native Javascript Boolean, enhanced with additional __dunder__ methods.\n"Integer-ness" of booleans is faked via batavia.builtins.Bool\'s __int__ method.';

batavia.builtins.bytearray = function(args, kwargs) {

//    bytearray(string, encoding[, errors]) -> bytearray
//    bytearray(bytes_or_buffer) -> mutable copy of bytes_or_buffer
//    bytearray(iterable_of_ints) -> bytearray
//    bytearray(int) -> bytes array of size given by the parameter initialized with null bytes
//    bytearray() -> empty bytes array

    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError("Batavia calling convention not used.");
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("<fn>() doesn't accept keyword arguments.");
    }


    if (args.length == 1 && batavia.isinstance(args[0], batavia.types.Bytes)) {
        // bytearray(bytes_or_buffer) -> mutable copy of bytes_or_buffer
        return new batavia.types.Bytearray(args[0]);
    } else {
        throw new batavia.builtins.NotImplementedError(
            "Not implemented"
        );
    }

};
batavia.builtins.bytearray.__doc__ = 'bytearray(iterable_of_ints) -> bytearray\nbytearray(string, encoding[, errors]) -> bytearray\nbytearray(bytes_or_buffer) -> mutable copy of bytes_or_buffer\nbytearray(int) -> bytes array of size given by the parameter initialized with null bytes\nbytearray() -> empty bytes array\n\nConstruct an mutable bytearray object from:\n  - an iterable yielding integers in range(256)\n  - a text string encoded using the specified encoding\n  - a bytes or a buffer object\n  - any object implementing the buffer API.\n  - an integer';

batavia.builtins.bytes = function(args, kwargs) {
    throw new batavia.builtins.NotImplementedError(
        "Builtin Batavia function 'bytes' not implemented");
};
batavia.builtins.bytes.__doc__ = 'bytes(iterable_of_ints) -> bytes\nbytes(string, encoding[, errors]) -> bytes\nbytes(bytes_or_buffer) -> immutable copy of bytes_or_buffer\nbytes(int) -> bytes object of size given by the parameter initialized with null bytes\nbytes() -> empty bytes object\n\nConstruct an immutable array of bytes from:\n  - an iterable yielding integers in range(256)\n  - a text string encoded using the specified encoding\n  - any object implementing the buffer API.\n  - an integer';

batavia.builtins.callable = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("callable() doesn't accept keyword arguments");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('callable() expected exactly 1 argument (' + args.length + ' given)');
    }
    if (typeof(args[0]) === "function" || (args[0] && args[0].__call__)) {
        return true;
    } else {
        return false;
    }
};
batavia.builtins.callable.__doc__ = 'callable(object) -> bool\n\nReturn whether the object is callable (i.e., some kind of function).\nNote that classes are callable, as are instances of classes with a\n__call__() method.';

batavia.builtins.chr = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("char() doesn't accept keyword arguments");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('char() expected exactly 1 argument (' + args.length + ' given)');
    }
    return String.fromCharCode(args[0]);
};
batavia.builtins.chr.__doc__ = 'chr(i) -> Unicode character\n\nReturn a Unicode string of one character with ordinal i; 0 <= i <= 0x10ffff.';

batavia.builtins.classmethod = function(args, kwargs) {
    throw new batavia.builtins.NotImplementedError(
        "Builtin Batavia function 'classmethod' not implemented");
};
batavia.builtins.classmethod.__doc__ = 'classmethod(function) -> method\n\nConvert a function to be a class method.\n\nA class method receives the class as implicit first argument,\njust like an instance method receives the instance.\nTo declare a class method, use this idiom:\n\n  class C:\n      def f(cls, arg1, arg2, ...): ...\n      f = classmethod(f)\n\nIt can be called either on the class (e.g. C.f()) or on an instance\n(e.g. C().f()).  The instance is ignored except for its class.\nIf a class method is called for a derived class, the derived class\nobject is passed as the implied first argument.\n\nClass methods are different than C++ or Java static methods.\nIf you want those, see the staticmethod builtin.';


batavia.builtins.compile = function(args, kwargs) {
    throw new batavia.builtins.NotImplementedError(
        "Builtin Batavia function 'compile' not implemented");
};
batavia.builtins.compile.__doc__ = "compile(source, filename, mode[, flags[, dont_inherit]]) -> code object\n\nCompile the source (a Python module, statement or expression)\ninto a code object that can be executed by exec() or eval().\nThe filename will be used for run-time error messages.\nThe mode must be 'exec' to compile a module, 'single' to compile a\nsingle (interactive) statement, or 'eval' to compile an expression.\nThe flags argument, if present, controls which future statements influence\nthe compilation of the code.\nThe dont_inherit argument, if non-zero, stops the compilation inheriting\nthe effects of any future statements in effect in the code calling\ncompile; if absent or zero these statements do influence the compilation,\nin addition to any features explicitly specified.";

batavia.builtins.complex = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("complex() doesn't accept keyword arguments");
    }
    if (!args || args.length > 2) {
        throw new batavia.builtins.TypeError('complex() expected at most 2 arguments (' + args.length + ' given)');
    }
    if (batavia.isinstance(args[0], batavia.types.Complex) && !args[1]) {
        return args[0];
    }
    var re = new batavia.types.Float(0);
    if (args.length >= 1) {
        re = args[0];
    }
    var im = new batavia.types.Float(0);
    if (args.length == 2 && args[1]) {
        im = args[1];
    }
    return new batavia.types.Complex(re, im);
};
batavia.builtins.complex.__doc__ = 'complex(real[, imag]) -> complex number\n\nCreate a complex number from a real part and an optional imaginary part.\nThis is equivalent to (real + imag*1j) where imag defaults to 0.';

batavia.builtins.copyright = function(args, kwargs) {
    console.log("Batavia: Copyright (c) 2015 Russell Keith-Magee. (BSD-3 Licence)\n"+
                "byterun: Copyright (c) 2013, Ned Batchelder. (MIT Licence)");
};
batavia.builtins.copyright.__doc__ = 'copyright()\n\ninteractive prompt objects for printing the license text, a list of\n    contributors and the copyright notice.';

batavia.builtins.credits = function(args, kwargs) {
    console.log("Thanks to all contributors, including those in AUTHORS, for supporting Batavia development. See https://github.com/pybee/batavia for more information");
};
batavia.builtins.credits.__doc__ = 'credits()\n\ninteractive prompt objects for printing the license text, a list of\n    contributors and the copyright notice.';

batavia.builtins.delattr = function(args, kwargs) {
    if (args) {
        try {
            if (batavia.builtins.getattr(args)) {
                delete args[0][args[1]];
                // False returned by bool(delattr(...)) in the success case
                return false;
            }
        } catch (err) {
            // This is maybe unecessary, but matches the error thrown by python 3.5.1 in this case
            if (err instanceof batavia.builtins.AttributeError) {
                throw new batavia.builtins.AttributeError(args[1]);
            }
            if (err instanceof batavia.builtins.TypeError) {
                throw new batavia.builtins.TypeError("delattr expected 2 arguments, got " + args.length);
            }
        }
    } else {
        throw new batavia.builtins.TypeError("delattr expected 2 arguments, got 0");
    }
};
batavia.builtins.delattr.__doc__ = "delattr(object, name)\n\nDelete a named attribute on an object; delattr(x, 'y') is equivalent to\n``del x.y''.";

batavia.builtins.dict = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (args.length > 1) {
        throw new batavia.builtins.TypeError("dict expected at most 1 arguments, got " + args.length);
    }
    if (batavia.isinstance(args[0], [batavia.types.Int, batavia.types.Bool])) {
        throw new batavia.builtins.TypeError("'" + batavia.type_name(args[0]) + "' object is not iterable");
    }
    if (batavia.isinstance(args[0], batavia.types.Str)) {
        throw new batavia.builtins.ValueError("dictionary update sequence element #0 has length 1; 2 is required");
    }
    //if single bool case

    //if multiple bool case

    // handling keyword arguments and no arguments
    if (args.length === 0 || args[0].length === 0) {
        if (kwargs) {
            return new batavia.types.Dict(kwargs);
        }
        else {
            return new batavia.types.Dict();
        }
    } else {
        // iterate through array to find any errors
        for (var i = 0; i < args[0].length; i++) {
            if (args[0][i].length !== 2) {
                // single number or bool in an iterable throws different error
                if (batavia.isinstance(args[0][i], [batavia.types.Bool, batavia.types.Int])) {
                    throw new batavia.builtins.TypeError("cannot convert dictionary update sequence element #" + i + " to a sequence");
                } else {
                    throw new batavia.builtins.ValueError("dictionary update sequence element #" + i + " has length " + args[0][i].length + "; 2 is required");
                }
            }
        }
    }
    // Passing a dictionary as argument
    if (batavia.isinstance(args[0], batavia.types.Dict)) {
        return args[0];
    }

    // passing a list as argument
    if (args.length === 1) {
        var dict = new batavia.types.Dict();
        for (var i = 0; i < args[0].length; i++) {
            var sub_array = args[0][i];
            if (sub_array.length === 2) {
                dict.__setitem__(sub_array[0], sub_array[1]);
            }
        }
        return dict;
    }
};
batavia.builtins.dict.__doc__ = "dict() -> new empty dictionary\ndict(mapping) -> new dictionary initialized from a mapping object's\n    (key, value) pairs\ndict(iterable) -> new dictionary initialized as if via:\n    d = {}\n    for k, v in iterable:\n        d[k] = v\ndict(**kwargs) -> new dictionary initialized with the name=value pairs\n    in the keyword argument list.  For example:  dict(one=1, two=2)";

batavia.builtins.dir = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("dir() doesn't accept keyword arguments");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('dir() expected exactly 1 argument (' + args.length + ' given)');
    }
    return Object.keys(args[0]);
};
batavia.builtins.dir.__doc__ = "dir([object]) -> list of strings\n\nIf called without an argument, return the names in the current scope.\nElse, return an alphabetized list of names comprising (some of) the attributes\nof the given object, and of attributes reachable from it.\nIf the object supplies a method named __dir__, it will be used; otherwise\nthe default dir() logic is used and returns:\n  for a module object: the module's attributes.\n  for a class object:  its attributes, and recursively the attributes\n    of its bases.\n  for any other object: its attributes, its class's attributes, and\n    recursively the attributes of its class's base classes.";

batavia.builtins.divmod = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("divmod() doesn't accept keyword arguments");
    }
    if (!args || args.length != 2) {
        throw new batavia.builtins.TypeError('divmod() expected exactly 2 argument (' + args.length + ' given)');
    }

    div = Math.floor(args[0]/args[1]);
    rem = args[0] % args[1];
    return new batavia.types.Tuple([div, rem]);
};
batavia.builtins.divmod.__doc__ = 'Return the tuple ((x-x%y)/y, x%y).  Invariant: div*y + mod == x.';

batavia.builtins.enumerate = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("enumerate() doesn't accept keyword arguments");
    }
    var result = [];
    var values = args[0];
    for (var i = 0; i < values.length; i++) {
        result.push([i, values[i]]);
    }
    // FIXME this should return a generator, not list
    return result;
};
batavia.builtins.enumerate.__doc__ = 'enumerate(iterable[, start]) -> iterator for index, value of iterable\n\nReturn an enumerate object.  iterable must be another object that supports\niteration.  The enumerate object yields pairs containing a count (from\nstart, which defaults to zero) and a value yielded by the iterable argument.\nenumerate is useful for obtaining an indexed list:\n    (0, seq[0]), (1, seq[1]), (2, seq[2]), ...';

batavia.builtins.eval = function(args, kwargs) {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'eval' not implemented");
};
batavia.builtins.eval.__doc__ = 'eval(source[, globals[, locals]]) -> value\n\nEvaluate the source in the context of globals and locals.\nThe source may be a string representing a Python expression\nor a code object as returned by compile().\nThe globals must be a dictionary and locals can be any mapping,\ndefaulting to the current globals and locals.\nIf only globals is given, locals defaults to it.\n';

batavia.builtins.exec = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'exec' not implemented");
};
batavia.builtins.exec.__doc__ = 'exec(object[, globals[, locals]])\n\nRead and execute code from an object, which can be a string or a code\nobject.\nThe globals and locals are dictionaries, defaulting to the current\nglobals and locals.  If only globals is given, locals defaults to it.';

batavia.builtins.filter = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("filter() doesn't accept keyword arguments");
    }
    return new batavia.types.filter(args, kwargs);
};
batavia.builtins.filter.__doc__ = 'filter(function or None, iterable) --> filter object\n\nReturn an iterator yielding those items of iterable for which function(item)\nis true. If function is None, return the items that are true.';

batavia.builtins.float = function(args) {
    if (args.length > 1) {
        throw new batavia.builtins.TypeError("float() takes at most 1 argument (" + args.length + " given)");
    }
    if (args.length === 0) {
        return 0.0;
    }

    var value = args[0];

    if (batavia.isinstance(value, batavia.types.Str)) {
        if (value.search(/[^0-9.]/g) === -1) {
            return new batavia.types.Float(parseFloat(value));
        } else {
            if (value === "nan" || value === "+nan" || value === "-nan") {
                return new batavia.types.Float(NaN);
            } else if (value === "inf" || value === "+inf") {
                return new batavia.types.Float(Infinity);
            } else if (value === "-inf") {
                return new batavia.types.Float(-Infinity);
            }
            throw new batavia.builtins.ValueError("could not convert string to float: '" + args[0] + "'");
        }
    } else if (batavia.isinstance(value, [batavia.types.Int, batavia.types.Bool, batavia.types.Float])) {
        return args[0].__float__();
    }
};

batavia.builtins.float.__doc__ = 'float([x]) -> Convert a string or a number to floating point.';

batavia.builtins.format = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'format' not implemented");
};
batavia.builtins.format.__doc__ = 'format(value[, format_spec]) -> string\n\nReturns value.__format__(format_spec)\nformat_spec defaults to ""';


batavia.builtins.frozenset = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("frozenset() doesn't accept keyword arguments.");
    }
    if (args && args.length > 1) {
        throw new batavia.builtins.TypeError("set expected at most 1 arguments, got " + args.length);
    }
    if (!args || args.length == 0) {
        return new batavia.types.FrozenSet();
    }
    return new batavia.types.FrozenSet(args[0]);
};
batavia.builtins.frozenset.__doc__ = 'frozenset() -> empty frozenset object\nfrozenset(iterable) -> frozenset object\n\nBuild an immutable unordered collection of unique elements.';

batavia.builtins.getattr = function(args) {
    if (args) {
        var attr = args[0][args[1]];
        if (attr !== undefined) {
            return attr;
        } else {
            if (args.length === 3) {
                return args[2];
            } else if (args.length === 2) {
                throw new batavia.builtins.AttributeError("'" + args[0] + "' object has no attribute '" + args[1] + "'");
            } else if (args.length < 2) {
                throw new batavia.builtins.TypeError("getattr expected at least 2 arguments, got " + args.length);
            } else {
                throw new batavia.builtins.TypeError("getattr expected at most 3 arguments, got " + args.length);
            }
        }
    } else {
        throw new batavia.builtins.TypeError("getattr expected at least 2 arguments, got 0");
    }
};
batavia.builtins.getattr.__doc__ = "getattr(object, name[, default]) -> value\n\nGet a named attribute from an object; getattr(x, 'y') is equivalent to x.y.\nWhen a default argument is given, it is returned when the attribute doesn't\nexist; without it, an exception is raised in that case.";

// TODO: this should be a proper dictionary
batavia.builtins.globals = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("globals() doesn't accept keyword arguments");
    }
    if (args && args.length != 0) {
        throw new batavia.builtins.TypeError('globals() takes no arguments (' + args.length + ' given)');
    }
    var globals = this.frame.f_globals;

    // support items() iterator
    globals.items = function() {
        var l = [];
        var keys = Object.keys(globals);
        for (var i in keys) {
            var k = keys[i];
            // workaround until we have a proper dictionary
            if (k == 'items') {
              continue;
            }
            l.push(new batavia.types.Tuple([k, globals[k]]));
        }
        l = new batavia.types.List(l);
        return l;
    };
    return globals;
};
batavia.builtins.globals.__doc__ = "globals() -> dictionary\n\nReturn the dictionary containing the current scope's global variables.";

batavia.builtins.hasattr = function(args) {
    if (args) {
        try {
            if (batavia.builtins.getattr(args)) {
                return true;
            }
        } catch (err) {
            if (err instanceof batavia.builtins.AttributeError) {
                return false;
            }
            if (err instanceof batavia.builtins.TypeError) {
                throw new batavia.builtins.TypeError("hasattr expected 2 arguments, got " + args.length);
            }
        }
    } else {
        throw new batavia.builtins.TypeError("hasattr expected 2 arguments, got 0");
    }
};
batavia.builtins.hasattr.__doc__ = 'hasattr(object, name) -> bool\n\nReturn whether the object has an attribute with the given name.\n(This is done by calling getattr(object, name) and catching AttributeError.)';

batavia.builtins.hash = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("hash() doesn't accept keyword arguments");
    }
    if (!args || args.length != 1) {
        throw new batavia.builtins.TypeError('hash() expected exactly 1 argument (' + args.length + ' given)');
    }
    var arg = args[0];
    // None
    if (arg === null) {
        return 278918143;
    }
    if (batavia.isinstance(arg, [batavia.types.Bytearray, batavia.types.Dict, batavia.types.JSDict, batavia.types.List, batavia.types.Set, batavia.types.Slice])) {
        throw new batavia.builtins.TypeError("unhashable type: '" + batavia.type_name(arg) + "'");
    }
    if (typeof arg.__hash__ !== 'undefined') {
        return batavia.run_callable(arg, arg.__hash__, [], null);
    }
    // Use JS toString() to do a simple default hash, for now.
    // (This is similar to how JS objects work.)
    return new batavia.types.Str(arg.toString()).__hash__();
};
batavia.builtins.hash.__doc__ = 'hash(object) -> integer\n\nReturn a hash value for the object.  Two objects with the same value have\nthe same hash value.  The reverse is not necessarily true, but likely.';

batavia.builtins.help = function() {
    console.log("For help, please see: https://github.com/pybee/batavia.");
};
batavia.builtins.help.__doc__ = 'In Python, this is a wrapper around pydoc.help. In Batavia, this is a link to the README.';

batavia.builtins.hex = function(args) {
    if (args.length !== 1) {
        throw new batavia.builtins.TypeError("hex() takes exactly one argument (" + args.length + " given)");
    };
    var int = args[0].val
    return "0x" + int.toString(16);
};
batavia.builtins.hex.__doc__ = "hex(number) -> string\n\nReturn the hexadecimal representation of an integer.\n\n   >>> hex(3735928559)\n   '0xdeadbeef'\n";

batavia.builtins.id = function() {
    throw new batavia.builtins.PolyglotError("'id' has no meaning here. See docs/internals/limitations#id");
};
batavia.builtins.id.__doc__ = 'Return the identity of an object.  This is guaranteed to be unique among simultaneously existing objects.  (Hint: it\'s the object\'s memory address.)';


batavia.builtins.input = function(prompt_text) {
    var user_input = prompt(prompt_text);
    return user_input;
};
batavia.builtins.input.__doc__ = 'input([prompt]) -> string\n\nRead a string from standard input.  The trailing newline is stripped.\nIf the user hits EOF (Unix: Ctl-D, Windows: Ctl-Z+Return), raise EOFError.\nOn Unix, GNU readline is used if enabled.  The prompt string, if given,\nis printed without a trailing newline before reading.';

batavia.builtins.int = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("int() doesn't accept keyword arguments");
    }

    var base = 10;
    var value = 0;
    if (!args || args.length === 0) {
        return new batavia.types.Int(0);
    } else if (args && args.length === 1) {
        value = args[0];
        if (batavia.isinstance(value, [batavia.types.Int, batavia.types.Bool])) {
            return value.__int__();
        }
    } else if (args && args.length === 2) {
        value = args[0];
        base = args[1];
    } else {
        throw new batavia.builtins.TypeError(
            "int() takes at most 2 arguments (" + args.length + " given)");
    }
    // TODO: this should be able to parse things longer than 53 bits
    var result = parseInt(value, base);
    if (isNaN(result)) {
        throw new batavia.builtins.ValueError(
            "invalid literal for int() with base " + base + ": " + batavia.builtins.repr([value], null)
        );
    }
    return new batavia.types.Int(result);
};
batavia.builtins.int.__doc__ = "int(x=0) -> integer\nint(x, base=10) -> integer\n\nConvert a number or string to an integer, or return 0 if no arguments\nare given.  If x is a number, return x.__int__().  For floating point\nnumbers, this truncates towards zero.\n\nIf x is not a number or if base is given, then x must be a string,\nbytes, or bytearray instance representing an integer literal in the\ngiven base.  The literal can be preceded by '+' or '-' and be surrounded\nby whitespace.  The base defaults to 10.  Valid bases are 0 and 2-36.\nBase 0 means to interpret the base from the string as an integer literal.\n>>> int('0b100', base=0)\n4";

batavia.builtins.isinstance = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("isinstance() takes no keyword arguments");
    }

    if (!args || args.length != 2) {
        throw new batavia.builtins.TypeError("isinstance expected 2 arguments, got " + args.length);
    }

    return batavia.isinstance(args[0], args[1]);
};
batavia.builtins.isinstance.__doc__ = "isinstance(object, class-or-type-or-tuple) -> bool\n\nReturn whether an object is an instance of a class or of a subclass thereof.\nWith a type as second argument, return whether that is the object's type.\nThe form using a tuple, isinstance(x, (A, B, ...)), is a shortcut for\nisinstance(x, A) or isinstance(x, B) or ... (etc.).";

batavia.builtins.issubclass = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'issubclass' not implemented");
};
batavia.builtins.issubclass.__doc__ = 'issubclass(C, B) -> bool\n\nReturn whether class C is a subclass (i.e., a derived class) of class B.\nWhen using a tuple as the second argument issubclass(X, (A, B, ...)),\nis a shortcut for issubclass(X, A) or issubclass(X, B) or ... (etc.).';

batavia.builtins.iter = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("iter() doesn't accept keyword arguments");
    }
    if (!args || args.length === 0) {
        throw new batavia.builtins.TypeError("iter() expected at least 1 arguments, got 0");
    }
    if (args.length == 2) {
        throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'iter' with callable/sentinel not implemented");
    }
    if (args.length > 2) {
        throw new batavia.builtins.TypeError("iter() expected at most 2 arguments, got 3");
    }
    var iterobj = args[0];
    if (iterobj !== batavia.builtins.None && typeof iterobj === 'object' && !iterobj.__class__) {
        // this is a plain JS object, wrap it in a JSDict
        iterobj = new batavia.types.JSDict(iterobj);
    }

    if (iterobj !== batavia.builtins.None && iterobj.__iter__) {
        //needs to work for __iter__ in JS impl (e.g. Map/Filter) and python ones
        return batavia.run_callable(iterobj, iterobj.__iter__, [], null);
    } else {
        throw new batavia.builtins.TypeError("'" + batavia.type_name(iterobj) + "' object is not iterable");
    }
};
batavia.builtins.iter.__doc__ = 'iter(iterable) -> iterator\niter(callable, sentinel) -> iterator\n\nGet an iterator from an object.  In the first form, the argument must\nsupply its own iterator, or be a sequence.\nIn the second form, the callable is called until it returns the sentinel.';

batavia.builtins.len = function(args, kwargs) {
    if (!args || args.length !== 1 || args[0] === undefined) {
        throw new batavia.builtins.TypeError("len() takes exactly one argument (" + args.length + " given)");
    }

    //if (args[0].hasOwnProperty("__len__")) {
        //TODO: Fix context of python functions calling with proper vm
        //throw new batavia.builtins.NotImplementedError('Builtin Batavia len function is not supporting __len__ implemented.');
        //return args[0].__len__.apply(vm);
    //}

    return new batavia.types.Int(args[0].length);
};
batavia.builtins.len.__doc__ = 'len(object)\n\nReturn the number of items of a sequence or collection.';

batavia.builtins.license = function() {
    console.log("LICENSE file is available at https://github.com/pybee/batavia/blob/master/LICENSE");
    batavia.builtins.credits();
    batavia.builtins.copyright();
};
batavia.builtins.license.__doc__ = 'license()\n\nPrompt printing the license text, a list of contributors, and the copyright notice';

batavia.builtins.list = function(args) {
    if (!args || args.length === 0) {
      return new batavia.types.List();
    }
    return new batavia.types.List(args[0]);
};
batavia.builtins.list.__doc__ = "list() -> new empty list\nlist(iterable) -> new list initialized from iterable's items";

batavia.builtins.locals = function() {
    return this.frame.f_locals;
};
batavia.builtins.locals.__doc__ = "locals() -> dictionary\n\nUpdate and return a dictionary containing the current scope's local variables.";

batavia.builtins.map = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }

    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("map() doesn't accept keyword arguments");
    }

    if (!args || args.length < 2) {
        throw new batavia.builtins.TypeError('map() must have at least two arguments.');
    }

    return new batavia.types.map(args, kwargs);
};
batavia.builtins.map.__doc__ = 'map(func, *iterables) --> map object\n\nMake an iterator that computes the function using arguments from\neach of the iterables.  Stops when the shortest iterable is exhausted.';


batavia.builtins.max = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (!args || args.length === 0) {
        throw new batavia.builtins.TypeError('max expected 1 arguments, got ' + args.length);
    }

    if (args.length > 1) {
        var list = batavia.builtins.tuple([args], batavia.builtins.None);
    } else if (batavia.isinstance(args[0], [
                batavia.types.List, batavia.types.Dict, batavia.types.Tuple,
                batavia.types.Set, batavia.types.Bytearray, batavia.types.Bytes,
                batavia.types.Range, batavia.types.Slice, batavia.types.FrozenSet,
                batavia.types.Str
            ])) {
        var list = batavia.builtins.tuple([args[0]], batavia.builtins.None);
    } else {
        throw new batavia.builtins.TypeError("'" + batavia.type_name(args[0]) + "' object is not iterable");
    }
    if (list.length === 0) {
        if ('default' in kwargs) {
            return kwargs['default'];
        } else {
            throw new batavia.builtins.ValueError("max() arg is an empty sequence");
        }
    }
    var max = list[0];
    for(var i = 1; i < list.length; i++) {
        if(list[i].__gt__(max)) {
            max = list[i];
        }
    }
    return max;
};
batavia.builtins.max.__doc__ = "max(iterable, *[, default=obj, key=func]) -> value\nmax(arg1, arg2, *args, *[, key=func]) -> value\n\nWith a single iterable argument, return its biggest item. The\ndefault keyword-only argument specifies an object to return if\nthe provided iterable is empty.\nWith two or more arguments, return the largest argument.";

batavia.builtins.memoryview = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'memoryview' not implemented");
};
batavia.builtins.memoryview.__doc__ = 'memoryview(object)\n\nCreate a new memoryview object which references the given object.';

batavia.builtins.min = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (!args || args.length === 0) {
        throw new batavia.builtins.TypeError('min expected 1 arguments, got ' + args.length);
    }

    if (args.length > 1) {
        var list = batavia.builtins.tuple([args], null);
    } else if (batavia.isinstance(args[0], [
                batavia.types.List, batavia.types.Dict, batavia.types.Tuple,
                batavia.types.Set, batavia.types.Bytearray, batavia.types.Bytes,
                batavia.types.Range, batavia.types.Slice, batavia.types.FrozenSet,
                batavia.types.Str
            ])) {
        var list = batavia.builtins.tuple([args[0]], null);
    } else {
        throw new batavia.builtins.TypeError("'" + batavia.type_name(args[0]) + "' object is not iterable");
    }
    if (list.length === 0) {
      if ('default' in kwargs) {
          return kwargs['default'];
      } else {
          throw new batavia.builtins.ValueError("min() arg is an empty sequence");
      }
    }
    var min = list[0];
    for(var i = 1; i < list.length; i++) {
        if(list[i].__lt__(min)) {
            min = list[i];
        }
    }
    return min;
};
batavia.builtins.min.__doc__ = "min(iterable, *[, default=obj, key=func]) -> value\nmin(arg1, arg2, *args, *[, key=func]) -> value\n\nWith a single iterable argument, return its smallest item. The\ndefault keyword-only argument specifies an object to return if\nthe provided iterable is empty.\nWith two or more arguments, return the smallest argument.";

batavia.builtins.next = function() {
    //if its iterable return next thing in iterable
    //else stop iteration
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'next' not implemented");
};
batavia.builtins.next.__doc__ = 'next(iterator[, default])\n\nReturn the next item from the iterator. If default is given and the iterator\nis exhausted, it is returned instead of raising StopIteration.';


batavia.builtins.object = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'object' not implemented");
};
batavia.builtins.object.__doc__ = "The most base type"; // Yes, that's the entire docstring.

batavia.builtins.oct = function(args) {
    if (!args || args.length !== 1) {
        throw new batavia.builtins.TypeError("oct() takes exactly one argument (" + (args ? args.length : 0) + " given)");
    }
    var value = args[0];
    if (batavia.isinstance(value, batavia.types.Int)) {
        if (value.val.isNeg()) {
            return "-0o" + value.val.toString(8).substr(1);
        } else {
            return "0o" + value.val.toString(8);
        }
    } else if (batavia.isinstance(value, batavia.types.Bool)) {
        return "0o" + value.__int__().toString(8);
    }

    if(!batavia.isinstance(value, batavia.types.Int)) {
        if(value.__index__) {
             value = value.__index__();
        } else {
            throw new batavia.builtins.TypeError("__index__ method needed for non-integer inputs");
        }
    }
    if(value < 0) {
        return "-0o" + (0 - value).toString(8);
    }

    return "0o" + value.toString(8);
};
batavia.builtins.oct.__doc__ = "oct(number) -> string\n\nReturn the octal representation of an integer.\n\n   >>> oct(342391)\n   '0o1234567'\n";

batavia.builtins.open = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'open' not implemented");
};
batavia.builtins.open.__doc__ = 'open() is complicated.'; // 6575 character long docstring

batavia.builtins.ord = function(args, kwargs) {
    return args[0].charCodeAt(0);
};
batavia.builtins.ord.__doc__ = 'ord(c) -> integer\n\nReturn the integer ordinal of a one-character string.';

batavia.builtins.pow = function(args) {
    var x, y, z;
    if (!args) {
      throw new batavia.builtins.TypeError("pow expected at least 2 arguments, got 0");
    }
    if (args.length === 2) {
        x = args[0];
        y = args[1];
        return x.__pow__(y);
    } else if (args.length === 3) {
        x = args[0];
        y = args[1];
        z = args[2];

        if (!batavia.isinstance(x, batavia.types.Int) ||
            !batavia.isinstance(y, batavia.types.Int) ||
            !batavia.isinstance(y, batavia.types.Int)) {
            throw new batavia.builtins.TypeError("pow() requires all arguments be integers when 3 arguments are present");
        }
        if (y < 0) {
          throw new batavia.builtins.TypeError("Builtin Batavia does not support negative exponents");
        }
        if (y == 0) {
          return 1;
        }
        if (z == 1) {
          return 0;
        }

        // right-to-left exponentiation to reduce memory and time
        // See https://en.wikipedia.org/wiki/Modular_exponentiation#Right-to-left_binary_method
        var result = 1;
        var base = x % z;
        while (y > 0) {
          if ((y & 1) == 1) {
            result = (result * base) % z;
          }
          y >>= 1;
          base = (base * base) % z;
        }
        return result;
    } else {
        throw new batavia.builtins.TypeError("pow expected at least 2 arguments, got " + args.length);
    }
};
batavia.builtins.pow.__doc__ = 'pow(x, y[, z]) -> number\n\nWith two arguments, equivalent to x**y.  With three arguments,\nequivalent to (x**y) % z, but may be more efficient (e.g. for ints).';

batavia.builtins.print = function(args, kwargs) {
    var elements = [], print_value;
    args.map(function(elm) {
        if (elm === null || elm === undefined) {
            elements.push("None");
        } else if (elm.__str__) {
            elements.push(batavia.run_callable(elm, elm.__str__, [], {}));
        } else {
            elements.push(elm.toString());
        }
    });
    batavia.stdout(elements.join(' ') + "\n");
};
batavia.builtins.print.__doc__ = "print(value, ..., sep=' ', end='\\n', file=sys.stdout, flush=False)\n\nPrints the values to a stream, or to sys.stdout by default.\nOptional keyword arguments:\nfile:  a file-like object (stream); defaults to the current sys.stdout.\nsep:   string inserted between values, default a space.\nend:   string appended after the last value, default a newline.\nflush: whether to forcibly flush the stream.";


batavia.builtins.property = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'property' not implemented");
};
batavia.builtins.property.__doc__ = 'property(fget=None, fset=None, fdel=None, doc=None) -> property attribute\n\nfget is a function to be used for getting an attribute value, and likewise\nfset is a function for setting, and fdel a function for del\'ing, an\nattribute.  Typical use is to define a managed attribute x:\n\nclass C(object):\n    def getx(self): return self._x\n    def setx(self, value): self._x = value\n    def delx(self): del self._x\n    x = property(getx, setx, delx, "I\'m the \'x\' property.")\n\nDecorators make defining new properties or modifying existing ones easy:\n\nclass C(object):\n    @property\n    def x(self):\n        "I am the \'x\' property."\n        return self._x\n    @x.setter\n    def x(self, value):\n        self._x = value\n    @x.deleter\n    def x(self):\n        del self._x\n';

batavia.builtins.range = function(args, kwargs){
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("range() doesn't accept keyword arguments");
    }
    if (!args || args.length === 0) {
        throw new batavia.builtins.TypeError('range() expected 1 arguments, got ' + args.length);
    }
    if (args.length > 3) {
     throw new batavia.builtins.TypeError('range() expected at most 3 arguments, got ' + args.length);
    }

    return new batavia.types.Range(args[0], args[1], args[2]);
};
batavia.builtins.range.__doc__ = 'range(stop) -> range object\nrange(start, stop[, step]) -> range object\n\nReturn a virtual sequence of numbers from start to stop by step.';

batavia.builtins.repr = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("repr() doesn't accept keyword arguments");
    }
    if (!args || args.length !== 1) {
        throw new batavia.builtins.TypeError('repr() takes exactly 1 argument (' + args.length + ' given)');
    }

    if (args[0] === null) {
        return 'None';
    } else if (args[0].__repr__) {
        return args[0].__repr__();
    } else {
        return args[0].toString();
    }
};
batavia.builtins.repr.__doc__ = 'repr(object) -> string\n\nReturn the canonical string representation of the object.\nFor most object types, eval(repr(object)) == object.';

batavia.builtins.reversed = function(args, kwargs) {
    var iterable = args[0];
    if (batavia.isinstance(iterable, [batavia.types.List, batavia.types.Tuple])) {
        var new_iterable = iterable.slice(0);
        new_iterable.reverse();
        return new batavia.types.List(new_iterable);
    }

    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'reversed' not implemented for objects");

};

batavia.builtins.reversed.__doc__ = 'reversed(sequence) -> reverse iterator over values of the sequence\n\nReturn a reverse iterator';


batavia.builtins.round = function(args) {
    var p = 0; // Precision
    if (!args) {
      throw new batavia.builtins.TypeError("Required argument 'number' (pos 1) not found");
    }
    if (args.length == 2) {
        p = args[1];
    }
    var result = 0;
    if (batavia.isinstance(args[0], batavia.types.Bool)) {
        result = args[0].__int__();
    } else {
        result = new batavia.vendored.BigNumber(args[0]).round(p);
    }
    if (args.length == 1) {
        return new batavia.types.Int(result);
    }
    return batavia.types.Float(result.valueOf());
};
batavia.builtins.round.__doc__ = 'round(number[, ndigits]) -> number\n\nRound a number to a given precision in decimal digits (default 0 digits).\nThis returns an int when called with one argument, otherwise the\nsame type as the number. ndigits may be negative.';

batavia.builtins.set = function(args,kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("set() doesn't accept keyword arguments.");
    }
    if (args && args.length > 1) {
        throw new batavia.builtins.TypeError("set expected at most 1 arguments, got " + args.length);
    }
    if (!args || args.length == 0) {
        return new batavia.types.Set();
    }
    return new batavia.types.Set(args[0]);
};
batavia.builtins.set.__doc__ = 'set() -> new empty set object\nset(iterable) -> new set object\n\nBuild an unordered collection of unique elements.';

batavia.builtins.setattr = function(args) {
    if (args.length !== 3) {
        throw new batavia.builtins.TypeError("setattr expected exactly 3 arguments, got " + args.length);
    }

    args[0][args[1]] = args[2];
};
batavia.builtins.setattr.__doc__ = "setattr(object, name, value)\n\nSet a named attribute on an object; setattr(x, 'y', v) is equivalent to\n``x.y = v''.";

batavia.builtins.slice = function(args, kwargs) {
    if (args.length == 1) {
        return new batavia.types.Slice({
            start: new batavia.types.Int(0),
            stop: args[0],
            step: new batavia.types.Int(1)
        });
    } else {
        return new batavia.types.Slice({
            start: args[0],
            stop: args[1],
            step: new batavia.types.Int(args[2] || 1)
        });
    }
};
batavia.builtins.slice.__doc__ = 'slice(stop)\nslice(start, stop[, step])\n\nCreate a slice object.  This is used for extended slicing (e.g. a[0:10:2]).';

batavia.builtins.sorted = function(args, kwargs) {
    var validatedInput = batavia.builtins.sorted._validateInput(args, kwargs);
    var iterable = validatedInput["iterable"];

    if (batavia.isinstance(iterable, [batavia.types.List, batavia.types.Tuple])) {
        iterable = iterable.map(validatedInput["preparingFunction"]);
        iterable.sort(function (a, b) {
            // TODO: Replace this with a better, guaranteed stable sort.
            // Javascript's default sort has performance problems in some
            // implementations and is not guaranteed to be stable, while
            // CPython's sorted is stable and efficient. See:
            // * https://docs.python.org/3/library/functions.html#sorted
            // * https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort
            if (a["key"].__gt__(b["key"])) {
                return validatedInput["bigger"];
            }

            if (a["key"].__lt__(b["key"])) {
                return validatedInput["smaller"];
            }
            return 0;
        });

        return new batavia.types.List(iterable.map(function (element) {
            return element["value"];
        }));
    }

    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'sorted' not implemented for objects");
};
batavia.builtins.sorted.__doc__ = 'sorted(iterable, key=None, reverse=False) --> new sorted list';

batavia.builtins.sorted._validateInput = function (args, kwargs, undefined) {
    var bigger = 1;
    var smaller = -1;
    var preparingFunction = function (value) {
        return {
            "key": value,
            "value": value
        };
    };


    if (kwargs !== undefined) {
        if (kwargs['iterable'] !== undefined) {
            throw new batavia.builtins.TypeError("'iterable' is an invalid keyword argument for this function");
        }

        if (kwargs["reverse"] !== undefined && kwargs["reverse"] === true) {
            bigger = -1;
            smaller = 1;
        }


        if (kwargs["key"] !== undefined) {
            //TODO: Fix context of python functions calling with proper vm
            throw new batavia.builtins.NotImplementedError('Builtin Batavia sorted function "key" function is not implemented.');
            //preparingFunction = function (value) {
            //    return {
            //        "key": kwargs["key"].__call__.apply(kwargs["key"]._vm, [value], null),
            //        "value": value
            //    };
            //}
        }
    }

    if (args === undefined || args.length === 0) {
        throw new batavia.builtins.TypeError("Required argument 'iterable' (pos 1) not found");
    }

    return {
        iterable: args[0],
        bigger: bigger,
        smaller: smaller,
        preparingFunction: preparingFunction
    };
};

batavia.builtins.staticmethod = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'staticmethod' not implemented");
};
batavia.builtins.staticmethod.__doc__ = 'staticmethod(function) -> method\n\nConvert a function to be a static method.\n\nA static method does not receive an implicit first argument.\nTo declare a static method, use this idiom:\n\n     class C:\n     def f(arg1, arg2, ...): ...\n     f = staticmethod(f)\n\nIt can be called either on the class (e.g. C.f()) or on an instance\n(e.g. C().f()).  The instance is ignored except for its class.\n\nStatic methods in Python are similar to those found in Java or C++.\nFor a more advanced concept, see the classmethod builtin.';

batavia.builtins.str = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("str() doesn't accept keyword arguments");
    }
    if (!args || args.length !== 1) {
        throw new batavia.builtins.TypeError('str() takes exactly 1 argument (' + args.length + ' given)');
    }

    if (args[0] === null) {
        return 'None';
    } else if (args[0].__str__) {
        return args[0].__str__();
    } else {
        return args[0].toString();
    }
};
batavia.builtins.str.__doc__ = 'str(object) -> string\n\nReturn the canonical string representation of the object.\nFor most object types, eval(repr(object)) == object.';

batavia.builtins.sum = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("sum() doesn't accept keyword arguments");
    }
    if (!args || args.length === 0) {
        throw new batavia.builtins.TypeError('sum() expected at least 1 argument, got ' + args.length);
    }
    if (args.length > 2) {
        throw new batavia.builtins.TypeError('sum() expected at most 2 argument, got ' + args.length);
    }

    try {
        return args[0].reduce(function(a, b) {
            return a.__add__(b);
        }, new batavia.types.Int(0));
    } catch (err) {
        throw new batavia.builtins.TypeError(
                "bad operand type for sum(): 'NoneType'");
    }
};
batavia.builtins.sum.__doc__ = "sum(iterable[, start]) -> value\n\nReturn the sum of an iterable of numbers (NOT strings) plus the value\nof parameter 'start' (which defaults to 0).  When the iterable is\nempty, return start.";

batavia.builtins.super = function(args, kwargs) {
    if (args.length > 0) {
        throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'super' with arguments not implemented");
    }

    return batavia.make_super(this.frame, args);
};
batavia.builtins.super.__doc__ = 'super() -> same as super(__class__, <first argument>)\nsuper(type) -> unbound super object\nsuper(type, obj) -> bound super object; requires isinstance(obj, type)\nsuper(type, type2) -> bound super object; requires issubclass(type2, type)\nTypical use to call a cooperative superclass method:\nclass C(B):\n    def meth(self, arg):\n        super().meth(arg)\nThis works for class methods too:\nclass C(B):\n    @classmethod\n    def cmeth(cls, arg):\n        super().cmeth(arg)\n';

batavia.builtins.tuple = function(args) {
    if (args.length === 0) {
      return new batavia.types.Tuple();
    }
    return new batavia.types.Tuple(args[0]);
};
batavia.builtins.tuple.__doc__ = "tuple() -> empty tuple\ntuple(iterable) -> tuple initialized from iterable's items\n\nIf the argument is a tuple, the return value is the same object.";

batavia.builtins.type = function(args, kwargs) {
    if (arguments.length != 2) {
        throw new batavia.builtins.BataviaError('Batavia calling convention not used.');
    }
    if (kwargs && Object.keys(kwargs).length > 0) {
        throw new batavia.builtins.TypeError("type() doesn't accept keyword arguments");
    }
    if (!args || (args.length != 1 && args.length != 3)) {
        throw new batavia.builtins.TypeError('type() takes 1 or 3 arguments');
    }

    if (args.length === 1) {
        if (args[0] === null) {
            return batavia.types.NoneType;
        } else {
            return args[0].__class__;
        }
    } else {
        return new batavia.types.Type(args[0], args[1], args[2]);
    }
};
batavia.builtins.type.__doc__ = "type(object_or_name, bases, dict)\ntype(object) -> the object's type\ntype(name, bases, dict) -> a new type";

batavia.builtins.vars = function() {
    throw new batavia.builtins.NotImplementedError("Builtin Batavia function 'vars' not implemented");
};
batavia.builtins.vars.__doc__ = 'vars([object]) -> dictionary\n\nWithout arguments, equivalent to locals().\nWith an argument, equivalent to object.__dict__.';

batavia.builtins.zip = function(args, undefined) {
    if (args === undefined) {
        return [];
    }

    var minLen = Math.min.apply(null, args.map(function (element) {
        return element.length;
    }));


    if (minLen === 0) {
        return [];
    }

    var result = [];
    for(var i = 0; i < minLen; i++) {
        var sequence = [];
        for(var iterableObj = 0; iterableObj < args.length; iterableObj++) {
            sequence.push(args[iterableObj][i]);
        }

        result.push(new batavia.types.Tuple(sequence));
    }

    return result;
};
batavia.builtins.zip.__doc__ = 'zip(iter1 [,iter2 [...]]) --> zip object\n\nReturn a zip object whose .__next__() method returns a tuple where\nthe i-th element comes from the i-th iterable argument.  The .__next__()\nmethod continues until the shortest iterable in the argument sequence\nis exhausted and then it raises StopIteration.';

// Mark all builtins as Python methods.
for (var fn in batavia.builtins) {
    batavia.builtins[fn].__python__ = true;
}

batavia.builtins.None = new batavia.types.NoneType();
batavia.builtins.NotImplemented = new batavia.types.NotImplementedType();
/*
 * A fake cell for closures.
 *
 * Closures keep names in scope by storing them not in a frame, but in a
 * separate object called a cell.  Frames share references to cells, and
 * the LOAD_DEREF and STORE_DEREF opcodes get and set the value from cells.
 *
 * This class acts as a cell, though it has to jump through two hoops to make
 * the simulation complete:
 *
 *     1. In order to create actual FunctionType functions, we have to have
 *        actual cell objects, which are difficult to make. See the twisty
 *        double-lambda in __init__.
 *
 *     2. Actual cell objects can't be modified, so to implement STORE_DEREF,
 *        we store a one-element list in our cell, and then use [0] as the
 *        actual value.
 */

batavia.core.Cell = function(value) {
    this.contents = value;
};

batavia.core.Cell.prototype.get = function() {
    return this.contents;
};

batavia.core.Cell.prototype.set = function(value) {
    this.contents = value;
};
/*****************************************************************
 * Root exception
 *****************************************************************/

BaseException = function(name, msg) {
    this.name = name;
    this.msg = msg;
};

batavia.builtins.BaseException = BaseException;
batavia.builtins.BaseException.__class__ = new batavia.types.Type('BaseException', [batavia.types.Object]);
batavia.builtins.BaseException.prototype.__class__ = batavia.builtins.BaseException.__class__;

batavia.builtins.BaseException.prototype.toString = function() {
    return this.__str__();
};

batavia.builtins.BaseException.prototype.__str__ = function() {
    if (this.msg) {
        return this.msg;
    } else {
        return '';
    }
};

batavia.builtins.BaseException.prototype.__repr__ = function() {
    if (this.msg) {
        return this.name + "(" + this.msg + ")";
    } else {
        return this.name + "()";
    }
};

/*****************************************************************
 * Top level exceptions
 *****************************************************************/

function SystemExit(msg) {
    batavia.builtins.BaseException.call(this, 'SystemExit', msg);
}
batavia.builtins.SystemExit = SystemExit;
batavia.builtins.SystemExit.prototype = Object.create(batavia.builtins.BaseException.prototype);
batavia.builtins.SystemExit.__class__ = new batavia.types.Type('SystemExit', [batavia.builtins.BaseException]);
batavia.builtins.SystemExit.prototype.__class__ = batavia.builtins.SystemExit.__class__;

function KeyboardInterrupt(msg) {
    batavia.builtins.BaseException.call(this, 'KeyboardInterrupt', msg);
}
batavia.builtins.KeyboardInterrupt = KeyboardInterrupt;
batavia.builtins.KeyboardInterrupt.prototype = Object.create(batavia.builtins.BaseException.prototype);
batavia.builtins.KeyboardInterrupt.__class__ = new batavia.types.Type('KeyboardInterrupt', [batavia.builtins.BaseException]);
batavia.builtins.KeyboardInterrupt.prototype.__class__ = batavia.builtins.KeyboardInterrupt.__class__;

function GeneratorExit(msg) {
    batavia.builtins.BaseException.call(this, 'GeneratorExit', msg);
}
batavia.builtins.GeneratorExit = GeneratorExit;
batavia.builtins.GeneratorExit.prototype = Object.create(batavia.builtins.BaseException.prototype);
batavia.builtins.GeneratorExit.__class__ = new batavia.types.Type('GeneratorExit', [batavia.builtins.BaseException]);
batavia.builtins.GeneratorExit.prototype.__class__ = batavia.builtins.GeneratorExit.__class__;

function Exception(name, msg) {
    if (arguments.length == 1) {
        // If only one argument is provided, it will be the message.
        batavia.builtins.BaseException.call(this, 'Exception', name);
    } else {
        batavia.builtins.BaseException.call(this, name, msg);
    }
}
batavia.builtins.Exception = Exception;
batavia.builtins.Exception.prototype = Object.create(batavia.builtins.BaseException.prototype);
batavia.builtins.Exception.__class__ = new batavia.types.Type('Exception', [batavia.builtins.BaseException]);
batavia.builtins.Exception.prototype.__class__ = batavia.builtins.Exception.__class__;

/*****************************************************************
 * All other exceptions
 *****************************************************************/

function BataviaError(msg) {
    batavia.builtins.Exception.call(this, 'BataviaError', msg);
}
batavia.builtins.BataviaError = BataviaError;
batavia.builtins.BataviaError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.BataviaError.__class__ = new batavia.types.Type('BataviaError', [batavia.builtins.Exception]);
batavia.builtins.BataviaError.prototype.__class__ = batavia.builtins.BataviaError.__class__;

function ArithmeticError(msg) {
    batavia.builtins.Exception.call(this, 'ArithmeticError', msg);
}
batavia.builtins.ArithmeticError = ArithmeticError;
batavia.builtins.ArithmeticError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.ArithmeticError.__class__ = new batavia.types.Type('ArithmeticError', [batavia.builtins.Exception]);
batavia.builtins.ArithmeticError.prototype.__class__ = batavia.builtins.ArithmeticError.__class__;

function AssertionError(msg) {
    batavia.builtins.Exception.call(this, 'AssertionError', msg);
}
batavia.builtins.AssertionError = AssertionError;
batavia.builtins.AssertionError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.AssertionError.__class__ = new batavia.types.Type('AssertionError', [batavia.builtins.Exception]);
batavia.builtins.AssertionError.prototype.__class__ = batavia.builtins.AssertionError.__class__;

function AttributeError(msg) {
    batavia.builtins.Exception.call(this, 'AttributeError', msg);
}
batavia.builtins.AttributeError = AttributeError;
batavia.builtins.AttributeError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.AttributeError.__class__ = new batavia.types.Type('AttributeError', [batavia.builtins.Exception]);
batavia.builtins.AttributeError.prototype.__class__ = batavia.builtins.AttributeError.__class__;

function BufferError(msg) {
    batavia.builtins.Exception.call(this, 'BufferError', msg);
}
batavia.builtins.BufferError = BufferError;
batavia.builtins.BufferError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.BufferError.__class__ = new batavia.types.Type('BufferError', [batavia.builtins.Exception]);
batavia.builtins.BufferError.prototype.__class__ = batavia.builtins.BufferError.__class__;

batavia.builtins.BytesWarning = undefined;

batavia.builtins.DeprecationWarning = undefined;

function EOFError(msg) {
    batavia.builtins.Exception.call(this, 'EOFError', msg);
}
batavia.builtins.EOFError = EOFError;
batavia.builtins.EOFError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.EOFError.__class__ = new batavia.types.Type('EOFError', [batavia.builtins.Exception]);
batavia.builtins.EOFError.prototype.__class__ = batavia.builtins.EOFError.__class__;

function EnvironmentError(msg) {
    batavia.builtins.Exception.call(this, 'EnvironmentError', msg);
}
batavia.builtins.EnvironmentError = EnvironmentError;
batavia.builtins.EnvironmentError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.EnvironmentError.__class__ = new batavia.types.Type('EnvironmentError', [batavia.builtins.Exception]);
batavia.builtins.EnvironmentError.prototype.__class__ = batavia.builtins.EnvironmentError.__class__;

function FloatingPointError(msg) {
    batavia.builtins.Exception.call(this, 'FloatingPointError', msg);
}
batavia.builtins.FloatingPointError = FloatingPointError;
batavia.builtins.FloatingPointError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.FloatingPointError.__class__ = new batavia.types.Type('FloatingPointError', [batavia.builtins.Exception]);
batavia.builtins.FloatingPointError.prototype.__class__ = batavia.builtins.FloatingPointError.__class__;

batavia.builtins.FutureWarning = undefined;

function IOError(msg) {
    batavia.builtins.Exception.call(this, 'IOError', msg);
}
batavia.builtins.IOError = IOError;
batavia.builtins.IOError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.IOError.__class__ = new batavia.types.Type('IOError', [batavia.builtins.Exception]);
batavia.builtins.IOError.prototype.__class__ = batavia.builtins.IOError.__class__;

function ImportError(msg) {
    batavia.builtins.Exception.call(this, 'ImportError', msg);
}
batavia.builtins.ImportError = ImportError;
batavia.builtins.ImportError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.ImportError.__class__ = new batavia.types.Type('ImportError', [batavia.builtins.Exception]);
batavia.builtins.ImportError.prototype.__class__ = batavia.builtins.ImportError.__class__;

batavia.builtins.ImportWarning = undefined;

function IndentationError(msg) {
    batavia.builtins.Exception.call(this, 'IndentationError', msg);
}
batavia.builtins.IndentationError = IndentationError;
batavia.builtins.IndentationError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.IndentationError.__class__ = new batavia.types.Type('IndentationError', [batavia.builtins.Exception]);
batavia.builtins.IndentationError.prototype.__class__ = batavia.builtins.IndentationError.__class__;

function IndexError(msg) {
    batavia.builtins.Exception.call(this, 'IndexError', msg);
}
batavia.builtins.IndexError = IndexError;
batavia.builtins.IndexError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.IndexError.__class__ = new batavia.types.Type('IndexError', [batavia.builtins.Exception]);
batavia.builtins.IndexError.prototype.__class__ = batavia.builtins.IndexError.__class__;

function KeyError(key) {
    var msg;
    if (key === null) {
        msg = "None";
    } else if (key['__repr__'] && !key.hasOwnProperty('__repr__')) {
        msg = key.__repr__();
    } else {
        msg = key.toString();
    }
    batavia.builtins.Exception.call(this, 'KeyError', msg);
}
batavia.builtins.KeyError = KeyError;
batavia.builtins.KeyError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.KeyError.__class__ = new batavia.types.Type('KeyError', [batavia.builtins.Exception], null, KeyError);
batavia.builtins.KeyError.prototype.__class__ = batavia.builtins.KeyError.__class__;

function LookupError(msg) {
    batavia.builtins.Exception.call(this, 'LookupError', msg);
}
batavia.builtins.LookupError = LookupError;
batavia.builtins.LookupError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.LookupError.__class__ = new batavia.types.Type('LookupError', [batavia.builtins.Exception]);
batavia.builtins.LookupError.prototype.__class__ = batavia.builtins.LookupError.__class__;

function MemoryError(msg) {
    batavia.builtins.Exception.call(this, 'MemoryError', msg);
}
batavia.builtins.MemoryError = MemoryError;
batavia.builtins.MemoryError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.MemoryError.__class__ = new batavia.types.Type('MemoryError', [batavia.builtins.Exception]);
batavia.builtins.MemoryError.prototype.__class__ = batavia.builtins.MemoryError.__class__;

function NameError(msg) {
    batavia.builtins.Exception.call(this, 'NameError', msg);
}
batavia.builtins.NameError = NameError;
batavia.builtins.NameError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.NameError.__class__ = new batavia.types.Type('NameError', [batavia.builtins.Exception]);
batavia.builtins.NameError.prototype.__class__ = batavia.builtins.NameError.__class__;

function NotImplementedException(msg) {
    batavia.builtins.Exception.call(this, 'NotImplementedException', msg);
}
batavia.builtins.NotImplementedException = NotImplementedException;
batavia.builtins.NotImplementedException.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.NotImplementedException.__class__ = new batavia.types.Type('NotImplementedException', [batavia.builtins.Exception]);
batavia.builtins.NotImplementedException.prototype.__class__ = batavia.builtins.NotImplementedException.__class__;

function NotImplementedError(msg) {
    batavia.builtins.Exception.call(this, 'NotImplementedError', msg);
}
batavia.builtins.NotImplementedError = NotImplementedError;
batavia.builtins.NotImplementedError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.NotImplementedError.__class__ = new batavia.types.Type('NotImplementedError', [batavia.builtins.Exception]);
batavia.builtins.NotImplementedError.prototype.__class__ = batavia.builtins.NotImplementedError.__class__;

function OSError(msg) {
    batavia.builtins.Exception.call(this, 'OSError', msg);
}
batavia.builtins.OSError = OSError;
batavia.builtins.OSError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.OSError.__class__ = new batavia.types.Type('OSError', [batavia.builtins.Exception]);
batavia.builtins.OSError.prototype.__class__ = batavia.builtins.OSError.__class__;

function OverflowError(msg) {
    batavia.builtins.Exception.call(this, 'OverflowError', msg);
}
batavia.builtins.OverflowError = OverflowError;
batavia.builtins.OverflowError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.OverflowError.__class__ = new batavia.types.Type('OverflowError', [batavia.builtins.Exception]);
batavia.builtins.OverflowError.prototype.__class__ = batavia.builtins.OverflowError.__class__;

batavia.builtins.PendingDeprecationWarning = undefined;

function PolyglotError(msg) {
    batavia.builtins.Exception.call(this, 'PolyglotError', msg);
}
batavia.builtins.PolyglotError = PolyglotError;
batavia.builtins.PolyglotError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.PolyglotError.__class__ = new batavia.types.Type('PolyglotError', [batavia.builtins.Exception]);
batavia.builtins.PolyglotError.prototype.__class__ = batavia.builtins.PolyglotError.__class__;

function ReferenceError(msg) {
    batavia.builtins.Exception.call(this, 'ReferenceError', msg);
}
batavia.builtins.ReferenceError = ReferenceError;
batavia.builtins.ReferenceError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.ReferenceError.__class__ = new batavia.types.Type('ReferenceError', [batavia.builtins.Exception]);
batavia.builtins.ReferenceError.prototype.__class__ = batavia.builtins.ReferenceError.__class__;

function RuntimeError(msg) {
    batavia.builtins.Exception.call(this, 'RuntimeError', msg);
}
batavia.builtins.RuntimeError = RuntimeError;
batavia.builtins.RuntimeError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.RuntimeError.__class__ = new batavia.types.Type('RuntimeError', [batavia.builtins.Exception]);
batavia.builtins.RuntimeError.prototype.__class__ = batavia.builtins.RuntimeError.__class__;

batavia.builtins.RuntimeWarning = undefined;

function StandardError(msg) {
    batavia.builtins.Exception.call(this, 'StandardError', msg);
}
batavia.builtins.StandardError = StandardError;
batavia.builtins.StandardError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.StandardError.__class__ = new batavia.types.Type('StandardError', [batavia.builtins.Exception]);
batavia.builtins.StandardError.prototype.__class__ = batavia.builtins.StandardError.__class__;

function StopIteration(msg) {
    batavia.builtins.Exception.call(this, 'StopIteration', msg);
}
batavia.builtins.StopIteration = StopIteration;
batavia.builtins.StopIteration.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.StopIteration.__class__ = new batavia.types.Type('StopIteration', [batavia.builtins.Exception]);
batavia.builtins.StopIteration.prototype.__class__ = batavia.builtins.StopIteration.__class__;

function SyntaxError(msg) {
    batavia.builtins.Exception.call(this, 'SyntaxError', msg);
}
batavia.builtins.SyntaxError = SyntaxError;
batavia.builtins.SyntaxError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.SyntaxError.__class__ = new batavia.types.Type('SyntaxError', [batavia.builtins.Exception]);
batavia.builtins.SyntaxError.prototype.__class__ = batavia.builtins.SyntaxError.__class__;

batavia.builtins.SyntaxWarning = undefined;

function SystemError(msg) {
    batavia.builtins.Exception.call(this, 'SystemError', msg);
}
batavia.builtins.SystemError = SystemError;
batavia.builtins.SystemError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.SystemError.__class__ = new batavia.types.Type('SystemError', [batavia.builtins.Exception]);
batavia.builtins.SystemError.prototype.__class__ = batavia.builtins.SystemError.__class__;

function TabError(msg) {
    batavia.builtins.Exception.call(this, 'TabError', msg);
}
batavia.builtins.TabError = TabError;
batavia.builtins.TabError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.TabError.__class__ = new batavia.types.Type('TabError', [batavia.builtins.Exception]);
batavia.builtins.TabError.prototype.__class__ = batavia.builtins.TabError.__class__;

function TypeError(msg) {
    batavia.builtins.Exception.call(this, 'TypeError', msg);
}
batavia.builtins.TypeError = TypeError;
batavia.builtins.TypeError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.TypeError.__class__ = new batavia.types.Type('TypeError', [batavia.builtins.Exception]);
batavia.builtins.TypeError.prototype.__class__ = batavia.builtins.TypeError.__class__;

function UnboundLocalError(msg) {
    batavia.builtins.Exception.call(this, 'UnboundLocalError', msg);
}
batavia.builtins.UnboundLocalError = UnboundLocalError;
batavia.builtins.UnboundLocalError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.UnboundLocalError.__class__ = new batavia.types.Type('UnboundLocalError', [batavia.builtins.Exception]);
batavia.builtins.UnboundLocalError.prototype.__class__ = batavia.builtins.UnboundLocalError.__class__;

function UnicodeDecodeError(msg) {
    batavia.builtins.Exception.call(this, 'UnicodeDecodeError', msg);
}
batavia.builtins.UnicodeDecodeError = UnicodeDecodeError;
batavia.builtins.UnicodeDecodeError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.UnicodeDecodeError.__class__ = new batavia.types.Type('UnicodeDecodeError', [batavia.builtins.Exception]);
batavia.builtins.UnicodeDecodeError.prototype.__class__ = batavia.builtins.UnicodeDecodeError.__class__;

function UnicodeEncodeError(msg) {
    batavia.builtins.Exception.call(this, 'UnicodeEncodeError', msg);
}
batavia.builtins.UnicodeEncodeError = UnicodeEncodeError;
batavia.builtins.UnicodeEncodeError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.UnicodeEncodeError.__class__ = new batavia.types.Type('UnicodeEncodeError', [batavia.builtins.Exception]);
batavia.builtins.UnicodeEncodeError.prototype.__class__ = batavia.builtins.UnicodeEncodeError.__class__;

function UnicodeError(msg) {
    batavia.builtins.Exception.call(this, 'UnicodeError', msg);
}
batavia.builtins.UnicodeError = UnicodeError;
batavia.builtins.UnicodeError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.UnicodeError.__class__ = new batavia.types.Type('UnicodeError', [batavia.builtins.Exception]);
batavia.builtins.UnicodeError.prototype.__class__ = batavia.builtins.UnicodeError.__class__;

function UnicodeTranslateError(msg) {
    batavia.builtins.Exception.call(this, 'UnicodeTranslateError', msg);
}
batavia.builtins.UnicodeTranslateError = UnicodeTranslateError;
batavia.builtins.UnicodeTranslateError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.UnicodeTranslateError.__class__ = new batavia.types.Type('UnicodeTranslateError', [batavia.builtins.Exception]);
batavia.builtins.UnicodeTranslateError.prototype.__class__ = batavia.builtins.UnicodeTranslateError.__class__;

batavia.builtins.UnicodeWarning = undefined;

batavia.builtins.UserWarning = undefined;

function ValueError(msg) {
    batavia.builtins.Exception.call(this, 'ValueError', msg);
}
batavia.builtins.ValueError = ValueError;
batavia.builtins.ValueError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.ValueError.__class__ = new batavia.types.Type('ValueError', [batavia.builtins.Exception]);
batavia.builtins.ValueError.prototype.__class__ = batavia.builtins.ValueError.__class__;

batavia.builtins.Warning = undefined;

function ZeroDivisionError(msg) {
    batavia.builtins.Exception.call(this, 'ZeroDivisionError', msg);
}
batavia.builtins.ZeroDivisionError = ZeroDivisionError;
batavia.builtins.ZeroDivisionError.prototype = Object.create(batavia.builtins.Exception.prototype);
batavia.builtins.ZeroDivisionError.__class__ = new batavia.types.Type('ZeroDivisionError', [batavia.builtins.Exception]);
batavia.builtins.ZeroDivisionError.prototype.__class__ = batavia.builtins.ZeroDivisionError.__class__;

batavia.core.Frame = function(kwargs) {
    var v, i;

    this.f_code = kwargs.f_code;
    this.f_globals = kwargs.f_globals;
    this.f_locals = kwargs.f_locals;
    this.f_back = kwargs.f_back;
    this.stack = [];

    if (this.f_back) {
        this.f_builtins = this.f_back.f_builtins;
    } else {
        this.f_builtins = this.f_globals['__builtins__'];
        if (this.f_builtins.hasOwnProperty('__dict__')) {
            this.f_builtins = this.f_builtins.__dict__;
        }
    }

    this.f_lineno = this.f_code.co_firstlineno;
    this.f_lasti = 0;

    if (this.f_code.co_cellvars.length > 0) {
        this.cells = {};
        if (this.f_back && !this.f_back.cells) {
            this.f_back.cells = {};
        }
        for (i = 0; i < this.f_code.co_cellvars.length; i++) {
            // Make a cell for the variable in our locals, or null.
            v = this.f_code.co_cellvars[i];
            this.cells[v] = new batavia.core.Cell(this.f_locals[v]);
            if (this.f_back) {
                this.f_back.cells[v] = this.cells[v];
            }
        }
    } else {
        this.cells = null;
    }

    if (this.f_code.co_freevars.length > 0) {
        if (!this.cells) {
            this.cells = {};
        }
        for (i = 0; i < this.f_code.co_freevars.length; i++) {
            v = this.f_code.co_freevars[i];
            assert(this.cells !== null);
            assert(this.f_back.cells, "f_back.cells: " + this.f_back.cells);
            this.cells[v] = this.f_back.cells[v];
        }
    }
    this.block_stack = [];
    this.generator = null;

};

batavia.core.Frame.prototype.__repr__ = function() {
    return '<Frame at 0x' + id(self) + ': ' + this.f_code.co_filename +' @ ' + this.f_lineno + '>';
};

batavia.core.Frame.prototype.line_number = function() {
    // Get the current line number the frame is executing.
    // We don't keep f_lineno up to date, so calculate it based on the
    // instruction address and the line number table.
    var lnotab = this.f_code.co_lnotab;
    var byte_increments = []; //six.iterbytes(lnotab[0::2]);
    var line_increments = []; //six.iterbytes(lnotab[1::2]);

    byte_num = 0;
    line_num = this.f_code.co_firstlineno;

    for (var incr in byte_increments) {
        var byte_incr = byte_increments[incr];
        var line_incr = line_increments[incr];

        byte_num += byte_incr;
        if (byte_num > this.f_lasti) {
            break;
        }
        line_num += line_incr;
    }

    return line_num;
};
batavia.core.Generator = Generator

function Generator(frame, vm) {
    this.vm = vm;
    this.gi_frame = frame;
    this.started = false;
    this.finished = false;
};

Generator.prototype = Object.create(Object.prototype);
Generator.prototype.__class__ = new batavia.types.Type('generator');

Generator.prototype.__iter__ = function() {
    return this;
}

Generator.prototype.__next__ = function() {
    return this.send(null)
}

Generator.prototype.send = function(value) {
    if (typeof value === 'undefined') {
        value = null;
    }
    if (!this.started) {
        if (value !== null) {
          // It's illegal to send a non-None value on first call.
          // TODO: raise a proper TypeError
          throw 'lolnope'
        }
        this.started = true
    }
    this.gi_frame.stack.push(value);
    var yieldval = this.vm.run_frame(this.gi_frame)
    if (this.finished) {
      throw new batavia.builtins.StopIteration();
    }
    return yieldval;
}

Generator.prototype['throw'] = function(type, value, traceback) {
    this.vm.last_exception = {
      'exc_type': type,
      'value': value !== null ? value : new type(),
      'traceback': traceback
    }
    var yieldval = this.vm.run_frame(this.gi_frame)
    if (this.finished) {
      throw new batavia.builtins.StopIteration();
    }
    return yieldval;
}

Generator.prototype['close'] = function() {
    return this['throw'](new batavia.builtins.StopIteration());
}

/*************************************************************************
 * A C-FILE like object
 *************************************************************************/

batavia.core.PYCFile = function(data) {
    this.magic = data.slice(0, 4);
    this.modtime = data.slice(4, 8);
    this.size = data.slice(8, 12);
    this.data = data.slice(12);

    batavia.BATAVIA_MAGIC = this.magic;

    // this.data = data;
    this.depth = 0;
    this.ptr = 0;
    this.end = this.data.length;
    this.refs = [];
};

batavia.core.PYCFile.EOF = '\x04';

batavia.core.PYCFile.prototype.getc = function() {
    if (this.ptr < this.end) {
        return this.data[this.ptr++].charCodeAt();
    }
    return batavia.core.PYCFile.EOF;
};

batavia.core.PYCFile.prototype.fread = function(n) {
    if (this.ptr + n <= this.end) {
        var retval = this.data.slice(this.ptr, this.ptr + n);
        this.ptr += n;
        return retval;
    }
    return batavia.core.PYCFile.EOF;
};

/*************************************************************************
 * Virtual Machine
 *************************************************************************/

batavia.VirtualMachine = function(loader) {
    // Initialize the bytecode module
    batavia.modules.dis.init();

    if (loader === undefined) {
        this.loader = function(name) {
            return document.getElementById('batavia-' + name).text.replace(/(\r\n|\n|\r)/gm, "").trim();
        };
    } else {
        this.loader = loader;
    }

    // Build a table mapping opcodes to method calls
    this.build_dispatch_table();

    // The call stack of frames.
    this.frames = [];

    // The current frame.
    this.frame = null;
    this.return_value = null;
    this.last_exception = null;
    this.is_vm = true;
};


/*
 * Build a table mapping opcodes to a method to be called whenever we encounter that opcode.
 *
 * Each such method will be invoked with apply(this, args).
 */
batavia.VirtualMachine.prototype.build_dispatch_table = function() {
    var vm = this;
    this.dispatch_table = batavia.modules.dis.opname.map(function(opname, opcode) {
        var operator_name, operator;

        if (opcode == batavia.modules.dis.NOP) {
            return function() {};
        } else if (opcode in batavia.modules.dis.unary_ops) {
            operator_name = opname.slice(6);
            switch (operator_name) {
                case "POSITIVE":
                    return function() {
                        var x = this.pop();
                        if (x === null) {
                            this.push(batavia.types.NoneType.__pos__());
                        } else if (x.__pos__) {
                            this.push(x.__pos__());
                        } else {
                            this.push(+x);
                        }
                    };
                case "NEGATIVE":
                    return function() {
                        var x = this.pop();
                        if (x === null) {
                            this.push(batavia.types.NoneType.__neg__());
                        } else if (x.__neg__) {
                            this.push(x.__neg__());
                        } else {
                            this.push(-x);
                        }
                    };
                case "NOT":
                    return function() {
                        var x = this.pop();
                        if (x === null) {
                            this.push(batavia.types.NoneType.__not__());
                        } else if (x.__not__) {
                            this.push(x.__not__());
                        } else {
                            this.push(-x);
                        }
                    };
                case "INVERT":
                    return function() {
                        var x = this.pop();
                        if (x === null) {
                            this.push(batavia.types.NoneType.__invert__());
                        } else if (x.__invert__) {
                            this.push(x.__invert__());
                        } else {
                            this.push(~x);
                        }
                    };
                default:
                    throw new batavia.builtins.BataviaError("Unknown unary operator " + operator_name);
            }
        } else if (opcode in batavia.modules.dis.binary_ops) {
            operator_name = opname.slice(7);
            switch (operator_name) {
                case 'POWER':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__pow__(items[1]));
                        } else if (items[0].__pow__) {
                            this.push(items[0].__pow__(items[1]));
                        } else {
                            this.push(Math.pow(items[0], items[1]));
                        }
                    };
                case 'MULTIPLY':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__mul__(items[1]));
                        } else if (items[0].__mul__) {
                            this.push(items[0].__mul__(items[1]));
                        } else {
                            this.push(items[0] * items[1]);
                        }
                    };
                case 'MODULO':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__mod__(items[1]));
                        } else if (items[0].__mod__) {
                            this.push(items[0].__mod__(items[1]));
                        } else {
                            this.push(items[0] % items[1]);
                        }
                    };
                case 'ADD':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__add__(items[1]));
                        } else if (items[0].__add__) {
                            this.push(items[0].__add__(items[1]));
                        } else {
                            this.push(items[0] + items[1]);
                        }
                    };
                case 'SUBTRACT':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__sub__(items[1]));
                        } else if (items[0].__sub__) {
                            this.push(items[0].__sub__(items[1]));
                        } else {
                            this.push(items[0] - items[1]);
                        }
                    };
                case 'SUBSCR':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__getitem__(items[1]));
                        } else if (items[0].__getitem__) {
                            this.push(items[0].__getitem__(items[1]));
                        } else {
                            this.push(items[0][items[1]]);
                        }
                    };
                case 'FLOOR_DIVIDE':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__floordiv__(items[1]));
                        } else if (items[0].__floordiv__) {
                            this.push(items[0].__floordiv__(items[1]));
                        } else {
                            this.push(items[0] / items[1]);
                        }
                    };
                case 'TRUE_DIVIDE':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__truediv__(items[1]));
                        } else if (items[0].__truediv__) {
                            this.push(items[0].__truediv__(items[1]));
                        } else {
                            this.push(items[0] / items[1]);
                        }
                    };
                case 'LSHIFT':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__lshift__(items[1]));
                        } else if (items[0].__lshift__) {
                            this.push(items[0].__lshift__(items[1]));
                        } else {
                            this.push(items[0] << items[1]);
                        }
                    };
                case 'RSHIFT':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__rshift__(items[1]));
                        } else if (items[0].__rshift__) {
                            this.push(items[0].__rshift__(items[1]));
                        } else {
                            this.push(items[0] >> items[1]);
                        }
                    };
                case 'AND':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__and__(items[1]));
                        } else if (items[0].__and__) {
                            this.push(items[0].__and__(items[1]));
                        } else {
                            this.push(items[0] & items[1]);
                        }
                    };
                case 'XOR':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__xor__(items[1]));
                        } else if (items[0].__xor__) {
                            this.push(items[0].__xor__(items[1]));
                        } else {
                            this.push(items[0] ^ items[1]);
                        }
                    };
                case 'OR':
                    return function() {
                        var items = this.popn(2);
                        if (items[0] === null) {
                            this.push(batavia.types.NoneType.__or__(items[1]));
                        } else if (items[0].__or__) {
                            this.push(items[0].__or__(items[1]));
                        } else {
                            this.push(items[0] | items[1]);
                        }
                    };
                default:
                    throw new batavia.builtins.BataviaError("Unknown binary operator " + operator_name);
            }
        } else if (opcode in batavia.modules.dis.inplace_ops) {
            operator_name = opname.slice(8);
            switch (operator_name) {
                case 'FLOOR_DIVIDE':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__ifloordiv__(items[1]);
                        } else if (items[0].__ifloordiv__) {
                            result = items[0].__ifloordiv__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] /= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'TRUE_DIVIDE':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__itruediv__(items[1]);
                        } else if (items[0].__itruediv__) {
                            result = items[0].__itruediv__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] /= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'ADD':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__iadd__(items[1]);
                        } else if (items[0].__iadd__) {
                            result = items[0].__iadd__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] += items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'SUBTRACT':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__isub__(items[1]);
                        } else if (items[0].__isub__) {
                            result = items[0].__isub__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] -= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'MULTIPLY':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__imul__(items[1]);
                        } else if (items[0].__imul__) {
                            result = items[0].__imul__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] *= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'MODULO':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__imod__(items[1]);
                        } else if (items[0].__imod__) {
                            result = items[0].__imod__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] %= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'POWER':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__ipow__(items[1]);
                        } else if (items[0].__ipow__) {
                            result = items[0].__ipow__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] = Math.pow(items[0], items[1]);
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'LSHIFT':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__ilshift__(items[1]);
                        } else if (items[0].__ilshift__) {
                            result = items[0].__ilshift__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] <<= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'RSHIFT':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__irshift__(items[1]);
                        } else if (items[0].__irshift__) {
                            result = items[0].__irshift__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] >>= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'AND':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__iand__(items[1]);
                        } else if (items[0].__iand__) {
                            result = items[0].__iand__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] &= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'XOR':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__ixor__(items[1]);
                        } else if (items[0].__ixor__) {
                            result = items[0].__ixor__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] ^= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                case 'OR':
                    return function() {
                        var items = this.popn(2);
                        var result;
                        if (items[0] === null) {
                            result = batavia.types.NoneType.__ior__(items[1]);
                        } else if (items[0].__ior__) {
                            result = items[0].__ior__(items[1]);
                            if (result === null) {
                                result = items[0];
                            }
                        } else {
                            items[0] |= items[1];
                            result = items[0];
                        }
                        this.push(result);
                    };
                default:
                    throw new batavia.builtins.BataviaError("Unknown inplace operator " + operator_name);
            }
        } else {
            // dispatch
            var bytecode_fn = vm['byte_' + opname];
            if (bytecode_fn) {
                return bytecode_fn;
            } else {
                return function() {
                    throw new batavia.builtins.BataviaError("Unknown opcode " + opcode + " (" + opname + ")");
                };
            }
        }
    });
};

/*
 * The main entry point.
 *
 * Accepts a DOM id for an element containing base64 encoded bytecode.
 */
batavia.VirtualMachine.prototype.run = function(tag, args) {
    try {
        var payload = this.loader(tag);
        var code = batavia.modules.marshal.load_pyc(this, payload);

        // Set up sys.argv
        batavia.modules.sys.argv = new batavia.types.List(['batavia']);
        if (args) {
            batavia.modules.sys.argv.extend(args);
        }

        // Run the code
        return this.run_code({'code': code});

    } catch (e) {
        if (e instanceof batavia.builtins.BataviaError) {
            console.log(e.msg);
        } else {
            throw e;
        }
    }
};

/*
 * An entry point for invoking functions.
 *
 * Accepts a DOM id for an element containing base64 encoded bytecode.
 */
batavia.VirtualMachine.prototype.run_method = function(tag, args, kwargs, f_locals, f_globals) {
    try {
        var payload = this.loader(tag);
        var code = batavia.modules.marshal.load_pyc(this, payload);

        var callargs = new batavia.types.JSDict();
        for (var i = 0, l = args.length; i < l; i++) {
            callargs[code.co_varnames[i]] = args[i];
        }
        callargs.update(kwargs);

        // Run the code
        return this.run_code({
            'code': code,
            'callargs': callargs,
            'f_locals': f_locals,
            'f_globals': f_globals
        });

    } catch (e) {
        if (e instanceof batavia.builtins.BataviaError) {
            console.log(e.msg);
        } else {
            throw e;
        }
    }
};

/*
 */
batavia.VirtualMachine.prototype.PyErr_Occurred = function() {
    return this.last_exception !== null;
};

batavia.VirtualMachine.prototype.PyErr_SetString = function(exc, message) {
    var exception = new exc(message);
    this.last_exception = {
        'exc_type': exception.__class__,
        'value': exception,
        'traceback': this.create_traceback()
    };
};

/*
 * Return the value at the top of the stack, with no changes.
 */
batavia.VirtualMachine.prototype.top = function() {
    return this.frame.stack[this.frame.stack.length - 1];
};

/*
 * Pop a value from the stack.
 *
 * Default to the top of the stack, but `i` can be a count from the top
 * instead.
 */
batavia.VirtualMachine.prototype.pop = function(i) {
    if (i === undefined) {
        i = 0;
    }
    return this.frame.stack.splice(this.frame.stack.length - 1 - i, 1)[0];
};

/*
 * Push value onto the value stack.
 */
batavia.VirtualMachine.prototype.push = function(val) {
    this.frame.stack.push(val);
};

/*
 * Pop a number of values from the value stack.
 *
 * A list of `n` values is returned, the deepest value first.
*/
batavia.VirtualMachine.prototype.popn = function(n) {
    if (n) {
        return this.frame.stack.splice(this.frame.stack.length - n, n);
    } else {
        return [];
    }
};

/*
 * Get a value `n` entries down in the stack, without changing the stack.
 */
batavia.VirtualMachine.prototype.peek = function(n) {
    return this.frame.stack[this.frame.stack.length - n];
};

/*
 * Move the bytecode pointer to `jump`, so it will execute next.
 */
batavia.VirtualMachine.prototype.jump = function(jump) {
    this.frame.f_lasti = jump;
};

batavia.VirtualMachine.prototype.push_block = function(type, handler, level) {
    if (level === null) {
        level = this.frame.stack.length;
    }
    this.frame.block_stack.push(new batavia.core.Block(type, handler, level));
};

batavia.VirtualMachine.prototype.pop_block = function() {
    return this.frame.block_stack.pop();
};

batavia.VirtualMachine.prototype.make_frame = function(kwargs) {
    var code = kwargs.code;
    var callargs = kwargs.callargs || {};
    var f_globals = kwargs.f_globals || null;
    var f_locals = kwargs.f_locals || null;

    if (!code.co_unpacked_code) {
        this.unpack_code(code);
    }

    // console.log("make_frame: code=" + code + ", callargs=" + callargs);

    if (f_globals !== null) {
        if (f_locals === null) {
            f_locals = f_globals;
        }
    } else if (this.frames.length > 0) {
        f_globals = this.frame.f_globals;
        f_locals = new batavia.types.JSDict();
    } else {
        f_globals = f_locals = new batavia.types.JSDict({
            '__builtins__': batavia.builtins,
            '__name__': '__main__',
            '__doc__': null,
            '__package__': null,
        });
    }
    f_locals.update(callargs);

    frame = new batavia.core.Frame({
        'f_code': code,
        'f_globals': f_globals,
        'f_locals': f_locals,
        'f_back': this.frame
    });
    return frame;
};

batavia.VirtualMachine.prototype.push_frame = function(frame) {
    this.frames.push(frame);
    this.frame = frame;
};

batavia.VirtualMachine.prototype.pop_frame = function() {
    this.frames.pop();
    if (this.frames) {
        this.frame = this.frames[this.frames.length - 1];
    } else {
        this.frame = null;
    }
};

batavia.VirtualMachine.prototype.create_traceback = function() {
    var tb = [];
    var frame;

    for (var f in this.frames) {
        frame = this.frames[f];

        // Work out the current source line by taking the
        // f_lineno (the line for the start of the method)
        // and adding the line offsets from the line
        // number table.
        var lnotab = frame.f_code.co_lnotab.val;
        var byte_num = 0;
        var line_num = frame.f_code.co_firstlineno;

        var byte_incr, line_incr;
        for (var idx = 1; idx < lnotab.length, byte_num < frame.f_lasti; idx += 2) {
            byte_num += lnotab[idx-1]
            if (byte_num < frame.f_lasti) {
                line_num += lnotab[idx];
            }
        }

        tb.push({
            'module': frame.f_code.co_name,
            'filename': frame.f_code.co_filename,
            'line': line_num
        });
    }
    return tb;
};

/*
 * Annotate a Code object with a co_unpacked_code property, consisting of the bytecode
 * unpacked into operations with their respective args
 */
batavia.VirtualMachine.prototype.unpack_code = function(code) {
    var pos = 0;
    var unpacked_code = [];
    var args;
    var extra = 0;

    while (pos < code.co_code.val.length) {
        var opcode_start_pos = pos;

        var opcode = code.co_code.val[pos++];

        // next opcode has 4-byte argument effectively.
        if (opcode == batavia.modules.dis.EXTENDED_ARG) {
            var lo = code.co_code.val[pos++];
            var hi = code.co_code.val[pos++];
            extra = (lo << 16) | (hi << 24);
            // emulate four NOPs
            unpacked_code[opcode_start_pos] = {
                'opoffset': opcode_start_pos,
                'opcode': batavia.modules.dis.NOP,
                'op_method': this.dispatch_table[batavia.modules.dis.NOP],
                'args': [],
                'next_pos': pos
            };
            unpacked_code[opcode_start_pos + 1] = {
                'opoffset': opcode_start_pos + 1,
                'opcode': batavia.modules.dis.NOP,
                'op_method': this.dispatch_table[batavia.modules.dis.NOP],
                'args': [],
                'next_pos': pos
            };
            unpacked_code[opcode_start_pos + 2] = {
                'opoffset': opcode_start_pos + 2,
                'opcode': batavia.modules.dis.NOP,
                'op_method': this.dispatch_table[batavia.modules.dis.NOP],
                'args': [],
                'next_pos': pos
            };
            unpacked_code[opcode_start_pos + 3] = {
                'opoffset': opcode_start_pos + 3,
                'opcode': batavia.modules.dis.NOP,
                'op_method': this.dispatch_table[batavia.modules.dis.NOP],
                'args': [],
                'next_pos': pos
            };
            continue;
        }

        if (opcode < batavia.modules.dis.HAVE_ARGUMENT) {
            args = [];
        } else {
            var lo = code.co_code.val[pos++];
            var hi = code.co_code.val[pos++];
            var intArg = lo | (hi << 8) | extra;
            extra = 0; // use extended arg if present

            if (opcode in batavia.modules.dis.hasconst) {
                args = [code.co_consts[intArg]];
            } else if (opcode in batavia.modules.dis.hasfree) {
                if (intArg < code.co_cellvars.length) {
                    args = [code.co_cellvars[intArg]];
                } else {
                    var_idx = intArg - code.co_cellvars.length;
                    args = [code.co_freevars[var_idx]];
                }
            } else if (opcode in batavia.modules.dis.hasname) {
                args = [code.co_names[intArg]];
            } else if (opcode in batavia.modules.dis.hasjrel) {
                args = [pos + intArg];
            } else if (opcode in batavia.modules.dis.hasjabs) {
                args = [intArg];
            } else if (opcode in batavia.modules.dis.haslocal) {
                args = [code.co_varnames[intArg]];
            } else {
                args = [intArg];
            }
        }

        unpacked_code[opcode_start_pos] = {
            'opoffset': opcode_start_pos,
            'opcode': opcode,
            'op_method': this.dispatch_table[opcode],
            'args': args,
            'next_pos': pos
        };
    }

    code.co_unpacked_code = unpacked_code;
};

batavia.VirtualMachine.prototype.run_code = function(kwargs) {
    var code = kwargs.code;
    var f_globals = kwargs.f_globals || null;
    var f_locals = kwargs.f_locals || null;
    var callargs = kwargs.callargs || null;
    var frame = this.make_frame({
        'code': code,
        'f_globals': f_globals,
        'f_locals': f_locals,
        'callargs': callargs
    });
    try {
        var val = this.run_frame(frame);

        // Check some invariants
        if (this.frames.length > 0) {
            throw new batavia.builtins.BataviaError("Frames left over!");
        }
        if (this.frame && this.frame.stack.length > 0) {
            throw new batavia.builtins.BataviaError("Data left on stack! " + this.frame.stack);
        }
        return val;
    } catch (e) {
        if (this.last_exception) {
            trace = ['Traceback (most recent call last):'];
            var frame;
            for (var t in this.last_exception.traceback) {
                frame = this.last_exception.traceback[t];
                trace.push('  File "' + frame.filename + '", line ' + frame.line + ', in ' + frame.module);
            }
            trace.push(this.last_exception.value.name + ': ' + this.last_exception.value.toString());
            console.log(trace.join('\n'));
            this.last_exception = null;
        } else {
            throw e;
        }
    }
};

batavia.VirtualMachine.prototype.unwind_block = function(block) {
    if (block.type === 'except-handler') {
        offset = 3;
    } else {
        offset = 0;
    }

    while (this.frame.stack.length > block.level + offset) {
        this.pop();
    }

    if (block.type === 'except-handler') {
        exc = this.popn(3);
        // we don't need to set the last_exception, as it was handled
    }
};

/*
 * Log arguments, block stack, and data stack for each opcode.
 */
batavia.VirtualMachine.prototype.log = function(opcode) {
    var op = opcode.opoffset + ': ' + opcode.byteName;
    for (var arg in opcode.args) {
        op += ' ' + opcode.args[arg];
    }
    var indent = "    " * (this.frames.length - 1);

    console.log("  " + indent + "data: " + this.frame.stack);
    console.log("  " + indent + "blks: " + this.frame.block_stack);
    console.log(indent + op);
};

/*
 * Manage a frame's block stack.
 * Manipulate the block stack and data stack for looping,
 * exception handling, or returning.
 */
batavia.VirtualMachine.prototype.manage_block_stack = function(why) {
    assert(why !== 'yield');

    var block = this.frame.block_stack[this.frame.block_stack.length - 1];
    if (block.type === 'loop' && why === 'continue') {
        this.jump(this.return_value);
        why = null;
        return why;
    }

    this.pop_block();
    this.unwind_block(block);

    if (block.type === 'loop' && why === 'break') {
        why = null;
        this.jump(block.handler);
        return why;
    }

    if (why === 'exception' &&
            (block.type === 'setup-except' || block.type === 'finally')) {
        this.push_block('except-handler');
        var exc = this.last_exception;
        // clear the last_exception so that we know it is handled
        this.last_exception = null;
        this.push(exc.traceback);
        this.push(exc.value);
        this.push(exc.exc_type);
        // PyErr_Normalize_Exception goes here
        this.push(exc.traceback);
        this.push(exc.value);
        this.push(exc.exc_type);
        why = null;
        this.jump(block.handler);
        return why;
    } else if (block.type === 'finally') {
        if (why === 'return' || why === 'continue') {
            this.push(this.return_value);
        }
        this.push(why);

        why = null;
        this.jump(block.handler);
        return why;
    }

    return why;
};

/*
 * Run a frame until it returns (somehow).
 *
 * Exceptions are raised, the return value is returned.
 * If the frame was halted partway through execution
 * (e.g. by yielding from a generator) then it will resume
 * from whereever it left off.
 *
 */
batavia.VirtualMachine.prototype.run_frame = function(frame) {
    var why, operation;

    this.push_frame(frame);

    // If there's an unhandled exception then resume
    // execution by handling it.

    if (this.last_exception) {
        why = 'exception'
        while (why && frame.block_stack.length > 0) {
            why = this.manage_block_stack(why);
        }
    }

    while (!why) {
        operation = this.frame.f_code.co_unpacked_code[this.frame.f_lasti];
        var opname = batavia.modules.dis.opname[operation.opcode];

        // advance f_lasti to next operation. If the operation is a jump, then this
        // pointer will be overwritten during the operation's execution.
        this.frame.f_lasti = operation.next_pos;

        // this.log(operation);

        // When unwinding the block stack, we need to keep track of why we
        // are doing it.
        try {
            why = operation.op_method.apply(this, operation.args);
        } catch (err) {
            // deal with exceptions encountered while executing the op.
            if (err instanceof batavia.builtins.BataviaError) {
                // Batavia errors are a major problem; ABORT HARD
                this.last_exception = null;
                throw err;
            } else if (this.last_exception == null) {
              this.last_exception = {
                  'exc_type': err.__class__,
                  'value': err,
                  'traceback': this.create_traceback()
              };
            }
            why = 'exception';
        }

        if (why === 'exception')  {
            // TODO: ceval calls PyTraceBack_Here, not sure what that does.
        }

        if (why === 'reraise') {
            why = 'exception';
        }

        if (why !== 'yield') {
            while (why && frame.block_stack.length > 0) {
                // Deal with any block management we need to do.
                why = this.manage_block_stack(why);
            }
        }
    }

    // TODO: handle generator exception state

    this.pop_frame();

    if (why === 'exception') {
        throw this.last_exception.value;
    }

    return this.return_value;
};

batavia.VirtualMachine.prototype.byte_LOAD_CONST = function(c) {
    this.push(c);
};

batavia.VirtualMachine.prototype.byte_POP_TOP = function() {
    this.pop();
};

batavia.VirtualMachine.prototype.byte_DUP_TOP = function() {
    this.push(this.top());
};

batavia.VirtualMachine.prototype.byte_DUP_TOPX = function(count) {
    var items = this.popn(count);
    for (var n = 0; n < 2; n++) {
        for (var i = 0; i < count; i++) {
            this.push(items[i]);
        }
    }
};

batavia.VirtualMachine.prototype.byte_DUP_TOP_TWO = function() {
    var items = this.popn(2);
    this.push(items[0]);
    this.push(items[1]);
    this.push(items[0]);
    this.push(items[1]);
};

batavia.VirtualMachine.prototype.byte_ROT_TWO = function() {
    var items = this.popn(2);
    this.push(items[1]);
    this.push(items[0]);
};

batavia.VirtualMachine.prototype.byte_ROT_THREE = function() {
    var items = this.popn(3);
    this.push(items[2]);
    this.push(items[0]);
    this.push(items[1]);
};

batavia.VirtualMachine.prototype.byte_ROT_FOUR = function() {
    var items = this.popn(4);
    this.push(items[3]);
    this.push(items[0]);
    this.push(items[1]);
    this.push(items[2]);
};

batavia.VirtualMachine.prototype.byte_LOAD_NAME = function(name) {
    var frame = this.frame;
    var val;
    if (name in frame.f_locals) {
        val = frame.f_locals[name];
    } else if (name in frame.f_globals) {
        val = frame.f_globals[name];
    } else if (name in frame.f_builtins) {
        val = frame.f_builtins[name];
    } else {
        throw new batavia.builtins.NameError("name '" + name + "' is not defined");
    }
    this.push(val);
};

batavia.VirtualMachine.prototype.byte_STORE_NAME = function(name) {
    this.frame.f_locals[name] = this.pop();
};

batavia.VirtualMachine.prototype.byte_DELETE_NAME = function(name) {
    delete this.frame.f_locals[name];
};

batavia.VirtualMachine.prototype.byte_LOAD_FAST = function(name) {
    var val;
    if (name in this.frame.f_locals) {
        val = this.frame.f_locals[name];
    } else {
        throw new batavia.builtins.UnboundLocalError("local variable '" + name + "' referenced before assignment");
    }
    this.push(val);
};

batavia.VirtualMachine.prototype.byte_STORE_FAST = function(name) {
    this.frame.f_locals[name] = this.pop();
};

batavia.VirtualMachine.prototype.byte_DELETE_FAST = function(name) {
    delete this.frame.f_locals[name];
};

batavia.VirtualMachine.prototype.byte_STORE_GLOBAL = function(name) {
    this.frame.f_globals[name] = this.pop();
};

batavia.VirtualMachine.prototype.byte_LOAD_GLOBAL = function(name) {
    var val;
    if (name in this.frame.f_globals) {
        val = this.frame.f_globals[name];
    } else if (name in this.frame.f_builtins) {
        val = this.frame.f_builtins[name];
    } else {
        throw new batavia.builtins.NameError("name '" + name + "' is not defined");
    }
    this.push(val);
};

batavia.VirtualMachine.prototype.byte_LOAD_DEREF = function(name) {
    this.push(this.frame.cells[name].get());
};

batavia.VirtualMachine.prototype.byte_STORE_DEREF = function(name) {
    this.frame.cells[name].set(this.pop());
};

batavia.VirtualMachine.prototype.byte_LOAD_LOCALS = function() {
    this.push(this.frame.f_locals);
};

// batavia.VirtualMachine.prototype.sliceOperator = function(op) {
//     start = 0;
//     end = null;          // we will take this to mean end
//     // op, count = op[:-2], int(op[-1]);
//     if count == 1:
//         start = this.pop()
//     elif count == 2:
//         end = this.pop()
//     elif count == 3:
//         end = this.pop()
//         start = this.pop()
//     l = this.pop()
//     if end is null:
//         end = len(l)
//     if op.startswith('STORE_'):
//         l[start:end] = this.pop()
//     elif op.startswith('DELETE_'):
//         del l[start:end]
//     else:
//         this.push(l[start:end])
// };

batavia.VirtualMachine.prototype.byte_COMPARE_OP = function(opnum) {
    var items = this.popn(2);
    var result;

    // "in" and "not in" operators (opnum 6 and 7) have reversed
    // operand order, so they're handled separately.
    // If the first operand is None, then we need to invoke
    // the comparison method in a different way, because we can't
    // bind the operator methods to the null instance.

    if (opnum === 6) {  // x in None
        if (items[1] === null) {
            result = batavia.types.NoneType.__contains__(items[0]);
        } if (items[1].__contains__) {
            result = items[1].__contains__(items[0]);
        } else {
            result = (items[0] in items[1]);
        }
    } else if (opnum === 7) {
        if (items[1] === null) {  // x not in None
            result = batavia.types.NoneType.__contains__(items[0]).__not__();
        } else if (items[1].__contains__) {
            result = items[1].__contains__(items[0]).__not__();
        } else {
            result = !(items[0] in items[1]);
        }
    } else if (items[0] === null) {
        switch(opnum) {
            case 0:  // <
                result = batavia.types.NoneType.__lt__(items[1]);
                break;
            case 1:  // <=
                result = batavia.types.NoneType.__le__(items[1]);
                break;
            case 2:  // ==
                result = batavia.types.NoneType.__eq__(items[1]);
                break;
            case 3:  // !=
                result = batavia.types.NoneType.__ne__(items[1]);
                break;
            case 4:  // >
                result = batavia.types.NoneType.__gt__(items[1]);
                break;
            case 5:  // >=
                result = batavia.types.NoneType.__ge__(items[1]);
                break;
            case 8:  // is
                result = items[1] === null;
                break;
            case 9:  // is not
                result = items[1] !== null;
                break;
            case 10:  // exception
                result = items[1] === null;
                break;
            default:
                throw new batavia.builtins.BataviaError('Unknown operator ' + opnum);
        }
    } else {
        switch(opnum) {
            case 0:  // <
                if (items[0].__lt__) {
                    result = items[0].__lt__(items[1]);
                } else {
                    result = items[0] < items[1];
                }
                break;
            case 1:  // <=
                if (items[0].__le__) {
                    result = items[0].__le__(items[1]);
                } else {
                    result = items[0] <= items[1];
                }
                break;
            case 2:  // ==
                if (items[0].__eq__) {
                    result = items[0].__eq__(items[1]);
                } else {
                    result = items[0] == items[1];
                }
                break;
            case 3:  // !=
                if (items[0].__ne__) {
                    result = items[0].__ne__(items[1]);
                } else {
                    result = items[0] != items[1];
                }
                break;
            case 4:  // >
                if (items[0].__gt__) {
                    result = items[0].__gt__(items[1]);
                } else {
                    result = items[0] > items[1];
                }
                break;
            case 5:  // >=
                if (items[0].__ge__) {
                    result = items[0].__ge__(items[1]);
                } else {
                    result = items[0] >= items[1];
                }
                break;
            case 8:  // is
                result = items[0] === items[1];
                break;
            case 9:  // is not
                result = items[0] !== items[1];
                break;
            case 10:  // exception match
                result = batavia.issubclass(items[0], items[1]);
                break;
            default:
                throw new batavia.builtins.BataviaError('Unknown operator ' + opnum);
        }
    }

    this.push(result);
};

batavia.VirtualMachine.prototype.byte_LOAD_ATTR = function(attr) {
    var obj = this.pop();
    if (obj.__getattr__ === undefined) {
        val = obj[attr];
    } else {
        val = obj.__getattr__(attr);
    }

    if (val instanceof batavia.types.Function) {
        // If this is a Python function, we need to know the current
        // context - if it's an attribute of an object (rather than
        // a module) we need to upgrade the Function to a Method.
        if (!(obj instanceof batavia.types.Module)) {
            val = new batavia.types.Method(obj, val);
        }
    } else if (val instanceof Function) {
        // If this is a native Javascript function, wrap the function
        // so that the Python calling convention is used. If it's a
        // class, wrap it in a method that uses the Python calling
        // convention, but instantiates the object rather than just
        // proxying the call.
        if (val.prototype && Object.keys(val.prototype).length > 0) {
            // Python class
            val = function(fn) {
                return function(args, kwargs) {
                    var obj = Object.create(fn.prototype);
                    fn.apply(obj, args);
                    return obj;
                };
            }(val);
        } else {
            // Native javascript method
            var doc = val.__doc__;
            if (val.__python__) {
                // this accepts Batavia-style arguments
                val = function(fn) {
                    var f = function(args, kwargs) {
                        return fn.apply(obj, [args, kwargs]);
                    };
                    f.__doc__ = doc;
                    return f;
                }(val);
            } else {
                val = function(fn) {
                    var f = function(args, kwargs) {
                        return fn.apply(obj, args);
                    };
                    f.__doc__ = doc;
                    return f;
                }(val);
            }
        }
    }
    this.push(val);
};

batavia.VirtualMachine.prototype.byte_STORE_ATTR = function(name) {
    var items = this.popn(2);
    if (items[1].__setattr__ === undefined) {
        items[1][name] = items[0];
    } else {
        items[1].__setattr__(name, items[0]);
    }
};

batavia.VirtualMachine.prototype.byte_DELETE_ATTR = function(name) {
    var obj = this.pop();
    delete obj[name];
};

batavia.VirtualMachine.prototype.byte_STORE_SUBSCR = function() {
    var items = this.popn(3);
    if (items[1].__setitem__) {
        items[1].__setitem__(items[2], items[0]);
    } else {
        items[1][items[2]] = items[0];
    }
};

batavia.VirtualMachine.prototype.byte_DELETE_SUBSCR = function() {
    var items = this.popn(2);
    if (items[1].__delitem__) {
        items[1].__delitem__(items[0]);
    } else {
        delete items[1][items[0]];
    }
};

batavia.VirtualMachine.prototype.byte_BUILD_TUPLE = function(count) {
    var items = this.popn(count);
    this.push(new batavia.types.Tuple(items));
};

batavia.VirtualMachine.prototype.byte_BUILD_LIST = function(count) {
    var items = this.popn(count);
    this.push(new batavia.types.List(items));
};

batavia.VirtualMachine.prototype.byte_BUILD_SET = function(count) {
    var items = this.popn(count);
    this.push(new batavia.types.Set(items));
};

batavia.VirtualMachine.prototype.byte_BUILD_MAP = function(size) {
    switch (batavia.BATAVIA_MAGIC) {
        case batavia.BATAVIA_MAGIC_35:
            var items = this.popn(size * 2);
            var dict = new batavia.types.Dict();

            for (var i = 0; i < items.length; i += 2) {
                dict.__setitem__(items[i], items[i + 1]);
            }

            this.push(dict);

            return;

        case batavia.BATAVIA_MAGIC_35a0:
        case batavia.BATAVIA_MAGIC_34:
            this.push(new batavia.types.Dict());

            return;

        default:
            throw new batavia.builtins.BataviaError(
                "Unsupported BATAVIA_MAGIC. Possibly using unsupported Python versionStrange"
            );
    }
};

batavia.VirtualMachine.prototype.byte_STORE_MAP = function() {
    switch (batavia.BATAVIA_MAGIC) {
        case batavia.BATAVIA_MAGIC_35:
            throw new batavia.builtins.BataviaError(
                "STORE_MAP is unsupported with BATAVIA_MAGIC"
            );

        case batavia.BATAVIA_MAGIC_35a0:
        case batavia.BATAVIA_MAGIC_34:
            var items = this.popn(3);
            if (items[0].__setitem__) {
                items[0].__setitem__(items[2], items[1]);
            } else {
                items[0][items[2]] = items[1];
            }
            this.push(items[0]);

            return;

        default:
            throw new batavia.builtins.BataviaError(
                "Unsupported BATAVIA_MAGIC. Possibly using unsupported Python versionStrange"
            );
    }
};

batavia.VirtualMachine.prototype.byte_UNPACK_SEQUENCE = function(count) {
    var seq = this.pop();

    // If the sequence item on top of the stack is iterable,
    // expand it into an array.
    if (seq.__iter__) {
        try {
            var iter = seq.__iter__();
            seq = [];
            while (true) {
                seq.push(iter.__next__());
            }
        } catch (err) {}
    }

    for (var i = seq.length; i > 0; i--) {
        this.push(seq[i - 1]);
    }
};

batavia.VirtualMachine.prototype.byte_BUILD_SLICE = function(count) {
    if (count === 2 || count === 3) {
        items = this.popn(count);
        this.push(batavia.builtins.slice(items));
    } else {
        throw new batavia.builtins.BataviaError("Strange BUILD_SLICE count: " + count);
    }
};

batavia.VirtualMachine.prototype.byte_LIST_APPEND = function(count) {
    var val = this.pop();
    var the_list = this.peek(count);
    the_list.push(val);
};

batavia.VirtualMachine.prototype.byte_SET_ADD = function(count) {
    var val = this.pop();
    var the_set = this.peek(count);
    the_set.add(val);
};

batavia.VirtualMachine.prototype.byte_MAP_ADD = function(count) {
    var items = this.popn(2);
    var the_map = this.peek(count);
    the_map[items[1]] = items[0];
};

batavia.VirtualMachine.prototype.byte_PRINT_EXPR = function() {
    batavia.stdout(this.pop());
};

batavia.VirtualMachine.prototype.byte_PRINT_ITEM = function() {
    var item = this.pop();
    this.print_item(item);
};

batavia.VirtualMachine.prototype.byte_PRINT_ITEM_TO = function() {
    var to = this.pop();  // FIXME - this is ignored.
    var item = this.pop();
    this.print_item(item);
};

batavia.VirtualMachine.prototype.byte_PRINT_NEWLINE = function() {
    this.print_newline();
};

batavia.VirtualMachine.prototype.byte_PRINT_NEWLINE_TO = function() {
    var to = this.pop();  // FIXME - this is ignored.
    this.print_newline(to);
};

batavia.VirtualMachine.prototype.print_item = function(item, to) {
    if (to === undefined) {
        // to = sys.stdout;  // FIXME - this is ignored.
    }
    batavia.stdout(item);
};

batavia.VirtualMachine.prototype.print_newline = function(to) {
    if (to === undefined) {
        // to = sys.stdout;  // FIXME - this is ignored.
    }
    batavia.stdout("");
};

batavia.VirtualMachine.prototype.byte_JUMP_FORWARD = function(jump) {
    this.jump(jump);
};

batavia.VirtualMachine.prototype.byte_JUMP_ABSOLUTE = function(jump) {
    this.jump(jump);
};

batavia.VirtualMachine.prototype.byte_POP_JUMP_IF_TRUE = function(jump) {
    var val = this.pop();
    var bool_value;
    if (val.__bool__ !== undefined) {
        val = val.__bool__()
    }

    if (val) {
        this.jump(jump);
    }
};

batavia.VirtualMachine.prototype.byte_POP_JUMP_IF_FALSE = function(jump) {
    var val = this.pop();
    if (val.__bool__ !== undefined) {
        val = val.__bool__();
    }

    if (!val) {
        this.jump(jump);
    }
};

batavia.VirtualMachine.prototype.byte_JUMP_IF_TRUE_OR_POP = function(jump) {
    var val = this.top();
    if (val.__bool__ !== undefined) {
        val = val.__bool__()
    }

    if (val) {
        this.jump(jump);
    } else {
        this.pop();
    }
};

batavia.VirtualMachine.prototype.byte_JUMP_IF_FALSE_OR_POP = function(jump) {
    var val = this.top();
    if (val.__bool__ !== undefined) {
        val = val.__bool__();
    }

    if (!val) {
        this.jump(jump);
    } else {
        this.pop();
    }
};

batavia.VirtualMachine.prototype.byte_SETUP_LOOP = function(dest) {
    this.push_block('loop', dest);
};

batavia.VirtualMachine.prototype.byte_GET_ITER = function() {
    this.push(batavia.builtins.iter([this.pop()], null));
};

batavia.VirtualMachine.prototype.byte_FOR_ITER = function(jump) {
    var iterobj = this.top();
    try {
        var v = iterobj.__next__();
        this.push(v);
    } catch (err) {
        if (err instanceof batavia.builtins.StopIteration) {
            this.pop();
            this.jump(jump);
        } else {
            throw err;
        }
    }
};

batavia.VirtualMachine.prototype.byte_BREAK_LOOP = function() {
    return 'break';
};

batavia.VirtualMachine.prototype.byte_CONTINUE_LOOP = function(dest) {
    // This is a trick with the return value.
    // While unrolling blocks, continue and return both have to preserve
    // state as the finally blocks are executed.  For continue, it's
    // where to jump to, for return, it's the value to return.  It gets
    // pushed on the stack for both, so continue puts the jump destination
    // into return_value.
    this.return_value = dest;
    return 'continue';
};

batavia.VirtualMachine.prototype.byte_SETUP_EXCEPT = function(dest) {
    this.push_block('setup-except', dest);
};

batavia.VirtualMachine.prototype.byte_SETUP_FINALLY = function(dest) {
    this.push_block('finally', dest);
};

batavia.VirtualMachine.prototype.byte_END_FINALLY = function() {
    var exc_type = this.pop();
    if (exc_type === batavia.builtins.None) {
        why = null;
    } else {
        value = this.pop();
        if (value instanceof batavia.builtins.BaseException) {
            traceback = this.pop();
            this.last_exception = {
                'exc_type': exc_type,
                'value': value,
                'traceback': traceback
            };
            why = 'reraise';
        } else {
            throw new batavia.builtins.BataviaError("Confused END_FINALLY: " + value.toString());
        }
    }
    return why;
};

batavia.VirtualMachine.prototype.byte_POP_BLOCK = function() {
    this.pop_block();
};

batavia.VirtualMachine.prototype.byte_RAISE_VARARGS = function(argc) {
    var cause, exc;
    if (argc == 2) {
        cause = this.pop();
        exc = this.pop();
    } else if (argc == 1) {
        exc = this.pop();
    }
    return this.do_raise(exc, cause);
};

batavia.VirtualMachine.prototype.do_raise = function(exc, cause) {
    if (exc === undefined) {  // reraise
        if (this.last_exception.exc_type === undefined) {
            return 'exception';      // error
        } else {
            return 'reraise';
        }
    } else if (exc instanceof batavia.builtins.BaseException) {
        // As in `throw ValueError('foo')`
        exc_type = exc.__class__;
        val = exc;
    } else {
        return 'exception';  // error
    }

    // If you reach this point, you're guaranteed that
    // val is a valid exception instance and exc_type is its class.
    // Now do a similar thing for the cause, if present.
    if (cause) {
        // if not isinstance(cause, BaseException):
        //     return 'exception'  // error

        val.__cause__ = cause;
    }

    this.last_exception = {
        'exc_type': exc_type,
        'value': val,
        'traceback': this.create_traceback()
    };
    return 'exception';
};

batavia.VirtualMachine.prototype.byte_POP_EXCEPT = function() {
    var block = this.pop_block();
    if (block.type !== 'except-handler') {
        throw new batavia.exception.BataviaError("popped block is not an except handler");
    }
    this.unwind_block(block);
};

// batavia.VirtualMachine.prototype.byte_SETUP_WITH = function(dest) {
//         ctxmgr = this.pop()
//         this.push(ctxmgr.__exit__)
//         ctxmgr_obj = ctxmgr.__enter__()
//         if PY2:
//             this.push_block('with', dest)
//         elif PY3:
//             this.push_block('finally', dest)
//         this.push(ctxmgr_obj)
// }
// batavia.VirtualMachine.prototype.byte_WITH_CLEANUP = function {
//         // The code here does some weird stack manipulation: the exit function
//         // is buried in the stack, and where depends on what's on top of it.
//         // Pull out the exit function, and leave the rest in place.
//         v = w = null
//         u = this.top()
//         if u is null:
//             exit_func = this.pop(1)
//         elif isinstance(u, str):
//             if u in ('return', 'continue'):
//                 exit_func = this.pop(2)
//             else:
//                 exit_func = this.pop(1)
//             u = null
//         elif issubclass(u, BaseException):
//             if PY2:
//                 w, v, u = this.popn(3)
//                 exit_func = this.pop()
//                 this.push(w, v, u)
//             elif PY3:
//                 w, v, u = this.popn(3)
//                 tp, exc, tb = this.popn(3)
//                 exit_func = this.pop()
//                 this.push(tp, exc, tb)
//                 this.push(null)
//                 this.push(w, v, u)
//                 block = this.pop_block()
//                 assert block.type == 'except-handler'
//                 this.push_block(block.type, block.handler, block.level-1)
//         else:       // pragma: no cover
//             throw "Confused WITH_CLEANUP")
//         exit_ret = exit_func(u, v, w)
//         err = (u is not null) and bool(exit_ret)
//         if err:
//             // An error occurred, and was suppressed
//             if PY2:
//                 this.popn(3)
//                 this.push(null)
//             elif PY3:
//                 this.push('silenced')

//     #// Functions
// }

batavia.VirtualMachine.prototype.byte_MAKE_FUNCTION = function(argc) {
    var name = this.pop();
    var code = this.pop();
    var defaults = this.popn(argc);
    var fn = new batavia.types.Function(name, code, this.frame.f_globals, defaults, null, this);
    this.push(fn);
};

batavia.VirtualMachine.prototype.byte_LOAD_CLOSURE = function(name) {
    this.push(this.frame.cells[name]);
};

batavia.VirtualMachine.prototype.byte_MAKE_CLOSURE = function(argc) {
    var name = this.pop();
    var items = this.popn(2);
    var defaults = this.popn(argc);
    var fn = new batavia.types.Function(name, items[1], this.frame.f_globals, defaults, items[0], this);
    this.push(fn);
};

batavia.VirtualMachine.prototype.byte_CALL_FUNCTION = function(arg) {
    return this.call_function(arg, null, null);
};

batavia.VirtualMachine.prototype.byte_CALL_FUNCTION_VAR = function(arg) {
    var args = this.pop();
    return this.call_function(arg, args, null);
};

batavia.VirtualMachine.prototype.byte_CALL_FUNCTION_KW = function(arg) {
    var kwargs = this.pop();
    return this.call_function(arg, null, kwargs);
};

batavia.VirtualMachine.prototype.byte_CALL_FUNCTION_VAR_KW = function(arg) {
    var items = this.popn(2);
    return this.call_function(arg, items[0], items[1]);
};

batavia.VirtualMachine.prototype.call_function = function(arg, args, kwargs) {
    //@arg is based on
    //https://docs.python.org/3/library/dis.html#opcode-CALL_FUNCTION
    var lenKw = Math.floor(arg / 256);
    var lenPos = arg % 256;
    var namedargs = new batavia.types.JSDict();
    for (var i = 0; i < lenKw; i++) {
        var items = this.popn(2);
        namedargs[items[0]] = items[1];
    }
    if (kwargs) {
        namedargs.update(kwargs);
    }
    var posargs = this.popn(lenPos);
    if (args) {
        posargs = posargs.concat(args);
    }

    var func = this.pop();
    // frame = this.frame
    var retval = batavia.run_callable(this, func, posargs, namedargs);
    this.push(retval);
};

batavia.VirtualMachine.prototype.byte_RETURN_VALUE = function() {
    this.return_value = this.pop();
    if (this.frame.generator) {
        this.frame.generator.finished = true;
    }
    return "return";
};

batavia.VirtualMachine.prototype.byte_YIELD_VALUE = function() {
    this.return_value = this.pop()
    return "yield";
};

// batavia.VirtualMachine.prototype.byte_YIELD_FROM = function {
//         u = this.pop()
//         x = this.top()

//         try:
//             if not isinstance(x, Generator) or u is null:
//                 // Call next on iterators.
//                 retval = next(x)
//             else:
//                 retval = x.send(u)
//             this.return_value = retval
//         except StopIteration as e:
//             this.pop()
//             this.push(e.value)
//         else:
//             // YIELD_FROM decrements f_lasti, so that it will be called
//             // repeatedly until a StopIteration is raised.
//             this.jump(this.frame.f_lasti - 1)
//             // Returning "yield" prevents the block stack cleanup code
//             // from executing, suspending the frame in its current state.
//             return "yield"

//     #// Importing
// }

batavia.VirtualMachine.prototype.byte_IMPORT_NAME = function(name) {
    var items = this.popn(2);
    this.push(
        batavia.builtins.__import__.apply(this, [[name, this.frame.f_globals, null, items[1], items[0]], null])
    );
};

batavia.VirtualMachine.prototype.byte_IMPORT_STAR = function() {
    // TODO: this doesn't use __all__ properly.
    var mod = this.pop();
    if ('__all__' in mod) {
        for (var n = 0; n < mod.__all__.length; n++) {
            var name = mod.__all__[n];
            this.frame.f_locals[name] = mod[name];
        }
    } else {
        for (var attr in mod) {
            if (attr[0] !== '_') {
                this.frame.f_locals[attr] = mod[attr];
            }
        }
    }
};

batavia.VirtualMachine.prototype.byte_IMPORT_FROM = function(name) {
    var mod = this.top();
    this.push(mod[name]);
};

// batavia.VirtualMachine.prototype.byte_EXEC_STMT = function() {
//     stmt, globs, locs = this.popn(3)
//     six.exec_(stmt, globs, locs) f
// };

batavia.VirtualMachine.prototype.byte_LOAD_BUILD_CLASS = function() {
    var make_class = batavia.make_class.bind(this);
    make_class.__python__ = true;
    this.push(make_class);
};

batavia.VirtualMachine.prototype.byte_STORE_LOCALS = function() {
    this.frame.f_locals = this.pop();
};

batavia.VirtualMachine.prototype.byte_SET_LINENO = function(lineno) {
    this.frame.f_lineno = lineno;
};

batavia.VirtualMachine.prototype.byte_EXTENDED_ARG = function(extra) {
};
// needed by the operator python module
batavia.modules._operator = {
    __doc__: "Operator interface.\n\nThis module exports a set of functions corresponding\nto the intrinsic operators of Python.  For example, operator.add(x, y)\nis equivalent to the expression x+y.  The function names are those\nused for special methods; variants without leading and trailing\n'__' are also provided for convenience."
};

// stub "implementation" of _weakref
// JS doesn't quite support weak references, though
// in the future we might be able to use WeakMap or WeakSet to hack it.
batavia.modules._weakref = {
    CallableProxyType: null, // not used directly in stdlib

    ProxyType: null, // not used directly in stdlib

    ReferenceType: null, // not used directly in stdlib

    getweakrefs: function(object) {
        return [];
    },
    getweakrefcount: function(object) {
        return 0;
    },
    proxy: function(object, callback) {
        // TODO: support the finalize callback
        return object;
    },
    ref: function(object) {
      return object;
    },
    __doc__: ""
};
batavia.stdlib['_weakrefset'] = '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';
batavia.stdlib['abc'] = '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';
batavia.stdlib['bisect'] = '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';
batavia.stdlib['colorsys'] = '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';
batavia.stdlib['copyreg'] = '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';
batavia.stdlib['token'] = '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BV9tYWluVgAAAHNiAAAAAAEMAQwBEwEWAQYBEgENAQMBEAESARoBIAEVAQoBBgEDAQwBBgENAQ8BBgEYAQwBEQESAgMBEAESARoBIAEVAQoBAwETARMBDQEQARIBBgENAR8BEAEDARMBEgEaASABFgFycQAAANoIX19tYWluX19OKUTaB19fZG9jX1/aB19fYWxsX19ySQAAANoETkFNRdoGTlVNQkVS2gZTVFJJTkfaB05FV0xJTkXaBklOREVOVNoGREVERU5U2gRMUEFS2gRSUEFS2gRMU1FC2gRSU1FC2gVDT0xPTtoFQ09NTUHaBFNFTUnaBFBMVVPaBU1JTlVT2gRTVEFS2gVTTEFTSNoEVkJBUtoFQU1QRVLaBExFU1PaB0dSRUFURVLaBUVRVUFM2gNET1TaB1BFUkNFTlTaBkxCUkFDRdoGUkJSQUNF2gdFUUVRVUFM2ghOT1RFUVVBTNoJTEVTU0VRVUFM2gxHUkVBVEVSRVFVQUzaBVRJTERF2gpDSVJDVU1GTEVY2glMRUZUU0hJRlTaClJJR0hUU0hJRlTaCkRPVUJMRVNUQVLaCVBMVVNFUVVBTNoITUlORVFVQUzaCVNUQVJFUVVBTNoKU0xBU0hFUVVBTNoMUEVSQ0VOVEVRVUFM2gpBTVBFUkVRVUFM2glWQkFSRVFVQUzaD0NJUkNVTUZMRVhFUVVBTNoOTEVGVFNISUZURVFVQUzaD1JJR0hUU0hJRlRFUVVBTNoPRE9VQkxFU1RBUkVRVUFM2gtET1VCTEVTTEFTSNoQRE9VQkxFU0xBU0hFUVVBTNoCQVTaBlJBUlJPV9oIRUxMSVBTSVPaAk9Q2gpFUlJPUlRPS0VO2ghOX1RPS0VOU3JHAAAA2gdnbG9iYWxz2gVpdGVtc3IBAAAA2gZleHRlbmTaBnZhbHVlc3ICAAAAcgMAAAByBAAAAHJxAAAA2ghfX25hbWVfX3JEAAAAckQAAAByRAAAAHJFAAAA2gg8bW9kdWxlPgEAAABzhAAAAAYCEgoGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYDCQETAhMCDAMMAwwEDDUMAQ==';
batavia.stdlib['operator'] = '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ACkCcjcAAAByOAAAAHI2AAAAcjYAAAByOQAAAHIhAAAAYgEAAHMEAAAAAAIKASkB2gEqKQFyZgAAAE4pZXJmAAAA2gdfX2FsbF9f2ghidWlsdGluc3IBAAAAcjoAAAByJQAAAHIiAAAAcgkAAAByKQAAAHILAAAAcg0AAAByKwAAAHIzAAAAchwAAAByHQAAAHICAAAAcgMAAAByCgAAAHIVAAAAchcAAAByGAAAAHIkAAAAcicAAAByKAAAAHIqAAAAciwAAAByLQAAAHIuAAAAci8AAAByMQAAAHIyAAAAcjQAAAByBQAAAHIGAAAAcgcAAAByCAAAAHIMAAAAchYAAAByMAAAAHIjAAAAcgQAAAByHwAAAHImAAAAcg4AAAByDwAAAHIQAAAAchEAAAByEgAAAHITAAAAchQAAAByGQAAAHIaAAAAchsAAAByHgAAAHIgAAAAciEAAADaCV9vcGVyYXRvctoLSW1wb3J0RXJyb3LaBl9fbHRfX9oGX19sZV9f2gZfX2VxX1/aBl9fbmVfX9oGX19nZV9f2gZfX2d0X1/aB19fbm90X1/aB19fYWJzX1/aB19fYWRkX1/aB19fYW5kX1/aDF9fZmxvb3JkaXZfX3I7AAAA2gdfX2ludl9f2gpfX2ludmVydF9f2gpfX2xzaGlmdF9f2gdfX21vZF9f2gdfX211bF9f2gdfX25lZ19f2gZfX29yX1/aB19fcG9zX1/aB19fcG93X1/aCl9fcnNoaWZ0X1/aB19fc3ViX1/aC19fdHJ1ZWRpdl9f2gdfX3hvcl9f2gpfX2NvbmNhdF9f2gxfX2NvbnRhaW5zX1/aC19fZGVsaXRlbV9fcjwAAADaC19fc2V0aXRlbV9f2ghfX2lhZGRfX9oIX19pYW5kX1/aC19faWNvbmNhdF9f2g1fX2lmbG9vcmRpdl9f2gtfX2lsc2hpZnRfX9oIX19pbW9kX1/aCF9faW11bF9f2gdfX2lvcl9f2ghfX2lwb3dfX9oLX19pcnNoaWZ0X1/aCF9faXN1Yl9f2gxfX2l0cnVlZGl2X1/aCF9faXhvcl9fcjYAAAByNgAAAHI2AAAAcjkAAADaCDxtb2R1bGU+CwAAAHPaAAAABgIVARgBEgEVARIBFQEYAQ8CEAUMBAwEDAQMBAwEDAYMBAwEDAQMBgwEDAQMBAwEDAQMAwYCDAQMBAwEDAQMBAwEDAQMBAwEDAQMBgwHDAQMCAwEDAQMCAwEDykTGxMUExYMBQwFDAgMBQwFDAUMBQwFDAUMBQwFDAUMBgMBDgENAQUCEAQGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgEGAQYBBgE=';
batavia.stdlib['stat'] = '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';
batavia.stdlib['this'] = '7gwNCuBMo1brAwAA4wAAAAAAAAAAAAAAAAcAAABAAAAAc34AAABkAABaAABpAABaAQB4SwBkCQBEXUMAWgIAeDoAZQMAZAMAgwEARF0sAFoEAGUFAGUEAGQEABdkAwAWZQIAF4MBAGUBAGUFAGUEAGUCABeDAQA8cSYAV3ETAFdlBgBkBQBqBwBkBgBkBwCEAABlAABEgwEAgwEAgwEAAWQIAFMpCmFYAwAAR3VyIE1yYSBicyBDbGd1YmEsIG9sIEd2eiBDcmdyZWYKCk9ybmhndnNoeSB2ZiBvcmdncmUgZ3VuYSBodHlsLgpSa2N5dnB2ZyB2ZiBvcmdncmUgZ3VuYSB2emN5dnB2Zy4KRnZ6Y3lyIHZmIG9yZ2dyZSBndW5hIHBiemN5cmsuClBiemN5cmsgdmYgb3JnZ3JlIGd1bmEgcGJ6Y3l2cG5ncnEuClN5bmcgdmYgb3JnZ3JlIGd1bmEgYXJmZ3JxLgpGY25lZnIgdmYgb3JnZ3JlIGd1bmEgcXJhZnIuCkVybnFub3Z5dmdsIHBiaGFnZi4KRmNycHZueSBwbmZyZiBuZXJhJ2cgZmNycHZueSByYWJodHUgZ2Igb2VybnggZ3VyIGVoeXJmLgpOeWd1Ymh0dSBjZW5wZ3Zwbnl2Z2wgb3JuZ2YgY2hldmdsLgpSZWViZWYgZnViaHlxIGFyaXJlIGNuZmYgZnZ5cmFneWwuCkhheXJmZiBya2N5dnB2Z3lsIGZ2eXJhcHJxLgpWYSBndXIgc25wciBicyBuem92dGh2Z2wsIGVyc2hmciBndXIgZ3J6Y2duZ3ZiYSBnYiB0aHJmZi4KR3VyZXIgZnViaHlxIG9yIGJhci0tIG5hcSBjZXJzcmVub3lsIGJheWwgYmFyIC0tYm9pdmJoZiBqbmwgZ2IgcWIgdmcuCk55Z3ViaHR1IGd1bmcgam5sIHpubCBhYmcgb3IgYm9pdmJoZiBuZyBzdmVmZyBoYXlyZmYgbGJoJ2VyIFFoZ3B1LgpBYmogdmYgb3JnZ3JlIGd1bmEgYXJpcmUuCk55Z3ViaHR1IGFyaXJlIHZmIGJzZ3JhIG9yZ2dyZSBndW5hICpldnR1ZyogYWJqLgpWcyBndXIgdnpjeXJ6cmFnbmd2YmEgdmYgdW5lcSBnYiBya2N5bnZhLCB2ZydmIG4gb25xIHZxcm4uClZzIGd1ciB2emN5cnpyYWduZ3ZiYSB2ZiBybmZsIGdiIHJrY3ludmEsIHZnIHpubCBvciBuIHRiYnEgdnFybi4KQW56cmZjbnByZiBuZXIgYmFyIHViYXh2YXQgdGVybmcgdnFybiAtLSB5cmcnZiBxYiB6YmVyIGJzIGd1YmZyIelBAAAA6WEAAADpGgAAAOkNAAAA2gBjAQAAAAAAAAACAAAABQAAAEMAAABzIgAAAGcAAHwAAF0YAH0BAHQAAGoBAHwBAHwBAIMCAJECAHEGAFOpACkC2gFk2gNnZXQpAtoCLjDaAWNyBgAAAHIGAAAA+h4uLi9vdXJvYm9yb3Mvb3Vyb2Jvcm9zL3RoaXMucHn6CjxsaXN0Y29tcD4cAAAAcwIAAAAJAHIMAAAATikCcgEAAAByAgAAACkI2gFzcgcAAAByCgAAANoFcmFuZ2XaAWnaA2NoctoFcHJpbnTaBGpvaW5yBgAAAHIGAAAAcgYAAAByCwAAANoIPG1vZHVsZT4VAAAAcwoAAAAGAgYBDQETAS4C';
