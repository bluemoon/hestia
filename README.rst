Hestia
======

The basic idea for this project is to build a multilanguage pluggable debugger and performance analysis tool
and to keep it as user oriented as possible, enabling things like automatic rebuilding of projects and reprofiling
on demand. Keep the work "behind the curtains" and let the user get the most done.
My plans for this project have been very long term, and still are very long term. I plan to use as many external tools as possible and integrate them as tightly as i can without restricting the program design.

Core Code
---------

- [ ] Basic Gui
 - [ ] Project dialogs
 - [ ] Project language settings
 - [ ] Global settings
 - [ ] Light editor
- [ ] Modular plugins
 - [ ] Message passing for threaded plugins?
  - [ ] MPI?
  
 [ ] API for plugins
[ ] Autotests on file changes
[ ] Dynamic compiler support, cython gcc etc.
[ ] Basic error detection for the compilers [regex, whatnot]

Code coverage
-------------
figleaf: ...

Static Analysis
---------------
dehydra: https://developer.mozilla.org/en/Dehydra
YASCA: 
PyChecker: 
RATS: 

Disassemblers
-------------
obj2asm: http://www.digitalmars.com/ctg/obj2asm.html
lida: http://lida.sourceforge.net/

Memory analysis
---------------
dmalloc: ...
daikon: ...
valgrind: ...

Performance Analysis
--------------------
gprof: ...

Unit testing
------------
(python) nose: ...
(C++) cxxtest: ...
