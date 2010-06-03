global imports
builtins = (
    ("py.monitoring.monitor"),    
)


imports = []
for module in builtins:
    try:
        loaded_module = __import__(module, globals(), locals(), [])
        for i in module.split(".")[1:]:
            loaded_module = getattr(loaded_module, i)
        imports.append(loaded_module)

    except KeyboardInterrupt:
        raise

    except Exception, E:
        print E
        continue

