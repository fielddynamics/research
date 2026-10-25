"""
alice_chat.py
==============

Train a 100-node GFD oscillator on Alice in Wonderland (vocab capped at 100
most informative content words). Then "interact" with it by free-association:
given an input phrase, embed each word, return the words this Alice-trained
oscillator associates with what you said.

This is NOT generation. The oscillator has no autoregressive mechanism.
It's free association — given a stimulus, return what the substrate links to it.

Like asking someone who's only ever read Alice in Wonderland: "what does
'hello' make you think of?"
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import re
import time
import numpy as np
from collections import Counter, defaultdict
from gfd_oscillator import GFDOscillator


# Alice in Wonderland — abridged but representative; we'll use first ~6000 words
# of the actual text (loaded inline for self-containment).
ALICE_TEXT = """
Alice was beginning to get very tired of sitting by her sister on the bank, and
of having nothing to do: once or twice she had peeped into the book her sister
was reading, but it had no pictures or conversations in it, "and what is the
use of a book," thought Alice "without pictures or conversations?"

So she was considering in her own mind, whether the pleasure of making a
daisy-chain would be worth the trouble of getting up and picking the daisies,
when suddenly a White Rabbit with pink eyes ran close by her.

There was nothing so very remarkable in that; nor did Alice think it so very
much out of the way to hear the Rabbit say to itself, "Oh dear! Oh dear! I
shall be late!" but when the Rabbit actually took a watch out of its
waistcoat-pocket, and looked at it, and then hurried on, Alice started to her
feet, for it flashed across her mind that she had never before seen a rabbit
with either a waistcoat-pocket, or a watch to take out of it, and burning with
curiosity, she ran across the field after it, and fortunately was just in time
to see it pop down a large rabbit-hole under the hedge.

In another moment down went Alice after it, never once considering how in the
world she was to get out again. The rabbit-hole went straight on like a tunnel
for some way, and then dipped suddenly down, so suddenly that Alice had not a
moment to think about stopping herself before she found herself falling down a
very deep well.

Either the well was very deep, or she fell very slowly, for she had plenty of
time as she went down to look about her and to wonder what was going to happen
next. First, she tried to look down and make out what she was coming to, but
it was too dark to see anything; then she looked at the sides of the well, and
noticed that they were filled with cupboards and book-shelves; here and there
she saw maps and pictures hung upon pegs.

Down, down, down. Would the fall never come to an end? "I wonder how many
miles I've fallen by this time?" she said aloud. "I must be getting somewhere
near the centre of the earth."

"Dinah'll miss me very much to-night, I should think!" Dinah was the cat. "I
hope they'll remember her saucer of milk at tea-time. Dinah my dear! I wish
you were down here with me! There are no mice in the air, I'm afraid, but you
might catch a bat, and that's very like a mouse, you know. But do cats eat
bats, I wonder?" And here Alice began to get rather sleepy, and went on
saying to herself, "Do cats eat bats? Do cats eat bats?" and sometimes, "Do
bats eat cats?"

Alice was not a bit hurt, and she jumped up on to her feet in a moment: she
looked up, but it was all dark overhead; before her was another long passage,
and the White Rabbit was still in sight, hurrying down it. There was not a
moment to be lost: away went Alice like the wind.

Suddenly she came upon a little three-legged table, all made of solid glass;
there was nothing on it except a tiny golden key, and Alice's first thought
was that it might belong to one of the doors of the hall.

Alice opened the door and found that it led into a small passage, not much
larger than a rat-hole: she knelt down and looked along the passage into the
loveliest garden you ever saw. How she longed to get out of that dark hall,
and wander about among those beds of bright flowers and those cool fountains.

There seemed to be no use in waiting by the little door, so she went back to
the table, half hoping she might find another key on it. This time she found
a little bottle on it, and round the neck of the bottle was a paper label,
with the words "DRINK ME," beautifully printed on it in large letters.

It was all very well to say "Drink me," but the wise little Alice was not
going to do that in a hurry. "No, I'll look first," she said, "and see
whether it's marked poison or not"; for she had read several nice little
histories about children who had got burnt, and eaten up by wild beasts and
other unpleasant things.

However, this bottle was not marked "poison," so Alice ventured to taste it,
and finding it very nice, she very soon finished it off.

"What a curious feeling!" said Alice; "I must be shutting up like a
telescope."

And so it was indeed: she was now only ten inches high, and her face
brightened up at the thought that she was now the right size for going
through the little door into that lovely garden.

After a while, finding that nothing more happened, she decided on going into
the garden at once; but, alas for poor Alice! when she got to the door, she
found she had forgotten the little golden key, and when she went back to the
table for it, she found she could not possibly reach it.

"Come, there's no use in crying like that!" said Alice to herself, rather
sharply; "I advise you to leave off this minute!" She generally gave herself
very good advice, though she very seldom followed it, and sometimes she
scolded herself so severely as to bring tears into her eyes.

