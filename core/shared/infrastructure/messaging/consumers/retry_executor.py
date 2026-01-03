import time
from core.shared.infrastructure.messaging.consumers.errors import RetryableError


class RetryExecutor:
    def __init__(self, policy):
        self.policy = policy

    def execute(self, handler):
        attempt = 1

        while True:
            try:
                handler()
                return  # SUCCESS
            except RetryableError as e:
                if attempt >= self.policy.max_attempts:
                    raise

                delay = self.policy.delay_for_attempt(attempt)
                print(f"[RETRY] attempt={attempt} sleeping={delay}s error={e}")
                time.sleep(delay)
                attempt += 1
