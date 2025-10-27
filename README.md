# Ring
This is an implementation of webrings for Slack personal channels! Channels are sorted by their IDs, and each channel's descriptions should contain links to the previous and next redirect URL in the ring, like so: https://ring.sahil.ink/next/YOUR_SLUG and https://ring.sahil.ink/prev/YOUR_SLUG.

It's live right now at https://ring.sahil.ink!

## Adding Your Channel
To add your Slack channel to the ring, submit a PR with an edit to `channels.yml`, adding an entry for your channel with its slug, Slack channel ID, and your user ID. You must be a channel manager of the personal channel.

```yaml
- channel_id: C1234567890
  user_id: U0987654321
  slug: mychannel
```
Your slug can be any unique identifier you choose - it will be used in the redirect URLs.

Please commit in the following format: `Add to ring: mychannel`.

## Checklist
When submitting a PR to add your channel, please ensure you complete the following checklist:
- [ ] I am a channel manager of the Slack personal channel I am adding.
- [ ] I have added the correct `channel_id` and `user_id` in `channels.yml`.
- [ ] I have added the `slug` I want for my channel in `channels.yml`.
- [ ] I have added the correct previous and next redirect URLs in my channel's description.