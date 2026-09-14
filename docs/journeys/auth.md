# Authentication journey — Saleor storefront

Phase: P01 — Explore Saleor customer journeys.
Status: Core manual authentication walkthrough COMPLETE — validation, rejection, sign-in, refresh, account access, authenticated login-route behavior, logout, and the signed-out account gate recorded. Source operation mapping complete for this scope; remaining evidence limitations are listed below. P01 overall remains in progress.
Source review date: 2026-09-14.
Reference checkout: sibling `storefront/`, latest commit `37bc4922`.
This commit identifies the checkout; source findings describe the working files inspected.

## Scope and evidence

Map customer sign-in, validation failures, signed-in state, refresh, and sign-out.
Dashboard administrator login is a separate surface; its P00 verification does not
confirm storefront authentication. Record registration and password-reset entry
points as follow-ups.

- **Source finding:** inspected implementation or English translation; needs runtime confirmation.
- **Observed:** supported by user-reported browser observations, an attached screenshot, or a recorded response. Identify the evidence source for each finding.
- **Pending:** unknown; do not treat as a successful check.

Use a local test account. Record an account alias, never its password, tokens,
cookies, or raw credential payloads. Planned local screenshot paths are under
`artifacts/journey-mapping/auth/`. Screenshots for the walkthrough are conversation
attachments; no local screenshot files have been verified. The artifacts directory
contains only `.gitkeep` at this review.

## Session record

| Field | Value |
| --- | --- |
| Browser/version, viewport, zoom | Browser appears to be Brave from screenshot chrome. AUTH-05 shows DevTools Responsive viewport **759 × 762**, Fit to window, and No throttling. AUTH-04b/05 requests identify Android 15 / Pixel 9 / Chrome 153, with Brave 153 client hints and mobile enabled; this is the reported request identity, not verification of physical hardware. Browser zoom, pixel ratio, and host browser version remain pending. Do not apply AUTH-05 dimensions retroactively to earlier captures. |
| Observation date/time | Evidence received 2026-09-14. AUTH-04b response Date: 11:56:09 UTC (17:26:09 IST); AUTH-05 response Date: 12:05:56 UTC (17:35:56 IST). Exact screenshot capture times not supplied. |
| Entry URL | `http://localhost:3000` |
| Final homepage URL, locale, channel | User-reported `http://localhost:3000/en/default-channel`; locale `en`, channel `default-channel` |
| Exact login URL | `http://localhost:3000/en/default-channel/login` — user report and screenshot address bar agree |
| Initial authentication state | Empty login form and account/person icon visible; screenshot shows a private-window indicator. Session cookies were not inspected. |
| Local test-account alias and prerequisites | AUTH-04a: `unknown-account`, confirmed unregistered by user. AUTH-04b/05: `registered-test-account`, confirmed registered by user and successfully signed in during AUTH-05. Account role/type is not separately verified. Account email, passwords, and tokens are not stored here. |
| Observed UI language | English, confirmed by visible login text |

## Source findings to verify

| Area | Finding |
| --- | --- |
| Login route | `/{locale}/{channel}/login`; observed URL uses locale `en` and channel `default-channel`. |
| Guest entry | Header account icon is a link with accessible name `Log in` in English. |
| Login form | Heading `Welcome Back`; labels `Email` and `Password`; submit `Sign In`. |
| Related controls | `Sign up` link, `Forgot password?` button, and password visibility button named `Show password` / `Hide password`. |
| Signed-in menu | Source provides a hidden `Open user menu` trigger label, account/orders links with relative destinations `/account` and `/account/orders`, and a logout control. Menu text is observed below; rendered roles, accessible names, and resolved link destinations remain pending. |
| Pending submission | Submit is disabled and reads `Signing in…`. |
| Valid sign-in | Browser sends `POST /api/auth/login` with email/password field names. Success returns HTTP 200 and `{"ok":true}`; code navigates to the locale/channel homepage. |
| Backend authentication | Installed `@saleor/auth-sdk` 1.0.3 defines operation `mutation tokenCreate`, selecting mutation field `tokenCreate`; its `signIn` method sends that document. Source evidence, not a runtime GraphQL capture. |
| Session check | Inspected GraphQL document is `query CurrentUser` selecting `me`. Login page uses it when a session exists; request timing and runtime results remain pending. |
| Account gate | Account layout resolves `CurrentUserProfile` selecting `me`; guest state renders `AccountLogin` in place. AUTH-07b confirms the login form at the unchanged `/account` URL. |
| Logout | `LogoutButton` calls `useLogout`, which invokes the `logout` server action then navigates to the locale/channel homepage. The action detaches customers from checkouts referenced by checkout cookies, calls SDK sign-out, and clears Saleor auth cookies. Runtime cookie deletion and action response were not captured. |
| Incorrect credentials | Invalid credential/password codes map to HTTP 401 at the storefront endpoint. English form alert: `Invalid email or password. Please try again.` |
| Empty/invalid form | Inputs are required; email has type `email`. Browser-native validation may prevent submission before custom validation runs. Record which behavior actually occurs. |

