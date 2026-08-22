#!/usr/bin/env python3
"""Merge new glossary entries into reference/glossary.mdx, keeping each letter
section alphabetical by term. Idempotent: an entry whose term already exists is
skipped rather than duplicated, so this can be re-run after future page additions.

Entry format assumed by the parser: a paragraph beginning `**Term** — ...`,
separated from its neighbours by a blank line, under a `## X` letter heading.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "src/content/docs/reference/glossary.mdx"

NEW = r"""
**Activation patching** — replacing one activation in a forward pass with the
value it took on a different input, then measuring the effect on the output. The
workhorse causal method in [interpretability](/foundations/interpretability/);
correlational evidence about a neuron means little without it.

**AdamW** — Adam with weight decay applied directly to the parameters rather than
folded into the gradient. The default optimiser for transformers, and the fix
matters: L2-in-the-gradient and true weight decay are not equivalent under
adaptive scaling. See [Optimization](/training/optimization/).

**Advantage** — how much better an action was than the policy's average from that
state, $A(s,a) = Q(s,a) - V(s)$. Subtracting the baseline leaves the policy
gradient unbiased while cutting its variance, which is why nearly every practical
method estimates advantages rather than raw returns. See [Reinforcement
Learning](/training/reinforcement-learning/).

**Anisotropy** — the tendency of contextual embeddings to occupy a narrow cone
rather than filling the space, so that random pairs of vectors have high cosine
similarity. Measured, and partly correctable by whitening or removing dominant
directions. See [Latent Spaces](/foundations/latent-spaces/).

**ATE (Average Treatment Effect)** — $\mathbb{E}[Y(1) - Y(0)]$, the expected
difference in outcome between treating everyone and treating no one. A
counterfactual quantity, not a correlation, and only identifiable from
observational data under assumptions you must state. See [Causal
Inference](/foundations/causal-inference/).

**Autoregressive model** — a generative model that factorises the joint
distribution into a product of conditionals, $p(x) = \prod_i p(x_i \mid x_{<i})$,
and samples one element at a time. Exact likelihoods, sequential sampling. See
[Generative Models](/architectures/generative-models/).

**Belief state** — the posterior over the hidden environment state given the full
history of observations and actions. The provably sufficient statistic for acting
optimally in a POMDP, and the thing every recurrent or latent-state model is
approximating whether it says so or not. See [State
Representations](/foundations/state-representations/).

**Bisimulation** — an equivalence relation that treats two states as identical
when they yield the same rewards and transition to equivalent states. Gives a
principled answer to "which details may a state representation discard", though
the exact metric is usually intractable. See [State
Representations](/foundations/state-representations/).

**Boltzmann machine** — an energy-based model over binary units with pairwise
couplings, trained by contrasting data statistics against model statistics. The
historical root of the modern [energy-based
model](/architectures/energy-based-models/) view, and the origin of the
positive/negative phase structure that still shapes the field.

**BPE (Byte-Pair Encoding)** — builds a subword vocabulary by repeatedly merging
the most frequent adjacent pair. Originally a 1994 compression algorithm,
repurposed for NLP; still the most widely deployed tokenizer. See
[Tokenization](/foundations/tokenization/).

**Byte-level BPE** — BPE run over raw bytes rather than Unicode characters, so
the vocabulary can represent any string with no out-of-vocabulary case at the
cost of longer sequences for non-Latin scripts. See
[Tokenization](/foundations/tokenization/).

**Calibration** — whether a model's stated confidence matches its empirical
accuracy. A model can be highly accurate and badly calibrated, which matters
whenever the output feeds a decision rather than a leaderboard. See
[Evaluation](/foundations/evaluation/).

**Circuit** — a subgraph of a network's computation that implements an
identifiable behaviour end to end. The unit of explanation in mechanistic
[interpretability](/foundations/interpretability/); [induction
heads](/training/in-context-learning/) are the canonical example.

**Confounder** — a variable that causes both the treatment and the outcome,
manufacturing an association between them that survives any amount of data. The
central obstacle in [causal inference](/foundations/causal-inference/), and the
reason "we controlled for it" is a claim requiring justification.

