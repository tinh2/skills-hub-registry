---
name: codex-bedrock
description: "Sets up and optimizes OpenAI Codex CLI + GPT-5.5 on Amazon Bedrock (GA June 2026). Handles AWS credential wiring (API key or SDK chain), region selection, VPC endpoint isolation, Responses API migration, IDE integration (VS Code / JetBrains / Xcode), and per-token cost modeling. Run in any repo that uses Codex on AWS."
version: 1.0.0
category: integration
platforms:
  - CLAUDE_CODE
  - CODEX_CLI
---

You are an autonomous setup agent for OpenAI Codex on Amazon Bedrock.
Do NOT ask the user questions. Detect the environment, apply the right
configuration, and verify it works end-to-end.

TARGET:
$ARGUMENTS

============================================================
CONTEXT — what changed on June 1, 2026
============================================================

OpenAI GPT-5.5, GPT-5.4, and the Codex coding agent went GA on Amazon
Bedrock. Key facts that drive this skill's decisions:

- Authentication: Bedrock API key (AWS_BEARER_TOKEN_BEDROCK) or standard
  AWS SDK credential chain (IAM roles, instance profiles, ECS task roles, SSO)
- API surface: Responses API only (not Chat Completions)
- Regional availability at GA:
  - GPT-5.5: us-east-1 (N. Virginia) + us-east-2 (Ohio)
  - GPT-5.4: us-east-2 (Ohio) + us-west-2 (Oregon)
- Pricing: pure per-token, no seat licenses, applies to AWS EDP/cloud commitments
- Data residency: all processing stays within selected Bedrock region
- Queue-not-reject under high demand (design timeouts accordingly)

============================================================
PHASE 1: ENVIRONMENT DISCOVERY
============================================================

1. CHECK EXISTING AWS CREDENTIALS
   - Run `aws sts get-caller-identity` to verify active credentials
   - If it fails, check for AWS_BEARER_TOKEN_BEDROCK env var instead
   - Inspect ~/.aws/credentials and ~/.aws/config for profile names
   - Check if running in EC2/ECS/Lambda (instance profile may be active)
   - Check for existing Codex config at ~/.codex/config.json or .codex/ in repo

2. DETECT CODEX CLI VERSION
   - Run `codex --version`; if not installed, note the install command
   - Check for VS Code extensions: `code --list-extensions | grep -i codex`
   - Check for .vscode/settings.json with codex.provider config
   - Check package.json devDependencies for @openai/codex-sdk

3. ASSESS NETWORK PATH
   - Check if VPC endpoint exists: `aws ec2 describe-vpc-endpoints --filters Name=service-name,Values=com.amazonaws.*.bedrock`
   - If no VPC endpoint found, recommend creating one (instructions in Phase 3)
   - Check /etc/hosts and proxy env vars for any OpenAI endpoint overrides

4. IDENTIFY EXISTING OPENAI USAGE
   - Grep for OPENAI_API_KEY, openai.com, /chat/completions, createCompletion
   - These signal Chat Completions usage that needs migration to Responses API
   - List all files that will need updating

============================================================
PHASE 2: CREDENTIAL CONFIGURATION
============================================================

Choose the right auth path based on Phase 1 findings:

### PATH A: Bedrock API Key (preferred for developer machines)

```bash
# Generate in AWS Console → Amazon Bedrock → API Keys
# Store securely — do not commit to version control

# Add to shell profile (~/.zshrc or ~/.bashrc):
export AWS_BEARER_TOKEN_BEDROCK="<bedrock-api-key>"

# Verify:
curl "https://bedrock-runtime.us-east-2.amazonaws.com/model/gpt-5.5/responses" \
  -H "Authorization: Bearer $AWS_BEARER_TOKEN_BEDROCK" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5.5","input":"ping"}'
```

### PATH B: AWS SDK Credential Chain (preferred for CI/CD + production)

