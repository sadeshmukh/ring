# Ring
This is an implementation of webrings for Slack personal channels! Channels are sorted by their IDs, and each channel's descriptions should contain links to the previous and next redirect URL in the ring. 

This README will be updated with the public deployment link soon.

## Adding Your Channel
To add your Slack channel to the ring, submit a PR with an edit to `channels.yml`, adding an entry for your channel with its slug, Slack channel ID, and your user ID. You must be a channel manager of the personal channel.

```yaml
- channel_id: C1234567890
  slug: mychannel
  added_by: U0987654321
```
Your slug can be any unique identifier you choose - it will be used in the redirect URLs.