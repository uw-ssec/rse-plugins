[Back to Design System Creation](../index.md)

# Atomic Design Methodology

A structured approach to building design systems from fundamental building blocks to complete pages.

---

## The Five Levels

Atomic Design organizes UI components into five hierarchical levels:

```
Atoms -> Molecules -> Organisms -> Templates -> Pages
```

Each level builds on the previous, creating a clear progression from simple to complex.

---

## Atoms

The smallest, indivisible UI elements. Atoms cannot be broken down further without losing their meaning.

**Examples:** buttons, inputs, labels, icons, badges, avatars, dividers, checkboxes.

```tsx
// atoms/Button.tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

function Button({ variant = 'primary', size = 'md', children, ...props }: ButtonProps) {
  return (
    <button className={cn(buttonVariants({ variant, size }))} {...props}>
      {children}
    </button>
  );
}

// atoms/Label.tsx
interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  required?: boolean;
}

function Label({ children, required, ...props }: LabelProps) {
  return (
    <label className="text-sm font-medium text-gray-700" {...props}>
      {children}
      {required && <span className="text-red-500 ml-0.5" aria-hidden="true">*</span>}
    </label>
  );
}

// atoms/Input.tsx
const Input = forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => (
    <input
      ref={ref}
      className={cn(
        'h-10 w-full rounded-md border border-gray-300 px-3 text-sm',
        'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
        'disabled:cursor-not-allowed disabled:opacity-50',
        className
      )}
      {...props}
    />
  )
);
```

---

## Molecules

Groups of atoms that work together as a functional unit.

**Examples:** search form (label + input + button), card header (avatar + name + timestamp), form field (label + input + error message).

```tsx
// molecules/FormField.tsx
interface FormFieldProps {
  label: string;
  name: string;
  error?: string;
  required?: boolean;
  children: React.ReactNode;
}

function FormField({ label, name, error, required, children }: FormFieldProps) {
  return (
    <div className="space-y-1.5">
      <Label htmlFor={name} required={required}>
        {label}
      </Label>
      {children}
      {error && (
        <p className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

// molecules/SearchBar.tsx
function SearchBar({ onSearch }: { onSearch: (query: string) => void }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2" role="search">
      <Input
        type="search"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        aria-label="Search"
      />
      <Button type="submit" variant="primary" size="md">
        Search
      </Button>
    </form>
  );
}

// molecules/UserInfo.tsx
function UserInfo({ user }: { user: { name: string; avatar: string; role: string } }) {
  return (
    <div className="flex items-center gap-3">
      <Avatar src={user.avatar} alt={user.name} size="md" />
      <div>
        <p className="text-sm font-medium text-gray-900">{user.name}</p>
        <p className="text-xs text-gray-500">{user.role}</p>
      </div>
    </div>
  );
}
```

---

## Organisms

Complex UI sections composed of molecules and atoms. Organisms form distinct sections of an interface.

**Examples:** navigation bar, hero section, footer, comment thread, product grid, sidebar.

```tsx
// organisms/SiteHeader.tsx
function SiteHeader() {
  return (
    <header className="border-b bg-white">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <Logo />
        <Navigation
          items={[
            { label: 'Products', href: '/products' },
            { label: 'Pricing', href: '/pricing' },
            { label: 'Docs', href: '/docs' },
          ]}
        />
        <div className="flex items-center gap-4">
          <SearchBar onSearch={handleSearch} />
          <UserMenu user={currentUser} />
        </div>
      </div>
    </header>
  );
}

// organisms/HeroSection.tsx
interface HeroSectionProps {
  title: string;
  subtitle: string;
  ctaLabel: string;
  ctaHref: string;
  image?: string;
}

function HeroSection({ title, subtitle, ctaLabel, ctaHref, image }: HeroSectionProps) {
  return (
    <section className="py-16 lg:py-24">
      <div className="mx-auto grid max-w-7xl items-center gap-12 px-4 lg:grid-cols-2">
        <div>
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 lg:text-5xl">
            {title}
          </h1>
          <p className="mt-4 text-lg text-gray-600">{subtitle}</p>
          <div className="mt-8">
            <Button as="a" href={ctaHref} size="lg">{ctaLabel}</Button>
          </div>
        </div>
        {image && <img src={image} alt="" className="rounded-xl shadow-lg" />}
      </div>
    </section>
  );
}
```

---

## Templates

Page-level layout structures that define where organisms are placed. Templates use placeholder content to show the structural skeleton.

