# Intra-sector Comovement

An informal analysis on intra-sector pair price reversions.

## Oversight

For some market sector $M$, we can think of it as a collection of equities $E_i$, where each $E_i$ serves the same sector of the economy:

$$
M := \set{ E_1, E_2, ..., E_n }
$$

Equities inside $M$ do not contribute equally to $M$'s performance. For instance, if $\text{MarketCap}(E_m) > \text{MarketCap}(E_n)$, we can generally assume that $E_m$ contributes more to market sector $M$ than $E_n$ does.

In every market sector $M$, there exists at least one sector leader $L$ who's market cap is substantially larger than the average market cap of an equity $E \in M$. Conversely, in every market sector $M$, there exists at least one sector follower $F$ who's market cap is smaller than that of the average market cap for an equity in $M$. 

## Key Rationale & Methods

The general rational is that the price $P_F$ of a sector follower equity $F \in M$ reacts in accordance to the overall sector, where the performance of the overall sector is heavily determined by sector leaders $L_1, L_2, ..., L_q \in M$. With this logic, we can write that that:

$$
\Delta P_F \propto \Delta P_L \text{ , during some } [a,b] \in [t_{min}, t_{max}]
$$

In an optimal system, we can write:

$$
P_F(t_j) - P_F(t_i) = \frac{1}{r} (P_L(t_j) - P_L(t_i)) \text{ , } r \in \mathbb{R}
$$

Using an index scale, we can remove our proportion coefficient. Define $\phi: \mathbb{R} \to \mathbb{R^+}$ as,

$$
\phi(t) = \frac{P(t)}{P(t_0)} \cdot p
$$

, for our scale value $p \in \mathbb{R}$. Still inside our Eutopian system, we would have that $\phi_F(t) = \phi_L(t)$ for all $t \in [t_{min}, t_{max}]$. 

## Hypothesis

Define our divergence bias to be a number $D$ such that if $|\phi_L(t) - \phi_F(t)| > D$, then $L$ and $F$ are diverging at time $t$ ($\phi_L$ and $\phi_F$ are diverging at time $t$). If $\partial D > 0$ on $[a,b]$, then $L$ and $F$ are in a diverging state on $[a,b]$.

**As $D$ increases, the probability that $L$ and $F$ will reconverge increases.**

$$
\text{(H1) }\large{\partial D > 0 \text{ on } [t_i, t_j] \implies \text{P}(|\phi_L(t_{j+1}) - \phi_F(t_{j+1})| < |\phi_L(t_j) - \phi_F(t_j)|) \to 1}
$$

## Divergent States as Area
Although market prices are discrete, we can generalize the notion of a diverging state to an area. Let a non-diverging state $\text{NonDiv}$ be an interval $[t_i, t_j]$ where $|\phi_L(t) - \phi_f(t)| < D \text{ for all } t \in \text{NonDiv}$. We can define the following:

$$

$$


