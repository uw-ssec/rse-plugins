[Back to Usability Evaluation](../usability-evaluation.md)

# Cognitive Walkthrough Methodology

## Overview

A cognitive walkthrough is a usability inspection method that evaluates how easy it is for new or infrequent users to accomplish tasks with a given interface. Unlike heuristic evaluation, which broadly assesses an interface against principles, a cognitive walkthrough follows a specific task step by step, evaluating learnability at each action. It focuses on the user's thought process when encountering the interface for the first time.

---

## Definition and When to Use

### What is a Cognitive Walkthrough?

A structured evaluation technique where analysts step through a task sequence from the user's perspective, asking a standardized set of questions at each step. The method is grounded in the CE+ theory of exploratory learning: users form goals, search for available actions, select an action they believe will make progress, and evaluate the system's feedback.

### When to Use

- **Early in design:** Evaluate wireframes or prototypes before user testing
- **Walk-up-and-use interfaces:** Kiosks, public terminals, consumer products
- **Onboarding and first-use flows:** Signup, setup wizards, first-time experiences
- **After redesigns:** Verify that new designs remain learnable
- **Resource constraints:** When you cannot recruit users for testing
- **Complex task flows:** Multi-step processes where learnability is critical

### When NOT to Use

- When evaluating expert-level features (cognitive walkthroughs focus on novice users)
- For broad usability assessment (use heuristic evaluation instead)
- When you need to measure actual user performance (use usability testing)

---

## Preparation Steps

### Step 1: Define User Profile

Document the target user's characteristics:
- Technical proficiency level
- Domain knowledge and familiarity
- Goals and motivations
- Prior experience with similar systems

```markdown
User Profile: First-time customer
- Technical skill: Basic (comfortable with email and web browsing)
- Domain knowledge: Knows what they want to buy but unfamiliar with this site
- Goal: Complete a purchase of a specific product
- Prior experience: Has used Amazon and similar e-commerce sites
```

### Step 2: Define the Task

Select a representative task that a new user would need to accomplish. The task should be:
- Specific and completable
- Representative of a common user goal
- Decomposable into discrete action steps

```markdown
Task: Purchase a medium blue t-shirt and have it shipped to a home address
```

### Step 3: Identify the Correct Action Sequence

Document every step the user must take to complete the task, from the starting screen to task completion. Be granular; each step should be a single user action.

```markdown
Action Sequence:
1. Navigate to the homepage
2. Click "Shop" in the main navigation
3. Click "T-Shirts" in the category menu
4. Click on the blue t-shirt product card
5. Select "Medium" from the size dropdown
6. Click "Add to Cart"
7. Click the cart icon in the header
8. Click "Proceed to Checkout"
9. Enter shipping address
10. Select shipping method
11. Enter payment information
12. Review order summary
13. Click "Place Order"
14. View order confirmation
```

### Step 4: Prepare Evaluation Materials

- Screenshots or prototype of each screen state
- The action sequence documented above
- Evaluation form with the four questions for each step
- User profile description for reference

---

## The Four Walkthrough Questions

At each step in the action sequence, evaluators ask these four questions from the perspective of the defined user:

### Question 1: Will the user try to achieve the right effect?

**What this asks:** Does the user's goal at this point match what the step requires? Will the user understand that this action is necessary to make progress?

**Success indicators:**
- The user's goal naturally leads them to seek this type of action
- The interface clearly communicates that this action is available and relevant
- No prerequisite knowledge is required that the user would not have

**Failure example:** The user wants to add an item to cart but does not realize they must first select a size. Nothing on the page indicates that size selection is required before the "Add to Cart" button becomes active.

### Question 2: Will the user notice that the correct action is available?

**What this asks:** Is the correct interface element visible and noticeable? Can the user find it without extensive searching?

**Success indicators:**
- The correct element is visible without scrolling (or scrolling is obviously needed)
- The element is visually prominent and distinguishable
- The element is in a location consistent with user expectations

**Failure example:** The "Proceed to Checkout" button is below the fold on the cart page, and the user sees only the cart items and totals without scrolling. Nothing indicates there is more content below.

### Question 3: Will the user associate the correct action with the desired effect?

**What this asks:** Once the user sees the correct element, will they understand that it does what they need? Is the label, icon, or affordance clear?

**Success indicators:**
- The label clearly describes the action's outcome
- The icon is universally recognizable or accompanied by text
- The affordance matches user expectations (buttons look clickable, links look linked)