The browser talks to the storefront authentication endpoint; the storefront talks
to `http://localhost:8000/graphql/`. A missing browser `graphql` request does not
prove that no GraphQL operation ran. Keep browser HTTP status, backend GraphQL
errors, and UI outcomes separate.

Source files under the sibling `storefront/` repository:

- `src/ui/components/nav/components/user-menu/user-menu-login-link.tsx`
- `src/ui/components/nav/components/user-menu/user-menu.tsx` (inspected when mapping the opened menu)
- `src/app/(storefront)/[locale]/[channel]/(main)/login/page.tsx`
- `src/ui/components/login-form.tsx`
- `src/ui/components/auth/login-mode.tsx`
- `src/lib/auth/bff-client.ts`, `src/lib/auth/bff-server.ts`
- `src/app/api/auth/login/route.ts`, `src/lib/auth/auth-api-utils.ts`
- `src/graphql/CurrentUser.graphql`, `messages/en.json`
- `src/lib/auth/logout-button.tsx`, `src/lib/auth/use-logout.ts`, `src/app/actions.ts`
- `src/lib/auth/server.ts`, `src/lib/auth/resolve-session-user.ts`, `src/lib/auth/fetch-authenticated-user.ts`
- `src/app/(storefront)/[locale]/[channel]/(main)/account/layout.tsx` and `get-current-user.ts`
- `src/ui/components/account/account-login.tsx`, `src/graphql/CurrentUserProfile.graphql`
- `src/lib/checkout.ts`, `src/graphql/CheckoutCustomerDetach.graphql`
- Installed dependency `node_modules/@saleor/auth-sdk/mutations.js` and `SaleorAuthClient.js` (version 1.0.3)

### GraphQL operation mapping (source evidence)

| Trigger | Operation name / field | Expected result and runtime evidence limit |
| --- | --- | --- |
| Credential submission through storefront BFF | Mutation `tokenCreate` / `tokenCreate` | SDK consumes tokens and errors; valid sign-in yields storefront HTTP 200 and `{"ok":true}`, rejected credentials yield HTTP 401 and the recorded error. Those BFF results are observed; raw GraphQL status/body and execution are not captured. |
| Login page session resolution | Query `CurrentUser` / `me` | An authenticated user leads to the homepage destination. Observed destination matches source; query execution/result remains unobserved. |
| Account route session resolution | Query `CurrentUserProfile` / `me` | Authenticated state renders account content; guest state renders login in place. Both UI states observed. The query's runtime execution/result is unobserved; a guest visit alone does not prove it ran. |
| Logout with a checkout cookie | Mutation `CheckoutCustomerDetach` / `checkoutCustomerDetach` | Source requests detachment and selects errors before clearing auth storage. Whether a checkout was present, detachment ran, or errors occurred in this walkthrough is unknown. |
| SDK sign-out | No GraphQL mutation in the inspected SDK `signOut` method | Clears auth storage; the storefront server action also clears auth cookies. Do not invent a logout API endpoint or token-revocation mutation. Guest UI is observed; token revocation is not tested. |

The SDK also defines `refreshToken` / `tokenRefresh`. A page refresh is not evidence
that this operation ran; expiry and refresh-token behavior are outside this walkthrough.

## Stable locator candidates

These are descriptions for later automation, not implemented tests. Confirm each
candidate's accessible name, uniqueness, visibility, and associated control in
the rendered page. Names depend on the observed locale.

| Element | Candidate from source | Runtime confirmation |
| --- | --- | --- |
| Guest account entry | Link, accessible name `Log in`, scoped to header if needed | Account/person icon visible; accessible name, role, and uniqueness pending |
| Form heading | Heading, name `Welcome Back` | Visible text confirmed; DOM role/name and uniqueness pending |
| Email input | Associated label `Email`; source association `for=email` / `id=email` | Visible label and `you@example.com` placeholder confirmed; DOM association and uniqueness pending |
| Password input | Associated label `Password`; source association `for=password` / `id=password` | Visible label and `Enter your password` placeholder confirmed; DOM association and uniqueness pending |
| Submit | Button, exact name `Sign In` | Visible text confirmed; DOM role/name, enabled state, and uniqueness pending |
| Authentication error | Role `alert`, with the observed error text | AUTH-04a/b confirm visible `Invalid email or password. Please try again.` banner; rendered DOM role and uniqueness pending |
| Password visibility | Button, name `Show password` / `Hide password` | Eye icon visible; accessible name and behavior pending |
| Registration entry | Link, name `Sign up` | Visible text confirmed; DOM role, destination, and uniqueness pending |
| Recovery entry | Button, name `Forgot password?` | Visible text confirmed; DOM role/name, behavior, and uniqueness pending |
| Signed-in menu trigger | Candidate button with accessible name containing `Open user menu`, from the source's hidden label; inspect whether avatar text also contributes to the name | `HB` badge and opened menu visually confirmed; rendered role/name and uniqueness pending |
| My account menu entry | Candidate menu item with exact visible text `My account`; source wraps a link with relative destination `/account` | AUTH-06b confirms destination `/en/default-channel/account` after the requested menu action; rendered role/name, href attribute, and uniqueness remain pending |
| My orders menu entry | Candidate menu item with exact visible text `My orders`; source wraps a link with relative destination `/account/orders` | Text visible in opened menu; rendered role/name, resolved href, uniqueness, and navigation pending |
| Sign-out menu entry | Candidate menu item with exact visible text `Log Out`; source wraps `LogoutButton` | Text visible in opened menu; AUTH-07a/b confirm guest UI and signed-out account gate after reported logout. Rendered role/name and uniqueness pending. |
| Account overview welcome | Candidate heading whose text starts with `Welcome back,`; account name is a test-data parameter | Personalized heading visually confirmed in AUTH-06b; rendered role, heading level, and uniqueness pending |

