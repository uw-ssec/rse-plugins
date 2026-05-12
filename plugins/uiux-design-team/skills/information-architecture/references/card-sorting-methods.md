[Back to Information Architecture](../information-architecture.md)

# Card Sorting Methodology

## Overview

Card sorting is a user research method that reveals how people naturally group, categorize, and label information. It is foundational to information architecture, directly informing navigation structures, content organization, and taxonomy design. This reference covers all major card sorting variants, analysis techniques, and practical execution guidance.

---

## Open Card Sorting

### Definition

Participants are given a set of cards (each representing a piece of content or functionality) and asked to organize them into groups that make sense to them. They also create and name the groups themselves.

### When to Use

- Early in the design process when no existing structure exists
- When redesigning an information architecture from scratch
- When you want to discover users' mental models without bias from existing labels
- When exploring a new content domain

### Process

1. Prepare 30-60 cards representing content items, features, or topics
2. Present cards in randomized order to each participant
3. Ask participants to sort cards into groups that feel natural
4. Ask participants to name each group
5. Allow participants to create as many or as few groups as desired
6. Optionally allow "unsure" pile for ambiguous items

### Strengths and Limitations

**Strengths:**
- Reveals natural mental models without researcher bias
- Discovers unexpected grouping patterns
- Generates category labels in users' own language

**Limitations:**
- Results can be highly variable across participants
- Harder to analyze than closed sorting
- Does not validate an existing structure

---

## Closed Card Sorting

### Definition

Participants are given predefined category labels and asked to sort cards into these existing categories.

### When to Use

- Validating a proposed navigation structure
- Testing whether users can find content within an existing taxonomy
- Comparing two or more alternative category structures
- After open card sorting to validate the discovered structure

### Process

1. Define 4-8 category labels based on the proposed structure
2. Prepare cards representing content items
3. Present categories and cards to participants
4. Ask participants to place each card in the most appropriate category
5. Optionally include a "None of these" category to identify misfit items
6. Record placement and confidence for each card

### Strengths and Limitations

**Strengths:**
- Directly validates a proposed structure
- Easier to analyze with clear quantitative metrics
- Less cognitive load for participants

**Limitations:**
- Does not reveal alternative organizational models
- Category labels may bias sorting behavior
- Cannot identify missing categories

---

## Hybrid Card Sorting

### Definition

A combination of open and closed methods. Participants sort cards into predefined categories but can also create new categories and rename existing ones.

### When to Use

- When you have a partial structure that needs refinement
- When you want to validate top-level categories while discovering subcategories
- As a middle-ground approach that balances structure with discovery

### Process

1. Provide predefined category labels as a starting point
2. Present content cards to participants
3. Allow sorting into existing categories, creating new ones, or renaming categories
4. Track which categories were used as-is, modified, or newly created
5. Analyze both the quantitative placement data and qualitative modifications

---

## Tools and Facilitation

### Online Tools

| Tool | Type | Key Features |
|------|------|-------------|
| OptimalSort | Dedicated | Open, closed, hybrid; built-in analysis |
| UserZoom | Suite | Card sorting + tree testing in one platform |
| UXtweak | Dedicated | Affordable; dendrogram analysis |
| Maze | Suite | Card sorting with other research methods |
| Miro/FigJam | General | Good for moderated sessions; flexible |

### In-Person Facilitation

**Materials needed:**
- Index cards or sticky notes (one item per card)
- Large table or wall space
- Camera or phone to photograph final sorts
- Recording device for think-aloud sessions
- Spreadsheet to log results

**Facilitation tips:**
- Use a consistent card size and format
- Randomize card order for each participant
- Avoid leading language ("Where would you put this?", not "Does this go in Settings?")
- Encourage think-aloud to understand reasoning
- Do not correct or guide participants during sorting
- Take photos of each completed sort before clearing

### Moderated vs Unmoderated

| Aspect | Moderated | Unmoderated |
|--------|-----------|-------------|
| **Depth of insight** | High (think-aloud, follow-up questions) | Low (quantitative only) |
| **Scale** | 8-15 participants | 30-50+ participants |
| **Time per session** | 30-60 minutes | 10-20 minutes |
| **Cost** | Higher (researcher time) | Lower (platform fee only) |
| **Best for** | Exploratory research, complex domains | Validation, statistical confidence |

---

## Participant Recruitment

### Sample Size Recommendations

| Sort Type | Minimum | Recommended | Statistical Confidence |
|-----------|---------|-------------|----------------------|
| Open (moderated) | 8 | 15-20 | Diminishing returns after 20-30 |
| Open (unmoderated) | 20 | 30-50 | Higher N needed for cluster stability |
| Closed | 15 | 30-50 | Need statistical power for category validation |
| Hybrid | 15 | 20-30 | Balance of qualitative and quantitative |

### Recruitment Criteria

- Recruit representative users of the product or website
- Include a mix of expertise levels (novice to expert)
- Ensure demographic and behavioral diversity
- Exclude stakeholders and team members (they are biased by internal knowledge)
- Screen for familiarity with the content domain (not the specific product)

### Incentives

- Remote/unmoderated sessions: $10-25 gift card
- Moderated sessions (30 min): $50-75
- Moderated sessions (60 min): $75-150
- Scale incentives appropriately for B2B or specialized audiences

---

## Analysis Methods

### Similarity Matrix

