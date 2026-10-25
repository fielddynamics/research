#!/usr/bin/env python3
"""
VERIFY: Where does the pointer ACTUALLY start?

Looking at the validation scripts and encoding documents to understand
the true initial state of the pi traversal.
"""

print('='*75)
print('VERIFYING THE POINTER ORIGIN')
print('='*75)
print()

# From field_closure_complete_validation.py section 1.7:
# The TRAVERSAL ALGORITHM is:
#   1. Start at position 0  <-- cumsum starts at 0
#   2. For each pi digit d:
#      - Add d to cumulative sum
#      - Position = cumsum mod 8
#      - Visit vertex at that position

print('THE ALGORITHM (from field_closure_complete_validation.py):')
print('-'*75)
print('''
    cumsum = 0                    # Initial counter value
    for digit in pi_digits:
        cumsum += digit           # Add the digit
        position = cumsum % 8     # Compute position
        # VISIT vertex at position
''')

print()
print('CRITICAL QUESTION: Is position 0 VISITED before the first digit?')
print()

# Let's trace it explicitly
PI_WITH_3 = [3, 1, 1, 0, 3, 7, 5, 5, 2, 4]

print('TRACING THE FIRST 5 STEPS:')
print('-'*75)

cumsum = 0
print(f'INITIAL STATE: cumsum = {cumsum}')
print(f'              position = cumsum mod 8 = {cumsum % 8}')
print()
print('But is this position VISITED? NO!')
print('The loop ADDS the digit BEFORE computing the visited position.')
print()

for step, digit in enumerate(PI_WITH_3[:5]):
    cumsum += digit
    position = cumsum % 8
    print(f'Step {step}: digit={digit}, cumsum={cumsum}, position={position}')

print()
print('='*75)
print('THE ANSWER')
print('='*75)
print()

print('The cumsum COUNTER starts at 0.')
print('But the FIRST VERTEX VISITED is determined by the FIRST DIGIT.')
print()
print('With pi (base 8) = 3.110375..., first digit = 3:')
print('  cumsum = 0 + 3 = 3')
print('  position = 3 mod 8 = 3')
print('  FIRST VISITED VERTEX = V3 (Wind, Tet B)')
print()

print('='*75)
print('VERIFICATION FROM FIELD_CLOSURE_ENCODING.MD SECTION 10.4')
print('='*75)
print()
print('"WITH the integer 3 included:')
print('First two digits: 3, 1')
print('Positions: 3 (Wind, Tet B) -> 4 (Thunder, Tet A)"')
print()
print('The FIRST position is 3, NOT 0!')
print()

print('='*75)
print('I CHING COMPLEMENTARY PAIR PROOF')
print('='*75)
print()
print('First position:  3 (Wind)')
print('Second position: 4 (Thunder)')
print('Sum: 3 + 4 = 7 (I Ching complementary pair!)')
print()
print('This ONLY works if the first position is 3, not 0.')
print('If first position were 0, first pair would be (0, 3) = sum 3 (NOT complementary)')
print()

print('='*75)
print('MY EARLIER ANSWER WAS INCORRECT')
print('='*75)
print()
print('I said: "The pointer starts at V0 (0,0,0)"')
print()
print('CORRECTION: The pointer does NOT start at any vertex.')
print('            The cumsum counter starts at 0.')
print('            But 0 is NOT a visited position.')
print('            The FIRST visited vertex is V3.')
print()

print('='*75)
print('THE CORRECT UNDERSTANDING')
print('='*75)
print()
print('Think of it like a database cursor or C++ pointer:')
print()
print('  int cumsum = 0;              // Counter initialized')
print('  for (int digit : pi_digits) {')
print('      cumsum += digit;         // Advance counter')
print('      int pos = cumsum % 8;    // Compute address')
print('      visit(vertex[pos]);      // Access the data')
print('  }')
print()
print('The counter starts at 0, but we only VISIT after adding a digit.')
print('So the first VISIT is to position 3 (from digit 3).')
print()

print('='*75)
print('THE "0" IS NOT AN ORIGIN VERTEX')
print('='*75)
print()
print('The "0" in cumsum = 0 is the INITIAL COUNTER VALUE, not a vertex.')
print('It is the REFERENCE POINT from which we measure displacement.')
print()
print('Like in physics:')
print('  - We set x = 0 as the origin')
print('  - But we don\'t "visit" x = 0')
print('  - Our first measurement is at x = displacement')
print()
print('Similarly:')
print('  - cumsum = 0 is the reference')
print('  - First digit "3" is the displacement')
print('  - First position visited = 0 + 3 = 3')
print()

print('='*75)
print('FINAL ANSWER')
print('='*75)
print()
print('Q: Where does the pointer START?')
print()
print('A: The cumulative sum starts at 0 as a REFERENCE VALUE.')
print('   But the FIRST VERTEX VISITED is V3.')
print()
print('   V3 = (0,1,1) in cube coordinates')
print('   V3 = Wind trigram in I Ching')
print('   V3 is in Tet B (even parity)')
print('   V3 is part of TIME face B0')
print()
print('   The "3" in pi (the integer part) IMMEDIATELY takes us to V3.')
print('   There is no "visit" to V0 before that.')
print()
print('   The I Ching complementary pair (3,4) = (Wind, Thunder) = sum 7')
print('   confirms this interpretation.')