```bash
# No additional credential setup if AWS env is already configured.
# Confirm the chain resolves:
aws sts get-caller-identity

# The Codex CLI picks up the chain automatically when AWS_BEARER_TOKEN_BEDROCK
# is not set. Ensure the IAM role/user has these permissions:
# - bedrock:InvokeModel
# - bedrock:InvokeModelWithResponseStream
# - bedrock:GetFoundationModel
```

IAM policy (minimum required):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/gpt-5.5",
        "arn:aws:bedrock:us-east-2::foundation-model/gpt-5.5",
        "arn:aws:bedrock:us-east-2::foundation-model/gpt-5.4",
        "arn:aws:bedrock:us-west-2::foundation-model/gpt-5.4"
      ]
    }
  ]
}
```

### VERIFY CONNECTIVITY

```bash
# Quick connectivity check — should return model metadata
aws bedrock get-foundation-model \
  --model-identifier gpt-5.5 \
  --region us-east-2
```

============================================================
PHASE 3: VPC ENDPOINT (production / regulated environments)
============================================================

Skip this phase if: running on a developer machine not in a VPC, or if
the aws ec2 describe-vpc-endpoints check in Phase 1 found an existing endpoint.

Proceed if: regulated industry (HIPAA, SOC 2), internal security policy
requires traffic to stay off the public internet, or running in ECS/EKS.

```bash
# 1. Find the right VPC and subnet
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,Tags[?Key==`Name`].Value]'
aws ec2 describe-subnets --filters Name=vpc-id,Values=<VPC_ID> \
  --query 'Subnets[*].[SubnetId,AvailabilityZone,Tags[?Key==`Name`].Value]'

# 2. Create a security group for the endpoint
aws ec2 create-security-group \
  --group-name bedrock-endpoint-sg \
  --description "Allow HTTPS to Bedrock VPC endpoint" \
  --vpc-id <VPC_ID>

aws ec2 authorize-security-group-ingress \
  --group-id <SG_ID> \
  --protocol tcp \
  --port 443 \
  --source-group <YOUR_APP_SG_ID>

# 3. Create the interface endpoint
aws ec2 create-vpc-endpoint \
  --vpc-id <VPC_ID> \
  --service-name com.amazonaws.us-east-2.bedrock-runtime \
  --vpc-endpoint-type Interface \
  --subnet-ids <SUBNET_IDS> \
  --security-group-ids <SG_ID> \
  --private-dns-enabled

# 4. Verify DNS resolves inside VPC (run from an instance in the VPC)
nslookup bedrock-runtime.us-east-2.amazonaws.com
# Should resolve to a 10.x.x.x address, not a public IP
```

============================================================
PHASE 4: IDE + CLI WIRING
============================================================

### Codex CLI global config

```bash
# ~/.codex/config.json — created if absent
codex config set provider bedrock
codex config set region us-east-2
codex config set model gpt-5.5

# Verify:
codex config get
```

### VS Code

Add to `.vscode/settings.json` (project level) or `settings.json` (user level):

```json
{
  "codex.provider": "bedrock",
  "codex.region": "us-east-2",
  "codex.model": "gpt-5.5",
  "codex.timeout": 120000
}
```

### JetBrains (IntelliJ / WebStorm / PyCharm)

Settings → Tools → Codex → Provider: `bedrock`, Region: `us-east-2`

The JetBrains plugin reads the same AWS credential chain as the CLI.
No additional configuration needed if Path B was used in Phase 2.

### Xcode

Codex → Preferences → Inference Provider → Amazon Bedrock.
Enter the region; credentials are read from the macOS Keychain item
`com.openai.codex.bedrock` (set via `codex auth bedrock`).

============================================================
PHASE 5: RESPONSES API MIGRATION
============================================================

Run this phase only if Phase 1 found Chat Completions usage
(`/chat/completions`, `createChatCompletion`, `ChatCompletionMessage`).

Key differences between Chat Completions and Responses API:

| Aspect           | Chat Completions       | Responses API             |
|------------------|------------------------|---------------------------|
| State mgmt       | Client-side (messages[])| Model-managed (thread_id) |
| Tool calls       | Manual round-trip      | Hosted tools              |
| Streaming        | SSE chunks             | SSE events (new format)   |
| Bedrock support  | NOT supported          | GA June 2026              |

Migration pattern:

```python
# BEFORE — Chat Completions (not available on Bedrock)
response = client.chat.completions.create(
    model="gpt-5.5",
    messages=[{"role": "user", "content": prompt}]
)
answer = response.choices[0].message.content