## Guided observation sequence

The core observation sequence through AUTH-07b is complete. Outstanding
URL/DOM/network/artifact evidence limitations are identified per case.
Screenshot filenames are planned until a local file is verified. Expected
results are candidates until confirmed.

| Step | Entry state and user action | Expected UI/API result to verify | Screenshot checkpoint |
| --- | --- | --- | --- |
| AUTH-01 | Fresh private window; open storefront and wait for stable content | Record redirected URL, locale/channel, guest header, and login entry | `auth-01-guest.png` |
| AUTH-02 | Open the guest login entry without entering credentials | Record exact URL, heading, labels, button names, initial errors, and locator uniqueness | `auth-02-login-empty.png` |
| AUTH-03a | Submit both fields empty | Record native versus application validation, focused field, exact text, URL, and whether an auth request was sent | `auth-03a-empty-fields.png` |
| AUTH-03b | Submit a malformed email with a disposable non-secret password | Record validation message, focused field, URL, and whether an auth request was sent | `auth-03b-invalid-email.png` |
| AUTH-04a | Submit a syntactically valid email that has not been registered, with a disposable password | Record request URL/method/status, response error code/message, visible rejection, and final page URL | `auth-04a-unknown-account.png` |
| AUTH-04b | Submit an existing local account with an intentionally wrong password once | Remain signed out; record request URL/method/status, response error code/message, visible rejection, and final page URL | `auth-04b-wrong-password.png` |
| AUTH-05 | Submit valid local credentials | Record endpoint success, final URL, and authenticated UI; verify the UI as well as the HTTP response | `auth-05-signed-in.png` |
| AUTH-05-menu | Open the signed-in account badge | Record menu entries and candidate locators; inspect account links and sign-out control | `auth-05-account-menu.png` |
| AUTH-06a | Refresh the signed-in homepage and reopen the account menu | Record whether the account badge/menu persist and the resulting URL/state | `auth-06a-session-refresh.png` |
| AUTH-06b | Open `My account` while signed in | Record actual destination URL, account-page text, authenticated identity, and any errors | `auth-06b-account-access.png` |
| AUTH-06c | Visit the login URL while signed in | Record resulting URL/state; source predicts a homepage redirect for an authenticated session | `auth-06c-authenticated-login-route.png` |
| AUTH-07a | Open the account badge and choose `Log Out` | Record final URL, guest header, visible messages, and actual sign-out request/action without assuming a logout mutation | `auth-07a-signed-out.png` |
| AUTH-07b | After logout, directly visit the previously observed account URL | Record final URL and whether the account overview is replaced by a login prompt or another access gate | `auth-07b-account-after-logout.png` |

For each completed step, add a record with:

- Observed URL/path and entry state.
- Action, exact visible text, and rendered locator evidence.
- Browser request method/URL/status and redacted response summary, or explicitly no request.
- Backend GraphQL operation name, mutation/query field, result, and evidence source;
  use `not observed` where server-side visibility is unavailable.
- Expected versus observed UI/API outcome.
- Screenshot path and any dynamic or obscured regions.

Additional negative paths to decide after the first walkthrough:
inactive/unconfirmed account and interrupted request. Keep unknown-account and
existing-account/wrong-password observations separate. Rate limiting is present in source; avoid
repeated invalid submissions during this mapping session.

## Observed record — AUTH-01 and AUTH-02

Evidence: user-reported homepage/login URLs and one attached login screenshot,
received 2026-09-14. This records visible page state; no DOM inspector or network
capture was supplied.

| Item | Observation |
| --- | --- |
| Homepage | User reports `http://localhost:3000/en/default-channel`. Homepage screenshot and redirect sequence not supplied. |
| Login page | User reports `http://localhost:3000/en/default-channel/login`; screenshot shows the same path. |
| Entry/action | Login page reached with both fields empty. The account icon click/navigation sequence was not separately described. |
| Browser tab title | `Sign In \| Saleor Store` |
| Form heading | `Welcome Back` |
| Registration prompt | `Don't have an account? Sign up` |
| Email field | Label `Email`; placeholder `you@example.com`; no value entered |
| Password field | Label `Password`; placeholder `Enter your password`; eye icon visible; no value entered |
| Recovery control | `Forgot password?` |
| Submit control | `Sign In`; no submitting text or spinner visible |
| Initial error state | No error or validation message visible in the captured form |
| Expected versus observed UI | Source-predicted empty login form and English text match the screenshot. Submission and navigation behavior have not been exercised. |
| Browser API / backend GraphQL | Not observed. No HTTP status, response, session validity, or executed GraphQL operation can be concluded from this screenshot. |
| Screenshot checkpoint | AUTH-02 supplied as a conversation attachment. Planned local filename: `artifacts/journey-mapping/auth/auth-02-login-empty.png`; file not verified. AUTH-01 homepage capture pending. |

