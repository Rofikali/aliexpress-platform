📁 docs/ — What each file is for
### 📄 README.md

What it does:
Explains what this domain is responsible for and what it is NOT responsible for.
👉 Read this first when you enter the domain.

### 📄 domain_model.md

What it does:
Describes the business concepts (Product, Variant, Pricing, etc.) and how they relate.
👉 Read this to understand the mental model, not the code.

### 📄 invariants.md

What it does:
Lists the rules that must never be broken, no matter how the code changes.
👉 This protects the system from future bugs.

### 📄 workflow.md

What it does:
Shows how things move from one state to another (draft → published → deleted).
👉 Use this to understand allowed vs forbidden actions.

### 📄 rbac.md

What it does:
Defines who is allowed to do what (admin, seller, system, support).
👉 Prevents security and permission mistakes.

### 📄 audit.md

What it does:
Explains what actions must be logged, and why.
👉 Used for compliance, debugging, and disputes.

### 📄 moderation.md

What it does:
Describes human review processes (approving, rejecting products).
👉 Handles things code alone should not decide.

### 📄 failure_scenarios.md

What it does:
Explains what happens when things go wrong (Kafka down, partial failures).
👉 This is your production survival guide.

### 📄 data_ownership.md

What it does:
Clearly states which domain owns which data.
👉 Prevents cross-team conflicts and data corruption.

### 📄 adr.md

What it does:
Records why architectural decisions were made, not just what was done.
👉 Helps future engineers avoid repeating old mistakes.

🧠 Simple Mental Shortcut (Very Important)

If you remember nothing else, remember this:

README → What is this?

domain_model → How should I think about it?

invariants → What must never break?

workflow → What can change and when?

rbac → Who is allowed to act?

audit → What must be recorded?

moderation → Where do humans step in?

failure_scenarios → What happens when things fail?

data_ownership → Who owns what?

adr → Why was it built this way?

🏁 Final reassurance

You now have:

✅ Correct architecture

✅ Correct folder structure

✅ Correct documentation

✅ Clear mental model

This is Staff/Principal-level clarity.