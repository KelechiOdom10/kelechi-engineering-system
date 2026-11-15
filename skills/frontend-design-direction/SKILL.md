---
name: frontend-design-direction
description: Set a deliberate visual direction and hierarchy for a new or redesigned UI. Use for greenfield pages or major redesigns, not when a design system already decides.
---

# Frontend design direction

1. State the user's job, the primary action, the audience, and the existing brand or product
   constraints. Read the current design system before choosing a visual direction.
2. Load `ui-skills` for overall direction, within the repository's stack and brand constraints. Choose one direction that supports the task: information-dense, editorial, calm, playful,
   technical, or another concrete description. Explain the choice in terms of the user and product,
   not current fashion.
3. Establish hierarchy before decoration. Decide the primary content, action, reading order, spacing
   rhythm, type scale, colour roles, and responsive layout. Apply `better-colors` when setting
   tokens and `better-typography` when setting the type scale. For a new design system, define
   each control size's height, padding, font size and icon size; render buttons, inputs and
   selects side by side per size in both themes to verify that scale and icon clearance.
4. Use the system's existing tokens, components, and assets where they fit. Create a new pattern only
   when the current system cannot express the required task or interaction.
5. Design interaction states with the visual system: loading, empty, error, focus, hover, disabled,
   success, keyboard operation, and reduced motion.
6. Check the rendered interface at the target breakpoints. Compare it with the stated direction and
   user task, then use `frontend-quality` for implementation and accessibility proof.

Use the [frontend design brief](../../templates/frontend-design-brief.md) when the direction needs
agreement before implementation.