**Contamination** — benchmark test data appearing in a model's training corpus.
Silently inflates reported scores and is difficult to rule out for web-scale
pretraining, which is why recent results on old benchmarks should be read
sceptically. See [Evaluation](/foundations/evaluation/).

**Continuous batching** — an inference scheduler that admits and retires requests
at the token level rather than waiting for a whole batch to finish. Large
throughput gains for generation workloads with heterogeneous lengths. See
[Inference](/systems/inference/).

**Contrastive divergence** — an approximate maximum-likelihood method for
energy-based models that runs only a few MCMC steps from the data rather than to
equilibrium. Biased, but the bias is often tolerable and the alternative is
intractable. See [Energy-Based
Models](/architectures/energy-based-models/).

**CTC (Connectionist Temporal Classification)** — a loss that marginalises over
all alignments between an input sequence and a shorter target, removing the need
for frame-level labels. The foundation of alignment-free speech recognition. See
[Speech and Audio](/domains/speech-audio/).

**Data parallelism** — replicating the model across devices and splitting the
batch, then all-reducing gradients. The simplest scaling axis and the first one
to use; it does nothing for models too large to fit on one device. See
[Distributed Training](/systems/distributed-training/).

**Demonstration** — an input–output example placed in the prompt. Min et al.
showed these largely supply label space, format and input distribution rather
than the mapping itself. See [In-Context
Learning](/training/in-context-learning/).

**Denoising score matching** — estimating $\nabla_x \log p(x)$ by training a model
to predict the noise added to corrupted data. The identity that connects
[energy-based models](/architectures/energy-based-models/) and
[diffusion](/architectures/diffusion/), and the reason diffusion sidesteps the
partition function entirely.

**Disentanglement** — the property that individual latent coordinates correspond
to independent generative factors. Intuitively appealing, provably unidentifiable
without inductive bias or supervision, and consequently much weaker in practice
than the visualisations suggest. See [Latent
Spaces](/foundations/latent-spaces/).

**do-operator** — Pearl's notation $p(y \mid do(x))$ for the distribution of $y$
under an intervention that sets $x$, as distinct from the observational
$p(y \mid x)$. The formal difference between causation and correlation. See
[Causal Inference](/foundations/causal-inference/).

**Double descent** — test error falling, rising near the interpolation threshold,
then falling again as capacity grows past it. Direct evidence that the classical
bias–variance picture is incomplete for overparameterised models. See
[Generalization](/foundations/generalization/).

**DPO (Direct Preference Optimization)** — fits a policy to preference pairs
directly through a closed-form relation to the implied reward, removing the
separate reward model and RL loop. Simpler and more stable than PPO-based RLHF,
with a narrower behaviour envelope. See [Post-Training](/training/post-training/).

**Energy function** — a scalar $E_\theta(x)$ assigning low values to plausible
configurations and high values to implausible ones. Defines a distribution only
after normalisation, and the whole difficulty of [energy-based
models](/architectures/energy-based-models/) lives in that normaliser.

**Fertility** — average tokens per word for a given tokenizer and language. The
standard measure of tokenizer efficiency; ratios above four between languages
translate directly into higher cost and shorter effective context for the
disadvantaged language. See [Tokenization](/foundations/tokenization/).

**Flow matching** — trains a continuous-time velocity field by regressing onto a
target vector field along a prescribed probability path, rather than reversing a
diffusion. Simpler objective, often straighter paths, fewer sampling steps. See
[Generative Models](/architectures/generative-models/).

**FSDP (Fully Sharded Data Parallel)** — shards parameters, gradients and
optimiser state across data-parallel ranks, gathering each layer only when
needed. The PyTorch-native form of the ZeRO idea. See [Distributed
Training](/systems/distributed-training/).

**GAN (Generative Adversarial Network)** — a generator trained against a
discriminator in a minimax game. Sharp samples, no tractable likelihood, and
training dynamics that are a genuine equilibrium problem rather than an
optimisation one. See [Generative Models](/architectures/generative-models/).

**Glitch token** — a token that appears in the vocabulary but was effectively
absent from training, leaving its embedding untrained and its behaviour erratic.
A direct consequence of fitting the tokenizer on a different corpus from the
model. See [Tokenization](/foundations/tokenization/).

