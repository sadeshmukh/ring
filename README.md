# Ring
This is an implementation of webrings for Hack Club Slack personal channels.

Check it out: https://ring.sahil.ink

Feel free to leave a star on the repo as well!

## More Info

Channels are sorted by their IDs, and each channel's descriptions contains links to the previous and next redirect URL in the ring, like so: https://ring.sahil.ink/next/slug and https://ring.sahil.ink/prev/slug. This way, the entire list of channels forms a ring. In the future, there are plans to visualize the entire ring on the home page. 

The server is automatically updated every fifteen minutes. You can check the current commit by visiting /version.

## Adding Your Channel
To add your Slack channel to the ring, submit a PR with an edit to `channels.yml`, adding an entry for your channel with its URL ending, Slack channel ID, and your user ID. You must be a channel manager of the personal channel.

```yaml
- channel_id: C1234567890
  user_id: U0987654321
  slug: mychannel
```

Your slug can be any unique identifier you choose - it will be used in the redirect URLs. Keep in mind the full URL will have to fit in your description, so keep it on the shorter side.

## Checklist
When submitting a PR to add your channel, please ensure you complete the following checklist:
- [ ] I am a channel manager of the Slack personal channel I am adding.
- [ ] I have added the correct `channel_id` and `user_id` in `channels.yml`.
- [ ] I have added the `slug` I want for my channel in `channels.yml`.
- [ ] I have added the correct previous and next redirect URLs in my channel's description (https://ring.sahil.ink/next/slug and https://ring.sahil.ink/prev/slug)