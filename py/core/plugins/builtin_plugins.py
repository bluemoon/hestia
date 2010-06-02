"""
List of builtin plugins.
"""

plugins = []
builtins = (
#    ("plugins.network_bridged", "NetworkBridged"),
#    ("plugins.storage_directory", "StorageDirectory"),
#    ("plugins.storage_iscsi", "StorageISCSI"),
    )

for module, cls in builtins:
    try:
        plugmod = __import__(module, globals(), locals(), [cls])
    except KeyboardInterrupt:
        raise
    except:
        continue
    plug = getattr(plugmod, cls)
    plugins.append(plug)
    globals()[cls] = plug
