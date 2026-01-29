## General outline for excellent technical documentation

### 1) Docs home

* **Choose-a-path entry points**

    * By *use case* (tiles like “accept payments”, “sell subscriptions”) ([Stripe Docs][3])
    * By *product / module* (browse-by-product index) ([Stripe Docs][3])
* **Two primary calls to action**

    * “Get started” (first working integration)
    * “Reference” (lookup)

### 2) Get started

Goal: fastest path to a working result.

* Account, auth, keys, permissions (as relevant) ([Stripe Docs][4])
* Local setup and tooling (CLI, SDK install) ([Stripe Docs][4])
* “Hello world” flow
* Next steps: link into Tutorials or a first How-to

### 3) Tutorials (learning-oriented)

Goal: build skill through a guided, end-to-end project.

* Beginner track (first app)
* Intermediate track (common real project)
* Each tutorial page typically contains:

    * Goal and outcome
    * Steps with checkpoints
    * “What you built” recap
    * Next links into How-to and Concepts

(Example framing: Django explicitly labels “Tutorials” as the hand-held path.) ([Django Project][2])

### 4) How-to guides / Tasks (goal-oriented recipes)

Goal: help a developer complete a concrete task during real work.

* “How to X” pages, one outcome per page ([Django Project][2])
* Tasks grouped by theme (deploy, secure, observe, scale)
* Common page shape:

    * Prerequisites
    * Steps
    * Verification
    * Variations and constraints
    * Links to relevant Reference entries

(Kubernetes calls these “Tasks”, separate from Tutorials and Concepts.) ([Kubernetes][5])

### 5) Concepts / Explanation (mental model)

Goal: help the reader understand “how it works” and “why it works that way”.

* Architecture overview
* Key abstractions and vocabulary
* Tradeoffs and design decisions
* Glossary (often centralized)

(Kubernetes uses a dedicated “Concepts” section; Django calls these “Topic guides”.) ([Kubernetes][5])

### 6) Reference (lookup)

Goal: authoritative, complete, and scannable.

* API reference (endpoints, resources) ([Stripe Docs][6])
* CLI reference (commands, flags)
* Configuration reference (schema, fields)
* Error reference (codes, messages, remediation)
* Limits and compatibility (rate limits, versions)

(Django calls this “Reference guides”; React has a dedicated “Reference” area distinct from “Learn”.) ([Django Project][2])

### 7) Quickstarts and end-to-end examples

Goal: copy, run, and adapt.

* Language/framework-specific quickstarts ([Stripe Docs][7])
* Downloadable or runnable sample apps
* Example gallery indexed by use case

(Stripe centers “Quickstarts” with interactive samples; Twilio emphasizes quickstarts plus API reference and SDKs.) ([Stripe Docs][7])

### 8) SDK and tooling docs

* Official SDK setup and usage patterns
* Version support and deprecations
* Generated API clients, OpenAPI notes (if applicable)

### 9) Troubleshooting and help

* FAQ ([Django Project][2])
* Common errors and fixes
* Debug and logging guides
* Support channels and escalation path

### 10) Upgrades, versions, and release notes

* Version selector and compatibility policy
* Migration guides for breaking changes
* Changelog and deprecations

### 11) Community and contribution

* “Edit this page” / docs-as-code workflow
* Style guide and content guide
* Contribution guide, review process

(You can see large projects include explicit documentation contribution guidance and style guidance alongside the user docs.) ([Kubernetes][5])

---

If you want, paste your current sidebar or table of contents, and I will map it into this structure with a minimal set of moves (rename, split, merge, and a suggested landing page).

[1]: https://diataxis.fr/start-here/?utm_source=chatgpt.com "Start here - Diátaxis in five minutes"
[2]: https://docs.djangoproject.com/en/6.0/ "Django documentation | Django documentation | Django"
[3]: https://docs.stripe.com/ "docs.stripe.com"
[4]: https://docs.stripe.com/get-started?utm_source=chatgpt.com "Get started"
[5]: https://kubernetes.io/docs/concepts/ "Concepts | Kubernetes"
[6]: https://docs.stripe.com/api?utm_source=chatgpt.com "Stripe API Reference"
[7]: https://docs.stripe.com/quickstarts?utm_source=chatgpt.com "Quickstart guides"
