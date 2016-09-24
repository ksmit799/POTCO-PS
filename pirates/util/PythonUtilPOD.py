from panda3d.direct import get_config_showbase
from panda3d.core import Camera
from direct.showbase.PythonUtil import getSetter, getSetterName
import sys

def mostDerivedLast(classList):
    """pass in list of classes. sorts list in-place, with derived classes
    appearing after their bases"""

    class ClassSortKey(object):
        __slots__ = 'classobj',
        def __init__(self, classobj):
            self.classobj = classobj
        def __lt__(self, other):
            return issubclass(other.classobj, self.classobj)

    classList.sort(key=ClassSortKey)

"""
ParamObj/ParamSet
=================

These two classes support you in the definition of a formal set of
parameters for an object type. The parameters may be safely queried/set on
an object instance at any time, and the object will react to newly-set
values immediately.

ParamSet & ParamObj also provide a mechanism for atomically setting
multiple parameter values before allowing the object to react to any of the
new values--useful when two or more parameters are interdependent and there
is risk of setting an illegal combination in the process of applying a new
set of values.

To make use of these classes, derive your object from ParamObj. Then define
a 'ParamSet' subclass that derives from the parent class' 'ParamSet' class,
and define the object's parameters within its ParamSet class. (see examples
below)

The ParamObj base class provides 'get' and 'set' functions for each
parameter if they are not defined. These default implementations
respectively set the parameter value directly on the object, and expect the
value to be available in that location for retrieval.

Classes that derive from ParamObj can optionally declare a 'get' and 'set'
function for each parameter. The setter should simply store the value in a
location where the getter can find it; it should not do any further
processing based on the new parameter value. Further processing should be
implemented in an 'apply' function. The applier function is optional, and
there is no default implementation.

NOTE: the previous value of a parameter is available inside an apply
function as 'self.getPriorValue()'

The ParamSet class declaration lists the parameters and defines a default
value for each. ParamSet instances represent a complete set of parameter
values. A ParamSet instance created with no constructor arguments will
contain the default values for each parameter. The defaults may be
overriden by passing keyword arguments to the ParamSet's constructor. If a
ParamObj instance is passed to the constructor, the ParamSet will extract
the object's current parameter values.

ParamSet.applyTo(obj) sets all of its parameter values on 'obj'.

SETTERS AND APPLIERS
====================
Under normal conditions, a call to a setter function, i.e.

 cam.setFov(90)

will actually result in the following calls being made:

 cam.setFov(90)
 cam.applyFov()

Calls to several setter functions, i.e.

 cam.setFov(90)
 cam.setViewType('cutscene')

will result in this call sequence:

 cam.setFov(90)
 cam.applyFov()
 cam.setViewType('cutscene')
 cam.applyViewType()

Suppose that you desire the view type to already be set to 'cutscene' at
the time when applyFov() is called. You could reverse the order of the set
calls, but suppose that you also want the fov to be set properly at the
time when applyViewType() is called.

In this case, you can 'lock' the params, i.e.

 cam.lockParams()
 cam.setFov(90)
 cam.setViewType('cutscene')
 cam.unlockParams()

This will result in the following call sequence:

 cam.setFov(90)
 cam.setViewType('cutscene')
 cam.applyFov()
 cam.applyViewType()

NOTE: Currently the order of the apply calls following an unlock is not
guaranteed.

EXAMPLE CLASSES
===============
Here is an example of a class that uses ParamSet/ParamObj to manage its
parameters:

class Camera(ParamObj):
    class ParamSet(ParamObj.ParamSet):
        Params = {
            'viewType': 'normal',
            'fov': 60,
            }
    ...

    def getViewType(self):
        return self.viewType
    def setViewType(self, viewType):
        self.viewType = viewType
    def applyViewType(self):
        if self.viewType == 'normal':
            ...

    def getFov(self):
        return self.fov
    def setFov(self, fov):
        self.fov = fov
    def applyFov(self):
        base.camera.setFov(self.fov)
    ...


EXAMPLE USAGE
=============

cam = Camera()
...

# set up for the cutscene
savedSettings = cam.ParamSet(cam)
cam.setViewType('closeup')
cam.setFov(90)
...

# cutscene is over, set the camera back
savedSettings.applyTo(cam)
del savedSettings

"""

