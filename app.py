
import streamlit as st
import random
import string
import time
from typing import List, Tuple

st.set_page_config(page_title="Palindrome & Parentheses Lab", layout="wide")

# =========================
# Core assignment functions
# =========================
def is_palindrome(text: str, ignore_case: bool = True, ignore_non_alnum: bool = False) -> bool:
    """Return True if `text` is a palindrome, False otherwise.

    Args:
        text: Input string to check.
        ignore_case: If True, case-insensitive comparison.
        ignore_non_alnum: If True, filter out all non-alphanumeric characters before checking.

    Notes:
        - Empty strings and 1-char strings are palindromes by convention.
    """
    if ignore_non_alnum:
        filtered = [ch for ch in text if ch.isalnum()]
        s = "".join(filtered)
    else:
        s = text

    if ignore_case:
        s = s.lower()

    # Two-pointer technique
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


def is_balanced_parentheses(s: str, paren_types: str = "()[]{}") -> bool:
    """Return True if parentheses/brackets/braces are balanced in `s`, else False.

    Args:
        s: Input string potentially containing bracket characters.
        paren_types: A string containing allowed pairs in order, e.g., "()[]{}".
                     Pairs are read left-to-right; e.g., '()[]' allows () and [].

    The algorithm uses a classic stack approach:
    - Push opening symbols onto the stack.
    - On a closing symbol, the top of the stack must be the corresponding opener.
    """
    pairs = {paren_types[i+1]: paren_types[i] for i in range(0, len(paren_types), 2)}
    openers = set(pairs.values())

    stack: List[str] = []
    for ch in s:
        if ch in openers:
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0


# =====================================
# Helper functions for step-by-step UI
# =====================================
def palindrome_steps(text: str, ignore_case: bool, ignore_non_alnum: bool) -> List[dict]:
    """Produce a list of steps showing the two-pointer palindrome check."""
    if ignore_non_alnum:
        display_source = ''.join(ch for ch in text if ch.isalnum())
    else:
        display_source = text

    s = display_source.lower() if ignore_case else display_source
    steps = []
    i, j = 0, len(s) - 1
    while i <= j:
        steps.append({
            "i": i,
            "j": j,
            "left": s[i] if i < len(s) else "",
            "right": s[j] if j >= 0 else "",
            "match": (s[i] == s[j]) if (i < len(s) and j >= 0) else False,
            "snapshot": s
        })
        if i < j and s[i] != s[j]:
            break
        i += 1
        j -= 1
    return steps


def parentheses_steps(s: str, paren_types: str = "()[]{}") -> Tuple[List[dict], bool]:
    """Produce steps for the stack-based parentheses check and the final result."""
    pairs = {paren_types[i+1]: paren_types[i] for i in range(0, len(paren_types), 2)}
    openers = set(pairs.values())

    steps = []
    stack: List[str] = []
    ok = True
    for idx, ch in enumerate(s):
        action = None
        detail = None
        if ch in openers:
            stack.append(ch)
            action = "push"
            detail = f"push '{ch}'"
        elif ch in pairs:
            if not stack:
                ok = False
                action = "fail"
                detail = f"no opener for '{ch}'"
            elif stack[-1] != pairs[ch]:
                ok = False
                action = "fail"
                detail = f"top '{stack[-1]}' doesn't match '{ch}'"
            else:
                stack.pop()
                action = "pop"
                detail = f"pop for '{ch}'"
        steps.append({
            "index": idx,
            "char": ch,
            "stack": stack.copy(),
            "action": action,
            "detail": detail
        })
        if action == "fail":
            break
    if ok and stack:
        ok = False
        steps.append({
            "index": len(s),
            "char": "",
            "stack": stack.copy(),
            "action": "fail",
            "detail": "unclosed opener(s) remaining"
        })
    return steps, ok


# ======================
# Generators for inputs
# ======================
def generate_word(length: int = 7, alphabet: str = string.ascii_lowercase, palindrome: bool = False) -> str:
    if length <= 0:
        return ""
    if palindrome:
        half = (length + 1) // 2
        left = ''.join(random.choice(alphabet) for _ in range(half))
        if length % 2 == 0:
            return left + left[::-1]
        return left + left[-2::-1]
    else:
        return ''.join(random.choice(alphabet) for _ in range(length))


