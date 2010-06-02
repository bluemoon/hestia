"""
## Todo:
##  create a document specifying the usage and styling of the plugin design

Python Plugin Framework
=======================
## There should only be 2 styles of plugins
##  1) a module with a class that specifies setup/teardown or subclasses Plugin
##  2) a module that has only functions to be used with setup/teardown as functions
##     but does not require setup nor teardown

This framework should provide:
  - Some commonly used plugin managers
  
To use one of them, just::

  from core.plugins import DefaultPluginManager

  manager = DefaultPluginManager()
  manager.loadPlugins()
  plugins = manager.getPlugins()
  
  # After some plugin change, refresh them
  manager.plguins = []
  manager.loadPlugins()
  plugins = manager.getPlugins()


Register plugins
----------------

Important note: different plugin managers may use different means to locate and
load plugins.

For L{EntryPointPluginManager}, it must be part of a package that uses
setuptools, and the plugin must be included in the entry points defined in the
setup.py for the package::

  setup(name="Some plugin",
        ...
        entry_points = {
            "package.plugins": [
                "someplugin = someplugin:SomePlugin"
                ]
            },
        ...
        )

Once the package is installed with install or develop, nose will be able
to load the plugin.

For L{DirectoryPluginManager}, it must be placed under directory C{plugins/}.
Every plugin file should have a C{__all__} attribute containing the implemented
plugin class.

Use plugins
-----------

After you have written you plugin and registered into the framework, the plugin
manager should be able to load it. Then you can get a proxy of your plugin
and call the implemented APIs defined in the interface::

  from pkg.plugins.manager import PluginProxy

  try:
      plugin = PluginProxy("interface", "name")
  except NotImplementedError:
      # exception handling
  # call plugin method
  plugin.method(args)

"""
import os
import re
import sys
import logging
import threading

from warnings import warn
from imp import find_module, load_module, acquire_lock, release_lock
import inspect
import textwrap



class Plugin(object):
    """Base class for plugins.

    Plugins should not be enabled by default.

    @cvar name: name
    @type name: C{str}
    @cvar description: description
    @type description: C{str}
    @cvar vendor: vendor
    @type vendor: C{str}
    @cvar copyright: copyright
    @type copyright: C{str}
    @cvar plugin_version: plugin version info. A tuple containing the five
        components of the version number: major, minor, micro, releaselevel,
        and serial. All values except releaselevel are integers; the release
        level is 'alpha', 'beta', 'candidate', or 'final'. The version value
        corresponding to 0.0.1 is (0, 0, 1, 'final', 0).
    @type plugin_version: C{tuple}
    @cvar required_api_version: required api version info
    @type required_api_version: C{tuple}
    @cvar supported_products: supported products
    @type supported_products: C{dict}
    @cvar interface: implemented interface
    @type interface: C{str}
    @cvar configuration: configuration options
    @type configuration: C{dict}
    #@cvar capabilities: implemented methods
    #@type capabilities: C{list}
    #@cvar enabled: enabled
    #@type enabled: C{bool}
    #@cvar configurable: configurable
    #@type configurable: C{bool}
    """
    name = None
    interface = ""
    description = ""
    vendor = ""
    copyright = ""
    plugin_version = ()
    required_api_version = ()
    supported_products = {}
    configuration = {}
    #capabilities = []
    #enabled = False
    #configurable = False

    def __init__(self):
        pass

    @classmethod
    def help(cls):
        """Return help for this plugin.
        """
        if cls.__class__.__doc__:
            # doc sections are often indented; compress the spaces
            return textwrap.dedent(cls.__class__.__doc__)
        return "(no help available)"

    @classmethod
    def caps(cls):
        """Return capabilities of this plugin.
        """
        return [attr
                for attr in dir(cls)
                if inspect.ismethod(getattr(cls, attr)) and \
                   attr in pkg.plugins.interface.get_caps(cls.interface)]



log = logging.getLogger("pkg.plugins.manager")