**Gradient accumulation** — summing gradients over several micro-batches before
stepping, to emulate a large batch under a memory limit. Equivalent to the large
batch only if normalisation statistics are handled correctly. See [Distributed
Training](/systems/distributed-training/).

**GRPO (Group Relative Policy Optimization)** — replaces the learned value
baseline with the mean reward of a sampled group of completions for the same
prompt. Cheaper than PPO and well suited to verifiable-reward settings such as
maths and code. See [Reinforcement
Learning](/training/reinforcement-learning/).

**Hopfield network** — an associative memory storing patterns as minima of an
energy landscape; retrieval is descent from a partial cue. The modern continuous
variant has an update rule equivalent to attention, which is why it keeps
reappearing. See [Energy-Based Models](/architectures/energy-based-models/).

**HuBERT** — self-supervised speech representation learning by predicting cluster
assignments of masked frames, where the clusters are refined across iterations.
See [Speech and Audio](/domains/speech-audio/).

**In-context learning** — adapting behaviour from examples in the prompt with no
weight update. Named for what it looks like rather than what it is; whether it
constitutes learning is exactly the open question. See [In-Context
Learning](/training/in-context-learning/).

**Induction head** — a two-layer attention circuit that finds an earlier
occurrence of the current token and copies what followed it. Emerges during
training in a sharp phase change that coincides with the onset of in-context
learning. See [In-Context Learning](/training/in-context-learning/).

**Instrumental variable** — a variable that affects the treatment but influences
the outcome only through it, enabling causal identification despite unmeasured
confounding. The exclusion restriction it requires is an assumption, not
something the data can check. See [Causal
Inference](/foundations/causal-inference/).

**Intrinsic dimension** — the dimension of the manifold the data actually
occupies, typically far below the ambient dimension. The quantitative content of
the manifold hypothesis, and estimable. See [Latent
Spaces](/foundations/latent-spaces/).

**Jensen's inequality** — for convex $f$, $f(\mathbb{E}[X]) \le \mathbb{E}[f(X)]$.
The one-line reason the ELBO is a lower bound on the log-evidence. See
[Probability for ML](/foundations/probability-for-ml/).

**Langevin dynamics** — sampling by gradient ascent on log-density plus injected
Gaussian noise. The standard sampler for [energy-based
models](/architectures/energy-based-models/); needs only the score, never the
partition function, which is precisely why it is used.

**Linear representation hypothesis** — the claim that human-interpretable
features are encoded as directions in activation space, so that concepts can be
added, removed and steered linearly. Well supported for many features, not a
theorem, and the honest statement is "often, not always". See [Latent
Spaces](/foundations/latent-spaces/).

**Logit lens** — decoding intermediate residual-stream activations through the
output unembedding to read off what the model "believes" partway through. A
useful, biased probe: later layers are what the unembedding was trained for. See
[Interpretability](/foundations/interpretability/).

**LoRA (Low-Rank Adaptation)** — trains a low-rank update $BA$ alongside frozen
weights, cutting trainable parameters by orders of magnitude. The default
parameter-efficient fine-tuning method; the rank is a real capacity constraint,
not a free lunch. See [Fine-Tuning](/training/fine-tuning/).

**Manifold hypothesis** — the assumption that natural high-dimensional data lies
near a low-dimensional manifold. The reason representation learning is possible
at all, and the premise nearly every method on this site inherits. See [Latent
Spaces](/foundations/latent-spaces/).

**Message passing** — the computational pattern of graph neural networks: each
node aggregates transformed messages from its neighbours, then updates its own
state. Expressive power is bounded by the Weisfeiler–Lehman test. See [Graph
Neural Networks](/domains/graph-neural-networks/).

**Mixed precision** — computing in bf16 or fp16 while keeping a master copy of
weights and certain reductions in fp32. Nearly free throughput, provided the
numerically sensitive operations stay in high precision. See [Distributed
Training](/systems/distributed-training/).

**Mode collapse** — a generator producing a narrow slice of the data
distribution while scoring well on sample quality. Characteristic failure of
adversarial training, and the reason likelihood-free evaluation needs coverage
metrics as well as fidelity ones. See [Generative
Models](/architectures/generative-models/).

