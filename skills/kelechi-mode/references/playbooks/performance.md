# Performance

1. Define the user-visible symptom and capture a baseline with the relevant measurement, trace, profile, or query plan.
2. Rank hypotheses by likely contribution and test them against measurements.
3. Identify the dominant path and owning boundary. Do not optimize code merely because it looks expensive.
4. Make the smallest trace-supported change and preserve correctness with targeted tests.
5. Repeat the same measurement under comparable conditions.
6. Report the before/after delta, variance, tradeoffs, and any remaining bottleneck. If measurement is inconclusive, say so.