The screenshot also shows navigation, search, the account/person and bag icons,
and the announcement `Free shipping on orders over $75.00`. The announcement is
page context, not authentication success evidence. A development indicator is
visible at the lower left. Future application captures should exclude browser
chrome and handle development UI separately; the login-form region is a useful
candidate for a focused checkpoint. No loader or transient form notification is
visible in this single capture; stability over time remains unverified.

## Observed record — AUTH-03a: empty-field validation

Evidence: two screenshots received 2026-09-14 in response to the empty-form
submission step. The first shows the validation bubble; the follow-up shows
the same validation state alongside the Network panel. Neither shows the
address bar.

| Item | Observation |
| --- | --- |
| Entry/action context | Requested action: leave both fields empty and click `Sign In` once. Screenshot shows the resulting validation state; the click itself is not captured. |
| Field values | Email and Password still display their placeholders; no entered values visible |
| Validation message | `Please fill out this field.` |
| Focus | Email input has a focus outline and visible caret; the validation bubble is anchored to it |
| Validation type | Browser-native required-field validation, identified from the bubble and inspected required-input source. DOM validity properties have not been inspected. |
| Other visible state | Login form remains visible; submit reads `Sign In`; no application error banner or submitting spinner visible |
| Expected versus observed UI | Required-field validation appears on Email before credentials can be submitted. This is expected invalid-input handling, not evidence of a server-rejected sign-in. |
| Current URL | Pending — address bar not shown; do not infer that the URL remained unchanged |
| Browser request / HTTP status | Follow-up Network capture has recording enabled, `Keep log` checked, Fetch/XHR selected, and text filter `/api/auth/login`. No matching rows appear; footer reads `0 / 2 requests`. No login HTTP status is available. |
| Network interpretation | No matching login Fetch/XHR request is recorded in the supplied capture. Together with the native required-field bubble, this supports validation blocking the login submission before the application's handler. The counter does not mean there were zero requests overall. |
| Backend GraphQL | Not observed. No backend authentication response is available; this is not a tested GraphQL rejection. |
| Screenshot checkpoint | Two AUTH-03a conversation attachments. Planned local files: `artifacts/journey-mapping/auth/auth-03a-empty-fields.png` and `artifacts/journey-mapping/auth/auth-03a-empty-fields-network.png`; neither file verified. |

The native validation bubble is distinct from the application's `role=alert`
authentication error. Keep the application-alert locator pending. Exact native
validation wording can depend on browser and language; preserve this text as the
observed wording for this session.

The validation captures show a narrower layout than AUTH-02: a hamburger menu is
visible and desktop navigation/search are not shown. The follow-up confirms
DevTools Responsive mode and Fit to window; exact viewport/zoom remain pending.
Treat these captures as different layout contexts,
not evidence of a visual regression. The bubble, focus outline, and caret are
intentional parts of this validation checkpoint; the development indicator is
still visible at the lower left.

## Observed record — AUTH-03b: malformed-email validation

Evidence: user-supplied screenshot received 2026-09-14, showing the form and
filtered Network panel after the requested malformed-email submission.

