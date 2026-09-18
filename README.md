# Code Coverage Exercise: `PrimeFinder`

This project tests `primes/prime_finder.py` with pytest and measures coverage with PyCharm's "Run with Coverage". The final result is **100% line and branch coverage**.

## Starting point

The original tests brought `prime_finder.py` to **73%** coverage (9 missing statements, 3 partially covered branches). The original tests only covered `is_prime(0)` and `is_prime(1)`, and invalid and valid lengths for `list_first_n_primes`.

## Branches that were untested

| Location | What was untested |
|---|---|
| `PrimeFinder.__init__` | The `if initial_limit < 1 or not isinstance(...)` condition was never true, so the `raise ValueError` never ran. |
| `PrimeFinder.is_prime` | The `if n > self._limit` condition was never true, so `_extend_sieve` was never called. |
| `PrimeFinder._extend_sieve` | The entire method was unreached, because it is only called from the branch above. |
| `PrimeFinder.list_first_n_primes` | The `if self.is_prime(n)` line was only partially covered: its False outcome never happened (see the note below). |

## Tests added

All of the new tests are in `tests/test_prime_finder.py`.

| Test | Covers |
|---|---|
| `TestInit.test_raises_value_error_given_invalid_limit` (parametrized with `0` and `-1`) | The `ValueError` in `__init__`. |
| `TestIsPrime.test_returns_true_given_a_prime_within_limit` and `test_returns_false_given_a_composite_within_limit` | The True and False results of `is_prime` for numbers inside the default limit of 1000. |
| `TestIsPrime.test_extends_sieve_and_classifies_given_n_above_limit` (parametrized with `1009` and `1010`) | The `n > self._limit` branch and every line of `_extend_sieve`, including both outcomes of its `if self._sieve[num]` check. |

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
