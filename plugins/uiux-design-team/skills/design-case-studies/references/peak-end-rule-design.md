# The Peak-End Rule: Designing the Moments Users Actually Remember

> Back to [Design Case Studies](../SKILL.md)

Our brain does not remember an experience as a whole. It compresses it. What we actually recall is how we felt at two specific points: the peak -- the most intense part of the experience -- and the end -- the last part of the experience. Everything else is basically noise. Nobel Prize-winning psychologist Daniel Kahneman discovered this, and the most successful products exploit it deliberately. This analysis breaks down how Airbnb, Ahead, and Uber each design their peak and end moments to boost bookings, create stickiness, and reduce churn -- and provides the exact step-by-step checklist to apply it to your own product.

## Table of Contents

| Section | Lines | Description |
|---------|-------|-------------|
| [The Peak-End Rule Thesis](#the-peak-end-rule-thesis) | 18-56 | Why your brain compresses experiences and what Disney teaches us about memory design |
| [Airbnb: Peaks That Drive Bookings](#airbnb-peaks-that-drive-bookings) | 58-122 | Micro-animations and confidence signals at the moment of finding the perfect listing |
| [Ahead: Peaks That Create Stickiness](#ahead-peaks-that-create-stickiness) | 124-189 | Personalized report construction as a "made for me" peak moment |
| [Uber: Endings That Reduce Churn](#uber-endings-that-reduce-churn) | 191-256 | Post-ride completion flow that creates a virtuous cycle for drivers and riders |
| [The Five-Step Checklist](#the-five-step-checklist) | 258-340 | Map, peak, end, clean, and test -- the exact process for designing peak-end moments |
| [Cross-Case Principles](#cross-case-principles) | 342-386 | Shared patterns across all three products |
| [Transferable Playbook](#transferable-playbook) | 388-460 | How to apply peak-end design to your own product |

## The Peak-End Rule Thesis

Daniel Kahneman's research revealed something counterintuitive: the duration of an experience barely affects how we remember it. A 6-hour theme park visit is compressed into two data points. A 3-minute app session is compressed into the same two data points. What matters is not how long the experience lasted or how consistent it was. What matters is the peak and the end.

### The Disney Proof

Waiting in line for 90 minutes in the sun, hustling between attractions, fighting for $10 fries -- not everything about the Disney experience is smooth. But Disney knew something most theme parks did not: they could intentionally design what visitors remember.

They did so by leaning in hard on the peaks and making sure the final moment felt carefully crafted:

| Moment | Disney's Design |
|--------|----------------|
| **Peak** | Surprise character interactions, the climax of a ride, the first sight of the castle |
| **End** | The last firework show of the night, music playing as you exit the park, a character wave at the gate |
| **Negative moments** | Long lines managed with entertainment, shaded queues, and progress indicators |

The result: about **70% of Disney park visitors come back for a second visit**. Not because the entire day was flawless, but because the moments they remember were.

If Disney can pull this off in a 6-hour, $200 experience, what could you do with your app in a couple of minutes?

### The Two Rules

1. **Peak = the most emotionally intense moment.** This is the moment users feel the strongest emotion -- excitement, delight, pride, relief. It does not have to be the most important action. It has to be the most felt action.

2. **End = the last thing that happens.** This is the final impression before the user closes the app, finishes the flow, or walks away. It colors the memory of the entire experience retroactively.

Design both deliberately. Leave neither to chance.

---

## Airbnb: Peaks That Drive Bookings

Airbnb is known as one of the most design-focused companies on the planet. Every screen feels like it was crafted by hand. But the strongest parts of the app come later, because Airbnb knows that the first core moment for guests -- the one they really want to elevate into a peak -- is when they find that perfect listing.

### The Design Decision

Airbnb invests disproportionate design attention in two moments:

- **The peak: finding the perfect listing.** Micro-animations spring to life as you browse. Supporting tags surface unique value specific to your pick -- "Rare find," "Guest favourite," "Great for families." Every signal is designed to make you feel confident and excited at the moment of discovery.
- **The end: completing the booking.** A super slick purchase animation in Airbnb's trademark 3D style celebrates the reservation. The transition from "browsing" to "booked" is not just confirmed -- it is celebrated.
- **The ambient layer.** Friendly openings, subtle animations, animated icons as you switch between tabs. These do not create the peak, but they elevate the baseline so the peak stands taller.

### The Business Impact

Knowing how data-driven the team at Airbnb is, these peak-end moments have been tested extensively. The micro-animations and confidence signals at the discovery moment help boost booking rates. The celebration animation at checkout ends the experience on a high note, creating a positive memory that drives return visits and referrals.

### Principle Mapping

| Principle | Application in Airbnb |
|-----------|----------------------|
| Peak-end rule (Kahneman) | The most emotionally intense moment (finding the perfect listing) and the last moment (booking confirmation animation) are designed with disproportionate care. Everything between is good, but these two moments are exceptional. |
| Norman: Visceral | Micro-animations and 3D booking celebrations trigger immediate emotional responses. The visceral delight at these moments elevates the entire memory of the app experience. |
| Norman: Behavioral | Supporting tags ("Rare find," "Guest favourite") reduce uncertainty at the decision moment. The user feels confident because the interface provides behaviorally relevant reassurance. |
| Norman: Reflective | The polished booking animation creates a moment worth remembering. "I just booked on Airbnb" feels like an event, not a transaction. |
| Gestalt: Figure-ground | Peak moments pop against the ambient baseline. The micro-animations at listing discovery stand out because the surrounding experience is calm and clean. |

### Key Design Patterns

**Identify your user's emotional peak and elevate it.** For Airbnb guests, the peak is not the search, not the comparison, not the filters. It is the moment of finding the perfect listing -- "this is the one." Every design investment at that moment pays disproportionate returns.

**End with celebration, not confirmation.** A green checkmark says "done." A 3D animation in your trademark style says "you just did something exciting." The difference in emotional impact is enormous. The booking confirmation is the last moment before the user closes the app. Make it memorable.

**Build an ambient baseline that makes peaks stand taller.** Airbnb's tab animations and subtle motion create a consistently pleasant baseline. The peak moments feel even more special because the rest of the experience is already good. Peaks are relative to the baseline.

### Transferable Lessons

1. **Identify your user's core emotional peak** and invest disproportionate design effort there. It is not the most important action -- it is the most felt action.
2. **End with celebration, not just confirmation.** The last moment colors the entire memory.
3. **Build a good baseline so peaks stand taller.** Ambient quality makes intentional peaks feel even more special.
4. **Use confidence signals at the peak moment.** Tags, badges, and reassurance copy amplify the feeling of "I made the right choice."

---

## Ahead: Peaks That Create Stickiness

Most wellness apps lean on moral pressure or habit dashboards. Ahead, an Apple Design Award winner, took a different path. They designed a flow that guides you kindly from start to finish, with a peak moment that makes you feel like the product was made specifically for you.

### The Design Decision

Ahead crafts a deliberate peak-end sequence during the onboarding and first-use experience:

- **Smooth entry.** A quiet splash screen sets the vibe immediately. No noise, no overwhelm.
- **Self-profiling journey.** Key questions answered at just the right cadence -- not too fast, not too slow.
- **The peak: personalized report construction.** You are not just shown a report. A brief gets constructed right in front of you -- animated, progressive, building piece by piece. The user feels "this is made for me" at exactly the right moment.
- **The end: gentle return nudge.** Before closing the app, a gentle nudge to come back tomorrow. Subtly reinforcing that your time meant something and that the app cares about seeing you return.

### The Business Impact

Ahead won an Apple Design Award, which recognizes apps that deliver outstanding user experiences. The peak-end strategy creates stickiness -- users return not because of guilt or gamification pressure, but because they remember the experience positively. The personalized report peak creates an emotional anchor ("this app understands me") that drives retention.

### Principle Mapping

| Principle | Application in Ahead |
|-----------|---------------------|
| Peak-end rule (Kahneman) | The personalized report construction is the peak -- the most emotionally intense moment of the onboarding. The gentle return nudge is the end -- the last impression before app closure. Both are crafted with intent. |
| Norman: Reflective | "This app was made for me" is a reflective-level response. The personalized report creates identity-level engagement that transcends the immediate interaction. |
| Norman: Behavioral | Questions arrive at the right cadence -- not overwhelming, not boring. The pacing is itself a design decision that shapes the user's experience of the flow. |
| IKEA effect | Watching your report build in front of you creates a sense of co-creation. You answered the questions; the app built something from your answers. Users value it more because they participated. |
| Familiarity principle | The personalized output makes the product feel familiar and personal from the first session, increasing trust and return likelihood. |

### Key Design Patterns

**Construct the peak visibly.** Ahead does not dump a completed report on the screen. It builds the report in front of you, piece by piece. The construction process is the peak, not the result. Watching something being made for you is more emotionally intense than receiving a finished product.

**End with care, not with emptiness.** A lot of apps just end. They fall off without closure or the feeling of "you're done" or "you're doing great." Ahead closes with a gentle message encouraging the user to return, reinforcing that their time mattered.

**Pacing as emotional design.** The cadence of the self-profiling questions is carefully controlled. Too fast feels rushed and impersonal. Too slow feels tedious. The right pacing creates a sense of thoughtful, intentional interaction.

**Friendly stickiness over guilt-based retention.** Ahead does not use streak pressure or shame. The return nudge is gentle and caring. Stickiness comes from the positive memory of the peak, not from fear of breaking a streak.

### Transferable Lessons

1. **Build the peak visibly.** Let users watch their personalized result being constructed. The process is more emotionally powerful than the product.
2. **End with care.** A gentle closing message creates a better memory than an abrupt exit or a harsh streak reminder.
3. **Pace the experience deliberately.** Every interaction has a tempo. Match it to the emotional state you want to create.
4. **Choose friendly stickiness over guilt.** Positive memories drive return visits more sustainably than gamification pressure.

---

## Uber: Endings That Reduce Churn

Uber cannot really brag about fancy skeuomorphic icons or super cool animations. But there is one thing they reliably do better than most: they end the journey extremely well.

### The Design Decision

Uber's post-ride flow is a carefully designed end moment:

- **The peak is the destination.** Uber knows their riders' peak is reaching their destination. This happens in the real world, not in the app. So Uber does not try to manufacture a peak inside the interface.
- **Phone vibration** as a transition signal -- a tactile cue that the ride experience is transitioning to the end moment.
- **Rating the driver.** A simple, fast interaction that gives the rider a sense of closure and participation.
- **Tip opportunity.** A gentle, optional prompt. Not enforced, not aggressive. The rider can choose to leave a tip or skip.
- **Double reward framing.** Both rating and tipping are framed as rewards the user gives, not tasks the user performs. This activates a sense of generosity rather than obligation.

### The Business Impact

The end-of-ride flow creates a virtuous cycle: tips and high ratings incentivize drivers to provide better service, which improves rider experience, which increases ride frequency, which increases demand and supply reliability. The ending is not just a user experience decision -- it is a business model decision. Satisfied drivers stay on the platform. Better drivers attract more riders. The end moment reduces churn on both sides of the marketplace.

### Principle Mapping

| Principle | Application in Uber |
|-----------|---------------------|
| Peak-end rule (Kahneman) | The peak (arriving at destination) is a real-world moment Uber cannot control. So they invest everything in the end -- the post-ride flow. The last app interaction colors the entire ride memory. |
| Norman: Behavioral | The rating and tipping flow is fast, gentle, and optional. It wraps a sense of completion around the ending without adding friction or obligation. |
| Cialdini: Reciprocity | The driver provided a good ride. The tip prompt leverages the natural reciprocity impulse at the moment it is strongest -- right after the service was delivered. |
| Completion bias | Humans feel satisfaction when they complete a sequence. Rating + optional tip = a two-step closing sequence that gives riders the feeling of "done" rather than "abandoned." |
| Endowment effect | By making tipping feel like a gift the rider gives (not a fee the rider pays), Uber shifts the framing from transaction to generosity. Riders feel good about tipping rather than reluctant. |

### Key Design Patterns

**Do not compete with real-world peaks.** Uber's riders' peak is reaching their destination -- a moment that happens in the physical world. Uber does not try to manufacture a digital peak to compete with it. Instead, they focus all design energy on the end moment, which is entirely within the app's control.

**Wrap completion around the ending.** The rating and tip flow gives riders a sense of closure. Without it, the ride just ends -- the car stops, you get out, and there is no designed ending. The post-ride flow transforms an abrupt conclusion into a gentle, satisfying close.

**Gentle, not enforced.** The tip prompt is optional and polite. Uber knows that forced endings feel like obligations, not conclusions. The gentleness is what makes users willing to participate.

**Design endings that serve the business.** Uber's end moment is not just good UX. It directly serves the business by incentivizing driver quality, reducing churn on both sides of the marketplace, and creating a virtuous cycle of improving service.

### Transferable Lessons

1. **If the peak happens outside your app, focus on the end.** You cannot always control the peak moment, but you can always design the end.
2. **Wrap completion around the ending.** Give users a closing action that creates a sense of "done" rather than "abandoned."
3. **Keep endings gentle and optional.** Forced endings feel like obligations. Gentle endings feel like conclusions.
4. **Design endings that serve the business.** The post-experience moment is an opportunity for ratings, referrals, tips, feedback, and other business-critical actions.

---

## The Five-Step Checklist

A step-by-step process for applying peak-end design to any product:

### Step 1: Map the Customer Journey

Lay out every step your user takes in your core flow -- from sign-up to task completion to whatever the end looks like. Use sticky notes, FigJam, or any digital board. For each step, ask:

- Where is the user slowed down?
- Where might stress peak?
- Where is the quiet in between?

Save this as a living tool you will iterate on as your product evolves.

### Step 2: Pick Your One Well-Timed Peak

Pick just one spot in the journey to spark the peak moment:

| Good Peak Placement | Why It Works |
|--------------------|-------------|
| After completing a core task | The user is already feeling accomplishment. Amplify it. |
| At a milestone | The user recognizes progress. Celebrate it. |
| At a point of high effort | The user has invested. Reward the investment. |
| At the moment of discovery | The user found what they were looking for. Make it feel special. |

The peak could be a badge, a sparkle, an animation, surprise copy, or a personalized result. It does not have to be elaborate. It has to be intentional and well-timed.

### Step 3: Design the Ending

Do not save the magic for the end -- peak first. But a lot of apps just end, falling off without closure. Instead, use the ending state for:

- **Celebrating what was done.** "You showed up today. That's huge."
- **Encouraging what comes next.** "See you tomorrow for Day 3."
- **Reaffirming progress.** A summary card, a check mark, a completion message.

It does not have to be fancy, but it should be designed with intent.

### Step 4: Clean Up Negative Moments

Negative moments are as memorable as positive ones. Find them and reduce them:

| Negative Moment | Design Fix |
|----------------|-----------|
| Wait screens | Add progress indicators, microcopy, or subtle animation |
| Error states | Use uplifting microcopy and clear recovery paths |
| Long forms | Break into steps, add progress bars, celebrate section completion |
| Uncertainty | Add help text, tooltips, or contextual guidance before users ask |
| Dead space | Turn delays into opportunities with loading tips or previews |

### Step 5: Test and Iterate

Run variations of your peak moments:

- Timing changes (earlier vs. later in the flow)
- Emojis vs. icons
- Animations vs. static feedback
- Copy variations ("Nice work!" vs. "Task complete" vs. a personalized message)

Watch where people drop off and where they stay around longer than expected or necessary. That is your signal to dig in and tweak.

---

## Cross-Case Principles

Four principles recur across all three products:

### 1. Peak and End Are Design Decisions, Not Accidents

None of these products leave their peak or end to chance. Airbnb chose the listing discovery moment as the peak and designed micro-animations specifically for it. Ahead chose the personalized report construction. Uber chose the post-ride rating flow. In each case, the peak and end are deliberate design decisions, not byproducts of feature development.

### 2. Peaks Are Relative to Baseline

Airbnb's peak moments feel special because the ambient experience is already pleasant. If the baseline is chaotic, the peak does not stand out. If the baseline is good, even a small peak creates a memorable high point. Invest in baseline quality so your peaks stand taller.

### 3. Endings Create Business Value

Uber's ending drives a virtuous cycle of better drivers and more rides. Ahead's ending drives return visits. Airbnb's ending drives positive memory and referrals. In every case, the end moment is not just a UX nicety -- it is a business-critical design decision that affects retention, revenue, and growth.

### 4. Most Apps Just End

The biggest missed opportunity in product design is the ending. Most apps fall off without closure. There is no designed ending -- just an abrupt stop. Designing even a simple closing moment (a message, a summary, a gentle nudge) separates your product from the vast majority that neglect this moment entirely.

---

## Transferable Playbook

### Choosing Your Peak-End Strategy

Match the strategy to your product's specific challenge:

| Product Challenge | Peak Strategy | End Strategy | Reference |
|------------------|--------------|-------------|-----------|
| **Driving conversions** | Elevate the decision moment with confidence signals and celebration | End with a polished confirmation animation that feels like an event | Airbnb |
| **Creating stickiness / return visits** | Build a personalized result visibly in front of the user | End with a gentle, caring nudge to return | Ahead |
| **Reducing churn / building marketplace health** | Let the real-world experience be the peak | Design a closing flow that serves both user satisfaction and business goals | Uber |
| **Onboarding new users** | Create an aha moment that demonstrates core value | End the first session with encouragement and a reason to come back | Ahead + Airbnb |
| **Task completion flows** | Celebrate the completion with animation or acknowledgment | Summarize what was accomplished and suggest the next step | All three |

### Implementation Priority

1. **Identify your current peak and end.** They already exist, even if undesigned. What is the most emotionally intense moment? What is the last thing users experience?
2. **Decide if they are the right moments.** Your current peak might be a negative peak (frustration, confusion). Your current end might be abrupt or empty.
3. **Design one intentional peak.** Start with one moment. Make it feel special. Test it.
4. **Design the ending.** Add closure, celebration, or encouragement. Even a simple message changes the memory.
5. **Clean up negative peaks.** Find the moments of frustration, confusion, or boredom, and wrap them in care.

### Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|-------------|-----------------|
| Designing peaks everywhere | If everything is a peak, nothing is. Constant celebration creates noise, not memory. | Pick one moment and invest deeply in it. |
| Ignoring the ending | The end retroactively colors the entire experience. An abrupt stop makes even a good experience feel incomplete. | Always design a closing moment, even a simple one. |
| Making the peak too early | A peak during onboarding fades if the rest of the experience is flat. The peak needs to happen at a moment of genuine user engagement. | Place peaks at moments of core action, achievement, or discovery, not during setup. |
| Confusing features with peaks | Adding a feature is not a peak. A peak is an emotionally intense moment. Features are functional; peaks are felt. | Design for emotion at the peak moment, not just functionality. |
| Forced endings | Mandatory ratings, aggressive upsells, or required feedback at the end transforms closure into obligation. | Keep endings gentle, optional, and generous in tone. |
| Neglecting negative moments | A single frustrating moment can become the peak if it is the most intense emotion in the session. Negative peaks override positive ones. | Audit for negative peaks and reduce them before designing positive ones. |

### The Bottom Line

Our brains compress experiences into two moments: the peak and the end. Everything else is noise. The products that understand this -- Airbnb, Ahead, Uber, Disney -- do not try to make every moment perfect. They identify the two moments that matter, design them with disproportionate care, and let the memory do the rest. Your product already has a peak and an end. The question is whether you designed them or left them to chance.

## See Also

- [Emotional Design as Growth Engine](emotional-design-growth.md) -- Duolingo's emotional feedback loops and Revolut's micro-interaction polish, related to designing peak moments
- [Onboarding Psychology](onboarding-psychology.md) -- Breathwork's eureka effect and Marathon's goal gradient as peak-end applications in first-use experiences
- [Psychological Design Engines](psychological-design-engines.md) -- Headspace's emotional anchoring and Discord's social proof as techniques for engineering peak moments
- [SaaS Conversion Psychology](saas-conversion-psychology.md) -- Blinkist's progressive disclosure and Headspace's framing as peak-end strategies for trial flows
- [Motion Design](../motion-design/SKILL.md) -- Animation principles for implementing celebration screens, micro-animations, and transition moments
- [UX Writing](../ux-writing/SKILL.md) -- Microcopy for endings, success states, and the gentle encouragement that closes experiences well
