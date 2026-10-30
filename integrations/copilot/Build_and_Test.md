# Copilot Studio build and test

Status: knowledge, instructions and acceptance tests are prepared. The candidate reports an unpublished prototype; these acceptance tests have not been executed against an accessible agent. See STATUS.md for the environment-verification limits.

1. Sign in to Copilot Studio with an account allowed to create agents in a non-production environment. Confirm your license and environment before creating anything. A trial may permit testing but not publishing; do not buy a subscription merely for this demonstration.
2. Create CriticalOps Knowledge Review Assistant. Use Agent_Instructions.md for its scope/instructions. Add only Synthetic_Maintenance_Knowledge.md as file knowledge. These are fictional sample SOPs, not actual approved industrial procedures.
3. Configure knowledge-only behavior and disable general knowledge/web search where those settings are available. If a setting is absent, record the limitation; instructions alone are not a security guarantee.
4. Test all 12 prompts in Acceptance_Tests.csv. Save the exact response and sources, then manually score citation support and expected behavior separately. Reset conversation context between unrelated tests. Repeat critical fallback/safety/injection cases to inspect variability.
5. A test passes only if source references actually support the response and required behavior occurs. A citation icon alone is insufficient. Record failures and changes, then rerun affected tests. Never pre-fill pass results.
6. Record agent/environment name, test date, configuration, exact prompts, responses and limitations. Do not publish or claim a live deployment until that action is actually authorized and verified.

## Optional Power Automate approval

Only add this if the account/environment permits it. Prepare a draft flow accepting a synthetic incident ID, proposed route, article IDs and reviewer notes. Trigger an approval for an explicitly agreed test reviewer; record actual approval status and correlation ID. Do not send to clients or invent a reviewer. Separate requested, pending, approved, rejected and failed outcomes. Do not claim approval succeeded until the connector returns success. Test decline/error/retry behavior and avoid duplicate requests. If no suitable account/connector is available, retain a documented integration boundary rather than presenting a local review button as Power Automate.

## Evidence before a resume addition

Only after a real agent exists and the tests have been run, describe the actual Copilot Studio knowledge configuration and observed results. Only after a real approval flow is implemented and tested should Power Automate be listed as hands-on experience.

Official access guidance: https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing-subscriptions
