[Back to Information Architecture](../information-architecture.md)

# Sitemap and Content Structure Patterns

## Overview

Sitemaps are structural blueprints that define how content is organized and connected within a digital product. Choosing the right structure pattern shapes how users navigate, how content scales, and how search engines index a site. This reference covers major structural patterns, content inventory methodology, URL conventions, and practical tools.

---

## Hierarchical Sitemaps

The most common pattern. Content is organized in a tree structure with a clear parent-child relationship.

### Structure

```
Home
├── Products
│   ├── Category A
│   │   ├── Product 1
│   │   └── Product 2
│   └── Category B
│       ├── Product 3
│       └── Product 4
├── About
│   ├── Team
│   ├── Careers
│   └── Press
├── Blog
│   ├── Post 1
│   └── Post 2
└── Contact
```

### When to Use

- Most websites and applications with clear content categories
- E-commerce product catalogs
- Corporate and marketing sites
- Documentation with logical topic groupings

### Design Principles

- Keep the hierarchy to 3-4 levels maximum
- Ensure every page is reachable within 3 clicks from the homepage
- Balance breadth (items per level) and depth (number of levels)
- Group content by user mental models, not internal organizational structure
- Each node should have a clear, non-overlapping relationship to its siblings

### Strengths and Limitations

**Strengths:** Intuitive, scalable, easy to navigate with breadcrumbs, SEO-friendly.

**Limitations:** Cross-category content requires cross-links or tagging; deep hierarchies increase navigation effort; rigid structure can be hard to restructure later.

---

## Flat Sitemaps

All or most content exists at the same level with minimal or no hierarchy.

### Structure

```
Home
├── Page A
├── Page B
├── Page C
├── Page D
├── Page E
├── Page F
└── Page G
```

### When to Use

- Small sites with fewer than 15-20 pages
- Single-page applications where content is divided into sections
- Portfolio sites
- Landing page microsites

### Design Principles

- Works best when all content is equally important
- Use clear and distinct page labels since there is no categorical grouping
- Consider alphabetical or priority-based ordering
- Combine with search for larger flat collections (e.g., a glossary)

### Strengths and Limitations

**Strengths:** Simple to understand and maintain; every page is one click from the homepage; no deep navigation.

**Limitations:** Does not scale beyond 15-20 items; no categorical context for users; can feel overwhelming if too many peer items exist.

---

## Hub-and-Spoke

A central hub page links out to individual spoke pages, which link back to the hub but not to each other.

### Structure

```
        ┌── Spoke A ──┐
        │              │
Hub ────┼── Spoke B ──┤
        │              │
        └── Spoke C ──┘

(Spokes return to Hub only)
```

### When to Use

- Mobile-first applications where each screen is a focused task
- Onboarding flows or wizards
- Dashboard-centric apps (hub = dashboard, spokes = detail views)
- Insurance or financial calculators (hub = selection, spokes = quote flows)

### Design Principles

- The hub acts as the control center and primary orientation point
- Each spoke is self-contained with a clear back-to-hub path
- Minimize cross-linking between spokes to maintain focus
- Hub should clearly communicate what each spoke contains

### Strengths and Limitations

**Strengths:** Focused user attention; simple mental model; works well for task-oriented flows.

**Limitations:** Cross-spoke navigation requires returning to the hub (extra clicks); not suited for content-heavy sites where users need to browse across categories.

---

## Sequential / Linear

Content is organized in a defined order, with users progressing from one page to the next.

### Structure

```
Step 1 → Step 2 → Step 3 → Step 4 → Confirmation
```

### When to Use

- Checkout and purchase flows
- Account setup and onboarding wizards
- Tutorial or learning sequences
- Application forms (tax filing, loan applications)

### Design Principles

- Show progress indicators (step numbers, progress bar)
- Allow backward navigation to review previous steps
- Save progress so users can resume later
- Minimize optional branches; keep the path linear
- Clearly indicate the total number of steps

### Variations

- **Branching linear:** The path splits based on user input and rejoins later
  ```
  Step 1 → Step 2 → [If A] → Step 3A → Step 4
                     [If B] → Step 3B ↗
  ```
- **Optional steps:** Some steps can be skipped without blocking progress

### Strengths and Limitations

**Strengths:** Clear progression; reduces cognitive load by presenting one task at a time; completion tracking is straightforward.

