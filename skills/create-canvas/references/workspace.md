# Freeform workspace contract

Apply when creating or changing a freeform controller. Content-only updates exercise affected behavior without rebuilding the controller.

## Source owns content

The typed registry owns membership, names, components, fixtures and dimensions. Add/duplicate/remove through source edits. Layout storage may contain only versioned camera, supported theme and bounded positions keyed by current IDs. Validate finite coordinates, zoom, size and counts; ignore stale IDs and unsupported versions. Storage failure must not break rendering. New entries always remain visible. Never store form drafts, account data, executable strings or a second content registry.

## Separate navigation from preview input

Place a readable name above each preview and a separate accessible move handle. Activating the name copies its exact text; show success only after the clipboard succeeds and provide selectable text on failure. Give handles keyboard movement and visible focus. Moving, copying, changing themes and moving the camera must not remount previews or erase input.

Provide empty-space pan, pointer-anchored wheel/pinch zoom, viewport-centered zoom buttons, fit-all and reset-camera. Reset only the camera. Keep positions and drafts. Fit measured bounds including labels/handles after layout settles. Preserve native control, text-selection, nested-scroll, modal and keyboard behavior. Explicit Space/middle-button pan owns the gesture, never activates the preview on release, and must not arm while editing. Preserve ordinary one-finger preview input; test actual touch/trackpad behavior before claiming it works.

Portals retain supported native roots, focus and screen-space geometry. Use public container APIs where needed; disclose transform limitations rather than patching preview DOM or libraries. Navigation is owned by the workspace and must not perform real project actions or silently discard it. Keep native Back/Forward behavior; do not trap history or leave document styles/listeners behind.

## Keep movement bounded and cheap

Convert movement into canvas coordinates at current zoom. Track gesture ownership, cancellation, lost capture, blur and changing pointer counts. Keep active gesture values outside component-wide render state; batch transform writes per animation frame, cache measurements and debounce saves. Restore owned document styles and clean listeners, observers and pending work on teardown. Do not virtualize away interactive state without evidence.

Exercise several zoom levels, portal alignment, input preservation, nested-scroll limits, reload with malformed/old layout, copying failure and keyboard navigation. Actual touch/history-swipe tests require suitable devices; synthetic events cannot establish them. Profile a representative populated canvas before claiming smooth performance. Report every unavailable case.
