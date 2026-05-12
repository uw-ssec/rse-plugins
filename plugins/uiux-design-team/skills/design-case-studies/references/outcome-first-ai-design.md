# Outcome-First Design in the AI Era

> Back to [Design Case Studies](../SKILL.md)

Most teams are still shipping outdated software without even realizing it -- designing BlackBerrys in the iPhone era. They pad AI features onto legacy interfaces instead of rethinking what an app even is. But companies like the Browser Company (Dia) and Intercom (Finn) have seen the next curve. They are not just adding AI to interfaces. They are replacing interfaces with outcomes. This analysis breaks down what outcome-first design means in the AI era, why these companies are betting their futures on it, and the framework for evaluating where AI should replace your interface entirely versus where the experience still matters.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [The BlackBerry Lesson](#the-blackberry-lesson) | 18-56 | Why winning companies fail when the interaction layer shifts |
| [Dia: The iPhone Moment for Browsing](#dia-the-iphone-moment-for-browsing) | 58-120 | Sunsetting a popular product to build an outcome-first browser |
| [Intercom Finn: Outcomes as a Pricing Model](#intercom-finn-outcomes-as-a-pricing-model) | 122-186 | A category leader throwing out its own playbook for AI-native resolution |
| [The AI Disruption Matrix](#the-ai-disruption-matrix) | 188-260 | Framework for evaluating where AI replaces UI versus where experience still matters |
| [Edge Cases: When Interfaces Must Stay](#edge-cases-when-interfaces-must-stay) | 262-316 | Privacy, information density, and judgment-heavy contexts |
| [Cross-Case Principles](#cross-case-principles) | 318-362 | Shared patterns across both products and the framework |
| [Transferable Playbook](#transferable-playbook) | 364-440 | How to apply outcome-first design to your own product |

## The BlackBerry Lesson

Most people forget BlackBerry was winning. They owned almost half the US smartphone market. Presidents used it. CEOs swore by it. Then Apple announced the iPhone, and within a few years, texting with keyboards and navigating with scroll balls was a thing of the past.

BlackBerry did not fail because they were bad at building phones. They failed because the rules of the game changed and they did not realize it until it was too late.

| Era | Interaction Layer | What Won |
|-----|------------------|----------|
| **Pre-iPhone** | Physical keyboard, scroll ball, menu navigation | Speed of email, security, physical precision |
| **Post-iPhone** | Touch-first, app-centric, gesture-based | Ecosystem, simplicity, direct manipulation |
| **AI era (now)** | Outcome-first, conversation-driven, invisible UI | Speed to outcome, automation, contextual intelligence |

The iPhone introduced a new interaction layer -- touch-first and app-centric -- while BlackBerry was still building for a world people were walking away from. Today, the same shift is happening again. Interfaces like keyboards back then are now becoming less important because with AI, we are forced to think much more about outcomes and much less about screens.

Most startups are still padding AI features onto legacy interfaces. That is the BlackBerry move. The question is no longer "how do we make this screen better?" It is "does the user even need this screen at all?"

---

## Dia: The iPhone Moment for Browsing

Arc was ambitious, beautiful, and clearly innovative. But at its core, it was still based on an old model of how interfaces should behave. Instead of incrementally iterating and padding it with AI features, the Browser Company announced that Arc would be no more. In its place, they would build a reimagined browser called Dia.

### The Design Decision

The Browser Company made one of the boldest moves in recent product history -- sunsetting a popular, growing product to build something fundamentally different:

- **Sunset Arc** despite significant user love and momentum, because the underlying model was outdated
- **Build Dia as outcome-first** -- not trying to deliver a better browsing experience, but trying to deliver browsing outcomes without making you browse
- **Collapse the flow** -- users do not navigate, they ask and it answers
- **Skip steps entirely** -- the journey itself often disappears, delivering what you came for faster than you knew was possible
- **Reject incremental AI addition** -- no "AI features bolted onto a browser," but a fundamentally new interaction model

### The Business Impact

Dia represents a strategic bet that the browsing paradigm is about to shift as dramatically as the phone paradigm shifted with the iPhone. The Browser Company is betting that the first company to deliver browsing outcomes without browsing will own the next era, just as the first company to deliver phone capabilities through touch owned the smartphone era.

### Principle Mapping

| Principle | Application in Dia |
|-----------|-------------------|
| Outcome-first design | Dia does not optimize the browsing journey. It removes the journey. The outcome (finding information, completing a task) is delivered directly, without requiring the user to navigate between pages, tabs, and search results. |
| Norman: Behavioral | The interaction model is reduced to its minimum: ask and receive. The cognitive load of browsing -- choosing links, evaluating pages, managing tabs -- is eliminated, not simplified. |
| Hick's Law (inverted) | Traditional browsers present unlimited choices (links, tabs, search results). Dia collapses choices to zero by delivering the answer directly. Decision fatigue is eliminated at the architectural level. |
| Progressive reduction | As AI capability increases, the interface progressively reduces. Dia is designed so that the better the AI gets, the less interface is needed. The product improves by becoming less visible. |
| Krug's "Don't Make Me Think" (extreme) | Browsing requires constant thinking -- which link, which tab, which result. Dia takes "don't make me think" to its logical conclusion: do not make the user interact at all. |

### Key Design Patterns

**Outcome, not experience.** Dia is not trying to deliver a better browsing experience. It is trying to deliver browsing outcomes without making you browse. This is the critical distinction. Outcome-first design in the AI era means the journey itself often disappears entirely.

**The courage to sunset.** The Browser Company did not try to evolve Arc into Dia. They understood that bolting AI onto an old interaction model would produce a better BlackBerry, not an iPhone. Sometimes the right move is to start from zero.

**Collapse, do not optimize.** Traditional product design optimizes flows -- fewer clicks, faster load times, clearer navigation. Outcome-first design collapses flows -- removing the steps entirely so the user goes directly from intent to result.

**Design for disappearance.** The better Dia's AI becomes, the less interface is needed. This inverts the traditional design goal. Instead of making the interface better, you make it less necessary. The product improves by becoming invisible.

### Transferable Lessons

1. **Ask whether the journey needs to exist at all.** Before optimizing a flow, ask whether AI can deliver the outcome directly.
2. **Bolting AI onto old interfaces is the BlackBerry move.** If the interaction model is outdated, incremental AI features will not save it.
3. **Have the courage to sunset.** If the underlying paradigm is shifting, protecting your existing product may be more dangerous than replacing it.
4. **Design for progressive disappearance.** Build products where better AI means less interface, not more features.

---

## Intercom Finn: Outcomes as a Pricing Model

Intercom was already a category leader in customer support. Super clear product-market fit, huge brand equity, thousands of customers. Which makes it kind of insane that instead of protecting this old playbook, they threw it out.

### The Design Decision

Within a week of ChatGPT launching, Intercom paused the road map and built Finn:

- **AI-native product** focused on one thing: resolving questions instantly
- **Outcome comes first** -- customers get a direct AI-powered resolution before they ever touch a help article or a human rep
- **Interface role changed** -- the dashboard still exists, but its role shifted from primary workspace to oversight layer
- **Pricing based on resolved tickets** -- the business model itself is based on successful outcomes, not seats or features
- **Cannibalized their own product** -- Finn directly competes with Intercom's traditional support product

### The Business Impact

Finn is now Intercom's fastest-growing product ever and has become the company's main focus. By aligning pricing with outcomes (resolved tickets), Intercom created a model where the customer only pays when the product actually works. This is the ultimate expression of outcome-first design: the business model and the product design share the same metric.

### Principle Mapping

| Principle | Application in Intercom Finn |
|-----------|------------------------------|
| Outcome-first design | Finn delivers the resolution before the interface. The customer's question is answered by AI before they navigate help articles, search knowledge bases, or wait for a human agent. |
| Norman: Behavioral | The support interaction is reduced from a multi-step flow (search, read, maybe contact support, wait for reply) to a single exchange (ask, receive answer). The cognitive load is near zero. |
| Jobs to Be Done (Christensen) | The job is not "navigate a help center." The job is "get my question answered." Finn is designed around the job, not around the interface that historically surrounded it. |
| Disruptive innovation (Christensen) | Intercom disrupted itself before a competitor could. They recognized that their existing product model -- human agents using a dashboard -- was vulnerable to AI-native alternatives. |
| Alignment of incentives | Pricing by resolved ticket means Intercom only makes money when the product delivers its intended outcome. The pricing model and the product design reinforce each other. |

### Key Design Patterns

**The interface did not disappear, but its role changed.** Finn still has a dashboard. But the dashboard shifted from being the primary workspace to being an oversight and exception-handling layer. The outcome (resolution) happens before the interface is needed.

**Outcome-based pricing as design constraint.** When your revenue depends on successful outcomes, every design decision is filtered through one question: does this help resolve the customer's question? This constraint produces clarity that feature-based pricing never does.

**Self-disruption over self-preservation.** Intercom could have protected their existing product and added AI as a feature. Instead, they built a product that competes with their own legacy offering. This is strategically painful but existentially necessary.

**One-thing focus.** Finn does one thing: resolve questions instantly. This extreme focus on a single outcome creates a product that is easy to understand, easy to adopt, and easy to measure.

### Transferable Lessons

1. **Align pricing with outcomes.** When you charge for results instead of access, every design decision becomes clearer.
2. **The interface can change roles without disappearing.** Dashboards and screens may shift from primary workspace to oversight layer as AI handles the primary flow.
3. **Self-disruption is safer than waiting to be disrupted.** Build the product that threatens your current model before someone else does.
4. **Focus on one outcome.** The clearer the target outcome, the more aggressively you can design toward it.

---

## The AI Disruption Matrix

Designing for outcomes is nothing new. But with AI, we can now design for outcomes by skipping steps entirely. The question is: which steps? Which flows? Which interfaces?

### The Matrix

Evaluate your product -- or individual flows within your product -- along two dimensions:

| | **Utility-Focused** | **Experience-Focused** |
|---|---|---|
| **Repetitive / Rule-Based** | **HIGH AI RISK** -- Automate or remove. These interfaces will be rebuilt from scratch. | **MODERATE AI RISK** -- AI amplifies but does not replace. Experience matters but efficiency gains are significant. |
| **Nuanced / Judgment-Heavy** | **MODERATE AI RISK** -- AI assists but human stays in the loop. Interface shifts to oversight. | **LOW AI RISK** -- Interface IS the value. AI enhances the experience but never replaces it. |

### High AI Risk: Automate or Remove

When something is highly repetitive, mechanical, rule-based, and utility-focused, you are in the AI danger zone. These are the interfaces that will be automated, removed, or rebuilt from scratch.

**Example: Video editing timelines.** A huge part of professional editing is rule-based -- trimming gaps, fine-tuning audio, syncing tracks, removing silences. All of this is now automatable by AI. If you are building the next editing app, the question is no longer "how do we make the timeline easier?" It is "does the user even need to touch the timeline at all?"

**Example: Customer support flows.** Searching knowledge bases, reading help articles, waiting for human agents -- these are repetitive utility steps between the user and their outcome (getting an answer). Finn eliminates them.

### Low AI Risk: Interface Is the Value

Apps that are emotion-oriented, judgment-heavy, or where the interaction itself is the value face low AI disruption risk.

**Example: Games.** While you are trying to reach an outcome (winning), the gameplay itself is the goal. AI can amplify the experience -- adjusting difficulty, generating narrative -- but it will not replace the UI or remove the human from the loop. Designing for delight becomes even more important.

**Example: Creative tools for expression.** A musician using a synthesizer is not trying to reach an outcome efficiently. The interaction with the instrument is the experience. AI can suggest, but it cannot replace the creative act.

### The Key Question

"Can AI replace this interface?" is the wrong question. The right question is: **is the interface just a means to an end, or is the experience itself?**

If the interface is a means to an end, AI will eventually eliminate it. If the interface is the experience, AI will enhance it.

---

## Edge Cases: When Interfaces Must Stay

Full outcome-first automation does not always make sense. Several contexts require interfaces to remain visible and interactive:

### Privacy-Sensitive Contexts

Checking your bank balance in a co-working space. You probably do not want to say it out loud and you definitely do not want an assistant reading it back to you. Voice-based or invisible interfaces fail when the content is sensitive and the environment is public.

**AI's role:** Background intelligence -- flagging unusual transactions, predicting upcoming bills, proactively nudging when spending spikes. The interface stays visual and private. AI works behind it, not instead of it.

### Information-Dense Decision-Making

Investment dashboards, analytics platforms, medical records. Users need to see multiple data points side by side, scan visual patterns, and make human decisions fast. Collapsing these into a single AI response would remove the context that enables judgment.

**AI's role:** Summarizing trends, recommending actions, highlighting anomalies. The interface stays visible and flexible. AI augments the data layer rather than replacing the visual layer.

### Regulatory and Accountability Contexts

Medical diagnosis, legal documents, financial audits. Removing the interface removes the audit trail. Humans need to see, verify, and sign off on decisions in regulated contexts.

**AI's role:** Drafting, flagging, pre-processing. The interface serves as the verification and accountability layer. AI does the work; the interface proves the work was reviewed.

### The Exception, Not the Rule

These are real constraints. But they are exceptions, not the rule. In most products, the default assumption should be that you are not thinking deeply enough about user outcomes and how you can cut steps.

---

## Cross-Case Principles

Four principles recur across both products and the framework:

### 1. Think in Outcomes, Not Screens

Both Dia and Finn start from the same question: what is the user trying to achieve? Not "what should this screen look like?" but "what outcome does the user want?" When you design around outcomes, the interface becomes a variable -- sometimes necessary, sometimes reducible, sometimes eliminable.

### 2. Collapse, Do Not Optimize

Traditional product design optimizes flows. Outcome-first design in the AI era collapses them. The difference is fundamental:

| Approach | Method | Result |
|----------|--------|--------|
| **Optimization** | Fewer clicks, faster loads, clearer navigation | Better journey to the same destination |
| **Collapse** | Remove steps entirely, deliver outcome directly | No journey at all -- just the destination |

Dia collapses browsing into asking. Finn collapses support into resolving. The pattern is the same: identify the steps between user and outcome, then ask which ones can disappear.

### 3. Self-Disruption Is a Design Strategy

Both companies disrupted themselves. The Browser Company sunset Arc. Intercom cannibalized their core product with Finn. In both cases, the teams recognized that protecting the existing model was more dangerous than replacing it. Self-disruption is not just a business strategy. It is a design strategy -- the willingness to abandon an interaction model when the underlying paradigm shifts.

### 4. The Interface Role Shifts, Not Disappears

Neither product eliminated its interface entirely. Dia still has visual elements. Finn still has a dashboard. But the interface's role changed from primary workspace to oversight layer, exception handler, and verification tool. The outcome happens first. The interface catches what the outcome-first flow misses.

---

## Transferable Playbook

### Evaluating Your Product for Outcome-First Design

Use these four questions to evaluate every flow in your product:

| Question | What It Reveals |
|----------|----------------|
| **What is the quickest line between user and outcome?** | The theoretical minimum path. Everything else is potentially removable. |
| **What parts of that journey are mechanical and slow today?** | The highest-priority candidates for AI automation or removal. |
| **What parts would users happily never do again if something else handled it?** | The steps where AI replacement will be welcomed, not resisted. |
| **Is the interface a means to an end, or the experience itself?** | Whether to collapse the interface (means to end) or enhance it (experience itself). |

### The Outcome-First Design Process

```
1. DEFINE THE OUTCOME
   → What does the user actually want to achieve?
   → Strip away all interface assumptions

2. MAP THE CURRENT JOURNEY
   → Every step, screen, click, and decision between user and outcome
   → Identify mechanical/repetitive steps vs. judgment/experience steps

3. APPLY THE AI DISRUPTION MATRIX
   → Utility + repetitive = automate or remove
   → Experience + nuanced = enhance, do not replace
   → Edge cases = interface stays, AI works behind it

4. COLLAPSE WHAT YOU CAN
   → Remove steps that AI can handle entirely
   → Shift interfaces from primary to oversight role
   → Deliver the outcome before the user reaches the interface

5. ENHANCE WHAT REMAINS
   → For experience-focused flows, design for more delight, not less interface
   → Use AI to amplify the human experience, not replace it
   → Design for progressive disappearance where appropriate
```

### Implementation by Product Type

| Product Type | AI Strategy | Interface Strategy |
|-------------|-------------|-------------------|
| **Customer support** | Resolve before escalation (Finn model) | Dashboard shifts to oversight and exception handling |
| **Search / Research** | Deliver answers directly (Dia model) | Navigation collapses into conversation |
| **Content editing** | Automate mechanical tasks (trim, sync, clean) | Timeline shifts to review and creative decision layer |
| **Data dashboards** | Summarize, flag, recommend | Interface stays visible; AI augments the data layer |
| **E-commerce** | Predict intent, pre-select, auto-complete | Browsing collapses for repeat purchases; discovery stays visual |
| **Creative tools** | Suggest, generate options, handle tedium | Interface IS the value; AI serves the creative human |
| **Games / Entertainment** | Adjust difficulty, generate content, personalize | Interface IS the value; AI enhances the experience |

### Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|-------------|-----------------|
| Bolting AI features onto legacy interfaces | Produces a better BlackBerry, not an iPhone. The interaction model remains outdated. | Rethink the interaction model from the outcome backward. |
| Automating everything | Removes interfaces that users actually need (privacy, information density, judgment, accountability). | Apply the matrix. Not every flow should be collapsed. |
| Protecting the existing product | Leaves you vulnerable to competitors who will disrupt the category. Self-preservation becomes self-destruction. | Self-disrupt before someone else does. Build the product that threatens your model. |
| Optimizing when you should collapse | Making a flow 20% faster when you could eliminate it entirely. Incremental improvement on an outdated model. | Ask whether the journey needs to exist at all before making it better. |
| Removing the interface entirely in edge cases | Fails in privacy-sensitive, information-dense, or regulated contexts. | Keep the interface; shift AI to the background. Augment, do not replace. |
| Designing AI features instead of AI outcomes | Adding "AI-powered search" or "AI suggestions" as features rather than redesigning around the outcome AI enables. | Start with the outcome. Design backward from there. Let the interface be whatever the outcome requires. |

### The Bottom Line

The same shift that killed BlackBerry is happening right now in software. Interfaces that were the primary interaction layer are becoming less important because AI enables direct delivery of outcomes. Most teams are still building better BlackBerrys -- padding AI features onto legacy interfaces. The companies that will define the next era are the ones asking a different question: does the user even need this interface at all? Think in terms of outcomes, not screens. Design around the fastest, least distracting path to get there. Even if that path disappears entirely.

## See Also

- [Developer Tools](developer-tools.md) -- Raycast's workflow embedding and opinionated UX, a pre-AI example of collapsing steps between user and outcome
- [SaaS Dashboards](saas-dashboards.md) -- Stripe and Linear's dashboard design, representing the current paradigm that outcome-first AI will transform
- [Psychological Design Engines](psychological-design-engines.md) -- Perplexity's feedback loops as an example of AI-native interaction design
- [Emotional Design as Growth Engine](emotional-design-growth.md) -- Experience-focused design that remains important when the interface IS the value
- [Design Philosophies](../design-philosophies/SKILL.md) -- Hick's Law and cognitive load theory, the theoretical foundations for why collapsing flows works
- [Information Architecture](../information-architecture/SKILL.md) -- Navigation and content structure patterns that outcome-first design may fundamentally reshape
