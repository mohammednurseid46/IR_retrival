import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.indexing.index_builder import IndexBuilder


if __name__ == '__main__':
    IndexBuilder().build_indexes()
    print('Index build complete.')