**MoE (Mixture of Experts)** — replaces a dense feed-forward layer with many
experts and a router that activates a few per token, decoupling parameter count
from per-token compute. See [Mixture of
Experts](/architectures/mixture-of-experts/).

**NCE (Noise-Contrastive Estimation)** — learns an unnormalised model by training
a classifier to distinguish data from a known noise distribution, turning density
estimation into discrimination. The ancestor of InfoNCE. See [Energy-Based
Models](/architectures/energy-based-models/).

**Neural collapse** — the terminal-phase phenomenon where within-class features
converge to their class means and those means arrange into a maximally separated
simplex. Elegant, well documented, and its relationship to generalisation is
still unsettled. See [Latent Spaces](/foundations/latent-spaces/).

**Normalizing flow** — a generative model built from invertible maps with
tractable Jacobian determinants, giving exact likelihoods and exact inference at
the cost of architectural constraints. See [Generative
Models](/architectures/generative-models/).

**Over-smoothing** — the convergence of node representations toward each other as
graph network depth increases, erasing the distinctions the network was meant to
learn. The main reason deep GNNs underperform shallow ones. See [Graph Neural
Networks](/domains/graph-neural-networks/).

**PagedAttention** — manages the KV cache in fixed-size non-contiguous blocks,
the way an OS pages memory, eliminating the fragmentation that otherwise wastes
most of the cache. See [Inference](/systems/inference/).

**Partition function** — the normaliser $Z(\theta) = \int e^{-E_\theta(x)}dx$
that turns an energy into a probability. Intractable in general, and essentially
every technique in [energy-based
models](/architectures/energy-based-models/) is a strategy for avoiding it.

**Pipeline parallelism** — splitting a model by layer across devices and flowing
micro-batches through the stages. Adds a pipeline bubble whose relative cost
falls as micro-batch count rises. See [Distributed
Training](/systems/distributed-training/).

**POMDP** — a Markov decision process in which the agent sees observations rather
than the true state. The formalism that makes state representation a problem
rather than a given. See [State
Representations](/foundations/state-representations/).

**PPO (Proximal Policy Optimization)** — a policy-gradient method that constrains
each update by clipping the importance ratio. Long the default for RLHF, being
displaced by simpler alternatives for language models. See [Reinforcement
Learning](/training/reinforcement-learning/).

**Predictive state representation** — represents state by the predicted outcomes
of future tests rather than by a posterior over hidden states. Grounded entirely
in observables, which sidesteps the question of what the "true" state is. See
[State Representations](/foundations/state-representations/).

**Quantization** — reducing numerical precision of weights or activations,
typically to int8 or 4-bit, to cut memory and bandwidth. The quality cost is
small when outlier channels are handled and large when they are not. See
[Inference](/systems/inference/).

**RAG (Retrieval-Augmented Generation)** — retrieving relevant documents and
conditioning generation on them. Addresses staleness and attribution; does not by
itself address the model ignoring or misreading what it retrieved. See
[Retrieval](/systems/retrieval/).

**Reward hacking** — optimising the specified reward in ways that violate the
intent behind it. Not a bug in the optimiser but a consequence of the reward
being a proxy. See [AI Safety](/foundations/ai-safety/).

**RLHF** — reinforcement learning from human feedback: fit a reward model to
human preference comparisons, then optimise the policy against it. The standard
post-training recipe, and the source of both instruction-following and
sycophancy. See [Post-Training](/training/post-training/).

**Score matching** — fits a model by matching $\nabla_x \log p_\theta(x)$ to the
data score, which eliminates the partition function because the gradient of
$\log Z$ with respect to $x$ is zero. See [Energy-Based
Models](/architectures/energy-based-models/).

**Selective scan** — the input-dependent state-space recurrence introduced by
Mamba, which lets the model choose what to keep and what to forget. What makes
SSMs competitive with attention on language rather than merely efficient. See
[State Space Models](/architectures/state-space-models/).

**SentencePiece** — a tokenizer implementation that operates on raw text with
whitespace treated as an ordinary symbol, so it needs no language-specific
pre-tokenizer. Often confused with an algorithm; it implements both BPE and
Unigram. See [Tokenization](/foundations/tokenization/).

