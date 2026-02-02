# AI Agents Workshop: Building Reliable Agents in 2026

**Duration:** Half-day (4 hours) or Full-day (8 hours)
**Audience:** Technical leads, developers, architects
**Prerequisites:** Basic understanding of LLMs and APIs

---

## Workshop Objectives

By the end of this workshop, participants will be able to:

1. Identify and mitigate AI hallucination risks
2. Design agents with proper intent disambiguation
3. Implement layered verification strategies
4. Apply appropriate control protocols based on risk
5. Navigate EU AI Act compliance requirements

---

## Agenda (Half-Day Version)

### Module 1: The Reliability Challenge (60 min)

**Theory (20 min)**
- Why AI hallucinations happen
- The business impact of unreliable agents
- Reframing hallucination as a validation problem

**Demo (20 min)**
- Live demonstration of hallucination scenarios
- RAG implementation walkthrough
- Chain of Verification in action

**Exercise (20 min)**
- Participants identify hallucination risks in their use cases
- Design a verification strategy for one scenario

---

### Module 2: The Intent Gap (60 min)

**Theory (20 min)**
- Intent Gap vs. Validation Gap
- Why "delete old files" goes wrong
- Living requirements artifacts

**Demo (20 min)**
- Disambiguation loop implementation
- Clarification chain patterns
- Intent artifact creation

**Exercise (20 min)**
- Participants write intent artifacts for their use cases
- Peer review and critique

---

### Module 3: Safety Architecture (60 min)

**Theory (20 min)**
- Control protocols by risk level
- Zero Trust for Agents
- The six attack vectors

**Demo (20 min)**
- Risk classification matrix
- Approval workflow implementation
- Security monitoring patterns

**Exercise (20 min)**
- Participants classify their planned agents by risk
- Design appropriate control protocols

---

### Module 4: Implementation Roadmap (60 min)

**Theory (20 min)**
- The 30-day sprint framework
- Validation maturity levels
- EU AI Act essentials

**Workshop (40 min)**
- Participants create their own 30-day plan
- Present and receive feedback
- Q&A and next steps

---

## Agenda (Full-Day Extension)

### Additional Modules

**Module 5: Hands-On RAG Implementation (90 min)**
- Set up vector database
- Implement embedding pipeline
- Build retrieval-augmented agent

**Module 6: Multi-Agent Orchestration (90 min)**
- LLM Council patterns
- Agent-to-agent communication
- Workflow decomposition

**Module 7: Compliance Deep Dive (60 min)**
- EU AI Act high-risk requirements
- GDPR implications for AI agents
- Documentation and audit trails

---

## Materials Provided

- [ ] Slide deck (34 slides)
- [ ] Video recording: https://youtu.be/64qeuW15J8g
- [ ] Code samples repository
- [ ] Intent artifact templates
- [ ] Risk classification matrix
- [ ] 30-day sprint template
- [ ] EU AI Act checklist

---

## Technical Requirements

**For Demos:**
- Python 3.10+
- Ollama (local LLM)
- FAISS or similar vector DB
- Access to cloud LLM APIs (optional)

**For Exercises:**
- Laptop with code editor
- Internet access
- Whiteboard/Miro for collaboration

---

## Facilitator Notes

### Key Messages to Reinforce

1. **"The bottleneck is validation, not hallucination prevention"**
   - Don't try to eliminate hallucinations
   - Build robust validation mechanisms

2. **"Friction is a feature, not a bug"**
   - High-risk actions need explicit approval
   - Low-risk can be autonomous

3. **"AI validates AI; humans validate validators"**
   - Solve the human validation bottleneck
   - Build trust incrementally

4. **"Start small, verify everything, scale trust"**
   - Don't boil the ocean
   - Pilot → Prove → Scale

### Common Questions

**Q: How do we know when to use which verification method?**
A: Use the layered approach. RAG for grounding, Chain of Verification for critical claims, Self-Consistency for reasoning, LLM Council for important decisions.

**Q: How do we handle EU AI Act compliance?**
A: First classify your system's risk level. High-risk requires 8 mandatory controls. Most business automation is Limited or Minimal risk.

**Q: What's the ROI of verification overhead?**
A: One prevented hallucination-based error typically costs more than thousands of verification calls. Focus on high-stakes decisions.

---

## Follow-Up Resources

- [Lyttek AI Journey](https://github.com/GLyttek/lyttek-ai-journey)
- [Training Video](https://youtu.be/64qeuW15J8g)
- [Code Samples](https://github.com/GLyttek/myscripts)

---

*Workshop developed by Lyttek GmbH, February 2026*
