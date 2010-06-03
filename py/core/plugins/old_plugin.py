import sys
import datetime
import time
import settings
import imp
import pprint
import traceback
#from karma import karmaModel

dispatchDictionary = {
    'modules':{
        'reload': {'function':  'plugin.plugin.reload_',
         'help':'reloads a specific module'
         },
        'load' : {'function' :  'plugin.plugin.load',
         'help':'loads a specific module'
         },
        'unload' : {'function': 'plugin.plugin.unload',
         'help' : 'unloads a specific module'
         },
        'alias' : {'function':  'plugin.plugin.alias',
         'help' : ''},
        'loaded': {'function':  'plugin.plugin.listLoaded',
         'help' : 'returns a list of loaded modules'
         }
        },
    'settings' : {
        'set':{
            'append' : {'function':'settings.settings.set_append'},
            'function': 'settings.settings.set_'
            },
        'get':{'function': 'settings.settings.get_'}
        },
    'help': {'function': 'plugin.help.runHelp'},
}

class help:
    def runHelp(self, help_input):
        p_plugin = plugin()

        commands = p_plugin.getCommands()
        common_commands = commands.copy()
        common_commands.update(dispatchDictionary)
        
        if len(help_input) == 1:
            if '.' in help_input[0]:
                help_input = help_input[0].split('.')
            else:
                help_input = [help_input[0]]
                
        if len(help_input) < 0:
            commands = map(lambda x: x, common_commands)
            return commands

        else:
            c_output = []
            try:
                c_cleanup = reduce(dict.get, help_input, common_commands)
                c_max_map = map(lambda x: len(x[0]), c_cleanup.items())
                c_max_len = reduce(lambda x, y: max(x, y), c_max_map)    
                for functions in c_cleanup:
                    if not isinstance(functions, dict):
                       c_filter = lambda x: x[0] == 'help'
                       c_map = filter(c_filter, c_cleanup[functions].items())
                       function_len = len(functions)
                       space_pad = (c_max_len - function_len) * ' '
                        
                       if len(c_map) > 0:
                           c_output.append('%s%s : %s' % (functions, space_pad, c_map[0][1]))
                       else:
                           c_output.append('%s%s : no help available' % (functions, space_pad))
                           
                    else:
                        print c_prev
                        c_output.append('%s : %s' % (pre_append, functions['help']))                    

            except Exception, e:
                print e
            if len(c_output):
                return c_output
            
