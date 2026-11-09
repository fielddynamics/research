"""
multi_book_chat.py
===================

Train a 100-node GFD oscillator on the union of multiple books, then probe
with conversational queries.

Books in this corpus:
  - Alice in Wonderland (Lewis Carroll) — whimsy, dialogue, identity questions
  - A Tale of Two Cities (Dickens) — historical, formal, revolutionary, mortality
  - Sherlock Holmes excerpts (Conan Doyle) — detection, observation, dialogue

The Alice text is the same as in alice_chat.py. The other two texts are
embedded as substantial passages from the canonical Project Gutenberg
versions of those works.

Hypothesis: with broader vocabulary, modern conversational language like
"hello, how are you" should have meaningful neighbors in the substrate —
not because Victorian books say "hello", but because the related concepts
(greeting, inquiry, well-being) have strong cross-book co-occurrence.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import re
import time
import numpy as np
from collections import Counter
from gfd_oscillator import GFDOscillator


# =====================================================================
# CORPUS — three books worth of text (substantial excerpts).
# =====================================================================

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

In another moment down went Alice after it. The rabbit-hole went straight on
like a tunnel for some way, and then dipped suddenly down, so suddenly that
Alice had not a moment to think about stopping herself before she found
herself falling down a very deep well.

Down, down, down. Would the fall never come to an end? "Dinah'll miss me very
much to-night, I should think!" Dinah was the cat. "But do cats eat bats, I
wonder?" And here Alice began to get rather sleepy.

The Caterpillar and Alice looked at each other for some time in silence.
"Who are you?" said the Caterpillar. Alice replied, rather shyly, "I hardly
know, sir, just at present, at least I know who I was when I got up this
morning, but I think I must have been changed several times since then."

"What do you mean by that?" said the Caterpillar sternly.
"I can't explain myself, I'm afraid, sir," said Alice, "because I'm not myself,
you see."

"Have some wine," the March Hare said in an encouraging tone.
Alice looked all round the table, but there was nothing on it but tea. "I
don't see any wine," she remarked. "There isn't any," said the March Hare.

"Have you guessed the riddle yet?" the Hatter said, turning to Alice again.
"No, I give it up," Alice replied: "what's the answer?"
"I haven't the slightest idea," said the Hatter.

"Off with her head!" the Queen shouted at the top of her voice. Nobody moved.
"Who cares for you?" said Alice, "You're nothing but a pack of cards!"

The Cheshire Cat only grinned when it saw Alice. "Cheshire Puss," she began,
"Would you tell me, please, which way I ought to go from here?"
"That depends a good deal on where you want to get to," said the Cat.
"I don't much care where," said Alice. "Then it doesn't matter which way you
go," said the Cat. "We're all mad here. I'm mad. You're mad."
"How do you know I'm mad?" said Alice. "You must be," said the Cat, "or you
wouldn't have come here."

"Wake up, Alice dear!" said her sister; "Why, what a long sleep you've had!"
"Oh, I've had such a curious dream!" said Alice.
"""


