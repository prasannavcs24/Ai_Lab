class Term:
    """Represents a term: either a Variable or a Constant."""
    def __init__(self, name: str, is_var: bool = False):
        self.name = name
        self.is_var = is_var

    def __repr__(self):
        return f"?{self.name}" if self.is_var else self.name

    def __eq__(self, other):
        return isinstance(other, Term) and self.name == other.name and self.is_var == other.is_var

    def __hash__(self):
        return hash((self.name, self.is_var))


class Literal:
    """Represents an atomic predicate sentence, e.g., Criminal(West)."""
    def __init__(self, predicate: str, terms: list[Term]):
        self.predicate = predicate
        self.terms = terms

    def __repr__(self):
        return f"{self.predicate}({', '.join(map(str, self.terms))})"

    def __eq__(self, other):
        return (isinstance(other, Literal) and 
                self.predicate == other.predicate and 
                self.terms == other.terms)

    def __hash__(self):
        return hash((self.predicate, tuple(self.terms)))


class Rule:
    """Definite Clause Rule: premises => conclusion."""
    def __init__(self, premises: list[Literal], conclusion: Literal):
        self.premises = premises
        self.conclusion = conclusion

    def __repr__(self):
        return f"{' ^ '.join(map(str, self.premises))} => {self.conclusion}"


# --- UNIFICATION & SUBSTITUTION HELPERS ---

def apply_subst(subst: dict[str, Term], literal: Literal) -> Literal:
    """Applies a substitution dictionary to a literal."""
    new_terms = []
    for term in literal.terms:
        if term.is_var and term.name in subst:
            new_terms.append(subst[term.name])
        else:
            new_terms.append(term)
    return Literal(literal.predicate, new_terms)


def unify_literals(l1: Literal, l2: Literal, theta: dict[str, Term] = None) -> dict[str, Term] | None:
    """Unifies two literals under a current substitution context."""
    if theta is None:
        theta = {}

    if l1.predicate != l2.predicate or len(l1.terms) != len(l2.terms):
        return None

    subst = dict(theta)
    for t1, t2 in zip(l1.terms, l2.terms):
        while t1.is_var and t1.name in subst:
            t1 = subst[t1.name]
        while t2.is_var and t2.name in subst:
            t2 = subst[t2.name]

        if t1 == t2:
            continue
        elif t1.is_var:
            subst[t1.name] = t2
        elif t2.is_var:
            subst[t2.name] = t1
        else:
            return None

    return subst


# --- FORWARD CHAINING ALGORITHM ---

def fol_fc_ask(facts: set[Literal], rules: list[Rule], query: Literal) -> dict[str, Term] | bool:
    """
    Executes Forward Chaining over First-Order Logic facts and rules.
    Returns the binding substitution dictionary if query is proven, else False.
    """
    known_facts = set(facts)

    # Initial test: is the query already a known fact?
    for fact in known_facts:
        subst = unify_literals(fact, query)
        if subst is not None:
            return subst

    step = 1
    while True:
        new_facts = set()
        print(f"--- Iteration {step} ---")

        for rule in rules:
            def match_premises(premise_idx: int, current_subst: dict[str, Term]):
                if premise_idx == len(rule.premises):
                    inferred = apply_subst(current_subst, rule.conclusion)
                    if inferred not in known_facts:
                        # Store substitution as frozenset to remain hashable inside sets
                        subst_tuple = frozenset(current_subst.items())
                        new_facts.add((inferred, subst_tuple))
                    return

                target_premise = apply_subst(current_subst, rule.premises[premise_idx])
                for fact in known_facts:
                    subst = unify_literals(target_premise, fact, current_subst)
                    if subst is not None:
                        match_premises(premise_idx + 1, subst)

            match_premises(0, {})

        if not new_facts:
            print("No new facts can be inferred.")
            return False

        # Add newly inferred facts to known facts & test against query
        for inferred_fact, subst_tuple in new_facts:
            print(f"Inferred New Fact: {inferred_fact}")
            known_facts.add(inferred_fact)

            goal_subst = unify_literals(inferred_fact, query)
            if goal_subst is not None:
                return goal_subst

        step += 1


# --- EXAMPLE SETUP & EXECUTION ---

if __name__ == "__main__":
    def V(name): return Term(name, is_var=True)
    def C(name): return Term(name, is_var=False)

    # KB Facts:
    # 1. American(West)
    # 2. Weapon(M1)
    # 3. Sells(West, M1, Nono)
    # 4. Hostile(Nono)
    kb_facts = {
        Literal("American", [C("West")]),
        Literal("Weapon", [C("M1")]),
        Literal("Sells", [C("West"), C("M1"), C("Nono")]),
        Literal("Hostile", [C("Nono")])
    }

    # KB Rules:
    # American(x) ^ Weapon(y) ^ Sells(x, y, z) ^ Hostile(z) => Criminal(x)
    rule1 = Rule(
        premises=[
            Literal("American", [V("x")]),
            Literal("Weapon", [V("y")]),
            Literal("Sells", [V("x"), V("y"), V("z")]),
            Literal("Hostile", [V("z")])
        ],
        conclusion=Literal("Criminal", [V("x")])
    )

    kb_rules = [rule1]

    # Target Query: Criminal(West)
    target_query = Literal("Criminal", [C("West")])

    print("Executing FOL Forward Chaining...\n")
    result = fol_fc_ask(kb_facts, kb_rules, target_query)

    print("\nResult:")
    if result is not False:
        print(f"SUCCESS: Query '{target_query}' is PROVEN!")
        print(f"Bindings: {result}")
    else:
        print(f"FAILURE: Query '{target_query}' could NOT be proven.")