**Limitations:** Inflexible for non-linear exploration; frustrating if users cannot skip irrelevant steps; backtracking can be confusing if data dependencies exist.

---

## Matrix / Faceted

Content can be accessed through multiple organizational dimensions simultaneously.

### Structure

```
Content Item: "Running Shoes - Men's - Nike - Size 10"

Accessible via:
  Category path:  Shoes > Running > Men's
  Brand path:     Nike > Running Shoes
  Size path:      Size 10 > Running Shoes
  Activity path:  Running > Shoes > Men's
```

### When to Use

- E-commerce with multi-attribute products
- Job boards (filter by location, role, industry, experience)
- Real estate listings (location, price, bedrooms, type)
- Any domain where content has multiple meaningful classification axes

### Design Principles

- Identify the 3-5 most important facets based on user research
- Allow filtering by multiple facets simultaneously
- Preserve filter state in URLs for sharing and bookmarking
- Show result counts per facet value to guide user expectations
- Support both browse (faceted navigation) and search entry points

### Strengths and Limitations

**Strengths:** Extremely flexible; supports diverse user mental models; scalable for large content sets.

**Limitations:** Complex to implement and maintain; requires robust tagging/metadata; can overwhelm users if too many facets are presented.

---

## Content Inventory Template

A content inventory catalogs every piece of content on a site. It is the essential first step before creating or restructuring a sitemap.

### Spreadsheet Structure

```markdown
| ID | URL | Page Title | Content Type | Section | Owner | Last Updated | Status | Notes |
|----|-----|-----------|-------------|---------|-------|-------------|--------|-------|
| 001 | /home | Home | Landing page | Root | Marketing | 2025-11-01 | Active | |
| 002 | /about | About Us | About | Company | Marketing | 2025-08-15 | Active | Needs update |
| 003 | /products | Products | Category | Products | Product | 2025-12-01 | Active | |
| 004 | /blog/old-post | Old Post | Blog post | Blog | Content | 2023-01-10 | Review | Low traffic |
```

### Columns Explained

| Column | Purpose |
|--------|---------|
| **ID** | Unique identifier for each content item |
| **URL** | Current URL of the page |
| **Page Title** | The H1 or document title |
| **Content Type** | Category page, product page, blog post, landing page, etc. |
| **Section** | Top-level section it belongs to |
| **Owner** | Person or team responsible for the content |
| **Last Updated** | Date of last meaningful update |
| **Status** | Active, Needs Review, Deprecated, Redirect, Delete |
| **Notes** | Migration notes, issues, or context |

### Conducting the Inventory

1. **Crawl the site** using Screaming Frog, Sitebulb, or a similar tool to capture all URLs
2. **Export to spreadsheet** and add metadata columns
3. **Categorize each page** by content type and section
4. **Assess each page:** Is it current? Accurate? Useful? High-traffic?
5. **Tag for action:** Keep as-is, update, merge with another page, redirect, or delete
6. **Prioritize:** Focus on high-traffic and high-value pages first

---

## Page Naming Conventions

### Labels for Navigation and Sitemaps

- Use plain language that matches user vocabulary (validate via card sorting)
- Keep labels to 1-3 words when possible
- Use nouns or noun phrases, not verbs ("Products" not "Browse Products")
- Avoid internal jargon ("Knowledge Base" not "KMS Portal")
- Be specific ("Pricing" not "Info", "Contact Us" not "Reach Out")
- Ensure sibling labels are mutually exclusive and collectively exhaustive

### Title Tag Conventions

```
[Page Title] | [Section] | [Site Name]

Examples:
"Canon EOS R5 | Cameras | PhotoStore"
"Pricing Plans | Acme Software"
"How to Reset Your Password | Help Center | Acme"
```

### Heading Hierarchy

Every page should have a clear heading structure that reflects its position in the sitemap:

```html
<h1>Cameras</h1>                    <!-- Page title (one per page) -->
  <h2>DSLR Cameras</h2>            <!-- Section -->
    <h3>Canon EOS R5</h3>          <!-- Subsection -->
    <h3>Nikon Z9</h3>
  <h2>Mirrorless Cameras</h2>
    <h3>Sony A7 IV</h3>
```

---

## URL Structure Best Practices

### Principles