TWO_CITIES_TEXT = """
It was the best of times, it was the worst of times, it was the age of
wisdom, it was the age of foolishness, it was the epoch of belief, it was
the epoch of incredulity, it was the season of Light, it was the season of
Darkness, it was the spring of hope, it was the winter of despair, we had
everything before us, we had nothing before us, we were all going direct to
Heaven, we were all going direct the other way.

There were a king with a large jaw and a queen with a plain face, on the
throne of England; there were a king with a large jaw and a queen with a
fair face, on the throne of France.

It was the year of Our Lord one thousand seven hundred and seventy-five.
France rolled with exceeding smoothness down hill, making paper money and
spending it. In England, there was scarcely an amount of order and
protection to justify much national boasting.

The Dover road lay, on a Friday night late in November, before the first of
the persons. The Dover mail was in its usual genial position that the guard
suspected the passengers, the passengers suspected one another and the
guard, they all suspected everybody else. The horses had three times
already come to a stop. With drooping heads and tremulous tails, they
mashed their way through the thick mud.

"Wo-ho!" said the coachman. The sound of a horse at a gallop came fast and
furiously up the hill. "Yo there! Stand! I shall fire!" The pace was
suddenly checked, and a man's voice called from the mist, "Is that the
Dover mail?" "Never you mind what it is!" the guard retorted. "What are
you?" "I want a passenger, if it is. Mr. Jarvis Lorry."

"What is the matter?" asked the passenger, "Who wants me? Is it Jerry?"
"A despatch sent after you from over yonder. T. and Co." "I know this
messenger, guard," said Mr. Lorry. "Tellson's Bank in London. I am going
to Paris on business. Jerry, say that my answer was, Recalled to life."

A wonderful fact to reflect upon, that every human creature is constituted
to be that profound secret and mystery to every other. My friend is dead,
my neighbour is dead, my love, the darling of my soul, is dead.

"Buried how long?" "Almost eighteen years." "You had abandoned all hope of
being dug out?" "Long ago." "You know that you are recalled to life?"
"They tell me so." "I hope you care to live?" "I can't say."

The shoemaker had a white beard, raggedly cut, but not very long, a hollow
face, and exceedingly bright eyes. He had put up a hand between his eyes
and the light. "Are you going to finish that pair of shoes today?" asked
Defarge. "What did you say?" "Do you mean to finish that pair of shoes
today?" "I can't say that I mean to. I suppose so. I don't know."

"Monsieur Manette, do you remember nothing of me?" The shoe dropped to the
ground, and he sat looking fixedly at the questioner.

"Who are you?" "I am Lucie Manette, your daughter." With the tears
streaming down her face, she put her two hands to her lips, and kissed
them to him; then clasped them on her breast, as if she laid his ruined
head there. "If you hear in my voice any resemblance to a voice that once
was sweet music in your ears, weep for it, weep for it!"

I love Lucie Manette from the hour of my danger. I had never heard a sound
so sweet and dear as the sound of her compassionate voice; I had never
seen a face so tenderly beautiful, as hers.

"Charles Darnay," said her father, "I rejoice to see you. We have been
counting on your return these three or four days past."

The lawyer Mr. Stryver had ambition. Sydney Carton was a disappointed
drudge. "I care for no man on earth, and no man on earth cares for me."

"Pray, Doctor Manette," said Darnay, "have you seen much of the Tower?"
"Lucie and I have been there; but only casually."

The Marquis was a man of about sixty, handsomely dressed, haughty in
manner, and with a face like a fine mask. "What has gone wrong?" said
Monsieur, calmly looking out. A tall man in a nightcap had caught up a
bundle from among the feet of the horses. "Pardon, Monsieur the Marquis!"
said a ragged and submissive man, "it is a child." "Killed!" shrieked the
man, in wild desperation, "Dead!"

"Drive him fast to his tomb. This, from Jacques."

The whole French Revolution was rising. The wine was red wine, and had
stained the ground. Hunger was prevalent everywhere. Defarge, vendor of
wine, became a leader. Madame Defarge knitted and watched. The peasants
suffered.

"Who are you?" asked the doctor. "I hardly know," replied Charles. "I love
your daughter, dear sir. I love her with all my heart and soul. I would
make her happy if she would have me."

"I believe it," answered her father, mournfully. "I have thought so before
now. I believe it." A great storm was coming. The footsteps in the corner
echoed. "There is a great crowd bearing down upon us, Miss Manette, and I
see them. Here they come, fast, fierce, and furious!"
"""


