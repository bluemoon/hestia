plugins = []
builtins = (
    ("monitoring.gnome_monitoring"),
    )

for module in builtins:
    try:
        plug_module = __import__(module, globals(), locals(), [])
    except KeyboardInterrupt:
        raise
    except:
        continue
    
