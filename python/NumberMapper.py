class NumberMapper:
	mapDict = {
		u"\u0966" : "0",
		u"\u0967" : "1",
		u"\u0968" : "2",
		u"\u0969" : "3",
		u"\u096A" : "4",
		u"\u096B" : "5",
		u"\u096C" : "6",
		u"\u096D" : "7",
		u"\u096E" : "8",
		u"\u096F" : "9",
		u"."		: ".",
		u"e"		: "e",
		u"E"		: "E",
		u"a"		: "a",
		u"A"		: "A",
		u"b"		: "b",
		u"B"		: "B",
		u"c"		: "c",
		u"C"		: "C",
		u"d"		: "d",
		u"D"		: "D",
		u"f"		: "f",
		u"F"		: "F",
		u"i"		: "j",
		u"I"		: "j",
		u"j"		: "j",
		u"J"		: "j",
	}
	def convNumber(self, number):
		ascii = ""
		for digit in number:
			ascii += self.mapDict[digit]
		return ascii

	def convInteger(self, number):
		return self.convNumber(number)
	def convFloat(self, number):
		return self.convNumber(number)
	def convHexa(self, number):
		return self.convNumber(number)
	def convOctal(self, number):
		return self.convNumber(number)