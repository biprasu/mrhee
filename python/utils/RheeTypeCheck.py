class RheeTypeCheck(object):
    """Type checking and handling errors also final unicode mapping"""

    def __init__(self):
        super(RheeTypeCheck, self).__init__()

    def e_print(self, bakra):
        'number, string, bool, array'

        collector = u''
        itype = self.get_type(bakra)

        if itype == 'num':  # number
            # map it back to unicode
            return str(bakra)
        elif itype == 'bool':  # booleans
            if bakra:
                return 'satya'
            return 'jhuto'
        elif itype == 'undefined':
            return "sunya"

        elif itype == 'array':
            collector = u'['

            for item in bakra[1][:-1]:
                collector += self.e_print(item) + ", "
            collector += self.e_print(bakra[1][-1]) + u']'

            return collector

        elif itype == 'function':
            return "(function instance of "  # + bakra[4] + ")"
        elif itype == 'object':
            return "(object instance of "  # + bakra[2] + ")"
        elif itype == 'class':
            return "(class instance of "  # + bakra[2] + ")"

        # else it is string
        return bakra

    def e_boolean(self, obj):
        'Everything except empty string, empty array, Null and False is true'
        itype = self.get_type(obj)

        if itype is 'undefined':
            return False
        elif itype is 'bool':
            return obj
        elif itype is 'string' and obj == "":
            return False
        elif itype is 'array' and obj[1] == []:
            return False
        return True

    def e_forloop(self, pre, post, step, lineno):
        if type(pre) in [int, float]:
            if type(post) in [int, float]:
                if type(step) in [int, float]:
                    return True
        self.error("Expressions in for loop should be numbers ", lineno)
        return False

    def e_arraycheck(self, arr, lineno):
        if not (self.get_type(arr) is 'array'):
            self.error("Array reference only allowed in array not in " + self.get_type(arr), lineno)
        return True

    def e_aryref(self, start, end, arlen, lineno):
        if not (type(start) in [int, float]):
            self.error("Array index should be number.", lineno)
            return

        if start >= arlen:
            self.error("Array index out of bound", lineno)
            return

        if end:
            if not (type(end) in [int, float]):
                self.error("Array index should be number.", lineno)
                return

            if end >= arlen:
                self.error("Array index out of bound", lineno)
                return
        return

    def e_aryassign(self, indx, lineno):
        if not (type(indx) in [int, float]):
            self.error("Array index should be number", lineno)
            return

    typeMap = {int 	: 'num',
			   float		: 'num',
			   str 		: 'string',
			   unicode		: 'string',
			   bool 		: 'bool',
			   type(None)	: 'undefined',
			   # tuple		: lambda x: x[0],			# can be array, object, class ,function
			   }

    def get_type(self, item):
        itype = type(item)

        if itype is tuple:
            return item[0]

        if not itype in self.typeMap:
            raise Exception("Contact Developer!! " + str(itype) + "in get_type")

        return self.typeMap[itype]

    def e_arithop(self, lhs, operator, rhs, lineno):
        'only type of number, string and array are allowed'
        try:
            ltype = self.get_type(lhs)
            rtype = self.get_type(rhs)

            if (ltype == 'num'):
                # if lhs = num, rhs should be num
                if not (rtype == 'num'):
                    raise RTypeError("Invalid operation between num and " + rtype)

                if operator == '/' and rhs == 0:
                    raise RTypeError("DivideByZero: You can't divide number by zero.")

            elif (ltype == "string"):
                # if lhs = string
                if (operator != "+"):
                    raise RTypeError("Invalid operator " + operator + " for string type")

                if (rtype == 'string' or rtype == 'num'):
                    return True

                raise RTypeError("Invalid operation between string and " + rtype)

            elif (ltype == 'array'):
                # if lhs = array
                if rtype == 'array' and operator == '+':
                    return True

                raise RTypeError("Invalid operation between array " + operator + " " + rtype)
            else:
                # NULL BOOLS
                # filterout function and object
                raise RTypeError("Invalid operation with " + ltype + " and " + rtype)
        except RTypeError as e:
            self.error("TypeError: " + e.message)

    def e_binop(self, lhs, rhs):
        if (self.get_type(lhs) != self.get_type(rhs)):
            return False
        return (self.get_type(lhs) == 'num')


class RTypeError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


if __name__ == '__main__':
    test = RheeTypeCheck()
    # print(test.e_print("43"))
    # print(test.e_print(43))
    # print(test.e_print(43e-3))
    # print(test.e_print(43e49))
    # print(test.e_print(None))
    # print(test.e_print(True))
    # print(test.e_print(False))
    # print(test.e_print(["43", 43, True, False, [None, 4e67, True]]))
    # print(test.e_print(('function', 'fparams', 'fbody', 'fenv', 'fname')))
    # print(test.e_print(('object', 'oenv', 'cname')))
    # print(test.e_print(('class', 'cenv', 'cname')))

    # print("")
    # print (test.e_boolean([]))
    # print (test.e_boolean(u""))
    # print (test.e_boolean(False))
    # print (test.e_boolean([34]))
    # print (test.e_boolean(None))
    # print (test.e_boolean(('object', 'oenv', 'cname')))
    # print (test.e_boolean(0))
    # print (test.e_boolean(3))

    print type(('array', [3, 4, 5],))
    print test.get_type(('array', [3, 4, 5],))
    print test.get_type(('function', [3, 4, 5],))
    print test.get_type(('class', [3, 4, 5],))
    print test.get_type(('object', [3, 4,
 5],))