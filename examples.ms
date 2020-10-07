
g = function (a,b,c = [1,2,,])
		@shape(c = ( null ,2)):
	x = a * b + c
	return x

g = function @shape(c = ( null ,2))
	(a,b,c = [1,2,,]):
	x = a * b + c
	return x
	
g = function extends shape(c: ( null ,2))
	(a,b,c = [1,2,,]):
	x = a * b + c
	return x

g = shape {'c': (null,2)} function (a,b,c = [1,2,,]):
		(a,b,c = [1,2,,]):
		x = a * b + c
		return x
	)


C = class (D):
	h = function (a):
		this.a = a


if a < b:
	a = b
else if a > b:
	b = a
else:
	return a


x = if a < b: a else: b
x = if a < 1: a elseif a < 2: b elseif a < 3: c else: d

x = if a < b: 
	a 
else:
	b


switch value:
	case a:
		do something
		break
	case b:
		do something
		break
	default:
		do something
		break





for i in 0 -> 10:
	a += i
	if a mod 2 == 0:
		continue
else:
	a = 0
	
x = for i in 0 -> 10: i^1 else: 0
s = sum for i in 0 -> 10: i
s = sum for i in 0 -> 10: if i mod 2 == 0: i else: continue
s = sum for i in 0 -> 10: 
	if i mod 2 == 0: 
		yield i 
	else: 
		continue


while i < 10:
	a /= 2
	if a < 2^-10:
		break



f(x) = {
	0 if x < 0
	x else
}

f(x) = x ^ 2

sin [5deg, 10deg, 20deg]
vec [5, 10]

[...for i=0->10: i,, ...for i=0->10: i^2,, ...for i=0->10: i^3]

dict = {
	'a': 1,
	'b': 2 + 3,
}


return
return x
return x if b

// order of precedence
Group		p	symbols

Assignment	0	=
constructs	1	class function if switch for while continue break return
codeblock	2	:
logic1		3	or
logic2		4	and
logic3		5	not
comparitors	6	< <= > >= != ==
bitwise1	7
bitwise2	8
bitwise3	9
range		10	->
add&sub		11	+ -
mul&div		12	* / # .* @
exponent	13	^ $
prefix		14	- + ~ $ ...
postfix		15	!
reference	16	. ..
value		17	val () [] {} ||


signals			, ; \n ) ] } |