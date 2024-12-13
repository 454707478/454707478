var window = {};
 function XRcO(e, t, a) {
    "use strict";
    var n, i, s, r = {}, o = window, l = o.BigInt = function(e) {
        this.digits = "boolean" == typeof e && 1 == e ? null : n.slice(0),
        this.isNeg = !1
    }
    ;
    r.setMaxDigits = function(e) {
        n = new Array(e);
        for (var t = 0; t < n.length; t++)
            n[t] = 0;
        i = new l,
        (s = new l).digits[0] = 1
    }
    ,
    r.setMaxDigits(20);
    r.biFromNumber = function(e) {
        var t = new l;
        t.isNeg = e < 0,
        e = Math.abs(e);
        for (var a = 0; e > 0; )
            t.digits[a++] = 65535 & e,
            e = Math.floor(e / 65536);
        return t
    }
    ;
    var c = r.biFromNumber(1e15);
    r.biFromDecimal = function(e) {
        for (var t, a = "-" == e.charAt(0), n = a ? 1 : 0; n < e.length && "0" == e.charAt(n); )
            ++n;
        if (n == e.length)
            t = new l;
        else {
            var i = (e.length - n) % 15;
            for (0 == i && (i = 15),
            t = r.biFromNumber(Number(e.substr(n, i))),
            n += i; n < e.length; )
                t = r.biAdd(r.biMultiply(t, c), r.biFromNumber(Number(e.substr(n, 15)))),
                n += 15;
            t.isNeg = a
        }
        return t
    }
    ,
    r.biCopy = function(e) {
        var t = new l(!0);
        return t.digits = e.digits.slice(0),
        t.isNeg = e.isNeg,
        t
    }
    ,
    r.reverseStr = function(e) {
        for (var t = "", a = e.length - 1; a > -1; --a)
            t += e.charAt(a);
        return t
    }
    ;
    var d = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"];
    r.biToString = function(e, t) {
        var a = new l;
        a.digits[0] = t;
        for (var n = r.biDivideModulo(e, a), s = d[n[1].digits[0]]; 1 == r.biCompare(n[0], i); )
            n = r.biDivideModulo(n[0], a),
            digit = n[1].digits[0],
            s += d[n[1].digits[0]];
        return (e.isNeg ? "-" : "") + r.reverseStr(s)
    }
    ,
    r.biToDecimal = function(e) {
        var t = new l;
        t.digits[0] = 10;
        for (var a = r.biDivideModulo(e, t), n = String(a[1].digits[0]); 1 == r.biCompare(a[0], i); )
            a = r.biDivideModulo(a[0], t),
            n += String(a[1].digits[0]);
        return (e.isNeg ? "-" : "") + r.reverseStr(n)
    }
    ;
    var u = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"];
    r.digitToHex = function(e) {
        for (var t = "", a = 0; a < 4; ++a)
            t += u[15 & e],
            e >>>= 4;
        return r.reverseStr(t)
    }
    ,
    r.biToHex = function(e) {
        for (var t = "", a = (r.biHighIndex(e),
        r.biHighIndex(e)); a > -1; --a)
            t += r.digitToHex(e.digits[a]);
        return t
    }
    ,
    r.charToHex = function(e) {
        return e >= 48 && e <= 57 ? e - 48 : e >= 65 && e <= 90 ? 10 + e - 65 : e >= 97 && e <= 122 ? 10 + e - 97 : 0
    }
    ,
    r.hexToDigit = function(e) {
        for (var t = 0, a = Math.min(e.length, 4), n = 0; n < a; ++n)
            t <<= 4,
            t |= r.charToHex(e.charCodeAt(n));
        return t
    }
    ,
    r.biFromHex = function(e) {
        for (var t = new l, a = e.length, n = 0; a > 0; a -= 4,
        ++n)
            t.digits[n] = r.hexToDigit(e.substr(Math.max(a - 4, 0), Math.min(a, 4)));
        return t
    }
    ,
    r.biFromString = function(e, t) {
        var a = "-" == e.charAt(0)
          , n = a ? 1 : 0
          , i = new l
          , s = new l;
        s.digits[0] = 1;
        for (var o = e.length - 1; o >= n; o--) {
            var c = e.charCodeAt(o)
              , d = r.charToHex(c)
              , u = r.biMultiplyDigit(s, d);
            i = r.biAdd(i, u),
            s = r.biMultiplyDigit(s, t)
        }
        return i.isNeg = a,
        i
    }
    ,
    r.biDump = function(e) {
        return (e.isNeg ? "-" : "") + e.digits.join(" ")
    }
    ,
    r.biAdd = function(e, t) {
        var a;
        if (e.isNeg != t.isNeg)
            t.isNeg = !t.isNeg,
            a = r.biSubtract(e, t),
            t.isNeg = !t.isNeg;
        else {
            a = new l;
            for (var n, i = 0, s = 0; s < e.digits.length; ++s)
                n = e.digits[s] + t.digits[s] + i,
                a.digits[s] = n % 65536,
                i = Number(n >= 65536);
            a.isNeg = e.isNeg
        }
        return a
    }
    ,
    r.biSubtract = function(e, t) {
        var a;
        if (e.isNeg != t.isNeg)
            t.isNeg = !t.isNeg,
            a = r.biAdd(e, t),
            t.isNeg = !t.isNeg;
        else {
            var n, i;
            a = new l,
            i = 0;
            for (var s = 0; s < e.digits.length; ++s)
                n = e.digits[s] - t.digits[s] + i,
                a.digits[s] = n % 65536,
                a.digits[s] < 0 && (a.digits[s] += 65536),
                i = 0 - Number(n < 0);
            if (-1 == i) {
                i = 0;
                for (s = 0; s < e.digits.length; ++s)
                    n = 0 - a.digits[s] + i,
                    a.digits[s] = n % 65536,
                    a.digits[s] < 0 && (a.digits[s] += 65536),
                    i = 0 - Number(n < 0);
                a.isNeg = !e.isNeg
            } else
                a.isNeg = e.isNeg
        }
        return a
    }
    ,
    r.biHighIndex = function(e) {
        for (var t = e.digits.length - 1; t > 0 && 0 == e.digits[t]; )
            --t;
        return t
    }
    ,
    r.biNumBits = function(e) {
        var t, a = r.biHighIndex(e), n = e.digits[a], i = 16 * (a + 1);
        for (t = i; t > i - 16 && 0 == (32768 & n); --t)
            n <<= 1;
        return t
    }
    ,
    r.biMultiply = function(e, t) {
        for (var a, n, i, s = new l, o = r.biHighIndex(e), c = r.biHighIndex(t), d = 0; d <= c; ++d) {
            a = 0,
            i = d;
            for (var u = 0; u <= o; ++u,
            ++i)
                n = s.digits[i] + e.digits[u] * t.digits[d] + a,
                s.digits[i] = 65535 & n,
                a = n >>> 16;
            s.digits[d + o + 1] = a
        }
        return s.isNeg = e.isNeg != t.isNeg,
        s
    }
    ,
    r.biMultiplyDigit = function(e, t) {
        var a, n, i, s = new l;
        a = r.biHighIndex(e),
        n = 0;
        for (var o = 0; o <= a; ++o)
            i = s.digits[o] + e.digits[o] * t + n,
            s.digits[o] = 65535 & i,
            n = i >>> 16;
        return s.digits[1 + a] = n,
        s
    }
    ,
    r.arrayCopy = function(e, t, a, n, i) {
        for (var s = Math.min(t + i, e.length), r = t, o = n; r < s; ++r,
        ++o)
            a[o] = e[r]
    }
    ;
    var p = [0, 32768, 49152, 57344, 61440, 63488, 64512, 65024, 65280, 65408, 65472, 65504, 65520, 65528, 65532, 65534, 65535];
    r.biShiftLeft = function(e, t) {
        var a = Math.floor(t / 16)
          , n = new l;
        r.arrayCopy(e.digits, 0, n.digits, a, n.digits.length - a);
        for (var i = t % 16, s = 16 - i, o = n.digits.length - 1, c = o - 1; o > 0; --o,
        --c)
            n.digits[o] = n.digits[o] << i & 65535 | (n.digits[c] & p[i]) >>> s;
        return n.digits[0] = n.digits[o] << i & 65535,
        n.isNeg = e.isNeg,
        n
    }
    ;
    var m = [0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535];
    function h(e) {
        var t = r
          , a = t.biDivideByRadixPower(e, this.k - 1)
          , n = t.biMultiply(a, this.mu)
          , i = t.biDivideByRadixPower(n, this.k + 1)
          , s = t.biModuloByRadixPower(e, this.k + 1)
          , o = t.biMultiply(i, this.modulus)
          , l = t.biModuloByRadixPower(o, this.k + 1)
          , c = t.biSubtract(s, l);
        c.isNeg && (c = t.biAdd(c, this.bkplus1));
        for (var d = t.biCompare(c, this.modulus) >= 0; d; )
            c = t.biSubtract(c, this.modulus),
            d = t.biCompare(c, this.modulus) >= 0;
        return c
    }
    function g(e, t) {
        var a = r.biMultiply(e, t);
        return this.modulo(a)
    }
    function f(e, t) {
        var a = new l;
        a.digits[0] = 1;
        for (var n = e, i = t; 0 != (1 & i.digits[0]) && (a = this.multiplyMod(a, n)),
        0 != (i = r.biShiftRight(i, 1)).digits[0] || 0 != r.biHighIndex(i); )
            n = this.multiplyMod(n, n);
        return a
    }
    r.biShiftRight = function(e, t) {
        var a = Math.floor(t / 16)
          , n = new l;
        r.arrayCopy(e.digits, a, n.digits, 0, e.digits.length - a);
        for (var i = t % 16, s = 16 - i, o = 0, c = o + 1; o < n.digits.length - 1; ++o,
        ++c)
            n.digits[o] = n.digits[o] >>> i | (n.digits[c] & m[i]) << s;
        return n.digits[n.digits.length - 1] >>>= i,
        n.isNeg = e.isNeg,
        n
    }
    ,
    r.biMultiplyByRadixPower = function(e, t) {
        var a = new l;
        return r.arrayCopy(e.digits, 0, a.digits, t, a.digits.length - t),
        a
    }
    ,
    r.biDivideByRadixPower = function(e, t) {
        var a = new l;
        return r.arrayCopy(e.digits, t, a.digits, 0, a.digits.length - t),
        a
    }
    ,
    r.biModuloByRadixPower = function(e, t) {
        var a = new l;
        return r.arrayCopy(e.digits, 0, a.digits, 0, t),
        a
    }
    ,
    r.biCompare = function(e, t) {
        if (e.isNeg != t.isNeg)
            return 1 - 2 * Number(e.isNeg);
        for (var a = e.digits.length - 1; a >= 0; --a)
            if (e.digits[a] != t.digits[a])
                return e.isNeg ? 1 - 2 * Number(e.digits[a] > t.digits[a]) : 1 - 2 * Number(e.digits[a] < t.digits[a]);
        return 0
    }
    ,
    r.biDivideModulo = function(e, t) {
        var a, n, i = r.biNumBits(e), o = r.biNumBits(t), c = t.isNeg;
        if (i < o)
            return e.isNeg ? ((a = r.biCopy(s)).isNeg = !t.isNeg,
            e.isNeg = !1,
            t.isNeg = !1,
            n = biSubtract(t, e),
            e.isNeg = !0,
            t.isNeg = c) : (a = new l,
            n = r.biCopy(e)),
            [a, n];
        a = new l,
        n = e;
        for (var d = Math.ceil(o / 16) - 1, u = 0; t.digits[d] < 32768; )
            t = r.biShiftLeft(t, 1),
            ++u,
            ++o,
            d = Math.ceil(o / 16) - 1;
        n = r.biShiftLeft(n, u),
        i += u;
        for (var p = Math.ceil(i / 16) - 1, m = r.biMultiplyByRadixPower(t, p - d); -1 != r.biCompare(n, m); )
            ++a.digits[p - d],
            n = r.biSubtract(n, m);
        for (var h = p; h > d; --h) {
            var g = h >= n.digits.length ? 0 : n.digits[h]
              , f = h - 1 >= n.digits.length ? 0 : n.digits[h - 1]
              , v = h - 2 >= n.digits.length ? 0 : n.digits[h - 2]
              , b = d >= t.digits.length ? 0 : t.digits[d]
              , y = d - 1 >= t.digits.length ? 0 : t.digits[d - 1];
            a.digits[h - d - 1] = g == b ? 65535 : Math.floor((65536 * g + f) / b);
            for (var w = a.digits[h - d - 1] * (65536 * b + y), S = 4294967296 * g + (65536 * f + v); w > S; )
                --a.digits[h - d - 1],
                w = a.digits[h - d - 1] * (65536 * b | y),
                S = 65536 * g * 65536 + (65536 * f + v);
            m = r.biMultiplyByRadixPower(t, h - d - 1),
            (n = r.biSubtract(n, r.biMultiplyDigit(m, a.digits[h - d - 1]))).isNeg && (n = r.biAdd(n, m),
            --a.digits[h - d - 1])
        }
        return n = r.biShiftRight(n, u),
        a.isNeg = e.isNeg != c,
        e.isNeg && (a = c ? r.biAdd(a, s) : r.biSubtract(a, s),
        t = r.biShiftRight(t, u),
        n = r.biSubtract(t, n)),
        0 == n.digits[0] && 0 == r.biHighIndex(n) && (n.isNeg = !1),
        [a, n]
    }
    ,
    r.biDivide = function(e, t) {
        return r.biDivideModulo(e, t)[0]
    }
    ,
    r.biModulo = function(e, t) {
        return r.biDivideModulo(e, t)[1]
    }
    ,
    r.biMultiplyMod = function(e, t, a) {
        return r.biModulo(r.biMultiply(e, t), a)
    }
    ,
    r.biPow = function(e, t) {
        for (var a = s, n = e; 0 != (1 & t) && (a = r.biMultiply(a, n)),
        0 != (t >>= 1); )
            n = r.biMultiply(n, n);
        return a
    }
    ,
    r.biPowMod = function(e, t, a) {
        for (var n = s, i = e, o = t; 0 != (1 & o.digits[0]) && (n = r.biMultiplyMod(n, i, a)),
        0 != (o = r.biShiftRight(o, 1)).digits[0] || 0 != r.biHighIndex(o); )
            i = r.biMultiplyMod(i, i, a);
        return n
    }
    ,
    o.BarrettMu = function(e) {
        this.modulus = r.biCopy(e),
        this.k = r.biHighIndex(this.modulus) + 1;
        var t = new l;
        t.digits[2 * this.k] = 1,
        this.mu = r.biDivide(t, this.modulus),
        this.bkplus1 = new l,
        this.bkplus1.digits[this.k + 1] = 1,
        this.modulo = h,
        this.multiplyMod = g,
        this.powMod = f
    }
    ;
    r.getKeyPair = function(e,t,a) {
        return new function(e, t, a) {
            var n = r;
            this.e = n.biFromHex(e),
            this.d = n.biFromHex(t),
            this.m = n.biFromHex(a),
            this.chunkSize = 2 * n.biHighIndex(this.m),
            this.radix = 16,
            this.barrett = new o.BarrettMu(this.m)
        }
        (e,t,a)
    }
    ,
    void 0 === o.twoDigit && (o.twoDigit = function(e) {
        return (e < 10 ? "0" : "") + String(e)
    }
    ),
    r.encryptedString = function(e, t) {
        for (var a = [], n = e.length, i = 0; i < n; )
            a[i] = e.charCodeAt(i),
            i++;
        for (; a.length % t.chunkSize != 0; )
            a[i++] = 0;
        var s, o, c, d = a.length, u = "";
        for (i = 0; i < d; i += t.chunkSize) {
            for (c = new l,
            s = 0,
            o = i; o < i + t.chunkSize; ++s)
                c.digits[s] = a[o++],
                c.digits[s] += a[o++] << 8;
            var p = t.barrett.powMod(c, t.e);
            u += (16 == t.radix ? r.biToHex(p) : r.biToString(p, t.radix)) + " "
        }
        return u.substring(0, u.length - 1)
    }
    ,
    r.decryptedString = function(e, t) {
        var a, n, i, s = t.split(" "), o = "";
        for (a = 0; a < s.length; ++a) {
            var l;
            for (l = 16 == e.radix ? r.biFromHex(s[a]) : r.biFromString(s[a], e.radix),
            i = e.barrett.powMod(l, e.d),
            n = 0; n <= r.biHighIndex(i); ++n)
                o += String.fromCharCode(255 & i.digits[n], i.digits[n] >> 8)
        }
        return 0 == o.charCodeAt(o.length - 1) && (o = o.substring(0, o.length - 1)),
        o
    }
    ,
    r.setMaxDigits(130)
    var obg_o = r.getKeyPair(e,t,a);
    var psw = "WJs#1357";
    // 密码加密值
    var psw_result = r.encryptedString(psw,obg_o);
    // 请求头Authorkey加密值
    var date = (new Date().getTime()).toString();
    var Authorkey = r.encryptedString(date,obg_o);
    var obj = {
       psw: psw_result,
       authorkey: Authorkey
    }
    return obj;
    // t.a = r
}