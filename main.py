"""Compare algorithms that solve an instance of the subset-sum problem."""

from pathlib import Path
import argparse
from itertools import combinations


def read_instance(path: str | Path) -> tuple[int, list[int]]:
    """Read a target and a list of integers from a text file."""
    lines = [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines()]
    lines = [line for line in lines if line and not line.startswith("#")]

    if not lines:
        raise ValueError("the input file is empty")

    first = lines[0]
    if ":" in first:
        first = first.split(":", 1)[1].strip()
    target = int(first)
    numbers = [int(line) for line in lines[1:]]
    return target, numbers


def brute_force_subset_sum(numbers: list[int], target: int) -> bool:
    """Test every subset; worst-case time complexity is O(2^n)."""
    for size in range(len(numbers) + 1):
        for subset in combinations(numbers, size):
            if sum(subset) == target:
                return True
    return False


def dynamic_subset_sum(numbers: list[int], target: int) -> bool:
    """Use pseudo-polynomial dynamic programming for non-negative integers."""
    if target < 0:
        return False

    reachable = [False] * (target + 1)
    reachable[0] = True
    for number in numbers:
        if number < 0:
            return brute_force_subset_sum(numbers, target)
        for total in range(target, number - 1, -1):
            if reachable[total - number]:
                reachable[total] = True
    return reachable[target]


def meet_in_the_middle_subset_sum(numbers: list[int], target: int) -> bool:
    """Split the input and enumerate 2^(n/2) subsets on each side."""
    midpoint = len(numbers) // 2
    left = numbers[:midpoint]
    right = numbers[midpoint:]

    def subset_sums(values: list[int]) -> set[int]:
        sums = {0}
        for value in values:
            sums |= {total + value for total in tuple(sums)}
        return sums

    right_sums = subset_sums(right)
    return any(target - total in right_sums for total in subset_sums(left))


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare subset-sum algorithms")
    parser.add_argument(
        "input",
        nargs="?",
        default="data.txt",
        help="text file containing the target on the first line (default: data.txt)",
    )
    args = parser.parse_args()

    target, numbers = read_instance(args.input)
    algorithms = (
        ("Brute force", brute_force_subset_sum),
        ("Dynamic programming", dynamic_subset_sum),
        ("Meet in the middle", meet_in_the_middle_subset_sum),
    )

    print(f"Target: {target}")
    print(f"Numbers: {numbers}")
    for name, algorithm in algorithms:
        print(f"{name}: {'found' if algorithm(numbers, target) else 'not found'}")


if __name__ == "__main__":
    main()
