
class ShellPluginManager(PluginManager):
    """Plugin manager that loads shell script plugins from plugin directories.
    """
    name = "shell"

    info_begin_re = re.compile(r"^### BEGIN PLUGIN INFO\s*$")
    info_end_re = re.compile(r"^### END PLUGIN INFO\s*$")
    info_line_re = re.compile(r"^# (?P<key>[^\s:]+):\s*(?P<value>.*\S)\s*$")
    info_line_plugin_version_re = re.compile(r"^# plugin_version:\s*(?P<value>.*\S)\s*$")
    info_line_required_api_version_re = re.compile(r"^# required_api_version:\s*(?P<value>.*\S)\s*$")
    info_line_conf_re = re.compile(r"^# configuration\s+(?P<key>[^\s:]+):\s*"
                                    "(?P<value>.*\S)\s*$")
    info_line_cont_re = re.compile(r"^#(\t|  )\s*(?P<cont>.*)$")

    def __init__(self, plugins=(), config={}):
        default_directory = os.path.join(os.path.dirname(
                                find_module("pkg")[1]), "pkg", "plugins")
        self.directories = config.get("directories", (default_directory,))
        PluginManager.__init__(self, plugins, config)

    def _get_version(self, value):
        """Change the dot separated string version to tuple.
        """
        version = []
        index = 0
        for val in value.split("."):
            if index > 4:
                break
            if index == 3:
                if val in ['alpha', 'beta', 'candidate', 'final']:
                    version.append(val)
                else:
                    log.warn("Invalide releaselevel: %s" % e)
                    return
            else:
                try:
                    version.append(int(val))
                except TypeError, e:
                    log.warn("Invalide version: %s" % e)
                    return
            index += 1
        return tuple(version)

    def _parse(self, file):
        fd = open(file)
        plug = Plugin()
        info_begin = False
        key = None
        value = None
        syntax_error = False
        # FIXME: Plugin.configuration is a class variable and in mutable type.
        # So we need bind it to the local namespace first to avoid affecting
        # other subclasses.
        plug.configuration = {}
        for line in fd:
            if not line.startswith("#"):
                if not info_begin:
                    continue
                else:
                    syntax_error = True
                    log.warn("Parse error: %s", line)
                    break
            if self.info_begin_re.match(line):
                info_begin = True
                continue
            if info_begin:
                if self.info_end_re.match(line):
                    break
                m = self.info_line_plugin_version_re.match(line)
                if m:
                    value = m.group("value")
                    version = self._get_version(value)
                    if not version:
                        syntax_error = True
                        break
                    setattr(plug, "plugin_version", version)
                    continue
                m = self.info_line_required_api_version_re.match(line)
                if m:
                    value = m.group("value")
                    version = self._get_version(value)
                    if not version:
                        syntax_error = True
                        break
                    setattr(plug, "required_api_version", version)
                    continue
                m = self.info_line_re.match(line)
                if m:
                    key = m.group("key")
                    value = m.group("value")
                    setattr(plug, key, value)
                    continue
                m = self.info_line_conf_re.match(line)
                if m:
                    key = m.group("key")
                    value = m.group("value")
                    plug.configuration[key] = value
                    continue
                m = self.info_line_cont_re.match(line)
                if m:
                    value = " ".join((value, m.group("cont")))
                    if key in plug.configuration:
                        plug.configuration[key] = value
                    elif key in dir(plug):
                        setattr(plug, key, value)
                    else:
                        syntax_error = True
                        log.warn("Parse error: %s", line)
                        break
                    continue
                # exception found
                syntax_error = True
                log.warn("Parse error: %s", line)
                break
        fd.close()
        # name and interface are required
        if not syntax_error and plug.name and plug.interface:
            return plug

    def loadPlugins(self):
        """Load plugins by iterating shell script files in plugin directories.
        """
        for dir in self.directories:
            try:
                file_list = os.listdir(dir)
            except OSError, e:
                log.warn("Failed to list dir: %s" % e)
                continue
            for f in os.listdir(dir):
                plug = self._parse(os.path.join(dir, f))
                if not plug:
                    continue
                self._loadPlugin(plug)