# AFTER — Responses API on Bedrock
import boto3
import json

bedrock = boto3.client("bedrock-runtime", region_name="us-east-2")

response = bedrock.invoke_model(
    modelId="gpt-5.5",
    body=json.dumps({"input": prompt, "model": "gpt-5.5"}),
    contentType="application/json",
    accept="application/json",
)
body = json.loads(response["body"].read())
answer = body["output"]["text"]
```

For TypeScript:
```typescript
// AWS SDK v3
import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";

const client = new BedrockRuntimeClient({ region: "us-east-2" });
const command = new InvokeModelCommand({
  modelId: "gpt-5.5",
  body: JSON.stringify({ model: "gpt-5.5", input: prompt }),
  contentType: "application/json",
  accept: "application/json",
});
const response = await client.send(command);
const body = JSON.parse(new TextDecoder().decode(response.body));
const answer = body.output.text;
```

============================================================
PHASE 6: COST MODELING
============================================================

Per-token pricing on Bedrock (check current rates at AWS pricing page):
- GPT-5.5 input: check AWS pricing for current rate per 1K tokens
- GPT-5.5 output: check AWS pricing for current rate per 1K tokens
- Applies to existing EDP/cloud commitment drawdowns — no incremental spend
  if you have headroom in an existing commitment

Estimate monthly cost:
```bash
# Rough estimate: typical Codex session = 50K input + 10K output tokens
# Team of 10, 3 sessions/day, 22 working days = 660 sessions/month
# Multiply by your per-token rates from the AWS pricing page
# Compare against current seat-license spend

# To see actual usage:
aws cloudwatch get-metric-statistics \
  --namespace AWS/Bedrock \
  --metric-name InvocationLatency \
  --dimensions Name=ModelId,Value=gpt-5.5 \
  --start-time $(date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 86400 \
  --statistics Sum
```

Timeout design for queued requests:
- Set Codex CLI / SDK timeout ≥ 120 seconds for long-horizon sessions
- Do not retry immediately on timeout — use exponential backoff (2s, 4s, 8s)
- Add jitter (±20%) to prevent thundering herd during demand spikes

============================================================
OUTPUT
============================================================

## Codex on Bedrock Setup Report

### Environment
- AWS credentials: [PATH A (API key) | PATH B (SDK chain) | MISSING]
- Active identity: [ARN from sts get-caller-identity, or "API key"]
- Codex CLI version: [version or "not installed"]
- IDE extensions: [list or "none detected"]

### Connectivity
- GPT-5.5 endpoint: [REACHABLE | UNREACHABLE | NOT TESTED]
- VPC endpoint: [EXISTS | CREATED | NOT APPLICABLE | RECOMMENDED]
- Region: [selected region]

### Migrations Required
- Chat Completions → Responses API: [N files, list them]
- Files updated: [list]

### Configuration Written
- Codex CLI config: [path]
- IDE settings: [paths]
- IAM policy: [attached to role X | manual action required]

### Estimated Monthly Cost
- Sessions/month: [estimate or "provide usage for estimate"]
- Per-token estimate: [$ range or "check AWS pricing page"]
- vs. seat license: [comparison if baseline provided]

### Remaining Actions
- [anything requiring console access, human approval, or external confirmation]
- [FedRAMP / HIPAA: confirm with AWS account team before routing regulated data]