**Speculative decoding** — a small draft model proposes several tokens and the
target model verifies them in one pass, accepting the longest correct prefix.
Output is distributionally identical to the target model. See
[Inference](/systems/inference/).

**SSM (State Space Model)** — a sequence model built on a linear recurrence that
can be evaluated as a convolution during training and a recurrence at inference,
giving linear-time generation with constant state. See [State Space
Models](/architectures/state-space-models/).

**Stationarity** — the property that a time series' statistical behaviour does
not change over time. Assumed by most classical forecasting methods and violated
by most real series, which is what differencing and detrending are for. See [Time
Series](/domains/time-series/).

**Sufficient statistic** — a function of the data that loses no information about
the quantity of interest. The precise standard a state representation must meet,
and the reason "compress the history" is only half the requirement. See [State
Representations](/foundations/state-representations/).

**Sycophancy** — a model agreeing with the user's stated position rather than
reporting its best estimate. A predictable consequence of optimising against
human approval ratings. See [AI Safety](/foundations/ai-safety/).

**Task vector** — a single activation direction, extracted from a prompt
containing demonstrations, that carries the task and can be transplanted into a
zero-shot forward pass to reproduce the behaviour. Causal evidence that
in-context tasks are represented compactly. See [In-Context
Learning](/training/in-context-learning/).

**TD learning** — updating a value estimate toward a bootstrapped target
$r + \gamma V(s')$ rather than a full Monte-Carlo return. Lower variance, biased
while the estimate is wrong, and the basis of most value-based RL. See
[Reinforcement Learning](/training/reinforcement-learning/).

**Tensor parallelism** — splitting individual weight matrices across devices so a
single layer is computed collectively. Needs high-bandwidth interconnect, since
it communicates within every layer rather than once per step. See [Distributed
Training](/systems/distributed-training/).

**Tokenizer-free model** — a model operating directly on bytes or characters,
learning its own segmentation. Removes the tokenizer's fairness and brittleness
problems at a compute cost that has been shrinking. See
[Tokenization](/foundations/tokenization/).

**Unigram LM** — a tokenizer that starts from a large candidate vocabulary and
prunes it to maximise corpus likelihood under a unigram model, keeping a
distribution over segmentations rather than a single greedy one. See
[Tokenization](/foundations/tokenization/).

**Weisfeiler–Lehman test** — a colour-refinement heuristic for graph isomorphism
that upper-bounds the expressive power of standard message-passing networks. The
reason some graph distinctions are unlearnable without extra features. See [Graph
Neural Networks](/domains/graph-neural-networks/).

**Whitening** — transforming features to have identity covariance. Used to
correct embedding anisotropy and, in Barlow Twins and VICReg, as the mechanism
that prevents collapse. See [Latent Spaces](/foundations/latent-spaces/).

**WordPiece** — a subword algorithm that merges the pair maximising corpus
likelihood rather than raw frequency, which is the single substantive difference
from BPE. See [Tokenization](/foundations/tokenization/).

**ZeRO** — shards optimiser state, gradients and parameters across data-parallel
ranks in three progressive stages, removing the redundancy of plain replication.
See [Distributed Training](/systems/distributed-training/).

**Arithmetic intensity** — floating-point operations performed per byte moved
from memory. Compare it to the machine's own ratio (about 295 FLOPs/byte for an
H100 in BF16) and you immediately know whether more compute or more bandwidth
would help. See [Accelerators](/hardware/accelerators/).

**BF16 (bfloat16)** — 16-bit float with FP32's 8 exponent bits and only 7
mantissa bits. Less precise than FP16 but with the same dynamic range, which is
why it displaced FP16 for training: low-precision failures are almost always
range failures, not precision failures. See
[Accelerators](/hardware/accelerators/).

**Chinchilla-optimal** — the parameter/token split that minimises loss for a
fixed *training* budget, roughly 20 tokens per parameter. Not the deployment
optimum, which is a smaller model trained longer. See [Compute
Budgeting](/hardware/compute-budgeting/).

**FP8** — 8-bit float in two variants: E4M3 (more precision, used for forward
weights and activations) and E5M2 (more range, used for gradients). The split
follows the same range-versus-precision logic that made BF16 win. See
[Accelerators](/hardware/accelerators/).

