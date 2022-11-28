---
name: Request or suggest a new solution accelerator or a new feature.
about: Have an idea for a new solution accelerator or a new feature?
title: '[new accelerator] <title>'
labels: ['New Feature', 'Needs Triage']
assignees: 'setuc'
---

body:
- type: textarea
  attributes:
    label: Why doesn't an existing solution accelerator work?
    description: |
    Concisely explain why a new solution accelerator is needed.Concisely explain why a new solution accelerator is needed.

  validations:
    required: true
- type: textarea
  attributes:
    label: What work is needed?
    description: |
    Concisely explain the infrastructure and MLOps work needed. Include as much detail as possible in how this would fit into the overall solution accelerator.
  validations:
    required: true
- type: textarea
  attributes:
    label: Anything else?
    description: |
    Links? References? Anything that will give us more context about the issue that you are encountering!
