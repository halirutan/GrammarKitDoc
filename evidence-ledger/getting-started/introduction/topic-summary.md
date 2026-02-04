# Topic Summary: Introduction to GrammarKit

## Documentation Outline Reference
Section 1.1: Introduction to GrammarKit
Source: info/documentation-outline.md

## Learning Objectives
Based on outline and evidence:
- Understand what GrammarKit is and the problems it solves
- Learn how GrammarKit fits into IntelliJ plugin development ecosystem
- Recognize when GrammarKit is the right tool for your project
- Master the basic concept of grammar-based parser generation

## Prerequisites
- IntelliJ IDEA basics (using the IDE, installing plugins)
- Java development knowledge (reading Java code, basic OOP concepts)
- Understanding of parsing concepts is helpful but not required

## Content Structure
Following documentation outline:

### 1. **What is GrammarKit?** - Opening with the Problem
   - Start with the problem: "How do you teach IntelliJ IDEA to understand a new language?"
   - Introduce GrammarKit as the solution: A tool that turns grammar descriptions into working parsers
   - Use analogy: Like a recipe (grammar) that produces a meal (parser)
   - Evidence: code-evidence.md lines 8-13, examples.md lines 6-18

### 2. **Overview of BNF grammar support and parser generation** - Core Capability
   - Explain BNF as "a way to describe language rules" (avoid technical jargon initially)
   - Show simplest possible example: `greeting ::= 'hello' 'world'`
   - Explain that GrammarKit turns this into Java code that recognizes the pattern
   - Evidence: examples.md lines 6-18, code-evidence.md lines 8-13

### 3. **Key features and capabilities** - What You Get
   - Live Preview: "See your grammar work in real-time"
   - Structure view: "Visualize how your grammar organizes code"
   - Automatic generation: "One click creates all the Java code you need"
   - Built-in helpers: Navigation, refactoring, error detection
   - Evidence: code-evidence.md lines 14-23

### 4. **Relationship to IntelliJ Platform language support** - The Bigger Picture
   - GrammarKit generates the foundation for language plugins
   - Creates PSI (Program Structure Interface) - "the way IntelliJ understands code structure"
   - Integrates seamlessly with IntelliJ's language support framework
   - Evidence: code-evidence.md lines 24-30, examples.md lines 35-48

### 5. **When to use GrammarKit** - Use Cases
   - Custom language plugin development: "Building support for a new programming language"
   - DSL support: "Adding a mini-language to your application"
   - File format parsers: "Teaching IntelliJ to understand your config files"
   - Evidence: code-evidence.md lines 32-49, examples.md lines 49-86

### 6. **Prerequisites** - What You Need to Know
   - Frame as "helpful background" not "requirements"
   - IntelliJ IDEA basics: Just need to know how to use the IDE
   - Java knowledge: You'll read generated Java code
   - Parsing concepts: Will be explained as we go
   - Evidence: code-evidence.md lines 51-66, references.md lines 63-68

## Evidence Mapping
- Outline: "Overview of BNF grammar support" → Supported by examples.md lines 6-18
- Outline: "Key features and capabilities" → Supported by code-evidence.md lines 14-23
- Outline: "Relationship to IntelliJ Platform" → Supported by code-evidence.md lines 24-30
- Outline: "Custom language plugin development" → Supported by examples.md lines 49-62
- Outline: "DSL support" → Supported by examples.md lines 63-73
- Outline: "File format parsers" → Supported by examples.md lines 74-86
- Outline: "Prerequisites" → Supported by code-evidence.md lines 51-66

## Key Takeaways
- GrammarKit transforms grammar descriptions into working parsers
- It's the standard tool for creating IntelliJ language plugins
- You don't need to be a parsing expert to start using it
- The tool handles the complex parts, you focus on your language design

## Documentation Notes
- **Tone**: Welcoming and encouraging, avoid intimidating technical terms
- **Examples**: Use the simplest possible examples (greeting, calculator)
- **Analogies**: Use cooking recipes, building blocks, or other familiar concepts
- **Progressive disclosure**: Mention advanced features exist but don't explain them
- **Visual elements**: Include screenshot of Live Preview to make it tangible
- **Common concerns**: Address "Do I need to know compiler theory?" (No!)
- **Next steps**: Clear path to installation and quick start tutorial

## Writing Guidance for Documentation Author

### Opening Hook
Start with a relatable problem: "Have you ever wanted IntelliJ IDEA to understand your custom file format or programming language? Maybe you have configuration files with a specific syntax, or you're creating a domain-specific language for your application. GrammarKit is the tool that makes this possible."

### Simplification Strategy
1. Replace "BNF" with "grammar rules" on first mention
2. Replace "PSI" with "code structure" initially
3. Replace "parser" with "code that understands your language"
4. Introduce technical terms gently with explanations

### Example Progression
1. Start with: `greeting ::= 'hello' 'world'` (everyone understands this)
2. Then show: `assignment ::= ID '=' NUMBER` (still simple but useful)
3. Avoid complex examples with recursion or advanced features

### Addressing Concerns
Include a box/callout: "You don't need a computer science degree! If you can describe your language's rules in plain English, you can write a grammar for it."

### Visual Support
- Screenshot of Live Preview showing a simple grammar
- Diagram showing: Grammar → GrammarKit → Parser → IDE Features
- Before/after: Grammar rule vs. IDE understanding the code