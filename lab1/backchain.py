from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def get_match(rules, hypothesis):
    for rule in rules:
        cons = rule.consequent()
        for temp in cons:
            matched = match(temp, hypothesis)
            if matched != None:
                yield matched, rule


def backchain_to_goal_tree(rules, hypothesis):
    lst = list()
    for matched, rule in get_match(rules, hypothesis):
        ant = rule.antecedent()
        lst.append(process_rule(ant, rules, hypothesis, matched))
    if not lst:
        return hypothesis

    result = OR(hypothesis)
    for x in lst:
        result.append(x)

    return simplify(result)

def process_rule(rule_expr, rules, hypothesis, matched):
    if isinstance(rule_expr, AND) or isinstance(rule_expr, OR):
        lst = []
        for expr in rule_expr:
            if isinstance(expr, str):
                next_hyp = populate(expr, matched)
                lst.append(backchain_to_goal_tree(rules, next_hyp))
            else:
                lst.append(process_rule(expr, rules, hypothesis, matched))
        return AND(lst) if isinstance(rule_expr, AND) else OR(lst)
    elif isinstance(rule_expr, str):
        next_hyp = populate(rule_expr, matched)
        return backchain_to_goal_tree(rules, next_hyp)
    else:
        raise NotImplementedError

# Here's an example of running the backward chainer - uncomment
# it to see it work:
#print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
