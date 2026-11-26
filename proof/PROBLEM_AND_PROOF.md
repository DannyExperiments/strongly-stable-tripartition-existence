# Problem and proof

A three-level source ranking is strongly stable if every preferred merge induces that same ranking. The existence decision asks whether any such ranking exists. [Liberatore's original question](https://www.jair.org/index.php/jair/article/download/11238/26438#page=51)

1. Truth sets of valuations encode the preferred merges. The first priority block where two truth sets differ decides strict dominance if one strictly contains the other there.
2. For membership in Σ₃ᴾ, guess a ranking. Every valuation that would induce a different ranking must have a dominating valuation, because an undominated one would supply a destabilizing outcome.
3. Reduce from ∃x∀y∃z quantified satisfiability. The top priority class pins x. For each y there are Good and Bad modes plus a Repair mode available exactly when the matrix has a witness z.
4. Repair keeps A and adds C ahead of the Bad modes' distinguishing markers. Hence both Bad modes are eliminated precisely when the repair exists. An always-available Good mode rules out the alternative ranking induced by the Bad modes.

The construction answers existence if and only if the quantified formula is true. It also supplies the base reduction of the separate skeptical-consequence problem. [Full proof](../paper/manuscript.pdf) · [Q622 companion](https://doi.org/10.5281/zenodo.24572374)