| Item | Observation |
| --- | --- |
| Entry/action context | Requested action: enter a malformed email and disposable test password, then click `Sign In` once. Screenshot shows Email containing `not-an-email` and a populated, masked Password field. |
| Validation message | `Please include an '@' in the email address. 'not-an-email' is missing an '@'.` |
| Focus | Email input has a focus outline and caret; validation bubble is anchored to it |
| Validation type | Browser-native email-format validation, consistent with the inspected `type=email` input. DOM validity properties remain uninspected. |
| Other visible state | Login form remains visible; submit reads `Sign In`; no application error banner or submitting spinner visible |
| Expected versus observed UI | The malformed email triggers native validation even with a populated password. The visible result agrees with the source-predicted email-format requirement. |
| URL before/after | Pending — address bar is outside the screenshot; no explicit URL report supplied for this attempt |
| Browser request / HTTP status | Fetch/XHR selected with `/api/auth/login` text filter; no matching rows; footer reads `0 / 2 requests`. No login HTTP status is available. Recording control is outside this capture. |
| Network interpretation | No matching login request is visible in the supplied capture. Together with the native validation bubble, this supports form validation blocking submission; the counter does not mean zero requests overall. |
| Backend GraphQL | Not observed; this case supplies no backend authentication response or GraphQL rejection evidence |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-03b-invalid-email.png`; file not verified. |

The native validation bubble overlaps the password-label/input region. Keep that
overlap as part of this error-state checkpoint; it does not establish that the
password control is missing. Exact browser validation text is session-specific.

## Observed record — AUTH-04a: unknown-account rejection

Evidence: user-supplied screenshot and subsequent pasted response/request
details received 2026-09-14. The user explicitly confirms that the submitted
email was not created as an account.

| Item | Observation |
| --- | --- |
| Entry/action context | Screenshot follows the requested incorrect-credentials submission. Email contains a syntactically valid example address and Password is populated and masked. |
| Test-account prerequisite | User confirms the email is not registered. Alias: `unknown-account`. Separate existing-account rejection evidence is recorded in AUTH-04b. |
| Visible application message | `Invalid email or password. Please try again.` in a red-tinted banner above Email |
| UI state | Login form remains visible, Email and masked Password remain populated, and submit reads `Sign In`. No native validation bubble is visible. |
| Browser request | Network text filter `/api/auth/login`, Fetch/XHR selected, one visible row named `login`, type `fetch`, initiator `bff-client.ts:20`; footer reads `1 / 3 requests` |
| HTTP status | `401 Unauthorized`, confirmed by screenshot and user-pasted request details |
| Request URL and method | User reports `POST http://localhost:3000/api/auth/login`, matching the source-mapped endpoint |
| Response body / error code | User-pasted response contains one `errors` entry: message `Please, enter valid credentials`, code `INVALID_CREDENTIALS`. Presentation escapes in the pasted text are normalized in the JSON below. |
| Expected versus observed | HTTP 401 and the displayed application error match the source-predicted rejected-credentials behavior. This is expected negative-path handling; successful authentication is not shown. |
| Current page URL | Pending — address bar outside the capture |
| Backend GraphQL | Not directly observed. Source connects the endpoint to `tokenCreate`, but this browser request does not reveal the executed GraphQL operation name or raw Saleor response. |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-04a-unknown-account.png`; file not verified. |

Observed storefront response (formatting normalized from the pasted text):

```json
{
  "errors": [
    {
      "message": "Please, enter valid credentials",
      "code": "INVALID_CREDENTIALS"
    }
  ]
}
```

The endpoint message and visible UI message differ: the form maps the error to
`Invalid email or password. Please try again.`. This response is from the
storefront endpoint, not a direct capture of the Saleor GraphQL response. The
request URL also does not establish the browser's current page URL.

The application banner introduces an error-state layout above the form fields.
Use it as part of this checkpoint. Its text is visually confirmed, while the
rendered `role=alert` and locator uniqueness still require DOM inspection.

## Observed record — AUTH-04b: existing-account / wrong-password case

Evidence: user confirms the submitted email is registered and supplies request
headers, response headers/body, and a screenshot in response to the wrong-password
step. Only relevant non-secret metadata is transcribed; raw cookie headers and
credential values are omitted.

| Item | Observation |
| --- | --- |
| Account and action | Alias `registered-test-account`; registration is user-confirmed. This attempt follows the requested deliberately incorrect-password step. A subsequent successful sign-in is recorded in AUTH-05; account type is not separately verified. |
| Request | `POST http://localhost:3000/api/auth/login`; relative request target and Host/Origin in the supplied headers establish the endpoint |
| Request page context | Referer is `http://localhost:3000/en/default-channel/login`, establishing the initiating page for this attempt. It does not independently establish the final page URL. |
| HTTP status and content type | `401 Unauthorized`; `application/json`, from user-pasted response headers and screenshot status |
| Response error | `errors[0].message` is `Please, enter valid credentials`; `errors[0].code` is `INVALID_CREDENTIALS` (presentation escape normalized). Same error object as AUTH-04a. |
| Visible application message | `Invalid email or password. Please try again.` in the banner above Email |
| UI state | Login form remains visible with populated Email, masked Password, and `Sign In` button. No successful-login UI or native validation bubble is shown. |
| Network evidence | One displayed `login` fetch row; HTTP 401; initiator `bff-client.ts:20`. Recording window and filter controls are not fully included in this screenshot. |
| Session-header metadata | Response sets an HttpOnly cookie with SameSite=Lax. Cookie names/values and raw headers are omitted; this header alone does not prove successful authentication. |
| Response timestamp | 2026-09-14 11:56:09 UTC (17:26:09 IST), from response Date header |
| Expected versus observed | Existing-account rejection produces HTTP 401, `INVALID_CREDENTIALS`, and the expected application message. Unknown-account and existing-account attempts have the same observed status, error code, response message, and UI message. |
| Final page URL | Not explicitly reported; screenshot shows the login form but excludes the address bar |
| Backend GraphQL | No direct GraphQL request/response capture. The endpoint is source-mapped to `tokenCreate`; its executed GraphQL operation name remains pending. |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-04b-wrong-password.png`; file not verified. |

The request reports a mobile Android/Pixel identity and Brave/Chromium version
153. Together with the earlier Responsive-mode capture, record this as browser
emulation context; do not infer a physical Android device or compare its layout
directly with the initial desktop screenshot. Matching error messages in these
two attempts do not establish broader account-enumeration or timing guarantees.

## Observed record — AUTH-05: successful sign-in

Evidence: user-pasted request/response details and screenshot received
2026-09-14 in response to the correct-password sign-in step. Token and cookie
values from the supplied headers are excluded from this document.

| Item | Observation |
| --- | --- |
| Account/action | Sign in to `registered-test-account` using its correct password, following the requested step |
| Request | `POST http://localhost:3000/api/auth/login`, established by request target and Host/Origin; content type `application/json` |
| Initiating page | Supplied Referer: `http://localhost:3000/en/default-channel/login` |
| HTTP status | `200 OK`, confirmed by supplied response headers and screenshot |
| Response JSON | `{"ok":true}`, supplied by the user; response content type `application/json` |
| Final page URL | `http://localhost:3000/en/default-channel`, visible in screenshot address bar |
| Signed-in UI | Header now displays an account-initials badge `HB` in place of the guest account/person icon. Homepage content is visible, including `Discover our collection`. The login form is no longer the displayed page. |
| Account menu | Closed in the initial successful-login screenshot; subsequent opened-menu evidence is recorded below |
| Network evidence | Recording active, Keep log checked, Fetch/XHR and `/api/auth/login` filter selected; one visible `login` row with status 200. Footer shows `1 / 111 requests`, reflecting the filter rather than total absence of other traffic. |
| Session metadata | Supplied response sets authentication cookies with HttpOnly and SameSite=Lax attributes. No cookie names/values or token strings are retained. Subsequent signed-in UI after refresh is recorded in AUTH-06a; expiry behavior remains untested. |
| Response timestamp | 2026-09-14 12:05:56 UTC (17:35:56 IST), from response Date header |
| Viewport/context | Responsive mode, 759 × 762, Fit to window, No throttling; browser and DevTools chrome are included in the evidence image |
| Expected versus observed | Source-predicted HTTP 200, success JSON, and locale/channel homepage destination match the evidence. The account badge supplies visible signed-in state beyond the navigation itself. |
| Backend GraphQL | Direct backend operation remains unobserved. Source mapping to `tokenCreate` is unchanged; the successful storefront response is not a raw GraphQL capture. |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-05-signed-in.png`; file not verified. |

Account initials depend on the test account. Use the badge as this session's
visible evidence, and inspect its accessible name/role before choosing a reusable
locator. Homepage promotional imagery and copy are surrounding page context,
not authentication assertions. The development indicator remains visible.

## Observed record — AUTH-05-menu: opened account menu

Evidence: user-supplied screenshot received 2026-09-14 in response to opening
the `HB` badge. The account dropdown is visible over homepage content.

| Item | Observation |
| --- | --- |
| Entry/action | Signed-in homepage; open the account badge. Screenshot shows the resulting dropdown anchored below the badge. |
| Identity region | Account display name and email visible above the menu entries; values omitted from this document, using alias `registered-test-account` |
| Menu text, top to bottom | `My account`, `My orders`, `Log Out` |
| Expected versus observed | The dropdown entries agree with the inspected menu component and English translations. Account navigation and logout are recorded subsequently in AUTH-06b and AUTH-07a/b; orders navigation remains outside this walkthrough. |
| Page URL | Homepage content visible; address bar outside this follow-up screenshot. Final URL from the preceding AUTH-05 capture is recorded separately. |
| Network / GraphQL | Panel remains filtered to login Fetch/XHR requests. This screenshot does not isolate requests caused by opening the menu or establish backend operation activity. |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-05-account-menu.png`; file not verified. |