class ParamObj:
    # abstract base for classes that want to support a formal parameter
    # set whose values may be queried, changed, 'bulk' changed (defer reaction
    # to changes until multiple changes have been performed), and
    # extracted/stored/applied all at once (see documentation above)

    # ParamSet subclass: container of parameter values. Derived class must
    # derive a new ParamSet class if they wish to define new params. See
    # documentation above.
    class ParamSet:
        Params = {
            # base class does not define any parameters, but they would
            # appear here as 'name': defaultValue,
            #
            # WARNING: default values of mutable types that do not copy by
            # value (dicts, lists etc.) will be shared by all class instances
            # if default value is callable, it will be called to get actual
            # default value
            #
            # for example:
            #
            # class MapArea(ParamObj):
            #     class ParamSet(ParamObj.ParamSet):
            #         Params = {
            #             'spawnIndices': Functor(list, [1,5,22]),
            #         }
            #
            }

        def __init__(self, *args, **kwArgs):
            self.__class__._compileDefaultParams()
            if len(args) == 1 and len(kwArgs) == 0:
                # extract our params from an existing ParamObj instance
                obj = args[0]
                self.paramVals = {}
                for param in self.getParams():
                    self.paramVals[param] = getSetter(obj, param, 'get')()
            else:
                assert len(args) == 0
                if __debug__:
                    for arg in kwArgs.keys():
                        assert arg in self.getParams()
                self.paramVals = dict(kwArgs)
        def getValue(self, param):
            if param in self.paramVals:
                return self.paramVals[param]
            return self._Params[param]
        def applyTo(self, obj):
            # Apply our entire set of params to a ParamObj
            obj.lockParams()
            for param in self.getParams():
                getSetter(obj, param)(self.getValue(param))
            obj.unlockParams()
        def extractFrom(self, obj):
            # Extract our entire set of params from a ParamObj
            obj.lockParams()
            for param in self.getParams():
                self.paramVals[param] = getSetter(obj, param, 'get')()
            obj.unlockParams()
        @classmethod
        def getParams(cls):
            # returns safely-mutable list of param names
            cls._compileDefaultParams()
            return cls._Params.keys()
        @classmethod
        def getDefaultValue(cls, param):
            cls._compileDefaultParams()
            dv = cls._Params[param]
            if callable(dv):
                dv = dv()
            return dv
        @classmethod
        def _compileDefaultParams(cls):
            if '_Params' in cls.__dict__:
                # we've already compiled the defaults for this class
                return
            bases = list(cls.__bases__)
            if object in bases:
                bases.remove(object)
            # bring less-derived classes to the front
            mostDerivedLast(bases)
            cls._Params = {}
            for c in (bases + [cls]):
                # make sure this base has its dict of param defaults
                c._compileDefaultParams()
                if 'Params' in c.__dict__:
                    # apply this class' default param values to our dict
                    cls._Params.update(c.Params)
        def __repr__(self):
            argStr = ''
            for param in self.getParams():
                argStr += '%s=%s,' % (param,
                                      repr(self.getValue(param)))
            return '%s.%s(%s)' % (
                self.__class__.__module__, self.__class__.__name__, argStr)
    # END PARAMSET SUBCLASS

    def __init__(self, *args, **kwArgs):
        assert issubclass(self.ParamSet, ParamObj.ParamSet)
        # If you pass in a ParamSet obj, its values will be applied to this
        # object in the constructor.
        params = None
        if len(args) == 1 and len(kwArgs) == 0:
            # if there's one argument, assume that it's a ParamSet
            params = args[0]
        elif len(kwArgs) > 0:
            assert len(args) == 0
            # if we've got keyword arguments, make a ParamSet out of them
            params = self.ParamSet(**kwArgs)

        self._paramLockRefCount = 0
        # these hold the current value of parameters while they are being set to
        # a new value, to support getPriorValue()
        self._curParamStack = []
        self._priorValuesStack = []

        # insert stub funcs for param setters, to handle locked params
        for param in self.ParamSet.getParams():

            # set the default value on the object
            setattr(self, param, self.ParamSet.getDefaultValue(param))

            setterName = getSetterName(param)
            getterName = getSetterName(param, 'get')

            # is there a setter defined?
            if not hasattr(self, setterName):
                # no; provide the default
                def defaultSetter(self, value, param=param):
                    #print '%s=%s for %s' % (param, value, id(self))
                    setattr(self, param, value)
                self.__class__.__dict__[setterName] = defaultSetter

            # is there a getter defined?
            if not hasattr(self, getterName):
                # no; provide the default. If there is no value set, return
                # the default
                def defaultGetter(self, param=param,
                                  default=self.ParamSet.getDefaultValue(param)):
                    return getattr(self, param, default)
                self.__class__.__dict__[getterName] = defaultGetter

            # have we already installed a setter stub?
            origSetterName = '%s_ORIG' % (setterName,)
            if not hasattr(self, origSetterName):
                # move the original setter aside
                origSetterFunc = getattr(self.__class__, setterName)
                setattr(self.__class__, origSetterName, origSetterFunc)
                """
                # if the setter is a direct member of this instance, move the setter
                # aside
                if setterName in self.__dict__:
                    self.__dict__[setterName + '_MOVED'] = self.__dict__[setterName]
                    setterFunc = self.__dict__[setterName]
                    """
                # install a setter stub that will a) call the real setter and
                # then the applier, or b) call the setter and queue the
                # applier, depending on whether our params are locked
                """
                setattr(self, setterName, types.MethodType(
                    Functor(setterStub, param, setterFunc), self, self.__class__))
                    """
                def setterStub(self, value, param=param, origSetterName=origSetterName):
                    # should we apply the value now or should we wait?
                    # if this obj's params are locked, we track which values have
                    # been set, and on unlock, we'll call the applyers for those
                    # values
                    if self._paramLockRefCount > 0:
                        priorValues = self._priorValuesStack[-1]
                        if param not in priorValues:
                            try:
                                priorValue = getSetter(self, param, 'get')()
                            except:
                                priorValue = None
                            priorValues[param] = priorValue
                        self._paramsSet[param] = None
                        getattr(self, origSetterName)(value)
                    else:
                        # prepare for call to getPriorValue
                        try:
                            priorValue = getSetter(self, param, 'get')()
                        except:
                            priorValue = None
                        self._priorValuesStack.append({
                            param: priorValue,
                            })
                        getattr(self, origSetterName)(value)
                        # call the applier, if there is one
                        applier = getattr(self, getSetterName(param, 'apply'), None)
                        if applier is not None:
                            self._curParamStack.append(param)
                            applier()
                            self._curParamStack.pop()
                        self._priorValuesStack.pop()
                        if hasattr(self, 'handleParamChange'):
                            self.handleParamChange((param,))

                setattr(self.__class__, setterName, setterStub)

        if params is not None:
            params.applyTo(self)

    def destroy(self):
        """
        for param in self.ParamSet.getParams():
            setterName = getSetterName(param)
            self.__dict__[setterName].destroy()
            del self.__dict__[setterName]
            """
        pass

    def setDefaultParams(self):
        # set all the default parameters on ourself
        self.ParamSet().applyTo(self)

    def getCurrentParams(self):
        params = self.ParamSet()
        params.extractFrom(self)
        return params

    def lockParams(self):
        self._paramLockRefCount += 1
        if self._paramLockRefCount == 1:
            self._handleLockParams()
    def unlockParams(self):
        if self._paramLockRefCount > 0:
            self._paramLockRefCount -= 1
            if self._paramLockRefCount == 0:
                self._handleUnlockParams()
    def _handleLockParams(self):
        # this will store the names of the parameters that are modified
        self._paramsSet = {}
        # this will store the values of modified params (from prior to
        # the lock).
        self._priorValuesStack.append({})
    def _handleUnlockParams(self):
        for param in self._paramsSet:
            # call the applier, if there is one
            applier = getattr(self, getSetterName(param, 'apply'), None)
            if applier is not None:
                self._curParamStack.append(param)
                applier()
                self._curParamStack.pop()
        self._priorValuesStack.pop()
        if hasattr(self, 'handleParamChange'):
            self.handleParamChange(tuple(self._paramsSet.keys()))
        del self._paramsSet
    def paramsLocked(self):
        return self._paramLockRefCount > 0
    def getPriorValue(self):
        # call this within an apply function to find out what the prior value
        # of the param was
        return self._priorValuesStack[-1][self._curParamStack[-1]]

    def __repr__(self):
        argStr = ''
        for param in self.ParamSet.getParams():
            try:
                value = getSetter(self, param, 'get')()
            except:
                value = '<unknown>'
            argStr += '%s=%s,' % (param, repr(value))
        return '%s(%s)' % (self.__class__.__name__, argStr)

