
REQUIRED = 1001001000
STRONG = 1000000
MEDIUM = 1000
WEAK = 1

def repr_strength(strength):
    return {
        REQUIRED: 'Required',
        STRONG: 'Strong',
        MEDIUM: 'Medium',
        WEAK: 'Weak'
    }[strength]
