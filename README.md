# PropellerAds MCP Server

**Democratizing Programmatic Advertising with AI**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0-green.svg)](https://modelcontextprotocol.io)

Transform your media buying with AI-powered campaign optimization. This MCP (Model Context Protocol) server integrates PropellerAds' powerful programmatic advertising platform with Claude, enabling automated campaign management, real-time optimization, and data-driven decision making.

**Created by [@jannafta](https://www.linkedin.com/in/jannafta-programmatic-performance-dsp-ssp-rtb/) | [Website](https://www.jannafta.com/ia)**

## Why PropellerAds MCP?

In the fast-paced world of programmatic advertising, success depends on quick decisions and continuous optimization. This MCP server brings the power of AI to your fingertips, allowing you to:

- **Automate Campaign Management**: Create, update, and optimize campaigns with natural language commands
- **Real-time Performance Analysis**: Get instant insights on ROI, CTR, conversions, and more
- **Smart Optimization**: AI-driven bid adjustments, creative rotation, and targeting refinement
- **Scale Efficiently**: Identify and capitalize on winning campaigns automatically
- **Save Time**: Focus on strategy while AI handles the repetitive tasks

Perfect for:
- Media Buyers and Performance Marketers
- iGaming Affiliates
- App Developers and Publishers
- Growth Hackers and Digital Agencies
- Anyone running PropellerAds campaigns

## Quick Start

### Prerequisites

1. **PropellerAds Account**: You need an active account with API access
   - Minimum requirement: $1000 total spend or deposit
   - Get your API token from: https://ssp.propellerads.com/#/app/profile

2. **Claude Desktop**: Install Claude Desktop app
   - Download from: https://claude.ai/download

3. **Python 3.10+**: Required for the MCP server

### Installation

#### Option 1: Install from PyPI (Recommended)

```bash
pip install propellerads-mcp
```

#### Option 2: Install from source

```bash
git clone https://github.com/JanNafta/propellerads-mcp.git
cd propellerads-mcp
pip install -e .
```

### Configuration

Add to your Claude Desktop configuration file:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "propellerads": {
      "command": "python",
      "args": ["-m", "propellerads_mcp"],
      "env": {
        "PROPELLERADS_API_TOKEN": "your_api_token_here"
      }
    }
  }
}
```

Restart Claude Desktop and you're ready to go!

## Example Commands

### Campaign Management

```
"Show me all my active campaigns sorted by ROI"

"Create a push campaign for gaming offers in Brazil with $100 daily budget"

"Pause all campaigns with negative ROI in the last 7 days"

"Clone my best performing campaign to Mexico, Colombia, and Peru"
```

### Performance Analysis

```
"What's my campaign performance for the last week?"

"Compare this week's performance vs last week"

"Show me the top 10 zones by conversions for campaign 12345"

"Which creatives have CTR below 0.5%?"
```

### Optimization

```
"Find all zones spending over $50 without conversions and blacklist them"

"Show me campaigns ready for scaling (ROI > 50%)"

"Find top performing zones for my dating campaigns"
```

## Available Tools

### Campaign Tools
- `list_campaigns` - View all campaigns with filters
- `get_campaign_details` - Get complete campaign information
- `create_campaign` - Create new advertising campaigns
- `update_campaign` - Modify campaign settings
- `start_campaigns` - Activate campaigns
- `stop_campaigns` - Pause campaigns
- `clone_campaign` - Duplicate successful campaigns

### Statistics Tools
- `get_performance_report` - Detailed performance metrics
- `get_campaign_performance` - Campaign summary with insights
- `compare_periods` - Period-over-period analysis
- `get_zone_performance` - Placement-level analytics
- `get_creative_performance` - Creative performance breakdown

### Optimization Tools
- `find_underperforming_zones` - Find zones wasting budget
- `find_top_zones` - Identify best placements for whitelisting
- `find_scaling_opportunities` - Find campaigns ready to scale
- `auto_blacklist_zones` - Automatically blacklist bad zones

### Targeting Tools
- `add_to_whitelist` - Add zones to campaign whitelist
- `add_to_blacklist` - Add zones to campaign blacklist

### Account Tools
- `get_balance` - Check account balance
- `get_available_countries` - List targetable countries
- `get_ad_formats` - List available ad formats

## Security & Permissions

- **API Token**: Stored securely in environment variables
- **Read Operations**: Executed without confirmation
- **Write Operations**: Require explicit user confirmation
- **Rate Limiting**: Respects PropellerAds API limits

## Use Cases

### Daily Optimization Routine
```
1. "Show me yesterday's performance for all campaigns"
2. "Find and blacklist underperforming zones"
3. "Show me campaigns ready for scaling"
```

### Campaign Scaling
```
1. "Find campaigns with ROI > 100% and at least 50 conversions"
2. "Clone top performer to similar GEOs"
3. "Increase budget by 50% for profitable campaigns"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/JanNafta/propellerads-mcp/issues)
- **Author**: [@jannafta](https://www.linkedin.com/in/jannafta-programmatic-performance-dsp-ssp-rtb/)
- **Website**: [jannafta.com/ia](https://www.jannafta.com/ia)

## Keywords

`propellerads` `mcp` `programmatic` `dsp` `ssp` `adtech` `adops` `performance-marketing` `igaming` `media-buying` `rtb` `cpm` `cpc` `cpa` `push-notifications` `popunder` `interstitial` `ai-automation` `claude` `anthropic`

---

**Made with love for the programmatic advertising community**
