import unittest
import sys
import os



# 加載所有測試
loader = unittest.TestLoader()
start_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests')
suite = loader.discover(start_dir, pattern='test_*.py')

# 運行測試
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite) 