**Failure example:** The button says "Continue" but the user expects it to say "Add to Cart." The user is unsure whether "Continue" will add the item or navigate to a different page.

### Question 4: If the correct action is performed, will the user see that progress is being made?

**What this asks:** After the user performs the action, does the system provide clear feedback indicating that the action was successful and the user is closer to their goal?

**Success indicators:**
- Visual feedback confirms the action (animation, state change, confirmation message)
- The user can see they are closer to the goal (progress indicator, page change)
- The feedback is timely (within 100-400ms)

**Failure example:** After clicking "Add to Cart," nothing visually changes. The cart icon does not update, and no confirmation toast appears. The user is unsure whether the item was added.

---

## Action Sequence Analysis

### Documenting Each Step

For each step in the action sequence, record the analysis:

```markdown
## Step 6: Click "Add to Cart"

### Screen State
[Screenshot or description of the product page with size selected]

### Q1: Will the user try to achieve the right effect?
YES. After selecting a size, the natural next step is to add the item to the cart.
The user's goal (purchase this shirt) maps directly to the "Add to Cart" action.

### Q2: Will the user notice the correct action is available?
YES. The "Add to Cart" button is large, green, and positioned directly below the
size selector. It is above the fold on both desktop and mobile.

### Q3: Will the user associate the action with the desired effect?
YES. "Add to Cart" is a universally understood label in e-commerce.
The shopping cart icon next to the text reinforces the meaning.

### Q4: Will the user see progress is being made?
PARTIAL. The cart icon in the header updates with a badge count (+1),
but this change is subtle and may be missed. There is no confirmation toast
or animation drawing attention to the cart update.

### Issues Found
- ISSUE CW-6a: Cart update feedback is too subtle. Add a confirmation toast
  or animate the cart icon to draw attention. Severity: Minor.
```

### Tracking Issues

Maintain a running issue log:

```markdown
| ID | Step | Question | Issue Description | Severity |
|----|------|----------|-------------------|----------|
| CW-1a | 3 | Q2 | "T-Shirts" category is in a dropdown; not visible without hover | Major |
| CW-5a | 5 | Q1 | No indication that size selection is required | Major |
| CW-6a | 6 | Q4 | Cart update feedback too subtle | Minor |
| CW-8a | 8 | Q2 | "Proceed to Checkout" below the fold | Major |
| CW-11a | 11 | Q3 | "Continue" label ambiguous; could mean "continue shopping" | Moderate |
```

---

## Success and Failure Stories

### Success Story

A narrative describing the user's thought process when the step works well:

> "The user sees the large green 'Add to Cart' button directly below the size selector. They recognize the familiar e-commerce pattern and click the button. The cart icon animates and displays a '1' badge. The user knows the item has been added and looks for a way to proceed to checkout."

### Failure Story

A narrative describing where and why the user's thought process breaks down:

> "The user has selected their t-shirt and is ready to add it to their cart, but the 'Add to Cart' button is grayed out. The user does not notice the small text above the button that says 'Please select a size.' They click the grayed-out button several times with no response. Frustrated, they scroll up and down looking for an error message. After 15 seconds, they notice the size dropdown is still set to 'Select Size' and realize they need to choose one."

**Failure stories are the most valuable output of a cognitive walkthrough.** They provide concrete, empathy-driven narratives that communicate usability problems effectively to stakeholders and developers.

---

## Comparison with Heuristic Evaluation

| Aspect | Cognitive Walkthrough | Heuristic Evaluation |
|--------|----------------------|---------------------|
| **Focus** | Learnability of specific task flows | Broad usability across the interface |
| **User model** | Novice/first-time user perspective | General user perspective |
| **Structure** | Step-by-step through task sequences | Free-form inspection against heuristics |
| **Output** | Issues tied to specific task steps | Issues tied to heuristic violations |
| **Evaluator count** | 1-3 sufficient | 3-5 recommended |
| **Time per evaluation** | 1-3 hours per task flow | 1-2 hours per evaluator |
| **Best for** | Walk-up-and-use, onboarding, setup flows | General usability audit |
| **Limitations** | Narrow scope (one task at a time) | May miss task-specific issues |

### When to Combine

Use both methods together for comprehensive coverage:
1. **Heuristic evaluation** to identify broad usability issues across the interface
2. **Cognitive walkthrough** to deeply analyze critical task flows for learnability

---

## Pluralistic Walkthrough Variant

### What It Is

A group-based walkthrough where users, developers, and usability experts review the interface together, step by step.

### Process

