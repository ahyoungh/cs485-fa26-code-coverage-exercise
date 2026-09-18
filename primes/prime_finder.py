class PrimeFinder:
    def __init__(self, initial_limit=1000):
        if initial_limit < 1 or not isinstance(initial_limit, int):
            raise ValueError("Initial limit must be a positive integer!")

        # Initialize the sieve up to the initial limit
        self._limit = initial_limit
        self._sieve = self._generate_sieve(self._limit)

    def is_prime(self, n):
        """ Returns True if n is a prime number, False otherwise """
        if n < 2:
            return False

        # If n exceeds the current limit, extend the sieve up to n
        if n > self._limit:
            self._extend_sieve(n)

        return self._sieve[n]

    def list_first_n_primes(self, length=50):
        """ Returns a list of first prime numbers (up to a given length) """

        if length < 1 or not isinstance(length, int):
            raise ValueError("Length must be a positive integer!")

        # list of primes
        primes = []

        # candidate number to check for primality
        n = 2

        # loop until we have enough primes in the list
        while len(primes) < length:
            if self.is_prime(n):
                primes.append(n)
            n += 1

        return primes

    @staticmethod
    def _generate_sieve(limit):
        # a private helper method that returns all primes up to a given limit using the "Sieve of Eratosthenes"
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False  # 0 and 1 are not prime numbers

        for num in range(2, int(limit ** 0.5) + 1):

            # if num is prime, then mark all multiples of num as not prime
            if sieve[num]:
                sieve[num * num: limit + 1: num] = [False] * len(range(num * num, limit + 1, num))

        return sieve

    def _extend_sieve(self, new_limit):
        # a private helper method that extends the sieve up to a new_limit
        old_limit = self._limit

        # extend the sieve list with True values for new indices
        self._sieve.extend([True] * (new_limit - self._limit))
        self._limit = new_limit

        # update sieve for numbers between old_limit and new_limit
        for num in range(2, int(new_limit ** 0.5) + 1):

            # if the number is prime, mark all multiples of num as not prime
            if self._sieve[num]:
                # calculate the starting point for marking multiples
                start = max(num ** 2, ((old_limit + num - 1) // num) * num)
                self._sieve[start: new_limit + 1: num] = [False] * len(range(start, new_limit + 1, num))
