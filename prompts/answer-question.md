The user will provide a section/paragraph/topic from the Grammar-Kit documentation that they don't understand.
Your task is to help them understand and create a custom explanation written for someone with no prior experience in 
parser development or IntelliJ plugin development.

If the user provides a markdown output file, then write your answer to that file.

# Your answer should contain:

1. A plain-language explanation of what the concept means and why it matters
2. Try to build upon the existing documentation so that the user later understands the original documentation better
3. A simple analogy or comparison to something familiar, if it helps
4. A minimal, step-by-step example that demonstrates the concept in isolation
5. What happens if you get it wrong (common mistakes)
6. A link back to the original documentation section for further reading


# Rules:

- Do NOT modify any existing files under docs/ or evidence-ledger/
- Instruct subagents to NOT modify any existing files under docs/ or evidence-ledger/
- The ONLY file you create is the output Markdown file above
- Use the @code-analyst agent to gather additional evidence from the Grammar-Kit source at /Grammar-Kit/ if the existing evidence doesn't fully explain the concept
- Use the @example-generator agent to create simple, beginner-friendly examples if the existing examples are too advanced
- Read the relevant evidence-ledger files and docs/ pages for context, but do not change them
- YOU MUST follow the style guide at .opencode/skills/human-style.md

