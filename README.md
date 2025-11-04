# Ring

The Slack Ring is an webring for Hack Club Slack personal channels.

Check it out: [r.sahil.ink/random](https://ring.sahil.ink/random) or try `/ring-random` on the Hack Club Slack.

Feel free to leave a star on the repo as well!

## What exactly is this?

Each channel's descriptions contains links to the previous and next redirect URL in the ring, like so: https://r.sahil.ink/n/slug and https://r.sahil.ink/p/slug. This way, the entire list of channels forms a ring! For more info, check the [Slack channel](https://hackclub.slack.com/archives/C09NLGSU5U3) and [Canvas](https://hackclub.slack.com/docs/T0266FRGM/F09NCDL31AT) for more information.

Commits are automatically pushed to r.sahil.ink every fifteen minutes. You can check the current commit by visiting /version.

## Commands
The webring is bundled with a Slack bot! Here are the available commands:
- /ring-links: Get the previous and next links when in a ring channel and provide the ring ID
- /ring-random: Jump to a random ring channel
- /ring-validate: Validate the current channel's links and provide them if not found

## Adding Your Channel

To add your Slack channel to the ring, submit a PR with an edit to `channels.yml`, adding an entry for your channel with its URL ending, Slack channel ID, and your user ID. You must be a channel manager of the personal channel.

```yaml
- channel_id: C1234567890
  user_id: U0987654321
  slug: mychannel
```

Your slug can be any unique identifier you choose, as long as it is not entirely a number. Keep in mind the full URL will have to fit in your description, so keep it on the shorter side.

Make sure to view the instructions upon opening a PR (`.github/pull_request_template.md`).