1. **Readable:** URLs should be human-readable and descriptive
2. **Consistent:** Follow the same pattern across the entire site
3. **Hierarchical:** URL path should reflect the sitemap hierarchy
4. **Stable:** URLs should not change; use redirects when they must

### Patterns

```
Good:
/products/cameras/canon-eos-r5
/blog/2025/11/how-to-choose-a-camera
/help/account/reset-password

Bad:
/p?id=4523
/products/cat3/subcat7/item
/page.php?section=blog&post=123
```

### URL Rules

| Rule | Example |
|------|---------|
| Use lowercase | `/products/cameras` not `/Products/Cameras` |
| Use hyphens, not underscores | `/reset-password` not `/reset_password` |
| No trailing slashes (or be consistent) | `/about` or `/about/` but not both |
| No file extensions | `/contact` not `/contact.html` |
| Keep it short | `/pricing` not `/our-pricing-and-plans-page` |
| No special characters | `/cafe-menu` not `/café-menu` |
| Reflect hierarchy | `/products/cameras/dslr` not `/dslr-cameras` |

### Redirect Strategy

When restructuring a sitemap, create a redirect map:

```markdown
| Old URL | New URL | Redirect Type | Reason |
|---------|---------|--------------|--------|
| /old-products | /products | 301 (permanent) | URL restructure |
| /temp-promo | /seasonal-sale | 302 (temporary) | Campaign redirect |
| /blog/draft-post | (none) | 410 (gone) | Content removed |
```

---

## XML Sitemap for SEO

An XML sitemap tells search engines which pages exist and how frequently they change. It is a separate artifact from the visual/structural sitemap.

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/</loc>
    <lastmod>2025-12-01</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://www.example.com/products</loc>
    <lastmod>2025-11-28</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://www.example.com/about</loc>
    <lastmod>2025-06-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
```

### Best Practices

- Submit the sitemap via Google Search Console and Bing Webmaster Tools
- Keep each sitemap file under 50,000 URLs or 50MB
- Use a sitemap index file for larger sites with multiple sitemaps
- Include only canonical URLs (no duplicates, no paginated variants)
- Update `lastmod` only when page content meaningfully changes
- Reference the sitemap in `robots.txt`: `Sitemap: https://www.example.com/sitemap.xml`
- Exclude pages with `noindex` meta tags from the XML sitemap

---

## Visual Sitemap Tools and Notation

### Tools

| Tool | Type | Best For |
|------|------|----------|
| **Figma / FigJam** | Design | Collaborative, visual sitemaps with custom notation |
| **Miro** | Whiteboard | Workshop-style sitemap creation with sticky notes |
| **Slickplan** | Dedicated | Professional sitemap creation with export options |
| **OmniGraffle** | Diagramming | Detailed, high-fidelity sitemap diagrams |
| **Lucidchart** | Diagramming | Team collaboration with templates |
| **draw.io (diagrams.net)** | Free | No-cost option with decent templates |
| **Screaming Frog** | Crawler | Automatically generate sitemaps from existing sites |

### Visual Notation Conventions

```
┌──────────────┐
│   Home Page   │   Rectangle = standard page
└──────────────┘

┌ ─ ─ ─ ─ ─ ─ ┐
│  Coming Soon  │   Dashed border = planned/future page
└ ─ ─ ─ ─ ─ ─ ┘

╔══════════════╗
║  Login Page   ║   Double border = requires authentication
╚══════════════╝

┌──────────────┐
│  External ↗   │   Arrow icon = external link
└──────────────┘

     ×3              Multiplier = repeated pattern
┌──────────────┐     (e.g., "Product Detail Page" ×200)
│ Product Page  │
└──────────────┘
```

### Color Coding

| Color | Meaning |
|-------|---------|
| Blue | Navigation/structural pages |
| Green | Content pages (blog, articles) |
| Orange | Transactional pages (checkout, forms) |
| Gray | Utility pages (404, terms, privacy) |
| Red | Pages flagged for deletion or redesign |

### Sitemap Presentation Tips

- Start with a high-level overview (Level 1-2 only) for stakeholder alignment
- Provide a detailed version (all levels) for the implementation team
- Include page count totals per section
- Note any content that will be newly created vs migrated
- Call out pages that require special functionality (search, dynamic filtering, user-generated content)
- Version the sitemap document and track changes over time
