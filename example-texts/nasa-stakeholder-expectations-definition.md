---
title: "4.1 Stakeholder Expectations Definition"
source: "NASA Systems Engineering Handbook"
source_url: "https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/"
pdf_url: "https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf"
license_note: "NASA-authored U.S. federal government handbook material; source-page images are omitted from this text fixture."
retrieved: "2026-05-13"
selection_note: "Official handbook section 4.1 selected as a high-quality, complex technical-process baseline, roughly handbook pages 45-53."
conversion_note: "Converted from NASA's official HTML handbook page; page chrome removed; image-only figures replaced with source-linked omission notes."
---
# 4.1 Stakeholder Expectations Definition

The Stakeholder Expectations Definition Process is the initial process within the SE
engine that establishes the foundation from which the system is designed and the product
is realized.
The main purpose of this process is to identify who the stakeholders are and
how they intend to use the product.
This is usually accomplished through use-case scenarios (sometimes referred to as Design
Reference Missions \[DRMs\]) and the ConOps.

## 4.1.1 Process Description

Figure 4.1-1 provides a typical flow diagram for the Stakeholder Expectations Definition
Process and identifies typical inputs, outputs, and activities to consider in defining
stakeholder expectations.

> Figure omitted from text fixture:
> [Flowchart showing the process for defining stakeholder expectations](https://www.nasa.gov/wp-content/uploads/2019/05/seh_figure_4-1_1_stakeholder_expectations_0.jpg).

### 4.1.1.1 Inputs

Typical inputs needed for the Stakeholder Expectations Definition Process include the
following:

- **Initial Customer Expectations:** These are the needs, goals, objectives, desires,
  capabilities, and other constraints that are received from the customer for the
  product within the product layer.
  For the top-tier products (final end item), these are the expectations of the
  originating customer who requested the product.
  For an end product within the product layer, these are the expectations of the
  recipient of the end item when transitioned.
- **Other Stakeholder Expectations:** These are the expectations of key stakeholders
  other than the customer.
  For example, such stakeholders may be the test team that will be receiving the
  transitioned product (end product and enabling products) or the trainers that will be
  instructing the operators or managers that are accountable for the product at this
  layer.
- **Customer Flow-down Requirements:** These are any requirements that are being flowed
  down or allocated from a higher level (i.e., parent requirements).
  They are helpful in establishing the expectations of the customer at this layer.

### 4.1.1.2 Process Activities

#### 4.1.1.2.1 Identify Stakeholders

A “stakeholder” is a group or individual that is affected by or has a stake in the
product or project. The key players for a project/product are called the key
stakeholders. One key stakeholder is always the “customer.”
The customer may vary depending on where the systems engineer is working in the PBS. For
example, at the topmost level, the customer may be the person or organization that is
purchasing the product.
For a systems engineer working three or four levels down in the PBS, the customer may be
the leader of the team that takes the element and integrates it into a larger assembly.
Regardless of where the systems engineer is working within the PBS, it is important to
understand what is expected by the customer.

Other interested parties are those who affect the project by providing broad,
overarching constraints within which the customers’ needs should be achieved.
These parties may be affected by the resulting product, the manner in which the product
is used, or have a responsibility for providing life cycle support services.
Examples include Congress, advisory planning teams, program managers, maintainers, and
mission partners. It is important that the list of stakeholders be identified early in
the process, as well as the primary stakeholders who will have the most significant
influence over the project.

The customer and users of the system are usually easy to identify.
The other key stakeholders may be more difficult to identify and they may change
depending on the type of the project and the phase the project is in.
Table 4.1-1 provides some examples of stakeholders in the life cycle phase that should
be considered.

> Figure omitted from text fixture:
> [Stakeholder Identification](https://www.nasa.gov/wp-content/uploads/2019/05/seh_table_4-1_1_stakeholder.jpg).

#### 4.1.1.2.2 Understand Stakeholder Expectations

Thoroughly understanding the customer and other key stakeholders’ expectations for the
project/product is one of the most important steps in the systems engineering process.
It provides the foundation upon which all other systems engineering work depends.
It helps ensure that all parties are on the same page and that the product being
provided will satisfy the customer.
When the customer, other stakeholders, and the systems engineer mutually agree on the
functions, characteristics, behaviors, appearance, and performance the product will
exhibit, it sets more realistic expectations on the customer’s part and helps prevent
significant requirements creep later in the life cycle.

Through interviews/discussions, surveys, marketing groups, e-mails, a Statement of Work
(SOW), an initial set of customer requirements, or some other means, stakeholders
specify what is desired as an end state or as an item to be produced and put bounds on
the achievement of the goals.
These bounds may encompass expenditures (resources), time to deliver, life cycle support
expectations, performance objectives, operational constraints, training goals, or other
less obvious quantities such as organizational needs or geopolitical goals.
This information is reviewed, summarized, and documented so that all parties can come to
an agreement on the expectations.

Figure 4.1-2 shows the type of information needed when defining stakeholder expectations
and depicts how the information evolves into a set of high-level requirements.
The yellow lines depict validation paths.
Examples of the types of information that would be defined during each step are also
provided.

> Figure omitted from text fixture:
> [Information Flow for Stakeholder Expectations](https://www.nasa.gov/wp-content/uploads/2019/05/seh_figure_4-1_2_information_flow.jpg).

Defining stakeholder expectations begins with the mission authority and strategic
objectives that the mission is meant to achieve.
Mission authority changes depending on the category of the mission.
For example, science missions are usually driven by NASA Science Mission Directorate
strategic plans, whereas the exploration missions may be driven by a Presidential
directive.
Understanding the objectives of the mission helps ensure that the project team
is working toward a common vision.
These goals and objectives form the basis for developing the mission, so they need to be
clearly defined and articulated.

The project team should also identify the *constraints* that may apply.
A “constraint” is a condition that is to be met.
Sometimes a constraint is dictated by external factors such as orbital mechanics, an
existing system that must be utilized (external interface), a regulatory restriction, or
the state of technology; sometimes constraints are the result of the overall budget
environment. Concepts of operation and constraints also need to be included in defining
the stakeholder expectations.
These identify how the system should be operated to achieve the mission objectives.

> **NOTE:** It is extremely important to involve stakeholders in all phases of a
> project. Such involvement should be built in as a self-correcting feedback loop that
> will significantly enhance the chances of mission success.
> Involving stakeholders in a project builds confidence in the end product and serves as
> a validation and acceptance with the target audience.

In identifying the full set of expectations, the systems engineer will need to interact
with various communities, such as those working in the areas of orbital debris, space
asset protection, human systems integration, quality assurance, and reliability.
Ensuring that a complete set of expectations is captured will help prevent “surprise”
features from arising later in the life cycle.
For example, space asset protection may require additional encryption for the forward
link commands, additional shielding or filtering for RF systems, use of a different
frequency, or other design changes that might be costly to add to a system that has
already been developed.

#### 4.1.1.2.3 Identify Needs, Goals, and Objectives

In order to define the goals and objectives, it is necessary to elicit the needs, wants,
desires, capabilities, external interfaces, assumptions, and constraints from the
stakeholders. Arriving at an agreed-to set of goals and objectives can be a long and
arduous task. Proactive iteration with the stakeholders throughout the systems
engineering process is the way that all parties can come to a true understanding of what
should be done and what it takes to do the job.
It is important to know who the primary stakeholders are and who has the decision
authority to help resolve conflicts.

Needs, Goals, and Objectives (NGOs) provide a mechanism to ensure that everyone
(implementer, customer, and other stakeholders) is in agreement at the beginning of a
project in terms of defining the problem that needs to be solved and its scope.
NGOs are not contractual requirements or designs.

Needs are defined in the answer to the question “What problem are we trying to solve?”
Goals address what must be done to meet the needs; i.e., what the customer wants the
system to do. Objectives expand on the goals and provide a means to document specific
expectations. (Rationale should be provided where needed to explain why the need, goal,
or objective exists, any assumptions made, and any other information useful in
understanding or managing the NGO.)

Well-written NGOs provide clear traceability from the needs, then to the goals, and then
to objectives.
For example, if a given goal does not support a need, or an objective does
not support a goal, it should not be part of the integrated set of NGOs.
This traceability helps ensure that the team is actually providing what is needed.

The following definitions (source: *Applied Space Systems Engineering* edited by Larson,
Kirkpatrick, Sellers, Thomas, and Verma) are provided to help the reader interpret the
NGOs contained in this product.

- **Need:** A single statement that drives everything else.
  It should relate to the problem that the system is supposed to solve but not be the
  solution. The need statement is singular.
  Trying to satisfy more than one need requires a trade between the two, which could
  easily result in failing to meet at least one, and possibly several, stakeholder
  expectations.
- **Goals:** An elaboration of the need, which constitutes a specific set of
  expectations for the system.
  Goals address the critical issues identified during the problem assessment.
  Goals need not be in a quantitative or measurable form, but they should allow us to
  assess whether the system has achieved them.
- **Objectives:** Specific target levels of outputs the system must achieve.
  Each objective should relate to a particular goal.
  Generally, objectives should meet four criteria.
  (1) They should be specific enough to provide clear direction, so developers,
  customers, and testers will understand them.
  They should aim at results and reflect what the system needs to do but not outline how
  to implement the solution.
  (2) They should be measurable, quantifiable, and verifiable.
  The project needs to monitor the system’s success in achieving each objective.
  (3) They should be aggressive but attainable, challenging but reachable, and targets
  need to be realistic.
  Objectives “To Be Determined” (TBD) may be included until trade studies occur,
  operations concepts solidify, or technology matures.
  Objectives need to be feasible before requirements are written and systems designed.
  (4) They should be results-oriented focusing on desired outputs and outcomes, not on
  the methods used to achieve the target (what, not how).
  It is important to always remember that objectives are not requirements.
  Objectives are identified during pre-Phase A development and help with the eventual
  formulation of a requirements set, but it is the requirements themselves that are
  contractually binding and will be verified against the “as-built” system design.

These stakeholder expectations are captured and are considered as initial until they can
be further refined through development of the concept of operations and final agreement
by the stakeholders.

#### 4.1.1.2.4 Establish Concept of Operations and Support Strategies

After the initial stakeholder expectations have been established, the development of a
Concept of Operations (ConOps) will further ensure that the technical team fully
understands the expectations and how they may be satisfied by the product, and that
understanding has been agreed to by the stakeholders.
This may lead to further refinement of the initial set of stakeholder expectations if
gaps or ambiguous statements are discovered.
These scenarios and concepts of how the system will behave provide an
implementation-free understanding of the stakeholders’ expectations by defining what is
expected without addressing how (the design) to satisfy the need.
It captures required behavioral characteristics and the manner in which people will
interact with the system.
Support strategies include provisions for fabrication, test, deployment, operations,
sustainment, and disposal.

The ConOps is an important component in capturing stakeholder expectations and is used
in defining requirements and the architecture of a project.
It stimulates the development of the requirements and architecture related to the user
elements of the system.
It serves as the basis for subsequent definition documents such as the operations plan,
launch and early orbit plan, and operations handbook, and it provides the foundation for
the long-range operational planning activities such as operational facilities, staffing,
and network scheduling.

The ConOps is an important driver in the system requirements and therefore should be
considered early in the system design processes.
Thinking through the ConOps and use cases often reveals requirements and design
functions that might otherwise be overlooked.
For example, adding system requirements to allow for communication during a particular
phase of a mission may require an additional antenna in a specific location that may not
be required during the nominal mission.
The ConOps should include scenarios for all significant operational situations,
including known off-nominal situations.
To develop a useful and complete set of scenarios, important malfunctions and
degraded-mode operational situations should be considered.
The ConOps is also an important aide to characterizing life cycle staffing goals and
function allocation between humans and systems.
In walking through the accomplishment of mission objectives, it should become clear when
decisions need to be made as to what the human operators are contributing vs.
what the systems are responsible for delivering.

The ConOps should consider all aspects of operations including nominal and off-nominal
operations during integration, test, and launch through disposal.
Typical information contained in the ConOps includes a description of the major phases;
operation timelines; operational scenarios and/or DRM (see Figure 4.1-3 for an example
of a DRM); fault management strategies, description of human interaction and required
training, end-to-end communications strategy; command and data architecture; operational
facilities; integrated logistic support (resupply, maintenance, and assembly); staffing
levels and required skill sets; and critical events.
The operational scenarios describe the dynamic view of the systems’ operations and
include how the system is perceived to function throughout the various modes and mode
transitions, including interactions with external interfaces, response to anticipated
hazard and faults, and during failure mitigations.
For exploration missions, multiple DRMs make up a ConOps.
The design and performance analysis leading to the requirements should satisfy all of
them.

> Figure omitted from text fixture:
> [Example of a Lunar Sortie DRM Early in the Life Cycle](https://www.nasa.gov/wp-content/uploads/2019/05/seh_figure_4-1_3_lunar_sortie.jpg).

Additional information on the development of the ConOps is discussed in Section 4.1.2.1
of the NASA Expanded Guidance for Systems Engineering document found at
https://nen.nasa.gov/web/se/doc-repository.

[**Appendix S**](https://www.nasa.gov/seh/appendix-s-concept-of-operations) contains one
possible outline for developing a ConOps.
The specific sections of the ConOps will vary depending on the scope and purpose of the
project.

### Concept of Operations vs. Operations Concept

#### Concept of Operations

Developed early in Pre-Phase A by the technical team, describes the overall high-level
concept of how the system will be used to meet stakeholder expectations, usually in a
time sequenced manner.
It describes the system from an operational perspective and helps facilitate an
understanding of the system goals.
It stimulates the development of the requirements and architecture related to the user
elements of the system.
It serves as the basis for subsequent definition documents and provides the foundation
for the long-range operational planning activities.

#### Operations Concept

A description of how the flight system and the ground system are used together to ensure
that the concept of operation is reasonable.
This might include how mission data of interest, such as engineering or scientific data,
are captured, returned to Earth, processed, made available to users, and archived for
future reference. It is typically developed by the operational team.
(See NPR 7120.5.)

#### 4.1.1.2.5 Define Stakeholder Expectations in Acceptable Statements

Once the ConOps has been developed, any gaps or ambiguities have been resolved, and
understanding between the technical team and stakeholders about what is
expected/intended for the system/product has been achieved, the expectations can be
formally documented.
This often comes in the form of NGOs, mission success criteria, and design drivers.
These may be captured in a document, spreadsheet, model, or other form appropriate to
the product.

The *design drivers* will be strongly dependent upon the ConOps, including the
operational environment, orbit, and mission duration requirements.
For science missions, the design drivers include, at a minimum, the mission launch date,
duration, and orbit, as well as operational considerations.
If alternative orbits are to be considered, a separate concept is needed for each orbit.
Exploration missions should consider the destination, duration, operational sequence
(and system configuration changes), crew interactions, maintenance and repair
activities, required training, and in situ exploration activities that allow the
exploration to succeed.

#### 4.1.1.2.6 Analyze Expectations Statements for Measures of Effectiveness

The *mission success criteria* define what the mission needs to accomplish to be
successful. This could be in the form of science missions, exploration concept for human
exploration missions, or a technological goal for technology demonstration missions.
The success criteria also define how well the concept measurements or exploration
activities should be accomplished.
The success criteria capture the stakeholder expectations and, along with programmatic
requirements and constraints, are used within the high-level requirements.

Measures of Effectiveness (MOEs) are the measures of success that are designed to
correspond to accomplishment of the system objectives as defined by the stakeholder’s
expectations.
They are stated from the stakeholder’s point of view and represent criteria
that are to be met in order for the stakeholder to consider the project successful.
As such, they can be synonymous with mission/project success criteria.
MOEs are developed when the NGOs or other stakeholder expectation documentation is
developed. Additional information on MOEs is contained in Section 6.7.2.4 of the NASA
Expanded Guidance for SE document at https://nen.nasa.gov/web/se/doc-repository.

#### 4.1.1.2.7 Validate That Defined Expectation Statements Reflect Bidirectional Traceability

The NGOs or other stakeholder expectation documentation should also capture the source
of the expectation. Depending on the location within the product layer, the expectation
may be traced to an NGO or a requirement of a higher layer product, to organizational
strategic plans, or other sources.
Later functions and requirements will be traced to these NGOs.
The use of a requirements management tool or model or other application is particularly
useful in capturing and tracing expectations and requirements.

#### 4.1.1.2.8 Obtain Stakeholder Commitments to the Validated Set of Expectations

Once the stakeholder and the technical team are in agreement with the expressed
stakeholder expectations and the concept of operations, signatures or other forms of
commitment are obtained.
In order to obtain these commitments, a concept review is typically held on a formal or
informal basis depending on the scope and complexity of the system (see
[**Section 6.7**](https://www.nasa.gov/seh/6.7-technical-assessment)). The stakeholder
expectations (e.g., NGOs), MOEs, and concept of operations are presented, discussed, and
refined as necessary to achieve final agreement.
This agreement shows that both sides have committed to the development of this product.

#### 4.1.1.2.9 Baseline Stakeholder Expectations

The set of stakeholder expectations (e.g., NGOs and MOEs) and the concept of operations
that are agreed upon are now baselined.
Any further changes will be required to go through a formal or informal (depending on
the nature of the product) approval process involving both the stakeholder and the
technical team.

#### 4.1.1.2.10 Capture Work Products

In addition to developing, documenting, and baselining stakeholder expectations, the
ConOps and MOEs discussed above and other work products from this process should be
captured. These may include key decisions made, supporting decision rationale and
assumptions, and lessons learned in performing these activities.

### 4.1.1.3 Outputs

Typical outputs for capturing stakeholder expectations include the following:

- **Validated Stakeholder Expectations:** These are the agreed-to set of expectations
  for this product layer.
  They are typically captured in the form of needs, goals, and objectives with
  constraints and assumptions identified.
  They may also be in the form of models or other graphical forms.
- **Concept of Operations:** The ConOps describes how the system will be operated during
  the life cycle phases that will meet stakeholder expectations.
  It describes the system characteristics from an operational perspective and helps
  facilitate an understanding of the system goals and objectives and other stakeholder
  expectations. Examples would be the ConOps document, model, or a Design Reference
  Mission (DRM).
- **Enabling Product Support Strategies:** These include any special provisions that
  might be needed for fabrication, test, deployment, operations sustainment, and
  disposal of the end product.
  They identify what support will be needed and any enabling products that will need to
  be developed in order to generate the end product.
- **Measures of Effectiveness:** A set of MOEs is developed based on the stakeholder
  expectations. These are measures that represent expectations that are critical to the
  success of the system, and failure to satisfy these measures will cause the
  stakeholder to deem the system unacceptable.

Other outputs that might be generated:

- **Human/Systems Function Allocation:** This describes the interaction of the hardware
  and software systems with all personnel and their supporting infrastructure.
  In many designs (e.g., human space flight) human operators are a critical total-system
  component and the roles and responsibilities of the humans-in-the-system should be
  clearly understood. This should include all human/system interactions required for a
  mission including assembly, ground operations, logistics, in-flight and ground
  maintenance, in-flight operations, etc.

## 4.1.2 Stakeholder Expectations Definition Guidance

Refer to Section 4.1.2 in the NASA Expanded Guidance for Systems Engineering at
https://nen.nasa.gov/web/se/doc-repository for additional guidance on:

- Concept of Operations (including examples),
- protection of space assets, and
- identification of stakeholders for each phase.