class plugin:
    class __impl:
        def __init__(self):
            self.s = settings.settings()
            self.class_   = {}
            self.modules  = {}
            self.hooks    = {}
            self.commands = {}
            
        def autoLoad(self):
            ## Autoload on startup
            for auto in self.s.Get('modules.autoload'):
                self.load([auto])

        def addClass(self, _class, name):
            self.class_[name] = _class

        def getClass(self, name):
            return self.class_[name]

        def runHook(self, hook, input):
            keys = self.hooks.keys()
            dict_mapped = map(self.hooks.get, keys)

            equal = lambda x: x[0] == hook
            filtered = lambda _filter: filter(equal, _filter.items())
            try:
                other = map(filtered, dict_mapped)[0][0]
            except:
                return 

            out = []
            for hook in other[1]:
                if 'custom' in hook:
                    h_split = hook.split('.')
                    hook = h_split[:1][0]
                out.append(self.execute(hook, None,  input, hook=True))
            return out

        def listLoaded(self, plugin_):
            return self.modules.keys()

        def load(self, plugin_):
            ##  set the plugin values
            ##  from the input dispatcher
            plugin = plugin_[0]
            paths = plugin_[1:]

            try:
                ##  load this thing with the real module
                fp, pathname, desc = imp.find_module(plugin, ['plugins'])
                self.modules[plugin] = imp.load_module(plugin, fp, pathname, desc)

            except Exception, exc:
                print exc

            finally:
                if fp:
                    fp.close()

            if self.modules[plugin]:
                if 'hooks' in self.modules[plugin].__dict__:
                    for keys in self.modules[plugin].__dict__['hooks']:
                        if not self.hooks.has_key(plugin):
                            self.hooks[plugin] = {}
                        if not self.hooks[plugin].has_key(keys):
                            self.hooks[plugin][keys] = []
                        for x in self.modules[plugin].__dict__['hooks'][keys]:
                            self.hooks[plugin][keys].append(x)

                if 'commands' not in self.modules[plugin].__dict__:
                    print 'doesnt contain commands, bailing out'
                    return

                self.commands[plugin] = self.modules[plugin].__dict__['commands']
                if 'alias' in self.modules[plugin].__dict__:
                    for k, v in self.modules[plugin].__dict__['alias'].items():
                        self.alias([k,v])

                return "Plugin %s loaded!" % plugin
            else:
                return "wtf..."

        def alias(self, input):
            plugin = input[0]
            paths =  input[1:]
            value = reduce(dict.get, input[0].split('.'), self.commands)
            self.commands[paths[0]] = value

        def getCommands(self):
            return self.commands

        def unload(self, Module):
            Module = Module[0]
            try:
                del self.class_[Module]
                del self.hooks[Module]
                del self.commands[Module]
                del self.modules[Module]
                del sys.modules[Module]
            except Exception, e:
                print e

            return 'Unloaded "%s"' % Module

        def reload_(self, module):
            module = module[0]
            try:
                del self.class_[module]
                del self.hooks[module]
                del self.modules[module]
                del self.commands[module]
                del sys.modules[module]
            except Exception, e:
                print e

            self.load([module])
            return 'Reloaded "%s"' % module

        def getModule(self, module):
            if self.modules.has_key(module):
                return self.modules[module]
            else:
                return False

        def dispatch(self, input, params):
            other = self.getCommands()
            try:
                ##print "dictionary:", dispatchDictionary
                ##print "input:", input
                ##print "value:", value
                value = reduce(dict.get, input, dispatchDictionary)
                if value == None:
                    value = reduce(dict.get, input, other)

            except (TypeError), e:
            ## empty
                try:
                    print "other:", other
                    value = reduce(dict.get, input, other)
                    print value
                    if value == None:
                        return None
                except (TypeError), e:
                    return e
            

            #return e
            key = input[0]
            if 'function' not in value:
                return

            if key not in value:
                if 'function' not in value:
                ## no function key
                    return
                if value['function'] is None:
                ## empty
                    return

                return self.execute(value['function'], input, params)

            ##  otherwise
            elif key in value:
                if 'function' not in value[key]:
                ## no function key
                    return
                if value[key]['function'] is None:
                ## empty
                    return

                return self.execute(value[key]['function'], input, params)

        def execute(self, command, input, params, hook=False):
            is_plugin = False
            cSplit = command.split('.')
            try:
                __import__(cSplit[:1][0])
            except ImportError, e:
                print "Import attempt 1:", e
            try:
                module = self.getModule(cSplit[1:2][0])
                if hook:
                    module = sys.modules[cSplit[1:2][0]]
                elif not module:
                    module = sys.modules[cSplit[:1][0]]
                else:
                    is_plugin = True
            except Exception, e:
                try:
                    module = sys.modules[cSplit[:1][0]]
                except Exception, e:
                    print "import attempt 2:", e
                    return

            if not is_plugin:
                module_name = cSplit[0]
                class_name  = '.'.join(cSplit[1:-1])
                func_name   = cSplit[-1]

                ## create an instance
                try:
                    Class = self.r_getattr(module, class_name)
                    if not self.class_.has_key(module_name):
                        self.class_[module_name] = {}
                    if not self.class_[module_name].has_key(class_name):
                        self.class_[module_name][class_name] = Class()

                    function = self.r_getattr(self.class_[module_name][class_name], func_name) 
                    output = function(params)

                except Exception, e:
                    exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                    print "*** print_tb:"
                    traceback.print_tb(exceptionTraceback, file=sys.stdout)
                    
                    print "Class attempt 1:", e
                    print "module_name:", module_name
                    print "class_name:", class_name
                    print "func_name:", class_name
                    
                    return
                
                return output
            else:
                module_name = cSplit[0]
                class_name  = '.'.join(cSplit[2:-1])
                func_name   = '.'.join(cSplit[-1:])
                ## create an instance
                try:
                    Class = self.r_getattr(module, class_name)
                    if not self.class_.has_key(module_name):
                        self.class_[module_name] = {}
                    if not self.class_[module_name].has_key(class_name):
                        self.class_[module_name][class_name] = Class()

                    function = self.r_getattr(self.class_[module_name][class_name], func_name) 
                    output = function(params)
                except Exception, e:
                    print "Class attempt 2:", e
                    return
                
                return output

        def r_getattr(self, object, attr):
            return reduce(getattr, attr.split('.'), object)

        def r_setattr(self, object, attr, value):
            attrs = attr.split('.')
            return setattr(reduce(getattr, attrs[:-1], object), attrs[-1], value)

        def add(self):
            pass

        def remove(self, item):
            del self.class_[item]
        
    __instance = None
    
    def __init__(self):
        """ Create singleton instance """
        # Check whether we already have an instance
        if plugin.__instance is None:
            # Create and remember instance
            plugin.__instance = plugin.__impl()
            # Store instance reference as the only member in the handle
            self.__dict__['_plugin__instance'] = plugin.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
    #def getSuper(self):
    #    print type(plugin)
    #    print type(plugin())
    #    print plugin().__class__.__name__
    #    print plugin().__class__
    #    return super(plugin, self)