**HBM (High-Bandwidth Memory)** — stacked DRAM sitting beside the compute die,
delivering terabytes per second. Where your model actually lives, and the
resource that most workloads are waiting on. See
[Accelerators](/hardware/accelerators/).

**MFU (Model FLOPs Utilisation)** — achieved model FLOP/s divided by the
hardware's peak. Well-tuned large-scale pretraining reaches 40–55%; plan with
40%, never with peak. The variant that also counts recomputation is HFU and is
always larger. See [Compute Budgeting](/hardware/compute-budgeting/).

**NVLink** — NVIDIA's GPU-to-GPU interconnect, 900 GB/s per GPU on Hopper and
1.8 TB/s on Blackwell, against roughly 50 GB/s per GPU over the datacenter
network. That ~18× cliff at the node boundary is what decides which parallelism
strategy goes where. See [Choosing Hardware](/hardware/choosing-hardware/).

**Roofline model** — plots attainable performance against arithmetic intensity as
two lines: a bandwidth-limited diagonal and a compute-limited ceiling. A bound
and a diagnostic rather than a prediction, and the fastest way to find out which
limit you are under. See [Accelerators](/hardware/accelerators/).

**SM (Streaming Multiprocessor)** — the repeated unit of an NVIDIA GPU, 132 of
them on an H100, each containing CUDA cores, tensor cores, shared memory and a
register file. See [Accelerators](/hardware/accelerators/).

**Sparse (2:4 structured)** — a sparsity pattern keeping two non-zeros in every
group of four, which tensor cores can exploit for 2× throughput. Worth knowing
mainly because vendor spec sheets often print sparse figures without saying so;
dense is exactly half. See [Accelerators](/hardware/accelerators/).

**Tensor core** — fixed-function unit that consumes small matrix tiles and emits
a matrix product. Essentially all advertised FLOPs come from these, and their
fixed tile shapes are why hidden sizes divisible by 128 run faster than nearby
values. See [Accelerators](/hardware/accelerators/).

**Compute rule (6ND)** — the estimate that training a model of $N$ parameters on $D$ tokens
costs about $6ND$ FLOPs: 2 for the forward pass, 4 for the backward. Breaks down
at long context, for mixture-of-experts, and below about 1B parameters. See
[Compute Budgeting](/hardware/compute-budgeting/).

**ANN (approximate nearest neighbour)** — index structures that trade exact
correctness for speed, since exact high-dimensional search has no known algorithm
beating a linear scan. HNSW and IVF-PQ are the two dominant families. See [Vector
Search](/embeddings/vector-search/).

**Binary quantization** — storing one bit per dimension (the sign), giving 32×
compression and turning similarity into a popcount. Recall is recovered by
rescoring a shortlist against full-precision vectors. See [Vector
Search](/embeddings/vector-search/).

**Cross-encoder** — scores a query and document jointly in one forward pass, so
every query token attends to every document token. More accurate than a dual
encoder and unable to search, since nothing can be precomputed. Used to rerank.
See [Text Embeddings](/embeddings/text-embeddings/).

**Distributional hypothesis** — the claim that a word's meaning is approximated by
the contexts it appears in. Incomplete — it cannot separate *good* from *bad* —
and the foundation of every embedding method nonetheless. See [Word
Embeddings](/embeddings/word-embeddings/).

**Dual encoder (bi-encoder)** — embeds query and document independently through
shared weights, so the corpus can be embedded offline. That independence is what
makes retrieval over billions of documents possible, and it is also the source of
the accuracy gap against cross-encoders. See [Text
Embeddings](/embeddings/text-embeddings/).

**Hard negative** — a negative example that is plausible and wrong, mined by BM25,
by the model itself, or from a stronger model's rankings. What moves retrieval
quality once random negatives have plateaued — and the mechanism that makes it
work is the same one that collects false negatives. See [Text
Embeddings](/embeddings/text-embeddings/).

**HNSW** — a multi-layer proximity graph searched by greedy descent from a sparse
top layer to a dense bottom one. Fast, and its graph costs roughly as much memory
again as the vectors. See [Vector Search](/embeddings/vector-search/).

