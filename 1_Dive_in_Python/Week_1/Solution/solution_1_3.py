import sys
count_step = int(sys.argv[1])
for dig in range(count_step):
	s = (count_step - dig - 1)*" " + (dig + 1)*"#"
	print (s)