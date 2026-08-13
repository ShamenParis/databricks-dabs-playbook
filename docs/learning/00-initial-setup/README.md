# Prerequisites and Local Setup

To follow along with these modules on your local machine, you need the Databricks CLI installed and authenticated.

## 1. Install the Databricks CLI

**Mac/Linux (using Homebrew):**

```bash
brew tap databricks/tap
brew install databricks
```

**Windows (using winget):**

```bash
winget search databricks
winget install Databricks.DatabricksCLI
```

**Verify the installation:**

```bash
databricks --version
```

![CLI Installation Success](01-cli-version.png)

## 2. Authenticate with Your Workspace

You can follow these modules at no cost using the Databricks Free Edition (the modern replacement for Community Edition).

### Option A: Databricks Free Edition

1. Open your Free Edition workspace in a browser.
2. Go to **User Settings > Developer > Access Tokens**.
3. Click **Generate New Token** and copy the value.
4. In your terminal, run:

```bash
databricks configure --host https://<your-free-edition-workspace-url>
```

5. Paste your token when prompted.

![Generate Access Token](02-access-token.png)

### Option B: Enterprise Workspace (Paid)

For enterprise environments, OAuth U2M (User-to-Machine) via the browser is the recommended approach.

1. In your terminal, run:

```bash
databricks auth login --host https://<your-enterprise-workspace-url>
```

2. A browser window will open. Log in with your standard credentials.
3. The CLI will automatically save the token to `~/.databrickscfg`.

**Verify your connection:**

```bash
databricks workspace list /Workspace/Users/<your-email>
```

![Authentication Success](03-auth-success.png)