if __debug__ and __name__ == '__main__':
    class ParamObjTest(ParamObj):
        class ParamSet(ParamObj.ParamSet):
            Params = {
                'num': 0,
            }
        def applyNum(self):
            self.priorValue = self.getPriorValue()
    pto = ParamObjTest()
    assert pto.getNum() == 0
    pto.setNum(1)
    assert pto.priorValue == 0
    assert pto.getNum() == 1
    pto.lockParams()
    pto.setNum(2)
    # make sure applyNum is not called until we call unlockParams
    assert pto.priorValue == 0
    assert pto.getNum() == 2
    pto.unlockParams()
    assert pto.priorValue == 1
    assert pto.getNum() == 2

"""
POD (Plain Ol' Data)

Like ParamObj/ParamSet, but without lock/unlock/getPriorValue and without
appliers. Similar to a C++ struct, but with auto-generated setters and
getters.

Use POD when you want the generated getters and setters of ParamObj, but
efficiency is a concern and you don't need the bells and whistles provided
by ParamObj.

POD.__init__ *MUST* be called. You should NOT define your own data getters
and setters. Data values may be read, set, and modified directly. You will
see no errors if you define your own getters/setters, but there is no
guarantee that they will be called--and they will certainly be bypassed by
POD internally.

EXAMPLE CLASSES
===============
Here is an example of a class heirarchy that uses POD to manage its data:

class Enemy(POD):
  DataSet = {
    'faction': 'navy',
    }

class Sailor(Enemy):
  DataSet = {
    'build': HUSKY,
    'weapon': Cutlass(scale=.9),
    }

EXAMPLE USAGE
=============
s = Sailor(faction='undead', build=SKINNY)

# make two copies of s
s2 = s.makeCopy()
s3 = Sailor(s)

# example sets
s2.setWeapon(Musket())
s3.build = TALL

# example gets
faction2 = s2.getFaction()
faction3 = s3.faction
"""
class POD:
    DataSet = {
        # base class does not define any data items, but they would
        # appear here as 'name': defaultValue,
        #
        # WARNING: default values of mutable types that do not copy by
        # value (dicts, lists etc.) will be shared by all class instances.
        # if default value is callable, it will be called to get actual
        # default value
        #
        # for example:
        #
        # class MapData(POD):
        #     DataSet = {
        #         'spawnIndices': Functor(list, [1,5,22]),
        #         }
        }
    def __init__(self, **kwArgs):
        self.__class__._compileDefaultDataSet()
        if __debug__:
            # make sure all of the keyword arguments passed in
            # are present in our data set
            for arg in kwArgs.keys():
                assert arg in self.getDataNames(), (
                    "unknown argument for %s: '%s'" % (
                    self.__class__, arg))
        # assign each of our data items directly to self
        for name in self.getDataNames():
            # if a value has been passed in for a data item, use
            # that value, otherwise use the default value
            if name in kwArgs:
                getSetter(self, name)(kwArgs[name])
            else:
                getSetter(self, name)(self.getDefaultValue(name))

    def setDefaultValues(self):
        # set all the default data values on ourself
        for name in self.getDataNames():
            getSetter(self, name)(self.getDefaultValue(name))
    # this functionality used to be in the constructor, triggered by a single
    # positional argument; that was conflicting with POD subclasses that wanted
    # to define different behavior for themselves when given a positional
    # constructor argument
    def copyFrom(self, other, strict=False):
        # if 'strict' is true, other must have a value for all of our data items
        # otherwise we'll use the defaults
        for name in self.getDataNames():
            if hasattr(other, getSetterName(name, 'get')):
                setattr(self, name, getSetter(other, name, 'get')())
            else:
                if strict:
                    raise "object '%s' doesn't have value '%s'" % (other, name)
                else:
                    setattr(self, name, self.getDefaultValue(name))
        # support 'p = POD.POD().copyFrom(other)' syntax
        return self
    def makeCopy(self):
        # returns a duplicate of this object
        return self.__class__().copyFrom(self)
    def applyTo(self, obj):
        # Apply our entire set of data to another POD
        for name in self.getDataNames():
            getSetter(obj, name)(getSetter(self, name, 'get')())
    def getValue(self, name):
        return getSetter(self, name, 'get')()

    @classmethod
    def getDataNames(cls):
        # returns safely-mutable list of datum names
        cls._compileDefaultDataSet()
        return cls._DataSet.keys()
    @classmethod
    def getDefaultValue(cls, name):
        cls._compileDefaultDataSet()
        dv = cls._DataSet[name]
        # this allows us to create a new mutable object every time we ask
        # for its default value, i.e. if the default value is dict, this
        # method will return a new empty dictionary object every time. This
        # will cause problems if the intent is to store a callable object
        # as the default value itself; we need a way to specify that the
        # callable *is* the default value and not a default-value creation
        # function
        if hasattr(dv, '__call__'):
            dv = dv()
        return dv
    @classmethod
    def _compileDefaultDataSet(cls):
        if '_DataSet' in cls.__dict__:
            # we've already compiled the defaults for this class
            return
        # create setters & getters for this class
        if 'DataSet' in cls.__dict__:
            for name in cls.DataSet:
                setterName = getSetterName(name)
                if not hasattr(cls, setterName):
                    def defaultSetter(self, value, name=name):
                        setattr(self, name, value)
                    cls.__dict__[setterName] = defaultSetter
                getterName = getSetterName(name, 'get')
                if not hasattr(cls, getterName):
                    def defaultGetter(self, name=name):
                        return getattr(self, name)
                    cls.__dict__[getterName] = defaultGetter
        # this dict will hold all of the aggregated default data values for
        # this particular class, including values from its base classes
        cls._DataSet = {}
        bases = list(cls.__bases__)
        # process in reverse of inheritance order, so that base classes listed first
        # will take precedence over later base classes
        bases.reverse()
        for curBase in bases:
            # skip multiple-inheritance base classes that do not derive from POD
            if issubclass(curBase, POD):
                # make sure this base has its dict of data defaults
                curBase._compileDefaultDataSet()
                # grab all inherited data default values
                cls._DataSet.update(curBase._DataSet)
        # pull in our own class' default values if any are specified
        if 'DataSet' in cls.__dict__:
            cls._DataSet.update(cls.DataSet)

    def __repr__(self):
        argStr = ''
        for name in self.getDataNames():
            argStr += '%s=%s,' % (name, repr(getSetter(self, name, 'get')()))
        return '%s(%s)' % (self.__class__.__name__, argStr)