def generate_parentheses(length: int = 8, paren_types: str = "()[]{}", balanced: bool = True) -> str:
    """Generate parentheses strings. If balanced=True, returns a balanced string (even length).
    For balanced strings we only use one type of parens '()' to ensure correctness, then optionally
    map some pairs to other types to add variety."""
    if length < 0:
        length = 0
    if balanced:
        if length % 2 == 1:
            length += 1  # balanced must be even
        n_pairs = length // 2
        # Generate a random Dyck word using +1 for '(' and -1 for ')'
        path = []
        opens = 0
        for _ in range(2 * n_pairs):
            if opens == 0:
                path.append(1); opens += 1
            elif opens == (2 * n_pairs - len(path)):
                path.append(-1); opens -= 1
            else:
                step = random.choice([1, -1]) if opens > 0 else 1
                opens += step
                path.append(step)
        base = ''.join('(' if x == 1 else ')' for x in path)
        # Optionally remap some matching pairs to other bracket types for variety
        types = [paren_types[i:i+2] for i in range(0, len(paren_types), 2)]
        # Use a stack to remap matching pairs consistently
        stack = []
        out = list(base)
        for i, ch in enumerate(base):
            if ch == '(':
                t = random.choice(types)
                stack.append(t)
                out[i] = t[0]
            else:
                t = stack.pop()
                out[i] = t[1]
        return ''.join(out)
    else:
        # Unbalanced: pick random brackets and guarantee a mismatch
        chars = ''.join(paren_types)
        s = ''.join(random.choice(chars) for _ in range(max(1, length)))
        # Force an imbalance by appending an extra closer if it accidentally balanced
        if is_balanced_parentheses(s, paren_types):
            s += random.choice([paren_types[i+1] for i in range(0, len(paren_types), 2)])
        return s


def generate_combined(word_len: int = 6, paren_len: int = 6, palindrome_word: bool = False, balanced_paren: bool = True) -> str:
    word = generate_word(word_len, palindrome=palindrome_word)
    parens = generate_parentheses(paren_len, balanced=balanced_paren)
    # Interleave randomly
    combined = []
    w_idx = p_idx = 0
    while w_idx < len(word) or p_idx < len(parens):
        if w_idx < len(word) and (p_idx == len(parens) or random.random() < 0.5):
            combined.append(word[w_idx]); w_idx += 1
        if p_idx < len(parens) and (w_idx == len(word) or random.random() < 0.5):
            combined.append(parens[p_idx]); p_idx += 1
    return ''.join(combined)


# =========
# Sidebar
# =========
st.sidebar.title("⚙️ Options")
st.sidebar.write("Adjust default behavior used by the checkers and animations.")

ignore_case = st.sidebar.checkbox("Ignore case (palindrome)", value=True)
ignore_non_alnum = st.sidebar.checkbox("Ignore non-alphanumeric (palindrome)", value=False)
paren_types = st.sidebar.text_input("Allowed bracket pairs", value="()[]{}")
speed = st.sidebar.slider("Animation speed (steps/sec)", min_value=0.5, max_value=10.0, value=3.0)

st.title("🔤 Palindrome & Parentheses Lab")
st.caption("An interactive Streamlit app for INFO‑H 501 — check palindromes, balance parentheses, combine both, visualize algorithms, and generate sample inputs.")

tabs = st.tabs(["Palindrome", "Parentheses", "Combined", "Generator", "About"])