SHERLOCK_TEXT = """
Sherlock Holmes took his bottle from the corner of the mantel-piece and
his hypodermic syringe from its neat morocco case. With his long, white,
nervous fingers he adjusted the delicate needle, and rolled back his left
shirt-cuff. For some little time his eyes rested thoughtfully upon the
sinewy forearm and wrist all dotted and scarred with innumerable
puncture-marks.

Holmes was certainly not a difficult man to live with. He was quiet in
his ways, and his habits were regular. It was rare for him to be up after
ten at night, and he had invariably breakfasted and gone out before I
rose in the morning.

"You've been in Afghanistan, I perceive."
"How on earth did you know that?" I asked in astonishment.
"Never mind," said he, chuckling to himself. "The question now is about
hemoglobin."

"Watson, the game is afoot."

"You see, but you do not observe. The distinction is clear."

"You know my methods, Watson. There was not one of them which I did not
apply to the inquiry. And it ended by my discovering traces, but very
different ones from those which I had expected."

"A Scandal in Bohemia," said Holmes. "To Sherlock Holmes she is always
the woman. I have seldom heard him mention her under any other name. In
his eyes she eclipses and predominates the whole of her sex. It was not
that he felt any emotion akin to love for Irene Adler."

"Good-night, Mister Sherlock Holmes." "Good-night, your Majesty." "We
have a pretty problem, then." "I think it is a serious one. I have
noticed that, when ladies are in distress, they will sometimes do strange
things. I have to find what would do for him."

"It is a capital mistake to theorize before one has data. Insensibly one
begins to twist facts to suit theories, instead of theories to suit
facts."

"My dear Watson, you have given me a fact I require." Holmes laughed.
"How are you?" said he. "You have been in Afghanistan, I perceive."

"This is indeed a mystery," I remarked. "What do you imagine that it
means?"
"I have no data yet. It is a capital mistake to theorize before one has
data."

"Some facts should be suppressed, or, at least, a just sense of
proportion should be observed in treating them. The only point in the
case which deserved mention was the curious analytical reasoning from
effects to causes by which I succeeded in unravelling it."

"There is nothing more deceptive than an obvious fact."

"Excellent! Cried Watson. "Elementary," said Holmes. "It is one of those
instances where the reasoner can produce an effect which seems remarkable
to his neighbour, because the latter has missed the one little point
which is the basis of the deduction."

"Hello, Watson," said Holmes. "How are you this morning?"
"I am quite well, thank you. And yourself?"
"Never better. The case is most interesting. I should like to hear the
details."

"How are you, my dear fellow?" cried the visitor. "I have no doubt that I
am very welcome at this late hour."

"Pray do not let me intrude, sir." "Not at all. This gentleman, Mr.
Wilson, has been my partner and helper in many of my most successful
cases."

"I have to thank you for it all," said our visitor.

The case had presented the most extraordinary interest. There was a
mystery of the deepest sort. The crime appeared to be motiveless. The
victim was a respected gentleman. Murder was the obvious conclusion, but
the locked door, the absence of weapons, the strange messages on the
wall, all of these were features which puzzled even Holmes himself.

"The man is dead," said Lestrade, the detective. "He has been dead for
some hours. We must find his murderer."
"It is good of you to come, Watson," said Holmes. "Tell me, what do you
make of it?"

"Watson, I have a question for you. Have you observed the dust on the
windowsill?"
"I confess I have not, Holmes."
"Then you have missed the most important clue of all. The murderer
entered through the window."

"A study in scarlet," murmured Holmes. "It is a string of murders, and
all very strange. I shall require your assistance."

"My dear Holmes!" "What is it, Watson?" "I believe you are right. I
believe we have our man." "Excellent. Let us go at once."

"Goodbye, Mr. Holmes," said the lady. "I owe you my life, and my
husband's, and my child's. I shall never forget your kindness."

"You did very well indeed," said he. "It was a very simple matter."

"Some morning," said Holmes, smiling, "I think we shall find that we have
our hands quite full."
"""


# =====================================================================
def tokenize(text):
    """Lowercase, strip punctuation, return word list. Keep contractions."""
    text = text.lower()
    text = re.sub(r"[^a-z\s']", " ", text)
    words = text.split()
    return [w for w in words if len(w) > 1]


def select_vocab(words, n=100):
    counts = Counter(words)
    return [w for w, _ in counts.most_common(n)]