Source candidate mapping: `DropdownMenuTrigger` contains the translated hidden
label `Open user menu`; `DropdownMenuItem` wraps each account/orders link and
the logout control. Confirm computed roles and accessible names in the rendered
DOM before treating the locator candidates as verified. Account-specific initials
and identity text should not be generic selectors or unmasked shared baselines.

## Observed record — AUTH-06a: signed-in state after refresh

Evidence: user-supplied screenshot received 2026-09-14 following the requested
Ctrl+R refresh and reopening of the account menu. The refresh action itself is
not captured; the image records the supplied post-refresh state.

| Item | Observation |
| --- | --- |
| Entry/action context | Signed-in homepage; requested refresh, wait for loading, then reopen the `HB` badge |
| Resulting URL | `http://localhost:3000/en/default-channel`, visible in the address bar |
| Account badge and identity | `HB` remains visible; opened menu displays the same test-account identity as AUTH-05-menu. Identity values omitted in favor of alias `registered-test-account`. |
| Menu entries | `My account`, `My orders`, `Log Out` remain visible |
| Other UI state | Homepage content displayed; no login form or authentication-error banner visible |
| Expected versus observed | Signed-in header and menu remain available in the screenshot supplied after the refresh step. This supports session persistence across this refresh; account access is recorded in AUTH-06b. Token-expiry behavior remains untested. |
| Browser evidence | Network recording enabled, Keep log checked, Fetch/XHR selected, and `/api/auth/login` filter retained. No matching rows; footer reads `0 / 73 requests`. |
| API / GraphQL limits | The login-only filter does not expose other refresh/session traffic. No specific session query, token refresh, HTTP response, or backend operation is established by this screenshot. |
| Viewport | Responsive mode, 759 × 762, Fit to window, No throttling |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-06a-session-refresh.png`; file not verified. |

The main promotional image differs from AUTH-05 (a Paper symbol is now visible
instead of the shoe image). Its cause is unverified and it is not an authentication
assertion. Preserve this observation without classifying it as a visual regression
or assuming it is intentional dynamic content.

## Observed record — AUTH-06b: signed-in account access

Evidence: user-supplied screenshot received 2026-09-14 following the requested
`My account` menu action. The account overview and address bar are visible.

| Item | Observation |
| --- | --- |
| Entry/action context | Signed-in homepage with account menu open; requested click on `My account` |
| Resulting URL | `http://localhost:3000/en/default-channel/account`, visible in the address bar |
| Signed-in state | `HB` badge retained; account overview displays a personalized `Welcome back, <first-name>` heading. The account name is normalized here to a placeholder. |
| Introductory text | `Here is an overview of your account activity.` |
| Account navigation | `Overview` selected; `Orders`, `Addresses`, and `Settings` visible; `Back to store` appears above the navigation |
| Recent orders section | Heading `Recent Orders`; empty-state text `You haven't placed any orders yet.` |
| Default address section | Heading `Default Address`; `Manage` control; empty-state text `No addresses saved yet.` |
| Authentication errors | No login form or authentication-error banner visible in the account overview |
| Browser request evidence | Text filter cleared, but Fetch/XHR remains selected. Displayed account request `account?_rsc=<dynamic>` returns HTTP 200; request type is fetch. Method and response body are not supplied. |
| Other development traffic | `__nextjs_original-stack-frames` fetch also returns HTTP 200. DevTools shows counters of 4 errors and 139 warnings; their contents and relationship to this navigation are uninspected. Do not characterize the whole page as error-free. |
| Expected versus observed | Observed destination matches the source's account link for the current locale/channel. Personalized overview and retained account badge support signed-in account access; the post-logout account gate is recorded in AUTH-07b. |
| API / GraphQL limits | Account fetch status 200 is browser navigation evidence, not a captured Saleor GraphQL response or proof that all downstream queries succeeded. The server-side operations remain unobserved. |
| Viewport | Responsive mode, 759 × 762, Fit to window, No throttling |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-06b-account-access.png`; file not verified. |

Account name, orders, and saved-address content depend on test data. The empty
states above describe this account at capture time, not universal expectations
for all users. Do not use the generated `_rsc` query value as a stable locator or
request identifier. Selected Overview styling and the section layout are useful
visual checkpoints; confirm DOM roles and link destinations separately.

## Observed record — AUTH-06c: login route while signed in

Evidence: user-supplied screenshot received 2026-09-14 after the requested visit
to the login URL in the signed-in tab. The selected login document request and
final homepage address bar are both visible.

| Item | Observation |
| --- | --- |
| Entry/action | Signed in as `registered-test-account`; navigate directly to the login page |
| Requested URL and method | `GET http://localhost:3000/en/default-channel/login`, shown in request Headers > General |
| Selected request status | `200 OK`; response content type `text/html; charset=utf-8` |
| Final page URL | `http://localhost:3000/en/default-channel`, visible in browser address bar |
| Visible state | Homepage content, `Discover our collection`, and the `HB` account badge remain visible; no login form or authentication-error banner shown |
| Expected versus observed | Visiting login while already signed in ends on the homepage with signed-in UI, matching the source-predicted destination. |
| Request distinction | This is the GET login-page document, not the POST `/api/auth/login` endpoint used to submit credentials. The observed document status is 200; no HTTP 3xx status or full redirect mechanism is established by the capture. |
| Network context | All selected, text filter empty, Keep log checked, recording enabled; 69 requests shown in the captured list |
| Response timestamp | 2026-09-14 15:38:26 UTC (21:08:26 IST), from the visible Date response header |
| Backend GraphQL | No direct backend operation capture; current-session query behavior remains source-mapped rather than runtime-observed |
| Viewport | Responsive mode, 759 × 762, Fit to window, No throttling |
| Screenshot checkpoint | Conversation attachment received. Planned local file: `artifacts/journey-mapping/auth/auth-06c-authenticated-login-route.png`; file not verified. |

