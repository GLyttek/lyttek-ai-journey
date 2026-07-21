# MCP Least-Privilege and Tool-Scoping Guide

Model Context Protocol makes tools and data easier to connect. It does not make those connections trustworthy by default. An MCP server is an execution boundary with identity, authorization, data-flow and supply-chain consequences.

## Start with an inventory

For every server, record:

| Field | Question |
|---|---|
| Owner/source/version | Who maintains the server and which reviewed version runs? |
| Transport | Local process or remote service? Which endpoint? |
| Operations | What can each tool read, write, send or trigger? |
| Data classes | What enters and leaves the server? |
| Identity | Which user or workload is represented? |
| Credentials | Where are tokens held and how are they scoped? |
| Destinations | Which downstream systems and networks are reachable? |
| Approval | Which calls require user or policy approval? |
| Limits | Rate, cost, timeout, retries and chain depth? |
| Verification | How is the effect checked and reversed? |
| Lifecycle | How is the server updated, disabled and retired? |

Unknown is not a low-risk answer.

## Progressive discovery

Do not expose the full tool catalog simply because the model might find it useful. Start with no tools or a minimal read-only set, then add narrowly scoped capabilities for the current task.

A useful progression is:

```text
discover approved metadata
→ request one task-relevant scope
→ authorize one operation class
→ execute through the host
→ verify outcome
→ drop elevation
```

The official MCP guidance describes progressive least-privilege scope models. The host still needs to decide which elevation is appropriate for its users and data.

## Authentication is not authorization

A valid token identifies or authenticates a caller. It does not prove that every requested tool, resource or downstream action is allowed.

- validate tokens for the MCP server as their intended audience;
- reject token passthrough;
- verify authorization on every request and resource handle;
- keep handles opaque, bounded and tied to the authenticated user;
- do not rely on connection state as permission;
- distinguish user-delegated access from background workload identity.

For server-to-server use, client credentials need especially narrow scopes because there may be no human present when the call occurs.

## Keep credentials out of model context

The host or broker holds credentials. The model calls typed operations with normalized parameters. The host adds authentication only after policy allows the request.

Do not place API keys, refresh tokens, SSH material or cloud CLI profiles in prompts, tool output or general memory.

## Treat tool metadata and output as untrusted

A tool description can be inaccurate or malicious. A tool result can contain prompt injection, active markup or data intended for a different destination.

- approve server provenance before connection;
- validate schemas and parameters;
- treat annotations as claims, not policy;
- sanitize or inertly render rich output;
- label source and trust level before returning data to the model;
- do not let one server's output authorize another server's call.

## Control cross-server data flow

Consider this chain:

```text
mail search → model summary → issue tracker → public repository
```

Each arrow changes destination and potentially data classification. The host must check every transition. Output truncation does not prevent exfiltration, and a sandbox does not help if the broker forwards an unauthorized payload.

## Network and OAuth boundary

MCP clients that fetch authorization metadata or connect to remote endpoints need SSRF and egress controls:

- require HTTPS in production;
- reject loopback, link-local and private destinations unless explicitly intended;
- validate redirects and authorization URLs;
- route discovery through an egress policy where appropriate;
- pin or review expected issuers and resources;
- log scope elevation and destination changes.

## Call policy

Before a sensitive call, evaluate:

```text
who is acting?
which server and tool?
which exact target and parameters?
which data crosses the boundary?
which downstream destination is involved?
which approval applies and when does it expire?
how will the real effect be verified?
```

For high-impact effects, bind approval to normalized parameters and use replay protection. A general “allow this server” click is not equivalent.

## One-click local servers

A local command can still read files, spawn processes and reach the network. Before executing a new server command:

- show the command and source;
- inspect package and update behavior;
- request explicit consent;
- run with restricted filesystem, process and network rights;
- avoid inheriting the user's entire environment;
- record which version was admitted.

## Review checklist

- [ ] server owner, source, version and license reviewed
- [ ] tool catalog minimized by task and caller scope
- [ ] token passthrough absent
- [ ] every request and handle is authorized
- [ ] credentials remain in the host or broker
- [ ] downstream destinations and egress constrained
- [ ] tool output treated as untrusted
- [ ] cross-server flow reviewed
- [ ] rates, retries, costs and duration bounded
- [ ] high-impact calls use exact approvals
- [ ] logs omit secrets but preserve decisions and outcomes
- [ ] disable, revoke and retirement paths tested

## Evidence boundary

This guide narrows the review surface. It is not a claim that OAuth, containers or human confirmation alone secure an MCP deployment. Test the actual client, server, identity provider, network and downstream API.

## References

- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)
- [MCP Authorization specification](https://modelcontextprotocol.io/specification/latest/basic/authorization)
- [MCP Client Best Practices](https://modelcontextprotocol.io/docs/develop/clients/client-best-practices)
- [OWASP Practical Guide for Securely Using Third-Party MCP Servers](https://genai.owasp.org/resource/cheatsheet-a-practical-guide-for-securely-using-third-party-mcp-servers-1-0/)
