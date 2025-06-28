""" Blacklist of words for the parser to check.

Note: 
- "os" is not banned as "cos" is a valid function
- "as" is not banned as "asin" is a valid function
"""

BANNED = ['config', 'sympy', 'env',
          # Dangerous built-ins
          'open', 'file', 'read', 'write', 'delete', 'remove',
          'system', 'subprocess', 'call', 'popen',
          'globals', 'locals', 'vars', 'dir', 'getattr', 'setattr',
          'compile', 'exec', 'eval', 'input', 'raw_input',
          # File operations
          'chdir', 'mkdir', 'rmdir', 'listdir', 'walk',
          'copy', 'move', 'rename', 'link', 'symlink',
          # Network operations
          'socket', 'urllib', 'requests', 'http', 'ftp',
          'urlopen', 'urlretrieve',
          # Process operations
          'kill', 'terminate', 'spawn', 'fork', 'thread',
          'multiprocessing', 'concurrent', 'asyncio',
          # Database operations
          'sqlite', 'mysql', 'postgresql', 'database',
          # Shell operations
          'shell', 'bash', 'cmd', 'powershell', 'terminal', 'echo',
          'python', 'py', 'pip', 'venv',
          # Memory operations
          'memory', 'malloc', 'free', 'collect',
          # Reflection/metaprogramming
          'inspect', 'getframe', 'currentframe', 'traceback',
          'marshal', 'pickle', 'dill', 'cloudpickle',
          # Other dangerous patterns
          'import', 'lambda', 'yield', 'async', 'await',
          'class', 'try', 'except', 'finally',
          'with', 'from', 'raise', 'assert', 'exit', 'quit']