Keep the requested login URL, its document response status, and the final page
URL as separate evidence fields. The final homepage alone would not establish
which route was requested; this capture supplies both.

## Observed record — AUTH-07a: logout

Evidence: user-supplied screenshot identified as after logging out, received
2026-09-14. The preceding signed-in menu provides the `Log Out` entry; the
click itself and its action response are not shown.

| Item | Observation |
| --- | --- |
| Entry/action | Signed-in session; user reports logging out |
| Final URL | `http://localhost:3000/en/default-channel`, visible in address bar |
| Visible state | Guest account/person icon replaces `HB`; homepage and `Discover our collection` visible. No account identity or opened signed-in menu shown. |
| Expected versus observed | Reported logout ends on the locale/channel homepage with guest UI, matching the inspected logout navigation. |
| Browser request evidence | Blank text filter, Fetch/XHR selected, Keep log enabled; `default-channel` fetch row shows HTTP 200; footer `1 / 75 requests`. Method, full URL, and body are not supplied. This row does not independently establish the logout action's status or endpoint. |
| API / GraphQL limits | Logout action response, cookie deletion, and any checkout detachment operation are not directly observed. Source mapping appears above. |
| Development indicators | One error and 24 warnings shown; their contents and relevance remain uninspected. |
| Viewport | Responsive 759 × 762, Fit to window, No throttling |
| Screenshot checkpoint | Conversation attachment received. Planned file: `artifacts/journey-mapping/auth/auth-07a-signed-out.png`; not verified locally. |