Soon her eye fell on a little glass box that was lying under the table: she
opened it, and found in it a very small cake, on which the words "EAT ME"
were beautifully marked in currants. "Well, I'll eat it," said Alice, "and
if it makes me grow larger, I can reach the key; and if it makes me grow
smaller, I can creep under the door; so either way I'll get into the garden."

"Curiouser and curiouser!" cried Alice; "now I'm opening out like the
largest telescope that ever was! Good-bye, feet!"

Just then her head struck against the roof of the hall: in fact she was now
more than nine feet high, and she at once took up the little golden key and
hurried off to the garden door.

After a time she heard a little pattering of feet in the distance, and she
hastily dried her eyes to see what was coming. It was the White Rabbit
returning, splendidly dressed, with a pair of white kid gloves in one hand
and a large fan in the other.

The Caterpillar and Alice looked at each other for some time in silence: at
last the Caterpillar took the hookah out of its mouth, and addressed her in a
languid, sleepy voice.

"Who are you?" said the Caterpillar.

This was not an encouraging opening for a conversation. Alice replied, rather
shyly, "I hardly know, sir, just at present, at least I know who I was when
I got up this morning, but I think I must have been changed several times
since then."

"What do you mean by that?" said the Caterpillar sternly.

"I can't explain myself, I'm afraid, sir," said Alice, "because I'm not
myself, you see."

"Have some wine," the March Hare said in an encouraging tone.

Alice looked all round the table, but there was nothing on it but tea. "I
don't see any wine," she remarked.

"There isn't any," said the March Hare.

"Then it wasn't very civil of you to offer it," said Alice angrily.

"It wasn't very civil of you to sit down without being invited," said the
March Hare.

The Hatter was the first to break the silence. "What day of the month is
it?" he said, turning to Alice: he had taken his watch out of his pocket,
and was looking at it uneasily.

"Have you guessed the riddle yet?" the Hatter said, turning to Alice again.

"No, I give it up," Alice replied: "what's the answer?"

"I haven't the slightest idea," said the Hatter.

"Off with her head!" the Queen shouted at the top of her voice. Nobody
moved.

"Who cares for you?" said Alice, "You're nothing but a pack of cards!"

The Cheshire Cat only grinned when it saw Alice. It looked good-natured,
she thought.

"Cheshire Puss," she began, "Would you tell me, please, which way I ought
to go from here?"

"That depends a good deal on where you want to get to," said the Cat.

"I don't much care where," said Alice.

"Then it doesn't matter which way you go," said the Cat.

"Oh, you can't help that," said the Cat: "we're all mad here. I'm mad.
You're mad."

"How do you know I'm mad?" said Alice.

"You must be," said the Cat, "or you wouldn't have come here."

"Beautiful Soup, so rich and green, waiting in a hot tureen! Who for such
dainties would not stoop? Soup of the evening, beautiful Soup!"

The King and Queen of Hearts were seated on their throne when they arrived,
with a great crowd assembled about them, all sorts of little birds and
beasts. The Knave was standing before them, in chains, with a soldier on
each side to guard him; and near the King was the White Rabbit, with a
trumpet in one hand, and a scroll of parchment in the other.

"The Queen of Hearts, she made some tarts, all on a summer day: the Knave
of Hearts, he stole those tarts, and took them quite away!"

"Consider your verdict," the King said to the jury.

"Not yet, not yet!" the Rabbit hastily interrupted. "There's a great deal
to come before that!"

The first witness was the Hatter. He came in with a teacup in one hand and
a piece of bread-and-butter in the other.

"Stupid things!" Alice began in a loud, indignant voice, but she stopped
hastily, for the White Rabbit cried out, "Silence in the court!"