def build_K(words, vocab, window=3):
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
            if words[j] in word_to_idx:
                wj = word_to_idx[words[j]]
                C[wi, wj] += 1
    total = C.sum()
    rt = C.sum(1)
    ct = C.sum(0)
    PPMI = np.zeros_like(C)
    for i in range(N):
        for j in range(N):
            if C[i, j] > 0 and rt[i] > 0 and ct[j] > 0:
                p_ij = C[i, j] / total
                p_i = rt[i] / total
                p_j = ct[j] / total
                PPMI[i, j] = max(0, np.log(p_ij / (p_i * p_j)))
    return PPMI, C


def embed_via_oscillator(K, n_dims=12, depth=8):
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
    words = tokenize(input_text)
    in_vocab = [w for w in words if w in vocab]
    oov = [w for w in words if w not in vocab]
    if not in_vocab:
        return None, words, oov
    query_vec = np.zeros(embedding.shape[1])
    for w in in_vocab:
        query_vec += embedding[vocab.index(w)]
    sims = []
    excl = set(in_vocab)
    for i, w in enumerate(vocab):
        if w in excl:
            continue
        sims.append((w, cos_sim(query_vec, embedding[i])))
    sims.sort(key=lambda x: -x[1])
    return sims[:k], in_vocab, oov


def main():
    print("=" * 78)
    print(" 100-node oscillator trained on 3 books")
    print(" Alice in Wonderland + A Tale of Two Cities + Sherlock Holmes")
    print("=" * 78)

    # Combine corpora
    all_text = ALICE_TEXT + " " + TWO_CITIES_TEXT + " " + SHERLOCK_TEXT
    words = tokenize(all_text)
    print(f"\n  Total content tokens: {len(words)}")
    print(f"  Per-book breakdown:")
    print(f"    Alice:      {len(tokenize(ALICE_TEXT))} tokens")
    print(f"    Two Cities: {len(tokenize(TWO_CITIES_TEXT))} tokens")
    print(f"    Sherlock:   {len(tokenize(SHERLOCK_TEXT))} tokens")

    # Top-100 vocab
    vocab = select_vocab(words, n=100)
    print(f"\n  Top-100 vocabulary selected.")
    counts = Counter(words)
    top_30 = [(w, counts[w]) for w in vocab[:30]]
    print(f"  Top 30: {[w for w, _ in top_30]}")

    # Build K
    print("\n  Building PPMI (window=3)...")
    K, C = build_K(words, vocab, window=3)
    n_edges = (C > 0).sum()
    print(f"    {n_edges} nonzero co-occurrence pairs")

    # Embed
    print("\n  Running oscillator with 12-mode deflation cascade...")
    t0 = time.time()
    emb, eigvals = embed_via_oscillator(K, n_dims=12, depth=8)
    print(f"    Done in {time.time()-t0:.1f}s")
    print(f"    Eigenvalues: {[f'{e:.2f}' for e in eigvals]}")

    # =================================================================
    print("\n" + "═" * 78)
    print(" INTERACTION")
    print("═" * 78)

    # The interesting prompts
    prompts = [
        "hello how are you",
        "what is your name",
        "tell me a story",
        "who are you",
        "are you mad",
        "do you remember",
        "the queen",
        "love is dead",
        "what do you observe",
        "what time is it",
        "i am tired",
        "where am i",
        "what do you see",
        "the rabbit hole",
        "good night",
    ]

    for prompt in prompts:
        print(f"\n  > {prompt}")
        result, in_vocab, oov = respond(prompt, emb, vocab, k=8)
        if not result:
            print(f"    [no in-vocab words; OOV: {oov}]")
            continue
        print(f"    [in-vocab: {in_vocab}]" + (f"  [oov: {oov}]" if oov else ""))
        print(f"    Substrate associates:")
        for w, s in result:
            print(f"      {w:>15s}  ({s:+.3f})")


if __name__ == "__main__":
    main()
