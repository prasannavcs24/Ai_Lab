from typing import Any, Dict, List, Union

# Define Term representations:
# - Variable: str starting with a lowercase letter (e.g., 'x', 'y')
# - Constant: str starting with an uppercase letter or number (e.g., 'A', 'John')
# - Function / Predicate: tuple where index 0 is the symbol name and rest are args
Term = Union[str, tuple]
Substitution = Dict[str, Term]


def is_variable(term: Term) -> bool:
    """Check if a term is a variable (strings starting with lowercase letters)."""
    return isinstance(term, str) and len(term) > 0 and term[0].islower()


def occurs_check(var: str, term: Term, subst: Substitution) -> bool:
    """
    Check if variable 'var' occurs inside 'term'.
    Prevents infinite circular structures like x = f(x).
    """
    term = apply_subst(subst, term)
    if var == term:
        return True
    if isinstance(term, tuple):
        return any(occurs_check(var, arg, subst) for arg in term[1:])
    return False


def apply_subst(subst: Substitution, term: Term) -> Term:
    """Apply substitution mapping to a term recursively."""
    if is_variable(term) and term in subst:
        return apply_subst(subst, subst[term])
    if isinstance(term, tuple):
        symbol = term[0]
        args = tuple(apply_subst(subst, arg) for arg in term[1:])
        return (symbol, *args)
    return term


def unify_var(var: str, term: Term, subst: Substitution) -> Union[Substitution, None]:
    """Unify a variable with a term under an existing substitution."""
    if var in subst:
        return unify(subst[var], term, subst)
    if is_variable(term) and term in subst:
        return unify(var, subst[term], subst)
    if occurs_check(var, term, subst):
        return None  # Occurs check failure
    
    # Add new mapping {var: term} and update existing bindings
    new_subst = dict(subst)
    new_subst[var] = term
    return new_subst


def unify(x: Term, y: Term, subst: Union[Substitution, None] = None) -> Union[Substitution, None]:
    """
    Find Most General Unifier (MGU) of two FOL terms/expressions x and y.
    Returns a dictionary mapping variables to terms if unifiable, else None.
    """
    if subst is None:
        subst = {}
        
    if subst is None:
        return None

    # Step 1: Identical terms
    if x == y:
        return subst

    # Step 2: Variable cases
    if is_variable(x):
        return unify_var(x, y, subst)
    if is_variable(y):
        return unify_var(y, x, subst)

    # Step 3: Compound terms (Functions or Predicates)
    if isinstance(x, tuple) and isinstance(y, tuple):
        # Must have same symbol name and same number of arguments
        if x[0] != y[0] or len(x) != len(y):
            return None
        
        # Recursively unify corresponding arguments
        for arg1, arg2 in zip(x[1:], y[1:]):
            subst = unify(arg1, arg2, subst)
            if subst is None:
                return None
        return subst

    # Step 4: Mismatch (e.g., constant vs different constant)
    return None

def print_result(expr1, expr2):
    mgu = unify(expr1, expr2)
    if mgu is not None:
        print(f"Unify({expr1}, {expr2})")
        print(f"  => Success MGU: {mgu}\n")
    else:
        print(f"Unify({expr1}, {expr2})")
        print(f"  => Failed (Not Unifiable)\n")


# Case 1: Standard variable to constant binding
# P(x, A) vs P(B, y)
print_result(("P", "x", "A"), ("P", "B", "y"))

# Case 2: Nested functions
# Knows(John, x) vs Knows(y, Mother(y))
print_result(("Knows", "John", "x"), ("Knows", "y", ("Mother", "y")))

# Case 3: Occurs check failure
# P(x) vs P(f(x))
print_result(("P", "x"), ("P", ("f", "x")))

# Case 4: Predicate/Constant mismatch
# P(A) vs Q(A)
print_result(("P", "A"), ("Q", "A"))