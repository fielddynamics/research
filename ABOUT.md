# About the author

*Where Gravity Field Dynamics came from: the idea of field closure.*

I'm a tech engineer with an interest in theoretical physics, and this whole body of work grew from one idea: **field closure**.

My working life has been spent building enterprise systems, including encryption systems for government. In that world, state has to close. A transaction either settles or it does not; there is no half-committed balance, and nothing is allowed to go unaccounted for. When I began thinking about gravity, I kept returning to the same question: if reality is informational at bottom, how could it keep its books any other way?

The requirement that a field must close is not my invention. Most tetrad formalisms carry it already, and general relativity enforces it: the tetrad must be non-degenerate, $\det(e) \neq 0$, with four independent directions defined at every point, and the constraint equations must hold on every slice before the field can evolve. Paper VII sets this out in its section *Field Closure: The Requirement GR Already Enforces*. What I have tried to do is take that requirement seriously as a process and follow where it leads.

That process is my answer to the question. Every part of a field has neighbours, and before the field can move on, each part must read its neighbours and settle with them into one consistent state, much as accounts settle in a transaction. Paper I names the steps: at the closure boundary the field *reads*, then *settles*, and the settled result is *registered*.

The point I most want a reader to take from this is why that sequence cannot be interrupted. A closure boundary is not private. Paper I is explicit that the boundary belongs to neither side; it is the interface the two share. Paper II shows that once closures are packed together, each one shares part of its boundary with every neighbour it touches. So when a field begins to close, the information it is reading sits partly on a surface that a neighbour also owns.

Now suppose a field gets halfway through closure, having read that shared surface, and before it settles the neighbour changes what is on it. The field would then settle against a state that no longer exists. Whatever it registers is either out of step with its neighbour across their common boundary, or it overwrites the neighbour's change. In both cases information the field was responsible for has been lost, and the closure is lossy. Paper I shows what lossy closure would look like: wakes behind moving bodies, drag, hysteresis, and errors accumulating over cosmic time. None of these are observed, which is why Paper I takes lossless closure as an empirical constraint rather than a preference.

So closure has to be atomic in the full sense an engineer means. It is not enough that the result is all or nothing. The state being read must also hold still until the result is recorded: nothing a field shares with its neighbours may change part-way through its closure. That is what Paper I means by settlement being consistent "across all interfaces simultaneously", and it is why the read has to be a snapshot. A snapshot is a read that cannot change underneath you while you settle against it. Read, settle and register as one indivisible step is what I call snapshot accounting, and it is the only way I can see an informational reality being managed. The papers here follow what that requirement implies, from the constitutive law that shapes galaxy rotation to the value of Newton's constant.

What you will find here is as far as I have been able to take the idea on my own, and I offer it humbly. I have worked on it independently, and it now needs what every piece of science needs: careful peer review by others. That is why I have opened everything up, the papers, the code, the working notes and even the dead ends. If the idea sparks your interest, I hope you will make use of it, look at it closely, and tell me where it holds and where it does not.

If you do, I would be glad to hear from you. Checks of the derivations, re-analyses of the data, errors found, assumptions questioned, or ideas for taking it further are all welcome, and a well-founded criticism is as valuable to me as a confirmation. You can reach me at stephen@fielddynamics.org, or open an issue on this repository.

— Stephen Nelson
