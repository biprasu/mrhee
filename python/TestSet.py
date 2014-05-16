#encoding=utf8
lextest = {
	'identifier1':u'_॥ॣ३_५६',
	'decimalInteger1':u'८९४',
	'decimalInteger2':u'०',
	'octalInteger1':u'००२७९',
	'hexaInteger1':u'०x०९४८५AF',
	'float1':u'९.४३',
	'float2':u'.४३',
	'float3':u'०.४३',
	'float4':u'९.४३e४',
	'float5':u'९.४३E४',
	'float6':u'.४३E४',
	'float7':u'२.E४',
	'float8':u'२.E-४',

	'imaginary':u'०i',
	'imaginary2':u'i',
	'imaginary3':u'.४३i',
	'imaginary4':u'०.३२e५७i',

# 	'comment':u'''टेस्ट टेस्ट // टेस्टटेस्ट
# तेस्ते /* फ्त्क्ज
# फ्क्ज्दा 
# */
# ''',

	# 'string':u'"test"',
	# 'string1':u"'test'",
	# 'string2':u'''"two line 
	# string"''',

}

gTest = {
	'normal' : u'''(९*९)^९%९''',
	'ident_condition'	: u'''((क*९)^-९%९==९%९)छ वा (९%९==९%९) छैन र ९%९==९%९ वा क == ख''',
	'string_condition'	: u''' "हाम्रो" == "तिम्रो" छैन''',
	'multiline'			: u'''
								क == "तिम्रो" छैन

								''',
	'input' 			: u'''
							क, ख, घ लेउ
							''',
	'assignment'		: u'''
						क = ४ * ख + ९ * (४ % ३) / (८i)
						''',
	'singleline if'		: u'''यदि प*ख == क छ भए क लेख''',
	'increment operator': u'''यदि प*ख == क छ भए क += ६''',
	'slif'				: u'''यदि ग == ख भए ख लेख अथवा ख लेख''',
	'mlif'				: u'''यदि क==ख भए
		'क' लेख
		क लेउ
		अथवा क==ख भए
		ब लेख
		अथवा क==ख भए
		ब लेख
		अथवा
		ल लेख
	दिय''',
	'forloop'			: u'''सबै क = १ देखि ८ : -१
		क लेख
		बैस
		''',
	'whileloop'			: u'''जब सम्म क == ख छ
		क लेख
		क += ४
		बज''',
	'repeatloop'		: u'''७*८ चोटि
		क लेख
		टिचो''',
	'functiondef'		: u'''काम टेस्ट(क, ख, ग)
					७*८ चोटि
						क लेख
					टिचो
					मका''',
	'classdef'			: u'''खाका वस्तु
		काम टेस्ट(क, ख, ग)
		७*८ चोटि
			क लेख
		टिचो
		मका
		काखा''',
	'functioncall'		: u'''टेस्ट('क', 'ख', 'ग')'''

}


error = [
		u'''ल, "छ", ल, त लेख''',
		u'''
						क += ७*त
						'''
		]