
g = function (a,b,c:(null,2) = [1,2,,]):
	x = a * b + c
	return x


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





for i = 0 -> 10:
	a += i
	if a mod 2 == 0:
		continue
else:
	a = 0
	
x = for i = 0 -> 10: i^1 else: 0
s = sum for i = 0 -> 10: i
s = sum for i = 0 -> 10: if i mod 2 == 0: i else: continue
s = sum for i = 0 -> 10: 
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


return
return x
return x if b
