# Reproducibility

From the repository root, with Python 3.11 or later and Git:

~~~sh
python3 -I scripts/verify_repository.py
python3 -I verification/src/replay.py
~~~

The standard-library replay checks all 256 truth tables with one bit per QBF block. It computes maxcons directly by inclusion at each prefix. It checks existence and the surviving modes for all 1,024 outer-choice/universal-challenge combinations, and verifies why the rival ranking cannot be strongly stable. It separately checks the displayed repair witnesses and the behavior of a formula shared across priority classes. [Expected output](verification/logs/replay.txt)

The replay checks finite instances. The manuscript proves the result for arbitrary explicit propositional sources and gives the padding argument used in the reduction. [Build the paper](paper/BUILD.md) · [Rebuild the figure and open the explorer](visualization/README.md)
