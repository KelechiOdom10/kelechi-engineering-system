---
name: create-canvas
description: Create or extend an isolated live workspace of named component or screen alternatives, preserving originals and real design-system behavior. Use for a design canvas, comparison workbench or meaningful visual variants; reuse an existing showcase when suitable.
---

# Create canvas

Make alternatives easy to inspect, name and revise. The skill creates a project-local workspace when invoked; it is not a preinstalled canvas application.

1. Read the project's instructions, design tokens, component public APIs and existing showcase or Storybook. Reuse the suitable host. For Humaans, load its frontend/browser adapter and inspect existing stories before adding a route. Establish the user's task, approved reference and distinct concept for each alternative; use `frontend-design-direction` when the direction is unsettled.
2. Start with one safe live preview and prove it mounts. Use synthetic fixtures, inert service callbacks and supported providers before mounting real components. An iframe alone does not prevent requests or writes. If safe isolation is unavailable, preserve a static reference and report the blocked live preview rather than mounting unsafe content.
3. Create a typed, discoverable source registry: stable ID, unique readable name, component, fixture, dimensions and, for freeform layouts, initial position. Keep production components independent of the workspace. Use public APIs; do not patch their exports, internals, portal roots or browser APIs to make an experiment work.
4. Preserve existing variants, IDs, names and positions unless the user asks to change them. Another version gets a new identity and independent state. Compare one concept with the same content, dimensions, theme and important states. Include the approved baseline; different colors alone are not different concepts. Additions must not reset the user's camera or erase drafts.
5. Use existing showcase navigation when it fits. When a freeform canvas is requested, follow [the workspace contract](references/workspace.md) for camera, separate move handles, copying, persistence and interaction isolation. Do not quietly replace requested pan/zoom behavior with a grid or build a controller when a comparison story already meets the request.
6. Run it in the permitted local environment and inspect the actual output at relevant widths and themes. Exercise inputs, keyboard focus, menus/portals and preserved state after moving or navigating. Use `ui-sweep` for a retained state catalog. Critique hierarchy, density, readability and primary action against the chosen reference; passing interaction checks do not establish design quality.
7. Hand over exact variant names, the running location, screenshots, chosen differences, known limits and untested device behavior. Keep experiments until a selection is made. Moving a chosen variant into production is a separate authorized change; no public publishing or dependency installation is implied.

Adapted from [Ibelick's create-canvas](https://github.com/ibelick/ui-skills/blob/main/skills/create-canvas/SKILL.md), with existing project showcases as the first host.