## Observed record — AUTH-07b: account access after logout

Evidence: second user-supplied screenshot identified as account access after
logout, received 2026-09-14.

| Item | Observation |
| --- | --- |
| Entry/action | Following logout, visit the previously observed account URL |
| Resulting URL | `http://localhost:3000/en/default-channel/account` remains in the address bar |
| Visible state | Guest account/person icon; `Welcome Back` login form with empty Email and Password fields, `Sign In`, `Sign up`, `Forgot password?`, and password visibility icon |
| Account content | The personalized overview, orders summary, and address summary seen in AUTH-06b are replaced by the login form. No authentication-error banner visible. |
| Expected versus observed | Signed-out account access displays an authentication gate in place, matching the account layout source. It does **not** navigate to `/login` in this capture. |
| Browser request evidence | Blank text filter, Fetch/XHR selected; only visible row is `__nextjs_original-stack-frames`, HTTP 200. Footer `1 / 37 requests`. This is development tooling traffic, not the account document's response status. |
| API / GraphQL limits | Account document status and server-side GraphQL execution are not captured. No credential submission is evidenced by this screenshot. |
| Development indicators | 16 warnings shown; contents uninspected |
| Viewport | Responsive 759 × 762, Fit to window, No throttling |
| Screenshot checkpoint | Conversation attachment received. Planned file: `artifacts/journey-mapping/auth/auth-07b-account-after-logout.png`; not verified locally. |

These observations complete the normal manual authentication flow and its recorded
negative paths. They establish visible signed-out behavior and the account-page
gate; they do not establish token revocation or authorization for every backend API.

## Evidence review and follow-ups

No further browser steps are required for this core walkthrough. Keep the following
limitations explicit when using this map for later adapter and test design:

- Semantic locator candidates are source-backed and visible text is observed;
  computed roles, accessible names, label associations, and uniqueness still need
  rendered DOM verification before automation relies on them.
- GraphQL operation names are source-mapped. Runtime backend requests/responses
  and the logout action response were not captured.
- Screenshots exist as conversation evidence, not verified local artifacts or
  approved visual baselines. Save redacted copies at the planned paths when curating
  evidence; the original desktop and later responsive captures are different contexts.
- Earlier validation/rejection final URLs, screenshot timestamps, browser zoom/DPR,
  and the contents of development warnings/errors remain unverified.
- Registration, password recovery, visibility toggling, inactive accounts, interrupted
  requests, token expiry, and orders navigation are follow-ups, not completed cases.

P01 continues with the remaining catalog, product, cart, and checkout journey maps.

## Screenshot and text checkpoints

Use the same viewport, zoom, locale, and channel throughout. Capture stable form
states after loaders settle. Record loading and disabled states separately.
Keep credentials and personal account details out of shared screenshots.

Candidate stable regions: form heading, labels, controls, and settled error alert.
Candidate dynamic regions: loading skeletons, `Signing in…`, focus/caret,
browser-native validation bubbles, account details, and transient notifications.
Confirm which actually appear before defining future masks or tolerances.

The inspected heading, labels, and alert are DOM text. Prefer DOM assertions for
them. OCR is not yet required; record any important visual-only text discovered
during the walkthrough.

## Completion checklist

- [x] Observe exact homepage/login URLs, locale/channel, and logged-out form (user-reported URLs and empty-login screenshot).
- [ ] Confirm stable locator candidates against rendered controls.
- [x] Record form validation and at least one server-rejected sign-in (native validation plus AUTH-04a unknown-account rejection, HTTP 401, response code/message, and visible error).
- [x] Record the separate existing-account/wrong-password case (AUTH-04b: user-confirmed registration, HTTP 401, `INVALID_CREDENTIALS`, and visible rejection; subsequent successful login recorded in AUTH-05).
- [x] Record successful sign-in, authenticated UI, and response evidence (AUTH-05: HTTP 200, success JSON, final homepage URL, and account badge).
- [x] Record the opened signed-in menu and visible account/orders/sign-out entries (AUTH-05-menu; DOM locator checks remain pending).
- [x] Record signed-in UI after homepage refresh (AUTH-06a; account badge/menu retained in supplied post-refresh screenshot).
- [x] Record signed-in account access (AUTH-06b: account URL, personalized overview, retained badge, and account fetch HTTP 200).
- [x] Record authenticated login-route behavior (AUTH-06c: GET login page, selected document status 200, final homepage URL, and retained account badge).
- [x] Record sign-out (AUTH-07a: homepage and restored guest icon; action response unobserved).
- [x] Record account access after logout (AUTH-07b: login form at unchanged account URL).
- [x] Identify GraphQL operations with source evidence; flag unresolved server-side visibility.
- [x] Record supplied screenshot checkpoints and candidate dynamic regions; no approved baselines claimed.
- [ ] Save and verify redacted local screenshot files at the planned paths.
- [x] Review remaining gaps; core manual walkthrough complete with the evidence limitations above.
