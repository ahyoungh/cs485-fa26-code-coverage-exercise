# Code Coverage Exercise: `PrimeFinder`

This project tests `primes/prime_finder.py` with pytest and measures coverage with PyCharm's "Run with Coverage". The final result is **100% line and branch coverage**.

## Starting point

The original tests brought `prime_finder.py` to **73%** coverage (9 missing statements, 3 partially covered branches). The original tests only covered `is_prime(0)` and `is_prime(1)`, and invalid and valid lengths for `list_first_n_primes`.

## Branches that were untested

1. `__init__`: `if initial_limit < 1 or not isinstance(initial_limit, int)` -> **True** outcome (`raise ValueError`)
2. `is_prime`: `if n > self._limit` -> **True** outcome (call to `_extend_sieve`)
3. `_extend_sieve`: method body never executed, so none of its branches ran
   1. `for num in range(2, int(new_limit ** 0.5) + 1)` -> loop body
   2. `if self._sieve[num]` -> **True** outcome (mark multiples as not prime)
   3. `if self._sieve[num]` -> **False** outcome (skip composite `num`)
4. `list_first_n_primes`: `if self.is_prime(n)` -> **False** outcome (see the note below)

## Tests added

All of the new tests are in `tests/test_prime_finder.py`.

- `TestInit.test_raises_value_error_given_invalid_limit` (parametrized with `0` and `-1`)
  - covers branch 1
- `TestIsPrime.test_returns_true_given_a_prime_within_limit`
  - covers the prime results of `is_prime` inside the default limit of 1000
- `TestIsPrime.test_returns_false_given_a_composite_within_limit`
  - covers the composite results of `is_prime` inside the default limit of 1000
- `TestIsPrime.test_extends_sieve_and_classifies_given_n_above_limit` (parametrized with `1009` and `1010`)
  - covers branches 2, 3.1, 3.2 and 3.3
- `TestFirstNPrimes.test_has_correct_number_of_elements_given_a_valid_length` (existing test)
  - covers branch 4, once `n += 1` is added

## Results

Final coverage report (coverage.py v7.16.1, branch coverage enabled, generated 2026-09-18):

| File | Statements | Missing | Branches | Partial | Coverage |
|---|---|---|---|---|---|
| `primes/__init__.py` | 0 | 0 | 0 | 0 | 100% |
| `primes/prime_finder.py` | 38 | 0 | 20 | 0 | 100% |
| `tests/__init__.py` | 0 | 0 | 0 | 0 | 100% |
| `tests/test_prime_finder.py` | 34 | 0 | 0 | 0 | 100% |
| **Total** | **72** | **0** | **20** | **0** | **100%** |

For `primes/prime_finder.py`, the coverage before and after:

| | Statements missing | Branches partial | Coverage |
|---|---|---|---|
| Before | 9 | 3 | 73% |
| After | 0 | 0 | 100% |

All 18 tests pass.

## Note: the increment in the `while` loop

`list_first_n_primes` originally had no `n += 1`, so `n` stayed at 2 for the whole loop:

```python
n = 2
while len(primes) < length:
    if self.is_prime(n):
        primes.append(n)
    # n was never incremented
```

Each pass appended 2 again, so the loop still ended once the list reached `length`. The function returned `[2, 2, 2, ...]` instead of the first primes. The existing length tests still passed because they only check `len(...)`. The bug also made the `if self.is_prime(n)` line partially covered, because `is_prime(2)` was always `True`, so the False outcome could never happen.

The fix is to add `n += 1` at the end of the `while` loop body, at the same indentation as the `if`:

```python
while len(primes) < length:
    if self.is_prime(n):
        primes.append(n)
    n += 1
```

The increment must be outside the `if`, so `n` advances after every candidate, prime or not. With it, non-primes such as 4 are skipped, which covers the False branch. The `length=1000` test also reaches 7919, which exercises `_extend_sieve` through `list_first_n_primes`.