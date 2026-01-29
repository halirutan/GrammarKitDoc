You are tasked with creating comprehensive documentation for the Grammar-Kit project. The documentation outline is defined in @info/documentation-outline.md, and you should follow the established workflow pattern.

## Task Selection Process
1. **Read @info/documentation-outline.md** to see the documentation structure with checkbox indicators:
   - [x] = Completed sections (no TODO items)
   - [ ] = Incomplete sections (contains TODO items)

2. **Select the next uncompleted section** following this priority order:
   1. Core Concepts (foundational knowledge)
   2. Getting Started (user onboarding)
   3. Parser Development (practical usage)
   4. Code Generation (technical details)
   5. IDE Integration (advanced features)
   6. Build Integration (automation)
   7. Advanced Topics (expert usage)
   8. Troubleshooting (problem solving)
   9. Reference (comprehensive listings)
   10. Appendices (supplementary material)

3. **Identify the corresponding .md file** in @docs/ directory that matches the selected section

## Documentation Creation Workflow
For the selected documentation page:

1. **Analyze Requirements**
    - Read the section in @info/documentation-outline.md to understand:
        - Main topics to cover (bullet points)
        - Examples needed
        - Visual aids required
        - Target audience and use cases

2. **Research Content**
    - Use the explore agent to search @Grammar-Kit/ source code for:
        - Implementation details
        - Code examples
        - Feature behavior
        - Keyboard shortcuts and UI interactions
    - Check @info/ folder for:
        - user-task-map.md for user workflows
        - file-meta.md for relevant files
        - Any extracted information about the topic

3. **Create Documentation Plan**
    - List all topics to cover based on the outline
    - Identify what information needs to be gathered
    - Plan the structure and flow

4. **Draft Content**
    - Use the drafter agent to write the initial content
    - Include all required topics from the outline
    - Add practical examples users can copy
    - Include cross-references to related sections

5. **Edit and Polish**
    - Use the copyeditor agent with @.opencode/skills/human-style.md
    - Key style requirements:
        - Avoid single-sentence paragraphs
        - Group related concepts into cohesive paragraphs
        - No motivational language or pep talks
        - Direct, task-oriented writing
        - Limit to 2-4 H2 sections per page
        - Use H3 sparingly

6. **Verify Technical Accuracy**
    - For any claims about behavior, verify against source code
    - Test code examples for correctness
    - Ensure keyboard shortcuts are accurate

## Quality Standards
- First paragraph must state what the page enables
- Include complete, runnable code examples
- Focus on tasks users want to accomplish
- Provide verification steps for instructions
- Link to the most logical next action
- Maintain consistency with existing pages

## Important Guidelines
- Follow the same thorough process used for completed pages
- Research extensively before writing
- Verify all technical claims
- Apply the human-style.md guidelines consistently
- Create documentation that helps users succeed

Begin by reading @info/documentation-outline.md to identify the next uncompleted section (marked with [ ]), then proceed with documenting that section.