**Hubness** — the high-dimensional phenomenon where a few points appear in a
disproportionate share of nearest-neighbour lists. An under-diagnosed cause of the
same irrelevant document surfacing across unrelated queries. See [Vector
Search](/embeddings/vector-search/).

**In-batch negatives** — using the other documents in a training batch as negatives
for each query, which makes them free. It also makes batch size part of the
objective rather than just the gradient estimator. See [Text
Embeddings](/embeddings/text-embeddings/).

**IVF-PQ** — partitions the space by k-means, searches the nearest few cells, and
scans product-quantized codes with precomputed distance tables. Compact, and
slower to a given recall than HNSW. See [Vector
Search](/embeddings/vector-search/).

**Matryoshka representation** — trained with the loss applied at several nested
prefix dimensions, so a truncated vector is still usable. Lets you pick the
dimension at query time instead of at training time. See [Text
Embeddings](/embeddings/text-embeddings/).

**MTEB** — the Massive Text Embedding Benchmark, aggregating 50-plus datasets
across eight task types. A real improvement on what preceded it and now heavily
optimised against; rank does not predict performance on your corpus. See [Text
Embeddings](/embeddings/text-embeddings/).

**PMI (pointwise mutual information)** — how much more often two words co-occur
than independence would predict. The quantity that skip-gram with negative
sampling turns out to be implicitly factorising. See [Word
Embeddings](/embeddings/word-embeddings/).

**Product quantization** — splits a vector into subvectors and replaces each with
a k-means centroid index, giving byte-per-subvector storage and distance
computation by table lookup rather than arithmetic. See [Vector
Search](/embeddings/vector-search/).

**SGNS (skip-gram with negative sampling)** — word2vec's default objective:
distinguish real word-context pairs from sampled fakes. Levy and Goldberg proved
its optimum satisfies $v_w^\top u_c = \mathrm{PMI}(w,c) - \log k$. See [Word
Embeddings](/embeddings/word-embeddings/).

**WEAT (Word Embedding Association Test)** — adapts the Implicit Association Test
to embeddings, measuring differential association between target and attribute
word sets. Found human-like biases, including harmful ones, in embeddings trained
on ordinary web text. See [Word Embeddings](/embeddings/word-embeddings/).

"""


def split_entries(block: str):
    parts = [p.strip() for p in re.split(r"\n\s*\n", block.strip()) if p.strip()]
    out = []
    for p in parts:
        m = re.match(r"\*\*(.+?)\*\*", p)
        if not m:
            print(f"WARN: unparsed entry: {p[:60]}", file=sys.stderr)
            continue
        out.append((m.group(1), p))
    return out


def sort_key(term: str):
    # Sort on the bare term, ignoring any parenthetical gloss and case.
    t = re.sub(r"\s*\(.*?\)", "", term)
    return re.sub(r"[^a-z0-9 ]", "", t.lower())


def main():
    text = GLOSSARY.read_text()
    head, body = text.split("\n## A\n", 1)
    body = "## A\n" + body

    # Parse existing sections.
    chunks = re.split(r"\n(?=## )", body)
    sections = {}
    order = []
    for c in chunks:
        letter = c.split("\n", 1)[0][3:].strip()
        rest = c.split("\n", 1)[1] if "\n" in c else ""
        sections[letter] = split_entries(rest)
        order.append(letter)

    existing = {sort_key(t) for entries in sections.values() for t, _ in entries}

    added = 0
    for term, para in split_entries(NEW):
        if sort_key(term) in existing:
            continue
        letter = sort_key(term)[0].upper()
        sections.setdefault(letter, [])
        sections[letter].append((term, para))
        existing.add(sort_key(term))
        added += 1

    letters = sorted(sections.keys())
    out = [head.rstrip(), ""]
    total = 0
    for letter in letters:
        entries = sorted(sections[letter], key=lambda e: sort_key(e[0]))
        total += len(entries)
        out.append(f"## {letter}")
        out.append("")
        for _, para in entries:
            out.append(para)
            out.append("")

    GLOSSARY.write_text("\n".join(out).rstrip() + "\n")
    print(f"added {added} entries; glossary now has {total} across {len(letters)} letters")


if __name__ == "__main__":
    main()