# ---------------
# Palindrome Tab
# ---------------
with tabs[0]:
    st.subheader("Palindrome Checker")
    col1, col2 = st.columns([2, 1])
    with col1:
        text_pal = st.text_input("Enter a word (or phrase):", value="racecar")
    with col2:
        animate_pal = st.checkbox("Show animated steps", value=True, key="anim_pal")

    # Result
    result_pal = is_palindrome(text_pal, ignore_case=ignore_case, ignore_non_alnum=ignore_non_alnum)
    st.markdown(f"**Result:** {'✅ Palindrome' if result_pal else '❌ Not a palindrome'}")

    # Steps / animation
    if animate_pal and text_pal:
        frames = palindrome_steps(text_pal, ignore_case, ignore_non_alnum)
        slot = st.empty()
        prog = st.progress(0, text="Animating…")
        pause = 1.0 / speed
        for k, step in enumerate(frames):
            snapshot = step['snapshot']
            i, j = step['i'], step['j']
            markers = ''.join([' ' for _ in snapshot])
            left_marker = ' ' * i + '↑'
            right_marker = ' ' * j + '↑' if j < len(snapshot) else ''
            slot.markdown(
                f"""

                **Normalized string:** `{snapshot}`


                **Pointers:**


                `{left_marker}` (left = {i})


                `{right_marker}` (right = {j})


                **Compare:** `{step['left']}` vs `{step['right']}` → {'match ✅' if step['match'] else 'mismatch ❌'}

                """
            )
            prog.progress(int((k+1) / max(1, len(frames)) * 100))
            time.sleep(pause)

# -----------------
# Parentheses Tab
# -----------------
with tabs[1]:
    st.subheader("Parentheses / Brackets Balance Checker")
    col1, col2 = st.columns([2, 1])
    with col1:
        text_par = st.text_input("Enter a parentheses string:", value="([]){}")
    with col2:
        animate_par = st.checkbox("Show animated steps", value=True, key="anim_par")

    steps, ok = parentheses_steps(text_par, paren_types=paren_types)
    st.markdown(f"**Result:** {'✅ Balanced' if ok else '❌ Not balanced'}")

    if animate_par and text_par:
        area = st.empty()
        prog = st.progress(0, text="Animating…")
        pause = 1.0 / speed
        for k, sstep in enumerate(steps):
            idx = sstep['index']
            ch = sstep['char']
            stack_repr = ' '.join(sstep['stack']) if sstep['stack'] else '∅'
            action = sstep['action'] or 'skip'
            detail = sstep['detail'] or '(not a bracket)'
            indicator = [' '] * len(text_par)
            if idx < len(text_par):
                indicator[idx] = '^'
            caret_line = ''.join(indicator)
            area.markdown(
                f"""

                **Input:** `{text_par}`


                `{caret_line}` (index = {idx})


                **Action:** {action} — {detail}


                **Stack:** `{stack_repr}`

                """
            )
            prog.progress(int((k+1) / max(1, len(steps)) * 100))
            time.sleep(pause)

# -------------
# Combined Tab
# -------------
with tabs[2]:
    st.subheader("Combined Input (Words + Parentheses)")
    st.write("Paste a string containing both letters and brackets. We'll check palindrome (on letters only if you enable *Ignore non-alphanumeric*) and bracket balance simultaneously.")

    combo = st.text_input("Enter a mixed string:", value="racecar()(())")
    run_combo = st.button("Run checks", key="run_combo")

    if run_combo or combo:
        # Palindrome check uses current sidebar options
        pal_res = is_palindrome(combo, ignore_case=ignore_case, ignore_non_alnum=ignore_non_alnum)
        par_steps, par_ok = parentheses_steps(combo, paren_types=paren_types)

        colA, colB = st.columns(2)
        with colA:
            st.markdown("### Palindrome on this input")
            st.markdown(f"**Result:** {'✅ Palindrome' if pal_res else '❌ Not a palindrome'}")
            if st.checkbox("Show palindrome steps (combined)", value=True, key="anim_combo_pal"):
                frames = palindrome_steps(combo, ignore_case, ignore_non_alnum)
                slot = st.empty()
                prog = st.progress(0, text="Animating palindrome…")
                pause = 1.0 / speed
                for k, step in enumerate(frames):
                    snapshot = step['snapshot']
                    i, j = step['i'], step['j']
                    left_marker = ' ' * i + '↑'
                    right_marker = ' ' * j + '↑' if j < len(snapshot) else ''
                    slot.markdown(
                        f"""

                        **Normalized string:** `{snapshot}`


                        `{left_marker}` (left = {i})


                        `{right_marker}` (right = {j})


                        **Compare:** `{step['left']}` vs `{step['right']}` → {'match ✅' if step['match'] else 'mismatch ❌'}

                        """
                    )
                    prog.progress(int((k+1) / max(1, len(frames)) * 100))
                    time.sleep(pause)

        with colB:
            st.markdown("### Parentheses on this input")
            st.markdown(f"**Result:** {'✅ Balanced' if par_ok else '❌ Not balanced'}")
            if st.checkbox("Show bracket steps (combined)", value=True, key="anim_combo_par"):
                area = st.empty()
                prog = st.progress(0, text="Animating brackets…")
                pause = 1.0 / speed
                for k, sstep in enumerate(par_steps):
                    idx = sstep['index']
                    ch = sstep['char']
                    stack_repr = ' '.join(sstep['stack']) if sstep['stack'] else '∅'
                    action = sstep['action'] or 'skip'
                    detail = sstep['detail'] or '(not a bracket)'
                    indicator = [' '] * len(combo)
                    if idx < len(combo):
                        indicator[idx] = '^'
                    caret_line = ''.join(indicator)
                    area.markdown(
                        f"""

                        **Input:** `{combo}`


                        `{caret_line}` (index = {idx})


                        **Action:** {action} — {detail}


                        **Stack:** `{stack_repr}`

                        """
                    )
                    prog.progress(int((k+1) / max(1, len(par_steps)) * 100))
                    time.sleep(pause)