```tsx
// templates/MarketingPageTemplate.tsx
interface MarketingPageTemplateProps {
  header: React.ReactNode;
  hero: React.ReactNode;
  features: React.ReactNode;
  testimonials?: React.ReactNode;
  cta: React.ReactNode;
  footer: React.ReactNode;
}

function MarketingPageTemplate({
  header, hero, features, testimonials, cta, footer,
}: MarketingPageTemplateProps) {
  return (
    <div className="min-h-screen flex flex-col">
      {header}
      <main className="flex-1">
        {hero}
        {features}
        {testimonials}
        {cta}
      </main>
      {footer}
    </div>
  );
}

// templates/DashboardTemplate.tsx
interface DashboardTemplateProps {
  sidebar: React.ReactNode;
  topBar: React.ReactNode;
  children: React.ReactNode;
}

function DashboardTemplate({ sidebar, topBar, children }: DashboardTemplateProps) {
  return (
    <div className="flex h-screen">
      <aside className="w-64 border-r bg-gray-50 overflow-y-auto">{sidebar}</aside>
      <div className="flex flex-1 flex-col">
        <div className="border-b bg-white px-6 py-3">{topBar}</div>
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
```

---

## Pages

Specific instances of templates filled with real content and connected to data sources.

```tsx
// pages/HomePage.tsx
function HomePage() {
  return (
    <MarketingPageTemplate
      header={<SiteHeader />}
      hero={
        <HeroSection
          title="Ship faster with our component library"
          subtitle="Production-ready components for modern web applications."
          ctaLabel="Get Started"
          ctaHref="/docs"
          image="/hero-image.webp"
        />
      }
      features={<FeaturesGrid features={FEATURES_DATA} />}
      testimonials={<TestimonialCarousel items={TESTIMONIALS_DATA} />}
      cta={<CTABanner />}
      footer={<SiteFooter />}
    />
  );
}
```

---

## Creation Workflow

### Step 1: Inventory

Audit existing designs and list every unique UI element. Group them by level.

### Step 2: Build Bottom-Up

1. Create atoms with complete variant support and accessibility.
2. Compose atoms into molecules. Validate that molecules work in isolation.
3. Assemble molecules into organisms. Test with realistic data.
4. Define templates that establish page structures.
5. Populate templates with real content to create pages.

### Step 3: Document

Every component at every level needs documentation.

---

## Component Documentation Template

```markdown
# ComponentName

Brief description of what the component does and when to use it.

## Level
Atom | Molecule | Organism

## Usage

\`\`\`tsx
<ComponentName variant="primary" size="md">
  Label
</ComponentName>
\`\`\`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | 'primary' \| 'secondary' | 'primary' | Visual style |
| size | 'sm' \| 'md' \| 'lg' | 'md' | Size of the component |

## Accessibility
- Role: button
- Keyboard: Enter/Space to activate
- ARIA: aria-disabled when disabled

## Do / Don't
- Do: Use primary for the main action on a page
- Don't: Use more than one primary button in a section
```

---

## Storybook Integration

Organize stories to mirror the atomic hierarchy.

```
stories/
  atoms/
    Button.stories.tsx
    Input.stories.tsx
    Badge.stories.tsx
  molecules/
    FormField.stories.tsx
    SearchBar.stories.tsx
  organisms/
    SiteHeader.stories.tsx
    HeroSection.stories.tsx
  templates/
    MarketingPageTemplate.stories.tsx
  pages/
    HomePage.stories.tsx
```

```tsx
// atoms/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from '@/components/atoms/Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  tags: ['autodocs'],
  parameters: {
    docs: {
      description: {
        component: 'Primary interactive element for triggering actions.',
      },
    },
  },
};
export default meta;
type Story = StoryObj<typeof Button>;

export const Default: Story = { args: { children: 'Button' } };
export const AllVariants: Story = {
  render: () => (
    <div className="flex gap-3">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  ),
};
```

---

## Naming Conventions

| Level | Directory | File Pattern | Example |
|-------|-----------|-------------|---------|
| Atom | `components/atoms/` | PascalCase | `Button.tsx` |
| Molecule | `components/molecules/` | PascalCase | `SearchBar.tsx` |
| Organism | `components/organisms/` | PascalCase | `SiteHeader.tsx` |
| Template | `components/templates/` | PascalCase + Template | `DashboardTemplate.tsx` |
| Page | `pages/` or `app/` | PascalCase + Page | `HomePage.tsx` |

### Alternative Flat Structure

Some teams prefer a flat structure with metadata over nested directories:

```
components/
  Button/
    Button.tsx
    Button.stories.tsx
    Button.test.tsx
    Button.module.css
    index.ts
```

Tag the level in Storybook titles (`Atoms/Button`) rather than enforcing it through the file system. This scales better when components are hard to categorize.