if __debug__ and __name__ == '__main__':
    class PODtest(POD):
        DataSet = {
            'foo': dict,
            }
    p1 = PODtest()
    p2 = PODtest()
    assert hasattr(p1, 'foo')
    # make sure the getter is working
    assert p1.getFoo() is p1.foo
    p1.getFoo()[1] = 2
    assert p1.foo[1] == 2
    # make sure that each instance gets its own copy of a mutable
    # data item
    assert p1.foo is not p2.foo
    assert len(p1.foo) == 1
    assert len(p2.foo) == 0
    # make sure the setter is working
    p2.setFoo({10:20})
    assert p2.foo[10] == 20
    # make sure modifications to mutable data items don't affect other
    # instances
    assert p1.foo[1] == 2

    class DerivedPOD(PODtest):
        DataSet = {
            'bar': list,
            }
    d1 = DerivedPOD()
    # make sure that derived instances get their own copy of mutable
    # data items
    assert hasattr(d1, 'foo')
    assert len(d1.foo) == 0
    # make sure derived instances get their own items
    assert hasattr(d1, 'bar')
    assert len(d1.bar) == 0

def clampScalar(value, a, b):
    # calling this ought to be faster than calling both min and max
    if a < b:
        if value < a:
            return a
        elif value > b:
            return b
        else:
            return value
    else:
        if value < b:
            return b
        elif value > a:
            return a
        else:
            return value

