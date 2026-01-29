# Technical Writing Skills

## General Tone

- **Conversational, respectful, not cute:** approachable and human, but avoids slang, jokes, and pop culture.
- **Warm, helpful, and solution-first:** shows empathy, takes responsibility when things fail, and points to a fix without blaming the user.
- **Crisp and scannable:** concise, direct, and precise so readers can search and skim fast.
- **Active, present, and reader-addressed:** uses present tense, active voice, simple phrasing, and speaks to “you” (not “we”).
- **Global-English friendly:** avoids idioms, jargon, Latin abbreviations, and culture-specific references to keep meaning stable and translatable.


## Core Principles

### 1. User-Centric Approach

- Write for the user's goals, not the code's structure
- Answer "How do I...?" before "How does it work?"
- Progressive disclosure: simple first, details later
- Assume intelligence, not knowledge

### 2. Clarity Over Completeness

- Every word should help the user
- Cut unnecessary technical details
- Use simple words for complex ideas
- One concept per paragraph

### 3. Practical Focus

- Start with working examples
- Show common use cases first
- Include "copy-paste-ready" code
- Explain what to expect

## Writing Style Guide

### Language

- **Active voice**: "Configure the server" not "The server is configured"
- **Present tense**: "The function returns" not "The function will return"
- **Second person**: "You can configure" not "One can configure"
- **Imperative mood**: "Run the command" not "You should run the command"

### Sentence Structure

- Short sentences (15-20 words average)
- One idea per sentence
- Vary sentence length for rhythm
- Use lists for multiple items

### Technical Terms

- Define on first use
- Use consistently throughout
- Provide glossary for complex projects
- Link to detailed explanations

## Document Structure

### Standard Sections

1. **Overview** - What and why in 2-3 sentences
2. **Prerequisites** - What users need first
3. **Quick Start** - Minimal working example
4. **Core Concepts** - Essential understanding
5. **Common Tasks** - 80% use cases
6. **Advanced Usage** - Power user features
7. **Troubleshooting** - Common problems
8. **Reference** - Complete details

### Information Hierarchy

```
# Page Title (H1)
Brief introduction paragraph

## Major Section (H2)
Section introduction

### Subsection (H3)
Specific topic

#### Detail Level (H4)
Rarely needed
```

## Code Examples

### Effective Examples

```java
// DO: Show context and purpose
// Configure database connection with retry logic
DatabaseConfig config = new DatabaseConfig()
    .withUrl("jdbc:postgresql://localhost/myapp")
    .withMaxRetries(3)
    .withTimeout(30);
```

### Poor Examples

```java
// DON'T: Code without context
DatabaseConfig config = new DatabaseConfig();
config.setUrl(url);
config.setRetries(3);
```

## Common Patterns

### Task-Based Organization

```markdown
## How to Connect to a Database

To connect to a database:

1. Add the dependency to your project
2. Configure the connection settings
3. Create a connection pool
4. Use the connection in your code

### Step 1: Add Dependency

...
```

### Feature Documentation

```markdown
## Authentication

Authentication protects your application by verifying user identity.

### When to Use

Use authentication when you need to:

- Restrict access to certain features
- Track user actions
- Personalize user experience

### Basic Setup

...
```

## Readthedocs Optimization

### Navigation

- Clear, descriptive page titles
- Logical grouping of topics
- Consistent naming patterns
- Breadcrumb-friendly structure

### Cross-References

```markdown
See [Configuration Guide](../configuration/index.md) for detailed options.

Related topics:

- [Authentication](../features/authentication.md)
- [Error Handling](../guides/error-handling.md)
```

### Search Optimization

- Use keywords naturally
- Include common synonyms
- Write descriptive headings
- Add meta descriptions

## Quality Checklist

### Before Writing

- [ ] Understand the user's goal
- [ ] Review code implementation
- [ ] Plan document structure
- [ ] Gather examples

### While Writing

- [ ] Focus on user tasks
- [ ] Use consistent terminology
- [ ] Include practical examples
- [ ] Add helpful diagrams

### After Writing

- [ ] Test all code examples
- [ ] Check links work
- [ ] Verify technical accuracy
- [ ] Read aloud for clarity

## Common Pitfalls to Avoid

### Technical Writing Sins

1. **The Code Mirror** - Documentation that just describes code structure
2. **The Mystery Novel** - Burying important information deep in text
3. **The Encyclopedia** - Trying to document everything
4. **The Time Machine** - Outdated examples and information
5. **The Puzzle** - Making users piece together information

### Better Approaches

1. **The Guide** - Focus on user journeys
2. **The Cookbook** - Provide recipes for common tasks
3. **The Map** - Show how pieces fit together
4. **The Tutor** - Teach concepts progressively
5. **The Assistant** - Anticipate user questions