A matrix showing how often each pair of cards was placed in the same group, expressed as a percentage across all participants.

```
             Card A   Card B   Card C   Card D
Card A        --       85%      20%      10%
Card B       85%       --       25%      15%
Card C       20%      25%       --       90%
Card D       10%      15%      90%       --
```

**Interpretation:**
- High similarity (70%+): Strong agreement these items belong together
- Medium similarity (40-69%): Some association; may belong in the same parent category
- Low similarity (< 40%): Generally seen as unrelated

**Usage:** Identify clear clusters and ambiguous items. Items with no high-similarity pairs may need to appear in multiple categories or require better labeling.

### Dendrogram (Hierarchical Cluster Analysis)

A tree diagram that shows how cards cluster together at various levels of similarity.

**How to read a dendrogram:**
- Cards that join at the bottom (high similarity) are strongly associated
- The height at which branches merge indicates the strength of the grouping
- Cut the tree at different heights to see different numbers of clusters
- A good cut point produces groups that are both cohesive internally and distinct from each other

**Practical steps:**
1. Build the similarity matrix from sort data
2. Apply hierarchical agglomerative clustering (average linkage is typical)
3. Visualize the dendrogram
4. Choose a cut-off threshold that produces a manageable number of groups (typically 4-8)
5. Validate the resulting groups against participant-created labels

### Standardization Grid

For open sorts, map participant-created group names to standardized categories.

```
Participant Labels          -> Standardized Category
"Account", "My Profile",   -> Account & Settings
"Settings", "Preferences"

"Help", "Support",         -> Help & Support
"FAQ", "Contact Us"
```

### Category Agreement Score

For closed sorts, calculate the percentage of participants who placed each card in the intended category.

```
Card: "Change password"
- Account Settings: 88% (intended)
- Security: 8%
- Help: 4%

Interpretation: Strong agreement. "Change password" fits well in Account Settings.
```

```
Card: "Billing history"
- Account Settings: 42%
- Payments: 38%
- Order History: 20%

Interpretation: Poor agreement. This item has split placement
and may need to appear in multiple navigation paths.
```

---

## Online vs In-Person

### Online Card Sorting

**Advantages:**
- Larger sample sizes at lower cost
- Geographic diversity of participants
- Automated data collection and analysis
- No scheduling constraints

**Disadvantages:**
- No think-aloud data unless screen-recorded
- Participants may rush through without careful thought
- Cannot ask follow-up questions in real-time
- Dropout rates of 20-40% are common

### In-Person Card Sorting

**Advantages:**
- Rich qualitative data from observation and conversation
- Can probe reasoning behind grouping decisions
- Lower dropout rate
- Physical manipulation may feel more natural for some participants

**Disadvantages:**
- Limited by geographic location and scheduling
- Smaller sample sizes
- Manual data entry required
- More expensive per participant

---

## Reporting Template

```markdown
# Card Sorting Study Report

## Study Details
- **Method:** [Open / Closed / Hybrid]
- **Moderation:** [Moderated / Unmoderated]
- **Tool:** [Platform name]
- **Date range:** [Start - End]
- **Number of cards:** [N]
- **Number of participants:** [N]
- **Completion rate:** [X%]

## Participant Demographics
[Summary of participant characteristics]

## Key Findings

### Strong Clusters (>70% agreement)
1. **[Category name]:** [List of cards in this cluster]
2. **[Category name]:** [List of cards]

### Moderate Clusters (40-70% agreement)
1. **[Category name]:** [List of cards, noting split placements]

### Ambiguous Items (<40% agreement)
1. **[Card name]:** Split between [Category A] (X%) and [Category B] (Y%)

### Category Labels (Open Sort Only)
[Most common participant-generated labels for each cluster]

## Dendrogram
[Include dendrogram visualization]

## Similarity Matrix Highlights
[Notable high and low similarity pairs]

## Recommendations
1. [Proposed category structure based on findings]
2. [Items that should appear in multiple navigation paths]
3. [Labels that should be user-tested further]
4. [Suggested follow-up: tree testing to validate]

## Appendix
- Full similarity matrix
- Raw data export
- Participant comments
```

---

## Tree Testing as Validation

After card sorting reveals a proposed structure, validate it with tree testing.

### What is Tree Testing?

Participants are given a text-only version of the proposed navigation hierarchy and asked to find where specific content lives. No visual design is applied -- only the structure is tested.

### Process

1. Build the proposed hierarchy based on card sorting results
2. Write 8-15 task scenarios ("Where would you find information about return policies?")
3. Recruit 50+ participants for statistical confidence
4. Measure: success rate, directness (found it without backtracking), and time to find

### Key Metrics

- **Success rate:** Percentage of participants who found the correct location
- **Directness:** Percentage who navigated directly without backtracking
- **First click accuracy:** Whether the first category selected was correct (strong predictor of overall success)

### Interpreting Results

| Success Rate | Directness | Interpretation |
|-------------|------------|----------------|
| >80% | >60% | Strong structure; item is well-placed |
| 60-80% | 40-60% | Acceptable but could improve with better labels |
| <60% | <40% | Problematic; restructure or provide multiple paths |

### Iteration Cycle

```
Open Card Sort -> Proposed Structure -> Tree Test -> Refine -> Re-test
```

Repeat until tree test success rates exceed 80% for all critical tasks.
