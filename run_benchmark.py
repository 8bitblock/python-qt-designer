import time
import timeit

baseline = """
elements = [{'id': i, 'name': f'El {i}'} for i in range(10000)]
selectedId = 9999
result = next((e for e in elements if e['id'] == selectedId), None)
"""

print(f"Python Equivalent Baseline (10,000 items, 10,000 runs):", timeit.timeit(baseline, number=10000))