def describeException(backTrace = 4):
    # When called in an exception handler, returns a string describing
    # the current exception.

    def byteOffsetToLineno(code, byte):
        # Returns the source line number corresponding to the given byte
        # offset into the indicated Python code module.

        import array
        lnotab = array.array('B', code.co_lnotab)

        line   = code.co_firstlineno
        for i in xrange(0, len(lnotab), 2):
            byte -= lnotab[i]
            if byte <= 0:
                return line
            line += lnotab[i+1]

        return line

    infoArr = sys.exc_info()
    exception = infoArr[0]
    exceptionName = getattr(exception, '__name__', None)
    extraInfo = infoArr[1]
    trace = infoArr[2]

    stack = []
    while trace.tb_next:
        # We need to call byteOffsetToLineno to determine the true
        # line number at which the exception occurred, even though we
        # have both trace.tb_lineno and frame.f_lineno, which return
        # the correct line number only in non-optimized mode.
        frame = trace.tb_frame
        module = frame.f_globals.get('__name__', None)
        lineno = byteOffsetToLineno(frame.f_code, frame.f_lasti)
        stack.append("%s:%s, " % (module, lineno))
        trace = trace.tb_next

    frame = trace.tb_frame
    module = frame.f_globals.get('__name__', None)
    lineno = byteOffsetToLineno(frame.f_code, frame.f_lasti)
    stack.append("%s:%s, " % (module, lineno))

    description = ""
    for i in xrange(len(stack) - 1, max(len(stack) - backTrace, 0) - 1, -1):
        description += stack[i]

    description += "%s: %s" % (exceptionName, extraInfo)
    return description

import __builtin__
__builtin__.describeException = describeException
__builtin__.config = get_config_showbase()