# -------------
# Generator Tab
# -------------
with tabs[3]:
    st.subheader("Generate Sample Inputs")
    st.write("Create custom examples to copy ➜ paste into the other tabs.")

    gtab = st.tabs(["Words", "Parentheses", "Combined"])

    with gtab[0]:
        st.markdown("#### Word Generator")
        gcol1, gcol2, gcol3 = st.columns(3)
        with gcol1:
            w_len = st.number_input("Length", min_value=1, max_value=64, value=7, step=1)
        with gcol2:
            w_pal = st.selectbox("Palindrome?", ["Yes (palindrome)", "No (random)"], index=0)
        with gcol3:
            alphabet = st.text_input("Alphabet (characters to sample from)", value=string.ascii_lowercase)

        if st.button("Generate word"):
            out = generate_word(int(w_len), alphabet=alphabet, palindrome=(w_pal.startswith("Yes")))
            st.code(out, language="text")

    with gtab[1]:
        st.markdown("#### Parentheses Generator")
        gcol1, gcol2, gcol3 = st.columns(3)
        with gcol1:
            p_len = st.number_input("Target length (even for balanced)", min_value=2, max_value=200, value=8, step=2)
        with gcol2:
            p_bal = st.selectbox("Balanced?", ["Yes", "No"], index=0)
        with gcol3:
            p_types = st.text_input("Allowed pairs", value=paren_types)

        if st.button("Generate parentheses"):
            out = generate_parentheses(int(p_len), paren_types=p_types, balanced=(p_bal == "Yes"))
            st.code(out, language="text")

    with gtab[2]:
        st.markdown("#### Combined Generator")
        cg1, cg2, cg3, cg4 = st.columns(4)
        with cg1:
            cw_len = st.number_input("Word length", min_value=1, max_value=64, value=6, step=1)
        with cg2:
            cp_len = st.number_input("Parentheses length", min_value=2, max_value=200, value=6, step=2)
        with cg3:
            cw_pal = st.checkbox("Word palindrome?", value=True)
        with cg4:
            cp_bal = st.checkbox("Parentheses balanced?", value=True)

        if st.button("Generate combined"):
            out = generate_combined(int(cw_len), int(cp_len), palindrome_word=cw_pal, balanced_paren=cp_bal)
            st.code(out, language="text")

# -------------
# About Tab
# -------------
with tabs[4]:
    st.markdown("""
    ### About this app
    - **Goal:** Bring two classic intro‑to‑CS functions to life: a palindrome checker and a balanced parentheses checker.
    - **Algorithms used:**
        - *Palindrome:* two-pointer technique from both ends.
        - *Parentheses:* stack-based matching of opener/closer pairs.
    - **Controls:** Use the left sidebar for case sensitivity, character filtering, allowed bracket types, and animation speed.
    - **Edge cases:** Empty strings are considered **palindromes** and **balanced** (by most conventions in assignments like this).
    - **Reusability:** The two functions `is_palindrome` and `is_balanced_parentheses` are implemented at the top and can be copied into your assignment.
    """)


