plugins = []
builtins = (
    ("monitoring.gnome_monitoring"),
    )

imports = []
for module in builtins:
    try:
        plug_module = __import__(module, globals(), locals(), [])
        imports.append(plug_module)
        
    except KeyboardInterrupt:
        raise
    except:
        continue
    