1. Assemble a group of 4-8 participants including:
   - 2-3 representative end users
   - 1-2 developers or designers
   - 1-2 usability specialists
   - 1 facilitator
2. Present each screen in the task sequence one at a time
3. Everyone writes down what they would do at each step (before discussion)
4. Go around the room and share answers
5. Discuss discrepancies and identify problems
6. Move to the next step

### Advantages Over Standard Cognitive Walkthrough

- Incorporates actual user perspectives alongside expert analysis
- Generates richer discussion and diverse viewpoints
- Developers hear usability concerns directly from users
- Builds team alignment around usability priorities

### Disadvantages

- Scheduling is difficult with diverse participants
- Group dynamics may suppress some opinions
- More time-consuming than individual walkthroughs
- Users may defer to experts in the room

---

## Reporting Findings

### Report Structure

```markdown
# Cognitive Walkthrough Report

## Study Information
- **Date:** [YYYY-MM-DD]
- **Evaluator(s):** [Names]
- **Interface version:** [Version/date]
- **User profile:** [Brief description]
- **Task evaluated:** [Task description]

## Action Sequence
[Numbered list of all steps]

## Summary of Findings
- **Total steps evaluated:** [N]
- **Steps with no issues:** [N]
- **Steps with minor issues:** [N]
- **Steps with major issues:** [N]
- **Steps with critical issues:** [N]

## Critical Path Issues
[Top 3-5 issues that would most likely cause task failure for a new user]

## Detailed Step-by-Step Analysis
[Full analysis of each step with the four questions]

## Issue Log
[Table of all issues with severity ratings]

## Recommendations
[Prioritized list of design changes to address the findings]

## Appendix
- Screenshots of each screen state
- User profile details
- Task scenario description
```

---

## Example Walkthrough: Signup Flow

### Task: Create a new account and complete profile setup

**User Profile:** New visitor who clicked a "Start Free Trial" link from a blog post. Basic web literacy. No prior experience with this product.

### Step 1: Land on Signup Page

- **Q1:** YES. User clicked "Start Free Trial" and expects to create an account.
- **Q2:** YES. The signup form is centered and prominent with clear "Create Account" heading.
- **Q3:** YES. Email and password fields are standard and recognizable.
- **Q4:** N/A. This is the starting state.
- **Issues:** None.

### Step 2: Enter Email Address

- **Q1:** YES. Email field is the first field and clearly labeled.
- **Q2:** YES. Field is visible with placeholder text "Enter your email."
- **Q3:** YES. Standard email input pattern.
- **Q4:** YES. Field validates format in real-time with a green checkmark.
- **Issues:** None.

### Step 3: Enter Password

- **Q1:** YES. After email, password is the expected next field.
- **Q2:** YES. Password field is directly below email.
- **Q3:** PARTIAL. Requirements are listed below the field but in small gray text.
- **Q4:** YES. Real-time strength indicator updates as user types.
- **Issues:**
  - CW-3a: Password requirements are low-contrast and may be overlooked until the user submits an invalid password. Severity: Minor.

### Step 4: Click "Create Account"

- **Q1:** YES. The user wants to proceed after filling in credentials.
- **Q2:** YES. Large blue button below the form.
- **Q3:** YES. "Create Account" label is clear and unambiguous.
- **Q4:** PARTIAL. A loading spinner appears, but after account creation the user is redirected to a dashboard with no welcome message or orientation.
- **Issues:**
  - CW-4a: No confirmation that the account was created. User lands on an empty dashboard with no guidance. Severity: Major.
  - CW-4b: No onboarding prompt or next-step guidance. Severity: Major.

### Step 5: Complete Profile (Name, Company, Role)

- **Q1:** NO. The user is on the dashboard and has no clear indication that profile completion is needed or beneficial. The profile section is in Settings, three clicks away.
- **Q2:** NO. There is no prompt, banner, or indicator pointing to profile completion.
- **Q3:** N/A. User cannot find the action.
- **Q4:** N/A. User cannot perform the action.
- **Issues:**
  - CW-5a: Profile completion is completely undiscoverable for new users. No prompt, tooltip, or onboarding step guides the user. Severity: Critical.

### Summary

The signup flow works well through account creation (Steps 1-4 with minor issues) but fails critically at post-signup onboarding (Step 5). The transition from "account created" to "productive user" has no guidance, violating the learnability principle that the cognitive walkthrough is designed to assess.

**Priority recommendations:**
1. Add a post-signup onboarding flow that guides profile completion
2. Display a welcome message confirming account creation
3. Increase contrast on password requirements text