"Wake up, Alice dear!" said her sister; "Why, what a long sleep you've
had!" "Oh, I've had such a curious dream!" said Alice, and she told her
sister all these strange Adventures of hers.
"""

# Minimal stop list — only true noise (single-letter, contractions of common verbs)
# Keeping pronouns, modal verbs, and conversational anchors so that we can
# actually interact with the system using natural language.
STOP_WORDS = set("a an the".split())

def tokenize(text):
    """Lowercase, strip punctuation, return word list."""
    text = text.lower()
    text = re.sub(r"[^a-z\s']", " ", text)
    words = text.split()
    return [w for w in words if len(w) > 1 and w not in STOP_WORDS]


def select_vocab(words, n=100):
    """Pick the top-n most frequent content words."""
    counts = Counter(words)
    return [w for w, _ in counts.most_common(n)]


def build_K(words, vocab, window=3):
    """Build PPMI co-occurrence matrix from streaming token positions."""
    word_to_idx = {w: i for i, w in enumerate(vocab)}
    N = len(vocab)
    C = np.zeros((N, N))

    for i, w in enumerate(words):
        if w not in word_to_idx:
            continue
        wi = word_to_idx[w]
        lo = max(0, i - window)
        hi = min(len(words), i + window + 1)
        for j in range(lo, hi):
            if j == i:
                continue
            wj_word = words[j]
            if wj_word in word_to_idx:
                wj = word_to_idx[wj_word]
                C[wi, wj] += 1

    # PPMI
    total = C.sum()
    row_t = C.sum(axis=1)
    col_t = C.sum(axis=0)
    PPMI = np.zeros_like(C)
    for i in range(N):
        for j in range(N):
            if C[i, j] > 0 and row_t[i] > 0 and col_t[j] > 0:
                p_ij = C[i, j] / total
                p_i = row_t[i] / total
                p_j = col_t[j] / total
                PPMI[i, j] = max(0, np.log(p_ij / (p_i * p_j)))
    return PPMI, C, word_to_idx


def embed_via_oscillator(K, n_dims=12, depth=8):
    """Deflation cascade."""
    N = len(K)
    K_res = K.copy()
    osc = GFDOscillator(dt=0.05, steps=2000)
    embedding = np.zeros((N, n_dims))
    eigvals = []
    for k in range(n_dims):
        graph = GFDOscillator.encode_weighted(N, K_res)
        state = osc.run_phase(graph, depth=depth, seed=42 + k * 137)
        if state.Sv[0] < 1e-10:
            break
        v = state.Vt[0] / np.linalg.norm(state.Vt[0])
        lam = float(v @ K_res @ v)
        eigvals.append(lam)
        embedding[:, k] = v * np.sqrt(abs(lam))
        K_res = K_res - lam * np.outer(v, v)
    return embedding, eigvals


def cos_sim(a, b):
    na = np.linalg.norm(a); nb = np.linalg.norm(b)
    return float(np.dot(a, b) / (na * nb)) if na > 1e-12 and nb > 1e-12 else 0.0


def respond(input_text, embedding, vocab, k=8):
    """Free-association response: given input, find what Alice's mind links to it.

    Method:
      1. Tokenize input, keep words in vocab.
      2. Sum their embeddings → compound query vector.
      3. Find top-k vocab words by cosine similarity to the query vector.
      4. Return them in order, excluding the input words themselves.
    """
    words = tokenize(input_text)
    in_vocab = [w for w in words if w in vocab]
    out_of_vocab = [w for w in words if w not in vocab]

    if not in_vocab:
        return None, words, out_of_vocab

    # Sum the embeddings of all input words
    query_vec = np.zeros(embedding.shape[1])
    for w in in_vocab:
        query_vec += embedding[vocab.index(w)]

    # Find nearest words
    sims = []
    excl = set(in_vocab)
    for i, w in enumerate(vocab):
        if w in excl:
            continue
        sims.append((w, cos_sim(query_vec, embedding[i])))
    sims.sort(key=lambda x: -x[1])
    return sims[:k], in_vocab, out_of_vocab


def main():
    print("=" * 76)
    print(" 100-node oscillator trained on Alice in Wonderland")
    print("=" * 76)

    # Tokenize and select vocab
    print("\n  Tokenizing Alice in Wonderland (with content words only)...")
    words = tokenize(ALICE_TEXT)
    print(f"    {len(words)} content tokens")
    vocab = select_vocab(words, n=100)
    print(f"    Top-100 vocab selected")

    # Show top vocabulary
    counts = Counter(words)
    top_freq = [(w, counts[w]) for w in vocab[:30]]
    print(f"    Top 30 most frequent: {[w for w, _ in top_freq]}")

    # Build K
    print("\n  Building PPMI co-occurrence (window=3)...")
    K, C, w2i = build_K(words, vocab, window=3)
    n_edges = (C > 0).sum()
    print(f"    {n_edges} nonzero co-occurrence pairs")

    # Embed
    print("\n  Running oscillator with 12-mode deflation cascade...")
    t0 = time.time()
    emb, eigvals = embed_via_oscillator(K, n_dims=12, depth=8)
    print(f"    Done in {time.time()-t0:.1f}s")
    print(f"    Eigenvalues: {[f'{e:.2f}' for e in eigvals]}")

    # Now the interaction
    print("\n" + "═" * 76)
    print(" INTERACTION")
    print("═" * 76)

    test_prompts = [
        "hello how are you",
        "what is your name",
        "tell me a story",
        "I am tired",
        "down the rabbit hole",
        "are you mad",
        "drink me",
        "the queen",
        "do you remember",
        "who are you",
    ]

    for prompt in test_prompts:
        print(f"\n  > {prompt}")
        result, in_vocab, oov = respond(prompt, emb, vocab, k=8)
        if not result:
            print(f"    [no words from this prompt are in Alice's vocabulary]")
            print(f"    OOV: {oov}")
            continue
        print(f"    in-vocab: {in_vocab}")
        if oov:
            print(f"    not-in-vocab (ignored): {oov}")
        # Format the response
        words_assoc = [w for w, _ in result]
        sims = [s for _, s in result]
        print(f"    associated words:")
        for w, s in result:
            print(f"      {w:>15s}  ({s:+.3f})")


if __name__ == "__main__":
    main()
